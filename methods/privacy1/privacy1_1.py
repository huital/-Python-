"""文献:Privacy Preserving Average Consensus的复现实现"""
from methods.base_method import Strategy
from typing import List
import numpy as np

class Node1_1:
    def __init__(self, initial_value: float, epsilon: float, psi):
        self.initial_value = initial_value
        self.epsilon = epsilon  # 控制增益
        self.psi = psi      # 噪声参数
        self.values = [initial_value]
        self.neighbors = {}
        self.noises = []    # 添加的噪声集
        self.last_noise = 0.0

    def add_neighbors(self, nodes: List) -> None:
        """
        建立和邻居的连接
        :param nodes:
        :return:
        """
        for node in nodes:
            self.neighbors[node] = []

    def send_message(self, t: int) -> float:
        """
        发送在t时刻含噪的扰动值给邻居
        :param t:
        :return:
        """
        return self.values[t] + self.noises[t]

    def receive_message(self, t: int) -> None:
        for node in self.neighbors:
            self.neighbors[node].append(node.send_message(t))

    def set_noise(self, t: int) -> None:
        """
        设置在t时刻的噪声
        :param t:
        :return:
        """
        if t == 0:
            self.last_noise = np.random.normal(0, 1)
            self.noises.append(self.last_noise)
        else:
            noise = np.random.normal(0, 1)
            zero_noise = np.power(self.psi, t) * noise - np.power(self.psi, t-1)*self.last_noise
            self.noises.append(zero_noise)
            self.last_noise = noise

    def update(self, t: int) -> None:
        """
        状态更新，通过t时刻的信息来获取t+1时刻的状态值
        :param t:
        :return:
        """
        input = 0.0
        for node in self.neighbors:
            input += self.epsilon*(self.neighbors[node][t] - self.values[t] - self.noises[t])

        next_value = self.values[t] + input + self.noises[t]
        self.values.append(next_value)

class Strategy1_1(Strategy):
    def __init__(self, system_title: str, threshold: int, n=3) -> None:
        self.system_title = system_title    # 系统名称
        self.threshold = threshold      # 系统运行停止时刻
        self.n = n  # 系统输出的精度值
        self.nodes = []     # 系统中的节点集

    def add_nodes(self, nodes: List[Node1_1]) -> None:
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
                node.set_noise(t)
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

    def get_internal_values(self, node=None, t=-1) -> float:
        """返回指定节点在t时刻的状态，缺node返回第一个，缺t返回最后时刻"""
        if node is not None:
            result = self.set_precision(node.values[t])
        else:
            result = self.set_precision(self.nodes[0].values[t])
        return result

    def get_final_values(self) -> List[float]:
        """返回所有节点的收敛值"""
        result = []
        for node in self.nodes:
            result.append(self.get_internal_values(node))
        return result

    def get_initial_values(self) -> List[float]:
        """返回所有节点的初始值"""
        result = []
        for node in self.nodes:
            result.append(self.get_internal_values(node, 0))
        return result

    def get_values_all(self) -> List[List[float]]:
        """返回所有节点的收敛全程值"""
        result = []
        for node in self.nodes:
            result.append(node.values)
        return result

    def set_precision(self, value: float):
        """设置返回值精度"""
        return np.round(value, self.n)
