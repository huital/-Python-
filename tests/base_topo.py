"""提供基本的拓扑连接方式"""
from typing import List

def system_5_1(nodes: List) -> List:
    """
    构建五个节点的无向图连接方式，具体可以看topo_5_1.png
    :param nodes:
    :return:
    """
    if len(nodes) != 5:
        print(f"节点数量不满足要求:预期5个，实际{len(nodes)}")
        return None

    node_1 = nodes[0]
    node_2 = nodes[1]
    node_3 = nodes[2]
    node_4 = nodes[3]
    node_5 = nodes[4]

    node_1.add_neighbors([node_2, node_4])
    node_2.add_neighbors([node_1, node_3])
    node_3.add_neighbors([node_2, node_4])
    node_4.add_neighbors([node_1, node_3, node_5])
    node_5.add_neighbors([node_4])

    return nodes


