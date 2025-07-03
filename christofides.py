import sys
from collections import defaultdict, deque
import networkx as nx

def read_graph(path):
    with open(path) as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise ValueError("Arquivo vazio")

    try:
        n = int(lines[0])
    except ValueError:
        raise ValueError("Primeira linha deve ser um inteiro (número de vértices)")

    if n <= 0:
        raise ValueError("Número de vértices deve ser positivo")

    if len(lines) < n + 1:
        raise ValueError(f"Esperadas {n+1} linhas, mas encontradas {len(lines)}")

    g = []
    for i in range(1, n + 1):
        parts = lines[i].split()
        if len(parts) != n:
            raise ValueError(f"Linha {i+1}: esperados {n} valores, encontrados {len(parts)}")

        row = []
        for x in parts:
            try:
                num = float(x)
            except ValueError:
                raise ValueError(f"Valor não numérico na linha {i+1}: '{x}'")
            if num < 0:
                raise ValueError(f"Peso negativo na linha {i+1}: {num}")
            row.append(num)
        g.append(row)

    return g, n

def prim_mst(g, n):
    if n == 0:
        return []

    in_mst = [False] * n
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[0] = 0
    edges = []

    for _ in range(n):
        try:
            u = min((d, i) for i, d in enumerate(dist) if not in_mst[i])[1]
        except ValueError:
            raise ValueError("Grafo não é conexo")

        in_mst[u] = True
        if parent[u] != -1:
            edges.append((parent[u], u))

        for v in range(n):
            if not in_mst[v] and g[u][v] < dist[v]:
                dist[v] = g[u][v]
                parent[v] = u

    if len(edges) != n - 1:
        raise ValueError("Grafo não é conexo")

    return edges

def find_odd_vertices(edges, n):
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    odd = [i for i, d in enumerate(deg) if d % 2 == 1]

    if len(odd) % 2 != 0:
        raise RuntimeError("Número ímpar de vértices de grau ímpar detectado")

    return odd

def min_weight_perfect_matching(g, odd):
    if len(odd) == 0:
        return []

    G = nx.Graph()
    G.add_nodes_from(odd)

    for i, u in enumerate(odd):
        for v in odd[i + 1:]:
            G.add_edge(u, v, weight=g[u][v])

    mate = nx.algorithms.matching.min_weight_matching(G, weight='weight')
    return list(mate)

def build_multigraph(n, mst, matching):
    adj = defaultdict(list)
    all_edges = mst + matching

    for u, v in all_edges:
        if u >= n or v >= n or u < 0 or v < 0:
            raise ValueError(f"Aresta inválida: ({u}, {v})")
        adj[u].append(v)
        adj[v].append(u)
    return adj

def eulerian_tour(adj, start):
    if start not in adj:
        raise ValueError("Vértice inicial não encontrado no grafo")

    local = {u: deque(neigh) for u, neigh in adj.items()}
    stack = [start]
    path = []

    while stack:
        u = stack[-1]
        if local.get(u):
            v = local[u].popleft()
            if u in local[v]:
                local[v].remove(u)
            stack.append(v)
        else:
            path.append(u)
            stack.pop()

    return path

def shortcut_eulerian(path):
    if not path:
        return []

    seen = set()
    tour = []
    for u in path:
        if u not in seen:
            seen.add(u)
            tour.append(u)
    tour.append(tour[0])
    return tour

def compute_cost(tour, g):
    if not tour:
        return 0.0

    cost = 0.0
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        if u < 0 or v < 0 or u >= len(g) or v >= len(g):
            raise ValueError(f"Vértice inválido no tour: {u} ou {v}")
        cost += g[u][v]
    return cost

def christofides(g, n):
    if n == 0:
        return [], 0.0
    if n == 1:
        return [0, 0], 0.0

    mst = prim_mst(g, n)
    odd = find_odd_vertices(mst, n)
    matching = min_weight_perfect_matching(g, odd)
    multi = build_multigraph(n, mst, matching)
    euler = eulerian_tour(multi, 0)
    ham = shortcut_eulerian(euler)
    cost = compute_cost(ham, g)
    return ham, cost

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python christofides.py <graph.txt>")
        sys.exit(1)

    try:
        graph, n = read_graph(sys.argv[1])
        tour, total = christofides(graph, n)
        print("Ciclo Hamiltoniano (0-based):")
        print(" -> ".join(map(str, tour)))
        print(f"Custo total: {total:.2f}")

    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
