"""测试文献:Privacy Preserving Average Consensus"""
from methods.privacy1.privacy1_1 import Node1_1, Strategy1_1
from visualization.text_visualization import *
from visualization.picture_visualization import *
from tests.base_topo import *

epsilon = 0.3
threshold = 50

def create_system_1_1_1() -> Strategy1_1:
    node_1 = Node1_1(1.0, epsilon, 0.8)
    node_2 = Node1_1(2.0, epsilon, 0.8)
    node_3 = Node1_1(3.0, epsilon, 0.8)
    node_4 = Node1_1(4.0, epsilon, 0.8)
    node_5 = Node1_1(5.0, epsilon, 0.8)
    strategy = Strategy1_1("基于注入节点噪声的隐私保护方法", threshold)
    nodes = system_5_1([node_1, node_2, node_3, node_4, node_5])
    strategy.add_nodes(nodes)

    return strategy

def run1_1():
    system1 = create_system_1_1_1()
    system1.run()
    show_consensus_result1(system1)
    show_system_consensus1(system1.get_values_all(), system1.system_title, system1.get_expect_average_value())


