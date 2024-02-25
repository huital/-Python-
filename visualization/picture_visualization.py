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
from matplotlib.colors import to_rgba

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

def show_system_consensus2(data: List[List[List[float]]], title: str, average: float, is_saved=None) -> None:
    """
    绘制状态分解的一致性更新过程展示
    :param data:
    :param title:
    :param is_saved: 需要保存的图片名称
    :return:
    """
    ticks = len(data[0][1])
    x_ticks = np.arange(ticks)
    average_value = [average] * ticks
    labels = []
    plt.figure(figsize=(8, 6))

    for i in range(len(data)):
        plt.plot(x_ticks, data[i][0], linewidth=2.5)
        labels.append(f"智能体{i+1}的alpha节点收敛轨迹")
        plt.plot(x_ticks, data[i][1], linewidth=2.5, linestyle='--')
        labels.append(f"智能体{i + 1}的beta节点收敛轨迹")

    plt.plot(x_ticks, average_value, c='black', linewidth=2.5, linestyle='--')
    labels.append("系统的期望平均值")

    plt.legend(labels=labels, loc='best')
    plt.xlabel("迭代次数")
    plt.ylabel("状态轨迹")

    if is_saved is None:
        plt.show()
    else:
        plt.savefig(is_saved)

def show_system_consensus2_compare(data: List[List[List[float]]],
                                   data2: List[List[List[float]]],
                                   title: str,
                                   average: float,
                                   is_saved=None) -> None:
    """
    绘制两种系统的所有子状态对比图，依据状态啊分解机制将会绘制两张图放在一起
    :param data:
    :param title:
    :param is_saved: 需要保存的图片名称
    :return:
    """
    ticks = len(data[0][1])
    x_ticks = np.arange(ticks)
    average_value = [average] * ticks
    labels = []
    labels2 = []
    plt.figure(figsize=(16, 6))
    plt.subplot(1, 2, 1)
    # 绘制alpha
    for i in range(len(data)):
        p1, = plt.plot(x_ticks, data[i][0], linewidth=2.5, linestyle='--')
        labels.append(f"系统1智能体{i+1}的alpha节点收敛轨迹")
        color = p1.get_color()
        faded_color = (*to_rgba(color)[:3], 0.5)
        plt.plot(x_ticks, data2[i][0], color=faded_color, linewidth=2.5)
        labels.append(f"系统2智能体{i + 1}的alpha节点收敛轨迹")
    plt.plot(x_ticks, average_value, c='black', linewidth=2.5, linestyle='--')
    labels.append("系统的期望平均值")
    plt.legend(labels=labels, loc='best')
    plt.xlabel("迭代次数")
    plt.ylabel("状态轨迹")

    # 绘制beta
    plt.subplot(1, 2, 2)
    for i in range(len(data)):
        p1, = plt.plot(x_ticks, data[i][1], linewidth=2.5, linestyle='--')
        labels.append(f"系统1智能体{i + 1}的beta节点收敛轨迹")
        color = p1.get_color()
        faded_color = (*to_rgba(color)[:3], 0.5)
        plt.plot(x_ticks, data2[i][1], color=faded_color, linewidth=2.5)
        labels.append(f"系统2智能体{i + 1}的beta节点收敛轨迹")
    plt.plot(x_ticks, average_value, c='black', linewidth=2.5, linestyle='--')
    labels.append("系统的期望平均值")
    plt.legend(labels=labels, loc='best')
    plt.xlabel("迭代次数")
    plt.ylabel("状态轨迹")

    if is_saved is None:
        plt.show()
    else:
        plt.savefig(is_saved)