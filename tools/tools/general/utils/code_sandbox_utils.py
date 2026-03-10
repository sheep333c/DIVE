"""
Code Execution Utilities

Executes code via SandboxFusion — an open-source multi-language sandbox.
Auto-starts a Docker container if SANDBOX_FUSION_URL is not set.

See: https://github.com/bytedance/SandboxFusion
"""

import atexit
import json
import os
import shutil
import subprocess
import time
from typing import Any, Dict, Optional, Tuple

SANDBOX_FUSION_IMAGE = "volcengine/sandbox-fusion:server-20250609"
SANDBOX_FUSION_CONTAINER = "dive-sandbox-fusion"
SANDBOX_FUSION_PORT = 8080


def clip_text(text: str, max_length: int = 5000) -> str:
    """Truncate long output, keeping head and tail."""
    if len(text) > max_length:
        half = max_length // 2
        return text[:half] + "\n... [truncated] ...\n" + text[-half:]
    return text


def _is_sandbox_ready(url: str, timeout: int = 5) -> bool:
    """Check if a SandboxFusion service is reachable."""
    try:
        from urllib import request as urllib_request
        req = urllib_request.Request(f"{url}/run_code", method="POST",
                                     data=json.dumps({"code": "", "language": "python"}).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib_request.urlopen(req, timeout=timeout):
            pass
        return True
    except Exception:
        return False


def _find_free_port() -> int:
    """Find a free TCP port on localhost."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def _start_sandbox_container(port: int = 0) -> str:
    """Start a SandboxFusion Docker container and return its URL.

    Reuses an existing container named 'dive-sandbox-fusion' if already running.
    """
    if not shutil.which("docker"):
        raise RuntimeError(
            "Docker is required to auto-start SandboxFusion. Either:\n"
            "  1. Install Docker: https://docs.docker.com/get-docker/\n"
            "  2. Or manually start SandboxFusion and set SANDBOX_FUSION_URL"
        )

    # Check if our container is already running (on any port)
    try:
        result = subprocess.run(
            ["docker", "inspect", "-f",
             "{{.State.Running}} {{(index (index .NetworkSettings.Ports \"8080/tcp\") 0).HostPort}}",
             SANDBOX_FUSION_CONTAINER],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if len(parts) == 2 and parts[0].lower() == "true":
                existing_port = int(parts[1])
                existing_url = f"http://localhost:{existing_port}"
                if _is_sandbox_ready(existing_url):
                    print(f"Reusing existing SandboxFusion container at {existing_url}")
                    return existing_url
    except Exception:
        pass

    # Remove stale container if exists
    subprocess.run(
        ["docker", "rm", "-f", SANDBOX_FUSION_CONTAINER],
        capture_output=True, timeout=15,
    )

    # Auto-find free port
    if port == 0:
        port = _find_free_port()

    # Start new container
    print(f"Starting SandboxFusion container ({SANDBOX_FUSION_IMAGE}) on port {port}...")
    result = subprocess.run(
        ["docker", "run", "-d",
         "--name", SANDBOX_FUSION_CONTAINER,
         "-p", f"{port}:{SANDBOX_FUSION_PORT}",
         SANDBOX_FUSION_IMAGE],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to start SandboxFusion container:\n{result.stderr}\n"
            f"Try pulling the image first: docker pull {SANDBOX_FUSION_IMAGE}"
        )

    url = f"http://localhost:{port}"

    # Wait for service to be ready
    print("Waiting for SandboxFusion to be ready...", end="", flush=True)
    for i in range(30):
        if _is_sandbox_ready(url):
            print(" ready!")
            return url
        print(".", end="", flush=True)
        time.sleep(2)

    raise RuntimeError(
        f"SandboxFusion container started but service not responding at {url} after 60s. "
        f"Check logs: docker logs {SANDBOX_FUSION_CONTAINER}"
    )


class SandboxFusionClient:
    """Client for the SandboxFusion HTTP API.

    Supports two execution modes:
      - /run_code  — single script execution (any language)
      - /run_jupyter — sequential cell execution with shared state (python3 kernel)

    API reference: https://bytedance.github.io/SandboxFusion/docs/api/
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 60,
        run_timeout: int = 30,
        max_output_length: int = 5000,
    ):
        self.base_url = (base_url or os.getenv("SANDBOX_FUSION_URL", "")).rstrip("/")
        if not self.base_url:
            # Auto-start a Docker container
            self.base_url = _start_sandbox_container()
            os.environ["SANDBOX_FUSION_URL"] = self.base_url
        self.timeout = timeout
        self.run_timeout = run_timeout
        self.max_output_length = max_output_length

    def _post(self, endpoint: str, payload: dict) -> dict:
        """Send a POST request to a SandboxFusion endpoint."""
        from urllib import request as urllib_request

        data = json.dumps(payload).encode("utf-8")
        req = urllib_request.Request(
            f"{self.base_url}{endpoint}",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib_request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def run_code(self, code: str, language: str = "python") -> Tuple[bool, Dict[str, Any]]:
        """Execute code via the /run_code endpoint."""
        try:
            data = self._post("/run_code", {
                "code": code,
                "language": language,
                "run_timeout": self.run_timeout,
            })

            if data.get("status") != "Success":
                return False, {
                    "status": "Error",
                    "return_code": -1,
                    "stdout": "",
                    "stderr": data.get("message", "SandboxFusion execution failed"),
                }

            run_result = data.get("run_result") or {}
            return True, {
                "status": run_result.get("status", "Finished"),
                "return_code": run_result.get("return_code", -1),
                "stdout": clip_text(run_result.get("stdout", ""), self.max_output_length),
                "stderr": clip_text(run_result.get("stderr", ""), self.max_output_length),
            }

        except Exception as e:
            return False, {
                "status": "Error",
                "return_code": -1,
                "stdout": "",
                "stderr": f"SandboxFusion request failed: {e}",
            }

    def run_jupyter(
        self,
        cells: list,
        kernel: str = "python3",
        cell_timeout: Optional[float] = None,
        total_timeout: Optional[float] = None,
    ) -> Tuple[bool, Dict[str, Any]]:
        """Execute code cells via the /run_jupyter endpoint.

        Cells share state (variables, imports persist across cells).

        Args:
            cells: List of code strings to execute sequentially.
            kernel: Jupyter kernel name (default: "python3").
            cell_timeout: Timeout per cell in seconds.
            total_timeout: Total timeout for all cells in seconds.

        Returns:
            (success, result) where result contains per-cell outputs.
        """
        try:
            payload: Dict[str, Any] = {
                "cells": cells,
                "kernel": kernel,
            }
            if cell_timeout is not None:
                payload["cell_timeout"] = cell_timeout
            if total_timeout is not None:
                payload["total_timeout"] = total_timeout
            else:
                payload["total_timeout"] = self.run_timeout * len(cells)

            data = self._post("/run_jupyter", payload)

            if data.get("status") != "Success":
                return False, {
                    "status": "Error",
                    "cells": [],
                    "stderr": data.get("message", "SandboxFusion jupyter execution failed"),
                }

            cell_results = []
            for cell in (data.get("cells_result") or []):
                cell_results.append({
                    "status": cell.get("status", ""),
                    "stdout": clip_text(cell.get("stdout", ""), self.max_output_length),
                    "stderr": clip_text(cell.get("stderr", ""), self.max_output_length),
                    "display": clip_text(cell.get("display", ""), self.max_output_length),
                })

            all_ok = all(c.get("status") == "Success" for c in (data.get("cells_result") or []))
            return all_ok, {
                "status": "Finished" if all_ok else "CellError",
                "cells": cell_results,
            }

        except Exception as e:
            return False, {
                "status": "Error",
                "cells": [],
                "stderr": f"SandboxFusion jupyter request failed: {e}",
            }


def get_code_sandbox_client(**kwargs) -> SandboxFusionClient:
    """Return a SandboxFusion client.

    If SANDBOX_FUSION_URL is set, connects to that endpoint.
    Otherwise, auto-starts a Docker container.
    """
    return SandboxFusionClient(**kwargs)


if __name__ == "__main__":
    client = get_code_sandbox_client()
    success, result = client.run_code("print('Hello, world!')")
    print(f"Success: {success}")
    print(f"Result: {json.dumps(result, indent=2)}")
