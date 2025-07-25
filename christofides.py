import sys
import heapq
import networkx as nx
from collections import defaultdict
import time

# Função para ler um grafo a partir de um arquivo.
# Arquivo deve ter um padrão de: 
# Na primeira linha: O número de vertices (n)
# Nas n linhas seguintes: A matriz de adjacência n×n com os pesos das arestas
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

    for i in range(n):
        for j in range(i + 1, n):
            if abs(g[i][j] - g[j][i]) > 1e-6:
                raise ValueError(f"A matriz não é simétrica: g[{i}][{j}]={g[i][j]} != g[{j}][{i}]={g[j][i]}")

    return g, n

# Algoritmo de Prim para encontrar a Árvore Geradora Mínima (MST)
def prim_mst(g, n):
    if n == 0:
        return [], 0.0

    in_mst = [False] * n
    parent = [-1] * n
    key = [float('inf')] * n
    key[0] = 0
    heap = [(0, 0)]

    mst_edges = []
    total_weight = 0.0

    # Processa enquanto houver vértices no heap
    while heap:
        weight, u = heapq.heappop(heap)

        # Ignora se já estiver na MST
        if in_mst[u]:
            continue

        in_mst[u] = True
        total_weight += weight

        # Adiciona aresta à MST (exceto para o vértice raiz)
        if parent[u] != -1:
            mst_edges.append((parent[u], u, {'weight': weight}))

        for v in range(n):
            if u == v or in_mst[v]:
                continue

            if g[u][v] < key[v]:
                parent[v] = u
                key[v] = g[u][v]
                heapq.heappush(heap, (g[u][v], v))

    return mst_edges, total_weight

# Encontra vértices com grau ímpar na MST
def find_odd_vertices(mst_edges, n):
    deg = [0] * n  # Inicializa graus dos vértices

    # Contagem dos graus
    for edge in mst_edges:
        u = edge[0]
        v = edge[1]
        deg[u] += 1
        deg[v] += 1

    # Filtra os vertices de grau impar
    odd = [i for i, d in enumerate(deg) if d % 2 == 1]

    if len(odd) % 2 != 0:
        raise RuntimeError("Número ímpar de vértices de grau ímpar detectado")

    return odd

# Encontra o emparelhamento perfeito mínimo entre vértices ímpares
def min_weight_perfect_matching(g, odd_vertices):
    if len(odd_vertices) == 0:
        return []

    # Cria um grafo completo com os vértices ímpares
    G = nx.Graph()
    for i in range(len(odd_vertices)):
        for j in range(i + 1, len(odd_vertices)):
            u = odd_vertices[i]
            v = odd_vertices[j]
            # Usa peso negativo para obter o mínimo emparelhamento
            G.add_edge(u, v, weight=-g[u][v])

    # Executa o algoritmo de emparelhamento máximo (com pesos negativos)
    matching = nx.max_weight_matching(
        G, maxcardinality=True, weight='weight'
    )

    return [(u, v) for u, v in matching]

# Constrói um multigrafo combinando MST e arestas do emparelhamento
def build_multigraph(mst_edges, matching_edges, n):
    all_edges = []

    # Adiciona as arestas da MST de forma ordenada
    for edge in mst_edges:
        u, v, _ = edge
        all_edges.append((min(u, v), max(u, v)))

    # Adiciona as arestas do emparelhamento perfeito de forma ordenada
    for u, v in matching_edges:
        all_edges.append((min(u, v), max(u, v)))

    return all_edges

