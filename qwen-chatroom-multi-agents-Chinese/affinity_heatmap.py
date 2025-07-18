# affinity_heatmap.py
import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from collections import defaultdict

matplotlib.use('TkAgg')  # 为 Mac 设置合适的后端

def load_chat_log(filename="chat_log.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def build_affinity_matrix(chat_log):
    speakers = sorted(set(msg["speaker"] for msg in chat_log))
    affinity = defaultdict(lambda: defaultdict(int))

    # 统计互动次数
    for msg in chat_log:
        speaker = msg["speaker"]
        for target in msg.get("respond_to", []):
            if target != "topic" and target != speaker:
                affinity[speaker][target] += 1

    # 获取所有非零分数
    all_scores = []
    for s1 in speakers:
        for s2 in speakers:
            score = affinity[s1][s2]
            if score > 0:  # 只收集非零分数
                all_scores.append(score)
    
    # 设置默认最大值为1，避免除以零
    max_score = max(all_scores) if all_scores else 1

    # 构建归一化矩阵
    matrix = np.zeros((len(speakers), len(speakers)))
    for i, s1 in enumerate(speakers):
        for j, s2 in enumerate(speakers):
            score = affinity[s1][s2]
            # 如果max_score为1且score为0，则保持为0
            matrix[i][j] = score / max_score if score > 0 else 0

    return speakers, matrix

def plot_affinity_heatmap(speakers, matrix):
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, xticklabels=speakers, yticklabels=speakers, annot=True, cmap="YlGnBu")
    plt.title("Agent Affinity Heatmap")
    plt.show()

if __name__ == "__main__":
    chat_log = load_chat_log("chat_log.json")
    speakers, matrix = build_affinity_matrix(chat_log)
    plot_affinity_heatmap(speakers, matrix)
