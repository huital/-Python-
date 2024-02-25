"""测试文献：Privacy-Preserving Average Consensus via State Decomposition
1、无向图下收敛验证（文字，仿真图）
2、修改任意分布测试是否输出一致（仿真图）
3、对节点构建观测器来窥测初始值，验证隐私保护性能（文字，仿真图）
"""
from methods.privacy2.privacy2_1 import Node2_1, Strategy2_1
from visualization.text_visualization import show_consensus_result2, show_observer_result
from visualization.picture_visualization import show_system_consensus2, show_system_consensus2_compare
from tests.base_topo import *

epsilon = 0.3
threshold = 70

"""
2_1_1编号意义，后续不重复写
2：状态分解方法
1：第一种方法
1：第一种拓扑结构
2_1_1:第一种基于状态分解思想的方法下的第一种拓扑结构
"""
def create_system_2_1_1() -> Strategy2_1:
    node_1 = Node2_1(1.0, epsilon)
    node_2 = Node2_1(2.0, epsilon)
    node_3 = Node2_1(3.0, epsilon)
    node_4 = Node2_1(4.0, epsilon)
    node_5 = Node2_1(5.0, epsilon)
    strategy = Strategy2_1("基于状态分解的隐私保护方法", threshold)
    nodes = system_5_1([node_1, node_2, node_3, node_4, node_5])

    for node in nodes:
        node.generate_initial_value()

    strategy.add_nodes(nodes)

    return strategy

def weight_function() -> List[float]:
    """生成边相关的权重参数"""
    weight_1_4 = (0.7 - 4.7 + epsilon*(5.2-1.3)) / (epsilon*(5.2-1.3))
    weight_5_4 = (3.5 + 2.5 + epsilon*(5.2-6.5)) / (epsilon*(5.2-6.5))
    return [weight_1_4, weight_5_4]

def create_system_2_1_2(initial_values_alpha: List[float]) -> Strategy2_1:
    """修改初始值分布的新实现"""
    node_1 = Node2_1(3.0, epsilon, -2.0)  # 1.0 -> 3.0 +2
    node_2 = Node2_1(2.0, epsilon)
    node_3 = Node2_1(3.0, epsilon)
    node_4 = Node2_1(5.0, epsilon, -1.0)    # 4.0 -> 5.0 +1
    node_5 = Node2_1(2.0, epsilon, 3.0)  # 5.0 -> 2.0 -3
    strategy = Strategy2_1("修改初始值分布的新实现", threshold)
    nodes = system_5_1([node_1, node_2, node_3, node_4, node_5])
    strategy.add_nodes(nodes)

    for i in range(len(nodes)):
        nodes[i].generate_initial_value1(initial_values_alpha[i])
        nodes[i].generate_weight_self()

    # 配置与边相关的权重参数，这里作者暂时未找到统一的规律，因此具体问题具体分析
    weights = weight_function()
    strategy.nodes[0].generate_weight([node_4], [weights[0]])
    strategy.nodes[3].generate_weight([node_1, node_5], [weights[0], weights[1]])
    strategy.nodes[4].generate_weight([node_4], [weights[1]])



    return strategy

def run2_1():
    system1 = create_system_2_1_1()
    system2 = create_system_2_1_2(system1.get_initial_values_alpha())
    # 系统运行区
    system1.run()
    system2.run()

    # 文字展示区
    show_consensus_result2(system1)
    show_consensus_result2(system2)

    # 仿真图展示区
    # show_system_consensus2(system1.get_values_all(), system1.system_title, system1.get_expect_average_value())
    # show_system_consensus2_compare(system1.get_values_all(),
    #                                system2.get_values_all(),
    #                                system1.system_title,
    #                                system1.get_expect_average_value())

    # 隐私保护性能测试区
    show_observer_result(system1.nodes[3], system1.nodes[4], epsilon, threshold, 1)
    show_observer_result(system2.nodes[3], system2.nodes[4], epsilon, threshold, -14.384615384615387)
