# 文献：Privacy-Preserving Average Consensus via State Decomposition的实现
from methods.base_method import Strategy
from typing import List
import numpy as np

class Node2_1:
    def __init__(self, initial_value, epsilon, value_delta=0.0):
        self.initial_value = initial_value
        self.epsilon = epsilon
        self.weight_0 = {}      # 与邻居的权重集合（t=0）
        self.weight_self_0 = 1.0    # 与自己的权重
        self.values_alpha = [initial_value]      # alpha子节点的状态轨迹
        self.values_beta = [initial_value]       # beta子节点的状态轨迹
        self.neighbors = {}
        self.value_delta = value_delta  # 构建相同输出是需要考虑的参数，具体含义参考文献

    def add_neighbors(self, nodes: List) -> None:
        """
        建立和邻居的连接
        :param nodes:
        :return:
        """
        for node in nodes:
            self.neighbors[node] = []
            self.weight_0[node] = 1.0

    def generate_weight_self(self):
        """
        如果需要和某个实现保持一致需要调用次函数生成对应权重
        具体的权重生成规则请参考文献
        """
        self.weight_self_0 = (2*self.value_delta + self.epsilon *
                              (self.values_alpha[0] - 2*self.value_delta - self.values_beta[0])) \
                             / (self.epsilon * (self.values_alpha[0] - self.values_beta[0]))

    def generate_weight(self, nodes: List, weights: List):
        for i in range(len(nodes)):
            self.weight_0[nodes[i]] = weights[i]

    def send_message(self, t: int) -> float:
        """
        在t时刻，只传送alpha节点的信息
        :param t:
        :return:
        """
        return self.values_alpha[t]

    def receive_message(self, t: int) -> None:
        for node in self.neighbors:
            self.neighbors[node].append(node.send_message(t))

    def generate_initial_value1(self, value_alpha: float) -> None:
        """
        根据给定的初始值来确定状态分解初始分布
        :param value_alpha: alpha节点的初始值
        :param value_beta: beta节点的初始值
        :return:
        """
        self.values_alpha[0] = value_alpha
        self.values_beta[0] = 2 * self.initial_value - value_alpha

    def generate_initial_value(self) -> None:
        """
        按照给定规律的初始分布
        :return:
        """
        self.values_alpha[0] = 1.3 * self.initial_value
        self.values_beta[0] = 2 * self.initial_value - self.values_alpha[0]

    def update(self, t: int) -> None:
        """
        通过t时刻的信息，来更新出t+1时刻的状态
        :param t:
        :return:
        """
        input_neighbor = 0.0    # 来自邻居的输入
        input_self = 0.0        # 来自内部beta节点的输入
        for node in self.neighbors:
            # 在t=0时刻采用设计号的权重参数
            if t == 0:
                input_neighbor += self.weight_0[node] * (self.neighbors[node][t] - self.values_alpha[t])
            else:
                input_neighbor += (self.neighbors[node][t] - self.values_alpha[t])
        if t== 0:
            input_self = self.weight_self_0 * (self.values_beta[t] - self.values_alpha[t])
        else:
            input_self = (self.values_beta[t] - self.values_alpha[t])
        # 状态更新
        next_value_alpha = self.values_alpha[t] + self.epsilon * (input_neighbor + input_self)
        next_value_beta = self.values_beta[t] - self.epsilon * input_self
        self.values_alpha.append(next_value_alpha)
        self.values_beta.append(next_value_beta)

class Strategy2_1(Strategy):
    def __init__(self, system_title: str, threshold: int, n=3) -> None:
        self.system_title = system_title    # 系统名称
        self.threshold = threshold      # 系统运行停止时刻
        self.n = n  # 系统输出的精度值
        self.nodes = []     # 系统中的节点集

    def add_nodes(self, nodes: List[Node2_1]) -> None:
        """
        添加节点集
        :param nodes:
        :return:
        """
        for node in nodes:
            self.nodes.append(node)

    def run(self) -> None:
        """
        运行流程：智能体生成噪声，智能体信息交互，智能体更新状态
        :return:
        """
        for t in range(self.threshold):
            for node in self.nodes:
                node.receive_message(t)
            for node in self.nodes:
                node.update(t)

    def get_expect_average_value(self) -> float:
        """返回系统预期的初始平均值"""
        average_value = 0.0
        for node in self.nodes:
            average_value += node.initial_value

        average_value /= len(self.nodes)
        return self.set_precision(average_value)

    def get_internal_values(self, node=None, t=-1) -> List[float]:
        """返回指定节点在t时刻的状态，缺node返回第一个，缺t返回最后时刻"""
        if node is not None:
            result = [self.set_precision(node.values_alpha[t]),
                      self.set_precision(node.values_beta[t])]
        else:
            result = [self.set_precision(self.nodes[0].values_alpha[t]),
                      self.set_precision(self.nodes[0].values_beta[t])]
        return result

    def get_final_values(self) -> List[List[float]]:
        """返回所有节点的收敛值"""
        result = []
        for node in self.nodes:
            result.append(self.get_internal_values(node))
        return result

    def get_initial_values(self) -> List[List[float]]:
        """返回所有节点的初始值"""
        result = []
        for node in self.nodes:
            result.append(self.get_internal_values(node, 0))
        return result

    def get_values_all(self) -> List[List[List[float]]]:
        """返回所有节点的收敛全程值"""
        result = []
        for node in self.nodes:
            result.append([node.values_alpha, node.values_beta])
        return result

    def get_initial_values_alpha(self):
        result = []
        for node in self.nodes:
            result.append(node.values_alpha[0])
        return result

    def set_precision(self, value: float):
        """设置返回值精度"""
        return np.round(value, self.n)




