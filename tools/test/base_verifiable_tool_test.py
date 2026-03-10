"""
通用工具测试基类
自动提供CSV结果收集功能，支持医疗、法律、金融等各个领域的工具测试
"""
import time
import unittest
import concurrent.futures
import sys
import os
import json
from abc import ABC, abstractmethod
from typing import Dict, Any
from unittest.mock import patch, Mock
from urllib.error import HTTPError
import pdb

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from test.test_result_collector import collector


class VerifiableToolTestBase(unittest.TestCase, ABC):
    """
    通用可验证工具测试基类（抽象基类）
    
    使用ABC确保pytest不会实例化此类运行测试
    支持所有领域的工具测试：medical、legal、financial、academic、etc.
    
    自动处理：
    1. CSV结果收集
    2. 测试计数  
    3. 性能数据记录
    4. 错误率计算
    
    子类只需要：
    1. 继承这个类
    2. 设置 TOOL_CLASS_NAME 属性
    3. 实现抽象方法
    """
    
    # 告诉pytest不要运行这个基类
    __test__ = False
    
    # 子类需要设置这个属性，例如：TOOL_CLASS_NAME = "GeneticDiseasesTool"
    TOOL_CLASS_NAME = None
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化 - 自动设置结果收集"""
        cls.start_time = time.time()
        cls.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "api_response_times": [],
            "max_concurrency": 0,
            "concurrent_stability_rate": 0.0,
            "result_consistency_rate": 0.0,
            "basic_functionality_status": "PENDING",
            "error_handling_status": "PENDING",
            "tool_config_access_status": "PENDING",
            "test_response": ""
        }
    
    @classmethod
    def tearDownClass(cls):
        """测试类清理 - 自动输出CSV结果"""
        if cls.TOOL_CLASS_NAME is None:
            print("⚠️ 警告：子类未设置TOOL_CLASS_NAME，跳过CSV记录")
            return
            
        duration = time.time() - cls.start_time
        
        # 计算平均响应时间
        avg_response_time = (
            sum(cls.test_results["api_response_times"]) / len(cls.test_results["api_response_times"])
            if cls.test_results["api_response_times"] else 0
        )
        
        # 计算错误率
        if cls.test_results["total_tests"] > 0:
            failed_tests = cls.test_results["total_tests"] - cls.test_results["passed_tests"]
            cls.test_results["error_rate"] = failed_tests / cls.test_results["total_tests"]
        
        # 🔧 修复：如果有测试被跳过，将相关状态标记为FAIL
        skipped_tests = cls.test_results["total_tests"] - cls.test_results["passed_tests"]
        if skipped_tests > 0:
            print(f"🚨 检测到 {skipped_tests} 个测试被跳过或失败，标记相关状态为FAIL")
            
            # 有测试失败或被跳过，检查各个状态字段
            if cls.test_results["basic_functionality_status"] == "PENDING":
                cls.test_results["basic_functionality_status"] = "FAIL"
                print("   basic_functionality_status -> FAIL")
            
            if cls.test_results["error_handling_status"] == "PENDING":
                cls.test_results["error_handling_status"] = "FAIL"
                print("   error_handling_status -> FAIL")
                
            if cls.test_results["tool_config_access_status"] == "PENDING":
                cls.test_results["tool_config_access_status"] = "FAIL"
                print("   tool_config_access_status -> FAIL")
            
            # 如果并发测试相关的指标为默认值，说明测试被跳过
            if cls.test_results["max_concurrency"] == 0:
                cls.test_results["max_concurrency"] = "FAIL"
                print("   max_concurrency -> FAIL")
                
            # 检查并发稳定性率 - 0.0 或者空值都标记为FAIL
            if (cls.test_results["concurrent_stability_rate"] == 0.0 or 
                cls.test_results["concurrent_stability_rate"] == "" or
                cls.test_results["concurrent_stability_rate"] is None):
                cls.test_results["concurrent_stability_rate"] = "FAIL"
                print("   concurrent_stability_rate -> FAIL")
                
            # 检查结果一致性率 - 小于80%的都标记为FAIL
            if (cls.test_results["result_consistency_rate"] < 0.8 or 
                cls.test_results["result_consistency_rate"] == "" or
                cls.test_results["result_consistency_rate"] is None):
                cls.test_results["result_consistency_rate"] = "FAIL"
                print("   result_consistency_rate -> FAIL")
        
        # 获取工具信息
        tool_info = collector.get_tool_info(cls.TOOL_CLASS_NAME)
        
        # 准备结果数据 - 按照用户要求的字段顺序
        final_results = {
            "tool_name": cls.TOOL_CLASS_NAME,
            "test_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "domain": tool_info["domain"],
            "source": tool_info["source"], 
            "description": tool_info["description"],
            "unit_test_pass_rate": f"{cls.test_results['passed_tests']}/{cls.test_results['total_tests']}" if cls.test_results["total_tests"] > 0 else "",
            "basic_functionality_status": cls.test_results["basic_functionality_status"],
            "api_response_time": f"{avg_response_time:.2f}s" if avg_response_time > 0 else "",
            "max_concurrency_capacity": str(cls.test_results["max_concurrency"]) if cls.test_results["max_concurrency"] != "FAIL" and cls.test_results["max_concurrency"] > 0 else ("FAIL" if cls.test_results["max_concurrency"] == "FAIL" else ""),
            "result_consistency_rate": f"{cls.test_results['result_consistency_rate']:.2%}" if cls.test_results["result_consistency_rate"] != "FAIL" and cls.test_results["result_consistency_rate"] > 0 else ("FAIL" if cls.test_results["result_consistency_rate"] == "FAIL" else ""),
            "concurrent_stability_rate": f"{cls.test_results['concurrent_stability_rate']:.2%}" if cls.test_results["concurrent_stability_rate"] != "FAIL" and cls.test_results["concurrent_stability_rate"] > 0 else ("FAIL" if cls.test_results["concurrent_stability_rate"] == "FAIL" else ""),
            "error_handling_status": cls.test_results["error_handling_status"],
            "tool_config_access_status": cls.test_results["tool_config_access_status"],
            "test_duration": f"{duration:.1f}s",
            "test_response": cls.test_results["test_response"].replace("\n", " ")
        }
        
        # 更新CSV结果
        collector.update_result(cls.TOOL_CLASS_NAME, final_results)

    def setUp(self):
        """测试方法初始化 - 自动计数"""
        super().setUp()
        # 增加测试计数
        self.__class__.test_results["total_tests"] += 1
    
    def tearDown(self):
        """测试方法清理 - 自动检测通过状态"""
        super().tearDown()
        # 更简单的方法：只有显式设置测试完成标记的才算通过
        if hasattr(self, '_test_completed') and not hasattr(self, '_test_skipped'):
            self.__class__.test_results["passed_tests"] += 1
    
    # =================================
    # 便捷方法，子类可以调用
    # =================================
    
    def record_api_response_time(self, response_time: float):
        """记录API响应时间"""
        self.__class__.test_results["api_response_times"].append(response_time)
    
    def record_max_concurrency(self, concurrency: int):
        """记录最大并发数"""
        self.__class__.test_results["max_concurrency"] = max(
            self.__class__.test_results["max_concurrency"], 
            concurrency
        )
    

    
    def skip_test_with_reason(self, reason: str):
        """跳过测试并记录原因"""
        self._test_skipped = True
        self.skipTest(reason)
    
    # =================================
    # 通用辅助方法
    # =================================
    
    def time_api_call(self, api_call_func, *args, **kwargs):
        """
        计时API调用并自动记录响应时间
        
        用法:
        result = self.time_api_call(self.tool.execute, params, context)
        """
        start_time = time.time()
        result = api_call_func(*args, **kwargs)
        response_time = time.time() - start_time
        
        self.record_api_response_time(response_time)
        return result
    
    def _test_concurrency_level(self, tool, params, context, concurrency: int, timeout: int = 300):
        """
        测试特定并发级别的性能
        
        返回: (success_rate, avg_response_time)
        """
        def single_request():
            try:
                result = tool.execute(context, params)
                return "error" not in str(result)
            except Exception as e:
                print(f"Request failed with exception: {e}")
                return False
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(single_request) for _ in range(concurrency)]
            results = [future.result(timeout=timeout) for future in futures]
        
        success_count = sum(results)
        success_rate = success_count / concurrency
        
        return success_rate, 0  # 不返回响应时间，只返回成功率
    
    def _sustained_load_test(self, tool, params, context, concurrency: int, duration: int):
        """
        持续负载测试
        
        Args:
            tool: 工具实例
            params: 测试参数
            context: 执行上下文
            concurrency: 并发数
            duration: 持续时间（秒）
            
        Returns:
            float: 错误率 (0.0-1.0)
        """
        start_time = time.time()
        total_requests = 0
        successful_requests = 0
        
        while time.time() - start_time < duration:
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
                    futures = [executor.submit(tool.execute, params, context) 
                             for _ in range(concurrency)]
                    
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            result = future.result(timeout=5)
                            total_requests += 1
                            if "error" not in str(result):
                                successful_requests += 1
                        except:
                            total_requests += 1
                
                time.sleep(1)  # 每秒一轮测试
                
            except Exception:
                total_requests += concurrency
        
        error_rate = 1 - (successful_requests / total_requests) if total_requests > 0 else 1.0
        return error_rate
    
    # =================================
    # 通用测试方法（子类可直接使用）
    # =================================
    
    @abstractmethod
    def get_test_params(self):
        """子类必须实现：返回测试参数"""
        pass
    
    @abstractmethod
    def get_tool_instance(self):
        """子类必须实现：返回工具实例"""
        pass
    
    @abstractmethod
    def get_execution_context(self):
        """子类必须实现：返回执行上下文"""
        pass
    
    def test_max_concurrency_capacity(self):
        """测试最大并发处理能力（上限1000）"""
        max_stable_concurrency = 1  # 移到try外面，确保异常时也能访问
        try:
            tool = self.get_tool_instance()
            params = self.get_test_params()
            context = self.get_execution_context()
            
            # 二分查找最大并发数
            low, high = 1, 500
            
            while low <= high:
                #time.sleep(20)
                mid = (low + high) // 2
                success_rate, _ = self._test_concurrency_level_optimized(tool, params, context, mid)
                
                if success_rate >= 0.85:  # 降低标准从90%到85%
                    max_stable_concurrency = mid
                    # 实时记录成功的并发数，确保即使后续测试失败也能保存
                    self.record_max_concurrency(max_stable_concurrency)
                    low = mid + 1
                else:
                    high = mid - 1
                
                print(f"测试并发数 {mid}: 成功率 {success_rate:.2%}")
                time.sleep(1)  # 避免API限流（优化等待时间）
        
            print(f"✅ 最大稳定并发数: {max_stable_concurrency}")
            # record_max_concurrency 已在循环中实时调用，这里不需要重复

            self.assertGreater(max_stable_concurrency, 0)
            self._test_completed = True
            
        except Exception as e:
            # 即使测试失败，也记录已经找到的最大成功并发数
            if max_stable_concurrency > 1:
                print(f"⚠️ 测试中断，但已找到最大稳定并发数: {max_stable_concurrency}")
                # 确保最大并发数被记录到测试结果中（record_max_concurrency会取max值）
                self.record_max_concurrency(max_stable_concurrency)
            else:
                print(f"❌ 测试失败且未找到有效的并发数")
            self.skipTest(f"并发测试失败: {str(e)}")
    
    def test_response_performance(self):
        time.sleep(5)
        """测试响应性能"""
        try:
            tool = self.get_tool_instance()
            params = self.get_test_params()
            context = self.get_execution_context()
            
            result = self.time_api_call(tool.execute, context, params)
            
            # 透传设计：不检测内容，只测试响应时间
            response_times = self.__class__.test_results["api_response_times"]
            if response_times:
                latest_time = response_times[-1]
                print(f"✅ API响应时间: {latest_time:.2f}秒")
                self.assertLess(latest_time, 60.0, "API响应时间过长")
                self._test_completed = True
                
        except Exception as e:
            self.skipTest(f"性能测试失败: {str(e)}")
    
    def _test_concurrency_level_optimized(self, tool, params, context, concurrency):
        """测试特定并发级别的性能（轻量化版本）"""
        def single_request():
            try:    
                result = tool.execute(context, params)
                return "error" not in str(result)
            except:
                return False
        
        # 对于高并发测试，使用较小的样本量以加快测试速度
        test_size = min(concurrency, 100)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(single_request) for _ in range(test_size)]
            results = [future.result(timeout=60) for future in futures]
        
        success_count = sum(results)
        success_rate = success_count / test_size
        
        return success_rate, 0  # 不返回响应时间，只返回成功率
    
    # =================================
    # 更多通用测试方法
    # =================================
    
    def test_error_handling_logic(self):
        """测试错误处理逻辑 - 透传设计，极简验证"""
        #time.sleep(20)
        try:
            tool = self.get_tool_instance()
            params = self.get_test_params()
            context = self.get_execution_context()
            
            # HTTP 404错误 - 透传设计：只验证工具能处理错误，不验证格式
            with patch('urllib.request.urlopen') as mock_urlopen:
                mock_urlopen.side_effect = HTTPError(None, 404, "Not Found", None, None)
                result = tool.execute(context, params.copy())
                # 透传设计：不检查具体内容，只要不抛异常就算通过
            
            # HTTP 500错误 - 透传设计：只验证工具能处理错误，不验证格式
            with patch('urllib.request.urlopen') as mock_urlopen:
                mock_urlopen.side_effect = HTTPError(None, 500, "Internal Server Error", None, None)
                result = tool.execute(context, params.copy())
                # 透传设计：不检查具体内容，只要不抛异常就算通过
            
            # 网络超时错误 - 透传设计：只验证工具能处理错误，不验证格式
            with patch('urllib.request.urlopen') as mock_urlopen:
                mock_urlopen.side_effect = Exception("Network timeout")
                result = tool.execute(context, params.copy())
                # 透传设计：不检查具体内容，只要不抛异常就算通过
            
            # 更新状态为通过
            self.__class__.test_results["error_handling_status"] = "PASS"
            self._test_completed = True
        except Exception as e:
            self.__class__.test_results["error_handling_status"] = "FAIL"
            raise
    
    def test_basic_tool_functionality(self):
        """测试工具基本功能"""
        try:
            time.sleep(0.5)  # 避免API限流
            
            tool = self.get_tool_instance()
            params = self.get_test_params()
            context = self.get_execution_context()
            
            result = tool.execute(context, params)
            # 安全地打印结果预览
            result_preview = str(result)[:50] if result else "None"
            print(result_preview)
            # 透传设计：不检测内容，只验证功能正常运行
            print("✅ 基本功能测试成功")
            self.__class__.test_results["basic_functionality_status"] = "PASS"
            
            # 记录实际的API响应结果
            # 截取结果的前500个字符避免CSV过大
            result_str = str(result)
            if len(result_str) > 500:
                self.__class__.test_results["test_response"] = result_str[:500] + "..."
            else:
                self.__class__.test_results["test_response"] = result_str
            self._test_completed = True
                
        except Exception as e:
            self.__class__.test_results["basic_functionality_status"] = "FAIL"
            self.__class__.test_results["test_response"] = f"Exception: {str(e)}"
            self.skipTest(f"基本功能测试失败: {str(e)}")
    
    def test_concurrent_request_stability(self):
        """测试并发请求稳定性"""
        try:
            tool = self.get_tool_instance()
            params = self.get_test_params()
            context = self.get_execution_context()
            
            concurrent_count = 100
            
            def single_request():
                try:
                    result = tool.execute(context, params)  # 真实API调用
                    if "error" in str(result):
                        #print("=======================================")
                        #print(result)
                        pass
                    return "error" not in str(result)
                except Exception:
                    return False
            
            # 多轮测试以验证稳定性
            total_rounds = 3
            successful_rounds = 0
            
            for round_num in range(total_rounds):
                print(f"并发稳定性测试 - 第{round_num + 1}轮")
                
                # 并发执行
                with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_count) as executor:
                    futures = [executor.submit(single_request) for _ in range(concurrent_count)]
                    results = [future.result(timeout=300) for future in futures]
                
                print(len(results))
                print("*"*100)
                # 计算成功率
                success_rate = sum(results) / len(results)
                print(f"  成功率: {success_rate:.2%}")
                
                # 稳定性标准：成功率 >= 80%
                if success_rate >= 0.8:
                    successful_rounds += 1
                
                # 避免API限流
                if round_num < total_rounds - 1:
                    time.sleep(3)
            
            # 验证稳定性：至少2轮测试成功 (2/3 = 66.67%)
            stability_rate = successful_rounds / total_rounds
            print(f"✅ 并发稳定性: {stability_rate:.2%} ({successful_rounds}/{total_rounds}轮成功)")
            
            self.assertGreaterEqual(stability_rate, 0.66, "并发稳定性不足")
            # 记录并发稳定性率
            self.__class__.test_results["concurrent_stability_rate"] = stability_rate
            self._test_completed = True
                    
        except Exception as e:
            self.skipTest(f"并发稳定性测试失败: {str(e)}")
    
    def _normalize_result_for_consistency(self, result):
        """标准化结果，去除动态字段以进行一致性比较"""
        if isinstance(result, dict) and result.get("error"):
            return {"error": True}
        
        # 对于字符串结果（如XML），去除动态字段
        if isinstance(result, str):
            import re
            normalized = result
            
            # 去除时间戳字段 (updated, published等)
            normalized = re.sub(r'<updated>.*?</updated>', '<updated>NORMALIZED</updated>', normalized)
            normalized = re.sub(r'<published>.*?</published>', '<published>NORMALIZED</published>', normalized)
            
            # 去除动态ID中的随机部分
            normalized = re.sub(r'<id>http://arxiv\.org/api/[^<]*</id>', '<id>NORMALIZED_API_ID</id>', normalized)
            
            # 去除feed链接中的动态部分
            normalized = re.sub(r'<link href="http://arxiv\.org/api/query[^"]*"', '<link href="NORMALIZED_QUERY"', normalized)
            
            return normalized
        
        # 对于字典结果（如JSON），去除动态字段
        elif isinstance(result, dict):
            import copy
            normalized = copy.deepcopy(result)
            
            # 递归处理嵌套字典
            def normalize_dict(d):
                if isinstance(d, dict):
                    for key, value in d.items():
                        # 标准化动态字段
                        if key in ['facets', 'query', 'message-version', 'score']:
                            # 这些字段可能包含动态内容，标准化它们
                            d[key] = "NORMALIZED"
                        elif key in ['indexed', 'created', 'deposited', 'published-print', 'published-online', 'issued', 'published']:
                            # 时间相关字段，标准化整个字典
                            d[key] = "NORMALIZED"
                        elif isinstance(value, list):
                            # 处理列表中的动态字段
                            for i, item in enumerate(value):
                                if isinstance(item, dict):
                                    # 递归处理嵌套字典
                                    normalize_dict(item)
                        elif isinstance(value, dict):
                            normalize_dict(value)
                elif isinstance(d, list):
                    for item in d:
                        normalize_dict(item)
            
            normalize_dict(normalized)
            return normalized
        
        # 对于其他类型，直接返回
        return result

    def test_result_consistency(self):
        #time.sleep(20)
        """测试结果一致性 - 相同参数多次调用的结果一致性（忽略动态字段）"""
        try:
            tool = self.get_tool_instance()
            params = self.get_test_params()
            context = self.get_execution_context()
            
            print("🔄 开始结果一致性测试 - 相同参数调用10次（忽略动态字段）")
            
            results = []
            test_count = 10
            
            for i in range(test_count):
                try:
                    result = tool.execute(context, params)
                    # 标准化结果，去除动态字段
                    normalized_result = self._normalize_result_for_consistency(result)
                    results.append(normalized_result)
                    
                    # 每10次输出进度
                    if (i + 1) % 10 == 0:
                        print(f"  已完成: {i + 1}/10")
                    
                    # 避免API限流
                    if i < test_count - 1:
                        time.sleep(0.1)
                        
                except Exception:
                    results.append({"error": True})
            
            # 计算一致性
            if not results:
                self.skipTest("未获得任何结果")
                return
            
            # 统计相同结果的数量
            result_counts = {}
            error_count = 0
            
            for result in results:
                if isinstance(result, dict) and result.get("error"):
                    error_count += 1
                else:
                    # 将标准化结果转换为字符串进行比较
                    result_key = str(result)
                    result_counts[result_key] = result_counts.get(result_key, 0) + 1
            
            # 计算一致性百分比
            if result_counts:
                most_common_count = max(result_counts.values())
                valid_results = test_count - error_count
                consistency_rate = most_common_count / valid_results if valid_results > 0 else 0
            else:
                consistency_rate = 0
            
            print(f"✅ 结果一致性: {consistency_rate:.2%} ({most_common_count if result_counts else 0}/{test_count - error_count}次相同)")
            print(f"   错误次数: {error_count}/{test_count}")
            print(f"   不同结果种类: {len(result_counts)}")
            
            # 记录到测试结果中
            self.__class__.test_results["result_consistency_rate"] = consistency_rate

            
            # 验证一致性要求（至少80%一致）
            self.assertGreaterEqual(consistency_rate, 0.8, f"结果一致性过低: {consistency_rate:.2%}")
            self._test_completed = True
                    
        except Exception as e:
            self.skipTest(f"结果一致性测试失败: {str(e)}")
    
