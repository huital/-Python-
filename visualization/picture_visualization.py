# 以绘图方式展现结果
from typing import List
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import matplotlib
import numpy as np
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.sans-serif'] = 'SimHei'  # 解决中文乱码
# plt.rc('font', family='Times New Roman')
# matplotlib.rcParams['font.family'] = 'Times New Roman'

def show_system_consensus1(data: List[List[float]], title: str, average: float, is_saved=None) -> None:
    """
    绘制非状态分解的一致性更新过程展示
    :param data:
    :param title:
    :param is_saved: 需要保存的图片名称
    :return:
    """
    ticks = len(data[0])
    x_ticks = np.arange(ticks)
    average_value = [average] * ticks
    labels = []
    plt.figure(figsize=(8, 6))

    for i in range(len(data)):
        plt.plot(x_ticks, data[i], linewidth=2.5)
        labels.append(f"智能体{i+1}的收敛轨迹")
    plt.plot(x_ticks, average_value, c='black', linewidth=2.5, linestyle='--')
    labels.append("系统的期望平均值")

    plt.legend(labels=labels, loc='best')
    plt.xlabel("迭代次数")
    plt.ylabel("状态轨迹")

    if is_saved is None:
        plt.show()
    else:
        plt.savefig(is_saved)