# Encontra um circuito euleriano no multigrafo nao-direcionado usando Hierholzer 
def find_eulerian_tour(edges, n):

    graph = defaultdict(list)
    edge_count = defaultdict(int)

    # Constrói a representação do grafo
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        # Usa tupla ordenada para identificar a aresta
        edge_count[(min(u, v), max(u, v))] += 1

    # Encontra um vértice inicial não isolado
    start = next(iter(graph.keys()), None)
    for node in graph:
        if graph[node]:
            start = node
            break

    # Algoritmo de Hierholzer para circuito euleriano
    # Pilha mantem o caminho atual sendo explorado
    stack = [start]
    tour = []

    while stack:
        u = stack[-1]  
        
        # Se tiver arestas saindo de u
        if graph[u]:
            # Pega uma aresta qualquer
            v = graph[u].pop()

            edge_key = (min(u, v), max(u, v))
            
            if edge_count[edge_key] > 0: # Se aresta existir
                # Marca a aresta 
                edge_count[edge_key] -= 1
                # Remove uma aresta paralela
                graph[v].remove(u)

                stack.append(v)
            else:
                continue
        else:
            tour.append(stack.pop())

    # Inverte para obter a ordem correta
    return tour[::-1]

# Converte o circuito euleriano em ciclo hamiltoniano por atalhos
def shortcut_eulerian_vertices(euler_tour):
    if not euler_tour:
        return []

    visited = set()  
    tour = []

    # Percorre o circuito euleriano, removendo vértices repetidos
    for v in euler_tour:
        if v not in visited:
            visited.add(v)
            tour.append(v)

    # Fecha o ciclo retornando ao início
    tour.append(tour[0])
    return tour

# Calcula o custo total de um ciclo
def calculate_tour_cost(tour, g):
    if len(tour) < 2:
        return 0.0

    cost = 0.0

    for i in range(len(tour) - 1):
        u = tour[i]
        v = tour[i + 1]
        cost += g[u][v]
    return cost

# Algoritmo de Christofides para TSP
def christofides(g, n):
    if n <= 1:
        return [], 0.0, [], 0.0

    tempos = {}

    inicio = time.time()
    mst_edges, mst_weight = prim_mst(g, n)
    tempos['MST'] = time.time() - inicio

    inicio = time.time()
    odd_vertices = find_odd_vertices(mst_edges, n)
    tempos['Vértices Ímpares'] = time.time() - inicio

    inicio = time.time()
    matching_edges = min_weight_perfect_matching(g, odd_vertices)
    tempos['Emparelhamento'] = time.time() - inicio

    inicio = time.time()
    multigraph_edges = build_multigraph(mst_edges, matching_edges, n)
    tempos['Multigrafo'] = time.time() - inicio

    inicio = time.time()
    euler_tour = find_eulerian_tour(multigraph_edges, n)
    tempos['Circuito Euleriano'] = time.time() - inicio

    inicio = time.time()
    hamiltonian_tour = shortcut_eulerian_vertices(euler_tour)
    tempos['Atalhos'] = time.time() - inicio

    inicio = time.time()
    tour_cost = calculate_tour_cost(hamiltonian_tour, g)
    tempos['Cálculo Custo'] = time.time() - inicio

    return mst_edges, mst_weight, hamiltonian_tour, tour_cost, tempos

# Ponto de entrada do programa
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python christofides.py <graph.txt>")
        sys.exit(1)

    try:
        inicio_total = time.time()

        inicio_leitura = time.time()
        graph, n = read_graph(sys.argv[1])
        tempo_leitura = time.time() - inicio_leitura

        inicio_algoritmo = time.time()
        mst_edges, mst_weight, tour, total, tempos_etapas = christofides(graph, n)
        tempo_algoritmo = time.time() - inicio_algoritmo

        tempo_total = time.time() - inicio_total

        # Saída formatada
        print("Árvore Geradora Mínima:")
        print(mst_edges)
        print(f"Peso da árvore geradora mínima: {mst_weight}")

        print("\nSolução Aproximada Encontrada por Christofides:")
        print(tour)
        print(f"Peso da Solução: {total}")


        # Relatório de tempos
        print("\nTempos de Execução:")
        print(f"- Leitura do arquivo: {tempo_leitura:.6f} segundos")
        for etapa, t in tempos_etapas.items():
            print(f"- {etapa}: {t:.6f} segundos")
        print(f"- Algoritmo Christofides: {tempo_algoritmo:.6f} segundos")
        print(f"- Tempo total (com leitura): {tempo_total:.6f} segundos")

    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
