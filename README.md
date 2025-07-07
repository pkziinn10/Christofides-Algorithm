hristofides Algorithm 🚀
Implementação em Python para resolver o Problema do Caixeiro Viajante (TSP) utilizando o Algoritmo de Christofides.

🧠 Visão Geral
O algoritmo executa os seguintes passos:

Construir uma Árvore Geradora Mínima (MST).

Encontrar os vértices de grau ímpar na MST.

Gerar um emparelhamento perfeito de peso mínimo entre os vértices ímpares.

Combinar MST + matching, formando um grafo Euleriano.

Encontrar um circuito de Euler.

Converter em circuito Hamiltoniano (removendo repetições).

⚙️ Pré-requisitos
Python 3.7+

networkx

matplotlib (opcional, para visualização)

Instalação:

bash
Copiar
Editar
pip install networkx matplotlib

🛠️ Como Executar
bash
Copiar
Editar
git clone https://github.com/seuusuario/Christofides-Algorithm.git
cd Christofides-Algorithm
python main.py --input caminho/para/grafo.txt --debug true
Parâmetros:

--input: caminho do arquivo de entrada (grafo)

--debug: true para visualizar passos intermediários

📂 Estrutura do Projeto
bash
Copiar
Editar
.
├── main.py             # Script principal
├── christofides.py     # Algoritmo de Christofides
├── utils.py            # Funções utilitárias
├── graphs/             # Exemplos de grafos
└── outputs/            # Saídas e gráficos gerados

📊 Exemplo de Uso
bash
Copiar
Editar
python main.py --input graphs/exemplo.txt --debug true
Gera:

MST construída

Vértices ímpares e matching mínimo

Circuito Euleriano e solução final

Visualizações opcionais

📝 Contribuição
Contribuições são bem-vindas:

Melhorias de performance

Suporte a novos formatos de entrada

Visualizações interativas

Testes automatizados

Abra uma issue ou envie um pull request.

📄 Licença
Distribuído sob a MIT License.
