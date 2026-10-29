import networkx as nx
import numpy as np

G = nx.Graph()

# 定义计算平均路径长度
def compute_average_path_length(graph,node):
    total_distance = sum(shortest_path_length[node].values())
    return total_distance / (len(graph.nodes) - 1)
# 定义计算邻居的聚集度
def compute_neighbor_clustering(graph,node):
    neighbors = list(graph.neighbors(node))
    if not neighbors:
        return 0
    return np.mean([clustering[n] for n in neighbors])
# 定义计算结构洞限制度SHC
def compute_constraint(graph, node):
    neighbors = list(graph.neighbors(node))
    constraint = 0
    for j in neighbors:
        p_ij = 1.0 / len(neighbors)  # 近似计算
        indirect_sum = sum((1.0 / len(list(graph.neighbors(q)))) for q in neighbors if j in graph.neighbors(q))
        constraint += (p_ij + p_ij * indirect_sum) ** 2
    return constraint
# Propagation diversity P_i
def compute_channel_capacity(node):
    #B_i = degree[node] * (1 - clustering[node])
    D_i = degree_centrality[node] * (1- clustering[node])
    S_i = degree_centrality[node] + eigenvector_centrality[node]  # 近似代替信息功率
    #N_i = average_path_length[node] + neighbor_clustering[node] + constraint[node]  # 近似噪声
    R_i = 1+neighbor_clustering[node] + constraint[node]
    return D_i * np.log2(1 + S_i / (R_i + 1e-6))  # 避免除零错误
def normalize_k_shell(k_shell_dict):
    """
    归一化 k-shell 值到 [0, 1] 范围

    参数:
        k_shell_dict: 包含节点 k-shell 值的字典，格式为 {node: k_shell_value}

    返回:
        归一化后的字典
    """
    if not k_shell_dict:
        return {}

    # 获取所有 k-shell 值
    values = list(k_shell_dict.values())

    # 计算最小值和最大值
    min_val = min(values)
    max_val = max(values)

    # 如果所有值相同（避免除以0）
    if max_val == min_val:
        return {node: 1.0 for node in k_shell_dict}

    # 归一化每个值
    normalized = {}
    for node, value in k_shell_dict.items():
        normalized[node] = (value - min_val) / (max_val - min_val)

    return normalized
#(Jaccard similarity)
def simjkd(graph,u, v):
    set_v = set( graph.neighbors(v))
    set_v.add(v)
    set_u = set( graph.neighbors(u))
    set_u.add(u)
    jac = len(set_v & set_u) * 1.0 / len(set_v | set_u)
    return jac

# Structural-relevance-weighted neighborhood reinforcement G_i
def compute_matthew_effect(graph):
    G={}
    for node in graph.nodes:
       
        dks_node=degree_centrality[node]*normalized_k_shell[node]
        neighbors = list(graph.neighbors(node))
        dks_n=0
        for j in neighbors:
            js=simjkd(graph, node, j)
            dks_n=dks_n+degree_centrality[j]*normalized_k_shell[j]*js
            # if(node==3 or node==8):
            #     print(node,j,degree_centrality[j]*normalized_k_shell[j]*js,degree_centrality[j],normalized_k_shell[j],js)
        dks=dks_node+dks_n
        G.setdefault(node,dks)



    return G


# 计算最终的关键节点评分 K_i
def compute_key_node_score(node):
    return channel_capacity[node] * matthew_effect[node]
# 1. 读取的数据集
allpath="./datasets/datalist1.txt"
allpathlist=''
# 1. 读取 Karate 网络数据
# graph = nx.karate_club_graph()
with open(allpath, 'r') as f:
    allpathlist = f.readlines()
    f.close()
pathfile = ''
for pt in allpathlist:
    pt = pt.strip('\n')
    pathfile = "./datasets/" + pt + '/data/' + pt + '.txt'
    G.clear()

    with open(pathfile) as file:
        for line in file:
            head, tail = [int(x) for x in line.split()]
            G.add_edge(head, tail)
    file.close()
    G = G.to_undirected()
    G.remove_edges_from(nx.selfloop_edges(G))

    # 2. 计算基本结构指标
    degree = dict(G.degree())  # 度数
    degree_centrality = nx.degree_centrality(G)  # 度中心性
    clustering = nx.clustering(G)  # 局部聚类系数
    # shortest_path_length = dict(nx.all_pairs_shortest_path_length(G))  # 所有最短路径
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=500)  # 特征向量中心性
    k_shell = nx.core_number(G)  # k-shell
    # 归一化后的 k-shell
    normalized_k_shell = normalize_k_shell(k_shell)
    #计算平均路径长度
    #average_path_length = {node: compute_average_path_length(G,node) for node in G.nodes}
    # 计算邻居的聚集度
    neighbor_clustering = {node: compute_neighbor_clustering(G,node) for node in G.nodes}
    # 计算结构洞限制度
    constraint = {node: compute_constraint(G, node) for node in G.nodes}
    #  Propagation diversity P_i
    channel_capacity = {node: compute_channel_capacity(node) for node in G.nodes}
    # Structural-relevance-weighted neighborhood reinforcement G_i
    # matthew_effect = {node: compute_matthew_effect(node) for node in G.nodes}
    matthew_effect = compute_matthew_effect(G)

    key_node_scores = {node: compute_key_node_score(node) for node in G.nodes}

    # 按得分排序
    sorted_nodes = sorted(key_node_scores.items(), key=lambda x: x[1], reverse=True)
    files = "./datasets/" + pt + '/sir_alg/sm_' + pt + '.txt'
    f1 = open(files, "w+")
    for key, val in sorted_nodes:
        f1.write(str(key) + '\t' + str(val) + "\n")

    f1.close()
    print(pt+" was donwn")
    # 输出排名结果
    # print("关键节点排序（降序）：")
    # for rank, (node, score) in enumerate(sorted_nodes, 1):
    #     print(f"排名 {rank}: 节点 {node}, 关键性得分 {score:.4f}")
