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
