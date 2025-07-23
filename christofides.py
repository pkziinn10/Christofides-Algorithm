import sys
import heapq
import networkx as nx
from collections import defaultdict
import time

# Função para ler um grafo a partir de um arquivo
def read_graph(path):
    # Abre o arquivo no caminho especificado
    with open(path) as f:
        # Lê todas as linhas não vazias, removendo espaços extras
        lines = [line.strip() for line in f if line.strip()]

    # Verifica se o arquivo está vazio
    if not lines:
        raise ValueError("Arquivo vazio")

    try:
        # Lê o número de vértices na primeira linha
        n = int(lines[0])
    except ValueError:
        raise ValueError("Primeira linha deve ser um inteiro (número de vértices)")

    # Valida se o número de vértices é positivo
    if n <= 0:
        raise ValueError("Número de vértices deve ser positivo")

    # Verifica se há linhas suficientes para a matriz
    if len(lines) < n + 1:
        raise ValueError(f"Esperadas {n+1} linhas, mas encontradas {len(lines)}")

    # Inicializa a matriz de adjacência
    g = []
    # Processa cada linha da matriz
    for i in range(1, n + 1):
        # Remove colchetes e espaços extras
        cleaned_line = lines[i].replace('[', '').replace(']', '').strip()
        # Divide os elementos por vírgula, ignorando vazios
        parts = [x.strip() for x in cleaned_line.split(',') if x.strip()]

        # Valida o número de colunas
        if len(parts) != n:
            raise ValueError(f"Linha {i+1}: esperados {n} valores, encontrados {len(parts)}")

        # Converte cada valor para float e verifica se é não-negativo
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

    # Valida a simetria da matriz (grafo não direcionado)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(g[i][j] - g[j][i]) > 1e-6:
                raise ValueError(f"A matriz não é simétrica: g[{i}][{j}]={g[i][j]} != g[{j}][{i}]={g[j][i]}")

    return g, n

# Algoritmo de Prim para encontrar a Árvore Geradora Mínima (MST)
def prim_mst(g, n):
    # Caso especial: grafo vazio
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
    # Conta as ocorrências de cada vértice nas arestas
    for edge in mst_edges:
        u = edge[0]
        v = edge[1]
        deg[u] += 1
        deg[v] += 1
    # Filtra vértices com grau ímpar
    odd = [i for i, d in enumerate(deg) if d % 2 == 1]

    # Verifica consistência (deve ser número par)
    if len(odd) % 2 != 0:
        raise RuntimeError("Número ímpar de vértices de grau ímpar detectado")

    return odd

# Encontra o emparelhamento perfeito mínimo entre vértices ímpares
def min_weight_perfect_matching(g, odd_vertices):
    # Caso sem vértices ímpares
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
    # Converte o resultado para lista de arestas
    return [(u, v) for u, v in matching]

# Constrói um multigrafo combinando MST e arestas do emparelhamento
def build_multigraph(mst_edges, matching_edges, n):
    all_edges = []

    # Adiciona todas as arestas da MST (1 cópia)
    for edge in mst_edges:
        u, v, _ = edge
        all_edges.append((min(u, v), max(u, v)))

    # Adiciona todas as arestas do emparelhamento (1 cópia)
    for u, v in matching_edges:
        all_edges.append((min(u, v), max(u, v)))

    return all_edges

# Encontra um circuito euleriano no multigrafo
def find_eulerian_tour(edges, n):
    # Cria lista de adjacência e contador de arestas
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
    stack = [start]
    tour = []  # Armazenará o tour final

    while stack:
        u = stack[-1]  # Pega o topo da pilha

        # Se ainda há arestas saindo de u
        if graph[u]:
            v = graph[u].pop()  # Pega um vizinho

            # Verifica se a aresta (u,v) ainda existe
            edge_key = (min(u, v), max(u, v))
            if edge_count[edge_key] > 0:
                # Remove uma ocorrência da aresta
                edge_count[edge_key] -= 1
                # Remove a aresta inversa da lista de adjacência
                graph[v].remove(u)
                # Empilha o próximo vértice
                stack.append(v)
            else:
                # Aresta já foi usada, tenta próximo vizinho
                continue
        else:
            # Adiciona vértice ao tour quando não tem mais arestas
            tour.append(stack.pop())

    # Inverte para obter a ordem correta
    return tour[::-1]

# Converte o circuito euleriano em ciclo hamiltoniano por atalhos
def shortcut_eulerian_vertices(euler_tour):
    if not euler_tour:
        return []

    visited = set()  # Controla vértices já visitados
    tour = []        # Tour resultante sem repetições

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
    # Soma os pesos entre vértices consecutivos
    for i in range(len(tour) - 1):
        u = tour[i]
        v = tour[i + 1]
        cost += g[u][v]
    return cost

# Algoritmo de Christofides para TSP
def christofides(g, n):
    # Casos especiais para grafos pequenos
    if n <= 1:
        return [], 0.0, [], 0.0

    tempos = {}

    # Etapa 1: Calcula a MST
    inicio = time.time()
    mst_edges, mst_weight = prim_mst(g, n)
    tempos['MST'] = time.time() - inicio

    # Etapa 2: Identifica vértices de grau ímpar na MST
    inicio = time.time()
    odd_vertices = find_odd_vertices(mst_edges, n)
    tempos['Vértices Ímpares'] = time.time() - inicio

    # Etapa 3: Encontra emparelhamento perfeito mínimo
    inicio = time.time()
    matching_edges = min_weight_perfect_matching(g, odd_vertices)
    tempos['Emparelhamento'] = time.time() - inicio


    # Etapa 4: Combina MST e emparelhamento num multigrafo
    inicio = time.time()
    multigraph_edges = build_multigraph(mst_edges, matching_edges, n)
    tempos['Multigrafo'] = time.time() - inicio

    # Etapa 5: Encontra circuito euleriano no multigrafo
    inicio = time.time()
    euler_tour = find_eulerian_tour(multigraph_edges, n)
    tempos['Circuito Euleriano'] = time.time() - inicio

    # Etapa 6: Remove vértices repetidos (atalho)
    inicio = time.time()
    hamiltonian_tour = shortcut_eulerian_vertices(euler_tour)
    tempos['Atalhos'] = time.time() - inicio

    # Etapa 7: Calcula o custo do ciclo
    inicio = time.time()
    tour_cost = calculate_tour_cost(hamiltonian_tour, g)
    tempos['Cálculo Custo'] = time.time() - inicio

    return mst_edges, mst_weight, hamiltonian_tour, tour_cost, tempos

# Ponto de entrada do programa
if __name__ == "__main__":
    # Verifica argumentos da linha de comando
    if len(sys.argv) != 2:
        print("Uso: python christofides.py <graph.txt>")
        sys.exit(1)

    try:
        # Medição do tempo total (inclui leitura do arquivo)
        inicio_total = time.time()

        # Leitura do grafo
        inicio_leitura = time.time()
        graph, n = read_graph(sys.argv[1])
        tempo_leitura = time.time() - inicio_leitura

        # Execução do algoritmo
        inicio_algoritmo = time.time()
        mst_edges, mst_weight, tour, total, tempos_etapas = christofides(graph, n)
        tempo_algoritmo = time.time() - inicio_algoritmo

        # Tempo total da execução
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
