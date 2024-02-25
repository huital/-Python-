# 通过文字形式来展示方法结果
import numpy as np
def show_consensus_result1(system):
    print("=======================================")
    print(f"{system.system_title}的收敛结果展示")
    initial_values = system.get_initial_values()
    final_values = system.get_final_values()
    expect_value = system.get_expect_average_value()

    for i in range(len(initial_values)):
        print(f"智能体{i+1}的初始值：{initial_values[i]}，收敛值：{final_values[i]}")
    print("++++++++++++++++++++")
    if np.abs(expect_value - final_values[0]) <= 0.1:
        print(f"系统达成平均共识：{expect_value}")
    else:
        print(f"收敛失败，请检查方法是否错误！")
    print("=======================================")

def show_consensus_result2(system):
    """基于状态分解的隐私保护收敛结果展示"""
    print("=======================================")
    print(f"{system.system_title}的收敛结果展示")
    initial_values = system.get_initial_values()
    final_values = system.get_final_values()
    expect_value = system.get_expect_average_value()

    for i in range(len(initial_values)):
        print(f"智能体{i + 1}的alpha节点初始值：{initial_values[i][0]}，收敛值：{final_values[i][0]}")
        print(f"智能体{i + 1}的beta节点初始值：{initial_values[i][1]}，收敛值：{final_values[i][1]}")
        print("----------------")
    print("++++++++++++++++++++")
    if np.abs(expect_value - final_values[0][0]) <= 0.1:
        print(f"系统达成平均共识：{expect_value}")
    else:
        print(f"收敛失败，请检查方法是否错误！")
    print("=======================================")

def show_observer_result(incurious_node, spied_node, epsilon, threshold, weight) -> None:
    """
    展示好奇节点通过已有信息对邻居的初始隐私窥测，注意这里一般只展示能推测成功的例子
    :param incurious_node: 好奇节点集合
    :param spied_node: 被窥测节点
    :param epsilon: 控制增益
    :param weights: 权重集合，邻居，自身
    :return:
    """
    result = [(incurious_node.values_alpha[-1] + incurious_node.neighbors[spied_node][0]) / 2.0]
    for i in range(0, threshold - 1):
        if i == 0:
            invisible_delta = incurious_node.neighbors[spied_node][i + 1] - incurious_node.neighbors[spied_node][
                i] - epsilon * weight * (
                                      incurious_node.values_alpha[i] - incurious_node.neighbors[spied_node][i])
        else:
            invisible_delta = incurious_node.neighbors[spied_node][i + 1] - incurious_node.neighbors[spied_node][
                i] - epsilon * (
                                      incurious_node.values_alpha[i] - incurious_node.neighbors[spied_node][i])
        result.append(result[i] + invisible_delta / 2.0)

    print("=======================================")
    print("智能体被窥测结果展示图")
    print(f"智能体的初始状态：{spied_node.initial_value}")
    print("系统推测的初始值为:", result[-1])
    if np.abs(result[-1] - spied_node.initial_value) <= 0.1:
        print("智能体的初始隐私泄露，隐私保护失效！")

    print("=======================================")