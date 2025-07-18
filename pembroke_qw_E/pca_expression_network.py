# pca_expression_network.py
import json
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_chat_log(filename="chat_log.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_agent_embeddings(chat_log):
    """Convert all messages from each Agent into embeddings and calculate average style vector"""
    agent_sentences = defaultdict(list)
    for entry in chat_log:
        agent_sentences[entry["speaker"]].append(entry["text"])

    agent_embeddings = {}
    for speaker, sentences in agent_sentences.items():
        sentence_vectors = model.encode(sentences)
        mean_vector = np.mean(sentence_vectors, axis=0)
        agent_embeddings[speaker] = mean_vector

    return agent_embeddings


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
            all_scores.append(affinity[s1][s2])
    max_score = max(all_scores) if all_scores else 1

    matrix = np.zeros((len(speakers), len(speakers)))
    for i, s1 in enumerate(speakers):
        for j, s2 in enumerate(speakers):
            score = affinity[s1][s2] / max_score
            matrix[i][j] = score

    return speakers, matrix


def plot_pca_expression_graph(agent_embeddings, speakers, affinity_matrix, edge_threshold=0.2):
    vectors = np.array([agent_embeddings[speaker] for speaker in speakers])
    pca = PCA(n_components=2)
    coords = pca.fit_transform(vectors)

    G = nx.Graph()
    for i, speaker in enumerate(speakers):
        G.add_node(speaker, pos=(coords[i][0], coords[i][1]))

    for i, s1 in enumerate(speakers):
        for j, s2 in enumerate(speakers):
            if i != j and affinity_matrix[i][j] >= edge_threshold:
                G.add_edge(s1, s2, weight=affinity_matrix[i][j])

    pos = nx.get_node_attributes(G, 'pos')
    weights = [G[u][v]['weight'] * 5 for u, v in G.edges()]

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', width=weights, font_size=10)
    plt.title("Agent Expression PCA + Affinity Network")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    chat_log = load_chat_log("chat_log.json")
    agent_embeddings = extract_agent_embeddings(chat_log)
    speakers, affinity_matrix = build_affinity_matrix(chat_log)
    plot_pca_expression_graph(agent_embeddings, speakers, affinity_matrix, edge_threshold=0.2)