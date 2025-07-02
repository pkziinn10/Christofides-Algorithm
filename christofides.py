import sys
from collections import defaultdict, deque
import networkx as nx  # só para emparelhamento perfeito de custo mínimo

def read_graph(path):
    with open(path) as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0])
    g = [[float(x) for x in row.split()] for row in lines[1:1+n]]
    return g, n

def prim_mst(g, n):
    in_mst = [False]*n
    dist = [float('inf')]*n
    parent = [-1]*n
    dist[0] = 0
    edges = []
    for _ in range(n):
        u = min((d,i) for i,d in enumerate(dist) if not in_mst[i])[1]
        in_mst[u] = True
        if parent[u] != -1:
            edges.append((parent[u], u))
        for v in range(n):
            if not in_mst[v] and g[u][v] < dist[v]:
                dist[v] = g[u][v]
                parent[v] = u
    return edges

def find_odd_vertices(edges, n):
    deg = [0]*n
    for u,v in edges:
        deg[u]+=1; deg[v]+=1
    return [i for i,d in enumerate(deg) if d%2==1]

def min_weight_perfect_matching(g, odd):
    # Cria grafo completo entre vértices ímpares
    G = nx.Graph()
    for u in odd:
        G.add_node(u)
    for i,u in enumerate(odd):
        for v in odd[i+1:]:
            G.add_edge(u, v, weight=g[u][v])
    # emparelhamento mínimo de custo (maxcardinality=True garante perfeito)
    mate = nx.algorithms.matching.min_weight_matching(G, weight='weight')
    return list(mate)

def build_multigraph(n, mst, matching):
    adj = defaultdict(list)
    for u,v in mst+matching:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def eulerian_tour(adj, start):
    # Hierholzer
    local = {u: deque(neigh) for u, neigh in adj.items()}
    stack = [start]
    path = []
    while stack:
        u = stack[-1]
        if local[u]:
            v = local[u].popleft()
            # remover aresta de v→u
            local[v].remove(u)
            stack.append(v)
        else:
            path.append(u)
            stack.pop()
    return path

def shortcut_eulerian(path):
    seen = set()
    tour = []
    for u in path:
        if u not in seen:
            seen.add(u)
            tour.append(u)
    tour.append(tour[0])
    return tour

def compute_cost(tour, g):
    return sum(g[tour[i]][tour[i+1]] for i in range(len(tour)-1))

def christofides(g, n):
    mst = prim_mst(g, n)
    odd = find_odd_vertices(mst, n)
    matching = min_weight_perfect_matching(g, odd)
    multi = build_multigraph(n, mst, matching)
    euler = eulerian_tour(multi, 0)
    ham = shortcut_eulerian(euler)
    cost = compute_cost(ham, g)
    return ham, cost

if __name__ == "_main_":
    if len(sys.argv) != 2:
        print("Uso: python christofides.py <graph.txt>")
        sys.exit(1)

    graph, n = read_graph(sys.argv[1])
    tour, total = christofides(graph, n)
    print("Ciclo Hamiltoniano (0-based):")
    print(" -> ".join(map(str, tour)))
    print(f"Custo total: {total:.2f}")
