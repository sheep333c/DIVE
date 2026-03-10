#!/usr/bin/env python3
"""Module entrypoint for python -m dive."""

from dotenv import load_dotenv
load_dotenv()

from .cli import main

if __name__ == "__main__":
    main()
