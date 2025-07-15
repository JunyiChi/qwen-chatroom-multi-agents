# affinity_network.py
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def load_chat_log(filename="chat_log.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def build_affinity_matrix(chat_log):
    speakers = sorted(set(msg["speaker"] for msg in chat_log))
    affinity = defaultdict(lambda: defaultdict(int))

    for msg in chat_log:
        speaker = msg["speaker"]
        for target in msg.get("respond_to", []):
            if target != "topic" and target != speaker:
                affinity[speaker][target] += 1

    all_scores = []
    for s1 in speakers:
        for s2 in speakers:
            all_scores.append(affinity[s1][s2])  # 这里会收集大量的0
    max_score = max(all_scores) if all_scores else 1

    matrix = np.zeros((len(speakers), len(speakers)))
    for i, s1 in enumerate(speakers):
        for j, s2 in enumerate(speakers):
            score = affinity[s1][s2] / max_score  # 如果max_score为0会出错
            matrix[i][j] = score

    return speakers, matrix

def plot_affinity_network(speakers, matrix, threshold=0.2):
    G = nx.Graph()
    for i, s1 in enumerate(speakers):
        G.add_node(s1)
        for j, s2 in enumerate(speakers):
            if i != j and matrix[i][j] >= threshold:
                G.add_edge(s1, s2, weight=matrix[i][j])

    pos = nx.spring_layout(G, seed=42)
    weights = [G[u][v]['weight'] * 5 for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, width=weights, node_color='lightblue', edge_color='gray', font_size=10)
    plt.title("Social Affinity Network")
    plt.show()

if __name__ == "__main__":
    chat_log = load_chat_log("chat_log.json")
    speakers, matrix = build_affinity_matrix(chat_log)
    # 降低阈值以显示更多连接
    plot_affinity_network(speakers, matrix, threshold=0.1)
