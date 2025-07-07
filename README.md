# 🛣️ Algoritmo de Christofides para TSP:
Este projeto implementa o Algoritmo de Christofides para resolver o Problema do Caixeiro Viajante (TSP) em grafos métricos, garantindo uma aproximação de até 3/2 (150%) do ótimo, utilizando Python e bibliotecas de grafos.

## 📁 Estrutura:
christofides.py: Implementação completa do algoritmo.

main.py: Script para executar o algoritmo com exemplos.

utils.py: Funções de leitura de grafos e visualização.

graphs/: Exemplos de grafos de entrada.

outputs/: Resultados e visualizações geradas.

## 🧪 Tecnologias Utilizadas:

Python

NetworkX

Matplotlib

Jupyter Notebook (opcional para análises)

## 🚀 Como executar
Clone este repositório:

bash
Copiar
Editar
git clone https://github.com/seuusuario/Christofides-Algorithm.git
Navegue até a pasta:

bash
Copiar
Editar
cd Christofides-Algorithm
Instale as dependências:

bash
Copiar
Editar
pip install networkx matplotlib
Execute o algoritmo em um grafo de exemplo:

bash
Copiar
Editar
python main.py --input graphs/exemplo.txt --debug true
Ou abra um notebook para visualização passo a passo:

bash
Copiar
Editar
jupyter notebook

### 📊 Objetivo
O principal objetivo deste projeto é demonstrar na prática como o Algoritmo de Christofides constrói soluções aproximadas para o TSP, detalhando cada etapa do processo:

✅ Construção da MST
✅ Identificação de vértices de grau ímpar
✅ Matching de peso mínimo
✅ Formação do circuito de Euler
✅ Conversão em circuito Hamiltoniano

### 📌 Resultados
Cálculo do custo total do percurso aproximado.

Visualização das etapas do algoritmo.

Análise do tempo de execução e escalabilidade.

Comparação com outros métodos aproximados ou exatos (em etapas futuras).

### ✨ Contribuições
Sinta-se à vontade para abrir issues ou pull requests com sugestões, correções de bugs ou melhorias no algoritmo! 👩‍💻👨‍💻

### 📄 Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.
