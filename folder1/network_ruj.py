import os
import networkx as nx
from itertools import combinations
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent / "ruj_s"

def json_to_list_of_lists():
    lol_authors = []

    for file in BASE.glob("*.json"):
        with open(file, "r") as f:
            data = json.load(f)

        for j in data["_embedded"]["searchResult"]["_embedded"]["objects"]:
            try:
                authors = j["_embedded"]["indexableObject"]["metadata"]["dc.contributor.author"]
                lol_authors.append([a["value"] for a in authors])
            except Exception:
                print(file.name)

    return lol_authors


def subgraph(G, min_degree = 2, save=True):
    """filtering nodes by degree"""
    filtered_nodes = [n for n, d in G.degree() if d > min_degree]
    subgraph = G.subgraph(filtered_nodes)
    if save:
        nx.write_gexf(subgraph, "sub_graph_co_occurrence.gexf")

def graph_data(data, save=False):
    """lol to graph data - .gexf export"""
    G = nx.Graph()
    for group in data:
        for a, b in combinations(group, 2):
            if G.has_edge(a, b):
                G[a][b]["weight"] += 1
            else:
                G.add_edge(a, b, weight=1)
    if save:
        nx.write_gexf(G, "co_occurrence.gexf")
    return G

def additional_var(G):
    """adding additional variables to nodes code snippets"""
    # Single attribute
    scores = {"label_1": 0.9, "label_2": 0.5, "label_3": 0.7}
    nx.set_node_attributes(G, scores, name="score")

    # Multiple attributes at once
    attrs = {
        "label_1": {"score": 0.9, "group": "A"},
        "label_2": {"score": 0.5, "group": "B"},
    }
    nx.set_node_attributes(G, attrs)

    #  One node at a time
    G.nodes["label_1"]["group"] = "A"

    # from df
    import pandas as pd

    meta = pd.DataFrame({"name": ["label_1", "label_2"], "score": [0.9, 0.5], "group": ["A", "B"]})
    attrs = meta.set_index("name").to_dict(orient="index")
    nx.set_node_attributes(G, attrs)


def main():
    data = json_to_list_of_lists()
    G = graph_data(data, save=True)

    # Structure
    print("Density       :", nx.density(G))
    print("Connected     :", nx.is_connected(G))
    print("Components    :", nx.number_connected_components(G))

    # Centrality
    degree = nx.degree_centrality(G) # who is most connected
    betweenness = nx.betweenness_centrality(G, weight="weight") # who acts as a bridge between others
    closeness = nx.closeness_centrality(G) # who can reach everyone most quickly
    print("Centrality:")
    for node in sorted(degree, key=degree.get, reverse=True):
        print(
            f"{node:20s}  degree={degree[node]:.2f}  betweenness={betweenness[node]:.2f}  closeness={closeness[node]:.2f}")

    # Clustering
    print("Avg clustering:", nx.average_clustering(G))

    #################################
    # Groupings within the network ##
    #################################
##################################################################
    # Communities (Louvain)
    from networkx.algorithms.community import louvain_communities
    communities = louvain_communities(G, weight="weight", seed=42)
    for i, community in enumerate(communities):
        print(f"Community {i}: {community}")
##################################################################
#     from networkx.algorithms.community import girvan_newman
#     communities = girvan_newman(G)
#     top_level = next(communities)  # First split into 2 communities
#     print([sorted(c) for c in top_level])
##################################################################
#     from networkx.algorithms.community import greedy_modularity_communities
#     communities = greedy_modularity_communities(G)
#     for i, c in enumerate(communities):
#         print(f"Community {i}: {sorted(c)}")



#     subgraph(G)


main()