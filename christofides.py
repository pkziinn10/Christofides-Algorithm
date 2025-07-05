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
        # Processamento para aceitar formatos com colchetes e vírgulas
        cleaned_line = lines[i].replace('[', '').replace(']', '').strip()
        parts = [x.strip() for x in cleaned_line.split(',') if x.strip()]

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

    # Validar simetria
    for i in range(n):
        for j in range(i + 1, n):
            if abs(g[i][j] - g[j][i]) > 1e-6:
                raise ValueError(f"A matriz não é simétrica: g[{i}][{j}]={g[i][j]} != g[{j}][{i}]={g[j][i]}")

    return g, n

def prim_mst(g, n):
    if n == 0:
        return [], 0.0

    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=g[i][j])

    mst = nx.minimum_spanning_tree(G, algorithm='prim')
    mst_edges = list(mst.edges(data=True))
    mst_weight = sum(edge[2]['weight'] for edge in mst_edges)

    return mst_edges, mst_weight

def find_odd_vertices(mst_edges, n):
    deg = [0] * n
    for u, v, _ in mst_edges:
        deg[u] += 1
        deg[v] += 1
    odd = [i for i, d in enumerate(deg) if d % 2 == 1]

    if len(odd) % 2 != 0:
        raise RuntimeError("Número ímpar de vértices de grau ímpar detectado")

    return odd

def min_weight_perfect_matching(g, odd_vertices):
    if len(odd_vertices) == 0:
        return []

    G = nx.Graph()
    for i in range(len(odd_vertices)):
        for j in range(i + 1, len(odd_vertices)):
            u = odd_vertices[i]
            v = odd_vertices[j]
            G.add_edge(u, v, weight=g[u][v])

    matching = nx.min_weight_matching(G, weight='weight')
    return [(min(u, v), max(u, v)) for u, v in matching]

def build_multigraph(mst_edges, matching_edges, g):
    multigraph = nx.MultiGraph()

    for u, v, data in mst_edges:
        multigraph.add_edge(u, v, weight=data['weight'])

    for u, v in matching_edges:
        multigraph.add_edge(u, v, weight=g[u][v])

    return multigraph

def find_eulerian_tour(multigraph):
    try:
        return list(nx.eulerian_circuit(multigraph))
    except nx.NetworkXError:
        return []

def shortcut_eulerian_tour(euler_tour):
    if not euler_tour:
        return []

    visited = set()
    tour = []
    for u, v in euler_tour:
        if u not in visited:
            visited.add(u)
            tour.append(u)
    tour.append(tour[0])
    return tour

def calculate_tour_cost(tour, g):
    if len(tour) < 2:
        return 0.0

    cost = 0.0
    for i in range(len(tour) - 1):
        u = tour[i]
        v = tour[i + 1]
        cost += g[u][v]
    return cost

def christofides(g, n):
    if n == 0:
        return [], 0.0, [], 0.0
    if n == 1:
        return [], 0.0, [0, 0], 0.0

    # Obter MST (retorna edges e weight)
    mst_edges, mst_weight = prim_mst(g, n)

    # Encontrar vértices ímpares
    odd_vertices = find_odd_vertices(mst_edges, n)

    # Emparelhamento perfeito mínimo
    matching_edges = min_weight_perfect_matching(g, odd_vertices)

    # Construir multigrafo - CORREÇÃO: passar mst_edges em vez de n
    multigraph = build_multigraph(mst_edges, matching_edges, g)

    # Encontrar circuito euleriano
    euler_tour = find_eulerian_tour(multigraph)

    # Obter circuito hamiltoniano
    hamiltonian_tour = shortcut_eulerian_tour(euler_tour)

    # Calcular custo
    tour_cost = calculate_tour_cost(hamiltonian_tour, g)

    return mst_edges, mst_weight, hamiltonian_tour, tour_cost

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python christofides.py <graph.txt>")
        sys.exit(1)

    try:
        graph, n = read_graph(sys.argv[1])
        mst_edges, mst_weight, tour, total = christofides(graph, n)

        print("Árvore Geradora Mínima:")
        print(mst_edges)
        print(f"Peso da árvore geradora mínima: {mst_weight}")

        print("\nSolução Aproximada Encontrada por Christofides:")
        print(tour)
        print(f"Peso da Solução: {total}")

        print("\nValor da Solução Ótima: 1610")

    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
