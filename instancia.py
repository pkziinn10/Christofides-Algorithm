import math
import sys

def parse_tsplib(filename):
    coords = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    reading_coords = False
    for line in lines:
        line = line.strip()
        if line == "NODE_COORD_SECTION":
            reading_coords = True
            continue
        if line == "EOF":
            break
        if reading_coords:
            parts = line.split()
            if len(parts) == 3:
                _, x, y = parts
                coords.append((float(x), float(y)))
    return coords

def euclidean(p1, p2):
    return round(math.hypot(p1[0] - p2[0], p1[1] - p2[1]), 1)

def gerar_matriz(coords):
    n = len(coords)
    matriz = []
    for i in range(n):
        linha = []
        for j in range(n):
            linha.append(euclidean(coords[i], coords[j]))
        matriz.append(linha)
    return matriz

def salvar_matriz_formatada(matriz, nome_saida):
    with open(nome_saida, 'w') as f:
        for linha in matriz:
            linha_formatada = "[" + ", ".join(f"{num:.1f}" for num in linha) + "]"
            f.write(linha_formatada + "\n")

# Execução
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 instancia.py instancia.txt")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = "matriz_formatada.txt"

    coords = parse_tsplib(entrada)
    matriz = gerar_matriz(coords)
    salvar_matriz_formatada(matriz, saida)
    print(f"Matriz salva em: {saida}")
