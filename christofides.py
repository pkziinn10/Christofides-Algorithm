import sys
import heapq
import networkx as nx
from collections import defaultdict

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

    # Estruturas para o algoritmo de Prim
    in_mst = [False] * n
    parent = [-1] * n
    key = [float('inf')] * n
    key[0] = 0
    heap = [(0, 0)]

    mst_edges = []
    total_weight = 0.0

    while heap:
        weight, u = heapq.heappop(heap)

        if in_mst[u]:
            continue

        in_mst[u] = True
        total_weight += weight

        if parent[u] != -1:
            mst_edges.append((parent[u], u, {'weight': weight}))

        for v in range(n):
            if u == v or in_mst[v]:
                continue

            if g[u][v] < key[v]:
                key[v] = g[u][v]
                parent[v] = u
                heapq.heappush(heap, (g[u][v], v))

    return mst_edges, total_weight

def find_odd_vertices(mst_edges, n):
    deg = [0] * n
    for edge in mst_edges:
        u = edge[0]
        v = edge[1]
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
            # Peso negativo para obter mínimo matching
            G.add_edge(u, v, weight=-g[u][v])

    matching = nx.max_weight_matching(
        G, maxcardinality=True, weight='weight'
    )
    return [(u, v) for u, v in matching]

def build_multigraph(mst_edges, matching_edges, n):
    # Lista de todas as arestas do multigrafo
    all_edges = []

    # Adiciona arestas da MST (1 cópia de cada)
    for edge in mst_edges:
        u, v, _ = edge
        all_edges.append((min(u, v), max(u, v)))

    # Adiciona arestas do emparelhamento (1 cópia de cada)
    for u, v in matching_edges:
        all_edges.append((min(u, v), max(u, v)))

    return all_edges

def find_eulerian_tour(edges, n):
    # Construir lista de adjacência com contagem de arestas
    graph = defaultdict(list)
    edge_count = defaultdict(int)

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        edge_count[(min(u, v), max(u, v))] += 1

    # Encontrar vértice de partida (qualquer vértice com arestas)
    start = next(iter(graph.keys()), None)
    for node in graph:
        if graph[node]:
            start = node
            break

    # Algoritmo de Hierholzer com contagem de arestas
    stack = [start]
    tour = []

    while stack:
        u = stack[-1]

        if graph[u]:
            v = graph[u].pop()

            # Verifica se a aresta ainda existe
            edge_key = (min(u, v), max(u, v))
            if edge_count[edge_key] > 0:
                # Remove a aresta do grafo
                edge_count[edge_key] -= 1
                # Remove a ocorrência inversa
                graph[v].remove(u)
                stack.append(v)
            else:
                # Aresta já foi removida, tenta próximo vizinho
                continue
        else:
            tour.append(stack.pop())

    return tour[::-1]

def shortcut_eulerian_vertices(euler_tour):
    if not euler_tour:
        return []

    visited = set()
    tour = []
    for v in euler_tour:
        if v not in visited:
            visited.add(v)
            tour.append(v)

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

    # Etapa 1: Árvore Geradora Mínima
    mst_edges, mst_weight = prim_mst(g, n)

    # Etapa 2: Encontrar vértices de grau ímpar
    odd_vertices = find_odd_vertices(mst_edges, n)

    # Etapa 3: Emparelhamento Perfeito Mínimo
    matching_edges = min_weight_perfect_matching(g, odd_vertices)

    # Etapa 4: Construir multigrafo
    multigraph_edges = build_multigraph(mst_edges, matching_edges, n)

    # Etapa 5: Encontrar circuito euleriano
    euler_tour = find_eulerian_tour(multigraph_edges, n)

    # Etapa 6: Atalho para ciclo hamiltoniano
    hamiltonian_tour = shortcut_eulerian_vertices(euler_tour)

    # Etapa 7: Calcular custo do ciclo
    tour_cost = calculate_tour_cost(hamiltonian_tour, g)

    return mst_edges, mst_weight, hamiltonian_tour, tour_cost

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python christofides.py <graph.txt>")
        sys.exit(1)

    try:
        graph, n = read_graph(sys.argv[1])
        mst_edges, mst_weight, tour, total = christofides(graph, n)

        # Formatação da saída conforme especificado
        print("Árvore Geradora Mínima:")
        print(mst_edges)
        print(f"Peso da árvore geradora mínima: {mst_weight}")

        print("\nSolução Aproximada Encontrada por Christofides:")
        print(tour)
        print(f"Peso da Solução: {total}")


    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
