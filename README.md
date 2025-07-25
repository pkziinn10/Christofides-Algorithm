# 📦 Algoritmo de Christofides para o Problema do Caixeiro Viajante (TSP)

Este projeto implementa uma solução aproximada para o Problema do Caixeiro Viajante (TSP) utilizando o **Algoritmo de Christofides**, que garante um limite superior de 1.5 vezes o ótimo para grafos completos com pesos que satisfazem a desigualdade do triângulo.

## 📁 Arquivos

- `christofides.py`: Implementa o algoritmo de Christofides, incluindo a leitura do grafo, cálculo da árvore geradora mínima, emparelhamento perfeito de vértices ímpares, construção do multigrafo, obtenção do circuito euleriano e aplicação de atalhos para gerar o ciclo hamiltoniano.
- `instancia.py`: Lê uma instância no formato **TSPLIB** e gera a matriz de distâncias euclidianas entre os pontos, salvando o resultado no formato esperado por `christofides.py`.

## ▶️ Como Usar

### 1. Gerar a Matriz de Adjacência

Utilize `instancia.py` para transformar uma instância TSPLIB (`.txt`) em uma matriz de distâncias:

```bash
python instancia.py instancia.txt
```

- Isso criará um arquivo `matriz_formatada.txt` com a matriz de adjacência no formato exigido pelo algoritmo.

### 2. Executar o Algoritmo de Christofides

Utilize `christofides.py` para calcular a solução aproximada do TSP:

```bash
python christofides.py matriz_formatada.txt
```

### 📝 Formato de Entrada Esperado (para `christofides.py`)

```
n
[linha 1 com n valores separados por vírgula]
[linha 2 com n valores]
...
[linha n com n valores]
```

Exemplo:

```
4
[0.0, 2.0, 9.0, 10.0]
[2.0, 0.0, 6.0, 4.0]
[9.0, 6.0, 0.0, 8.0]
[10.0, 4.0, 8.0, 0.0]
```

## 🧠 Etapas do Algoritmo de Christofides

1. Construção da **Árvore Geradora Mínima** com Prim.
2. Identificação dos vértices de **grau ímpar**.
3. Cálculo do **Emparelhamento Perfeito de Menor Peso** entre esses vértices.
4. Combinação das arestas da MST com o emparelhamento para formar um **multigrafo euleriano**.
5. Geração de um **circuito euleriano**.
6. Aplicação de **atalhos** para gerar um ciclo **hamiltoniano**.
7. Cálculo do **custo total** do tour.

## 📊 Saída

O programa imprime:

- A árvore geradora mínima e seu peso.
- A solução aproximada encontrada (ciclo hamiltoniano).
- O custo total da solução.
- Os tempos de execução para cada etapa.

## 🛠️ Requisitos

- Python 3
- Bibliotecas:
  - `networkx`
  - `math`
  - `heapq`

Instale com:

```bash
pip install networkx
```

## 👤 Autoria

Este projeto foi desenvolvido como parte de um trabalho acadêmico para estudo do **Problema do Caixeiro Viajante** e uso de algoritmos de aproximação em grafos.
