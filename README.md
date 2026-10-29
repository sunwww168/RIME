Identifying vital nodes is an important task in complex network analysis, with applications in epidemic spreading, information diffusion, and network management.

RIME is a topology-based node-ranking method that balances propagation potential and structural redundancy. Unlike methods that primarily emphasize positive structural properties, RIME explicitly considers the diminishing propagation benefits caused by redundant local connections.

The proposed method consists of two complementary components:

Redundancy-aware propagation potential: Evaluates a node's effective spreading potential by combining normalized degree, eigenvector centrality, local clustering, and structural-hole constraint.

Neighborhood reinforcement: Aggregates the intrinsic structural potential of neighboring nodes using Jaccard similarity to characterize their structural relevance.

These components are multiplicatively integrated to produce the final RIME score. Nodes are ranked in descending order of their scores.

Key Features

Parameter-free node importance evaluation.

Explicit consideration of structural redundancy.

Similarity-weighted neighborhood reinforcement.

Multiplicative integration of complementary structural information.

Applicable to undirected and unweighted complex networks.

Experimental Evaluation

RIME is evaluated on eight real-world networks against eleven representative node-ranking methods.

The evaluation includes:

SIR-based spreading capability.

Kendall's rank correlation.

Top-k influential node identification.

Ranking discrimination and CCDF analysis.

Component-wise ablation experiments.

Additional case studies investigate its applicability to epidemic contact networks and hydrological monitoring networks.
