# 所有方法都必须实现的基础接口，统一名称，方便后续调用
from abc import ABC, abstractmethod
from typing import List
from typing import Any
class Strategy(ABC):
    @abstractmethod
    def add_nodes(self, nodes: List) -> None:
        """添加节点集"""
        pass

    @abstractmethod
    def run(self) -> None:
        """具备隐私保护能力的分布式控制协议运行"""
        pass

    @abstractmethod
    def get_expect_average_value(self) -> float:
        """返回系统预期的初始平均值"""
        pass

    @abstractmethod
    def get_internal_values(self, node=None, t=-1) -> Any:
        """
        返回指定节点在t时刻的状态，缺参时自定义功能
        返回值类型由子类决定
        """
        pass

    @abstractmethod
    def get_final_values(self) -> Any:
        """返回所有节点的收敛值"""
        pass

    @abstractmethod
    def get_initial_values(self) -> Any:
        """返回所有节点的初始值"""
        pass

    @abstractmethod
    def get_values_all(self) -> Any:
        """返回所有节点的收敛全程值"""
        pass
