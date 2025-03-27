import threading
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import time

# Função para gerar fractais usando um Sistema de Funções Iteradas (IFS)
def gerar_fractal(transformacoes, probabilidades, iteracoes=100000):
    if not abs(sum(probabilidades) - 1.0) < 1e-6:
        raise ValueError("As probabilidades devem somar 1.")
    x, y = 0.0, 0.0
    pontos = []
    for _ in range(iteracoes):
        r = random.random()
        acumulado = 0.0
        for i, prob in enumerate(probabilidades):
            acumulado += prob
            if r < acumulado:
                transformacao = transformacoes[i]
                break
        x, y = transformacao(x, y)
        pontos.append((x, y))
    return pontos

# Funções para cada fractal, como o Triângulo de Sierpinski, etc.

# Triângulo de Sierpinski
def sierpinski():
    transformacoes = [
        lambda x, y: (0.5 * x, 0.5 * y),
        lambda x, y: (0.5 * x + 0.5, 0.5 * y),
        lambda x, y: (0.5 * x + 0.25, 0.5 * y + 0.5)
    ]
    probabilidades = [1/3, 1/3, 1/3]
    pontos = gerar_fractal(transformacoes, probabilidades, iteracoes=100000)
    return pontos, "sierpinski", 'black'

# Samambaia de Barnsley
def samambaia_barnsley():
    transformacoes = [
        lambda x, y: (0.0, 0.16 * y),
        lambda x, y: (0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6),
        lambda x, y: (0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6),
        lambda x, y: (-0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44)
    ]
    probabilidades = [0.01, 0.85, 0.07, 0.07]
    pontos = gerar_fractal(transformacoes, probabilidades, iteracoes=100000)
    return pontos, "samambaia_barnsley", 'green'

# Conjunto de Mandelbrot
def mandelbrot(width=800, height=800, max_iter=100):
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    image = np.zeros((height, width))
    for row in range(height):
        for col in range(width):
            c = complex(x_min + (x_max - x_min) * col / width,
                        y_min + (y_max - y_min) * row / height)
            z = 0.0j
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z * z + c
                n += 1
            image[row, col] = n
    return image, "mandelbrot", 'hot'

# Conjunto de Julia
def julia(c=-0.7 + 0.27015j, width=800, height=800, max_iter=100):
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    image = np.zeros((height, width))
    for row in range(height):
        for col in range(width):
            z = complex(x_min + (x_max - x_min) * col / width,
                        y_min + (y_max - y_min) * row / height)
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z * z + c
                n += 1
            image[row, col] = n
    return image, "julia", 'twilight_shifted'

# Função para salvar as imagens
def salvar_imagem(pontos, titulo, cmap):
    plt.figure()
    if isinstance(pontos, np.ndarray):  # Caso dos conjuntos de Mandelbrot ou Julia
        plt.imshow(pontos, cmap=cmap, interpolation='bilinear')
    else:  # Para os fractais baseados em IFS
        x_vals, y_vals = zip(*pontos)
        plt.scatter(x_vals, y_vals, s=0.1, color=cmap, marker='.')
    plt.title(titulo)
    plt.axis('off')
    plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", f"{titulo}.png"), bbox_inches='tight', dpi=300)
    plt.close()

# Função principal que cria as threads para gerar todos os fractais
def gerar_todos_fractais():
    threads = []
    resultados = []
    
    # Função para armazenar os resultados das threads
    def tarefa(fractal):
        resultados.append(fractal())

    # Criação das threads para gerar os fractais simultaneamente
    for fractal in [sierpinski, samambaia_barnsley, mandelbrot, julia]:
        thread = threading.Thread(target=tarefa, args=(fractal,))
        threads.append(thread)
        thread.start()

    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()

    # Após todas as threads terem terminado, criar as imagens
    for pontos, titulo, cmap in resultados:
        salvar_imagem(pontos, titulo, cmap)

    print("Todos os fractais foram gerados e salvos.")

# Função para medir o tempo de execução com e sem threads
def medir_tempo():
    print("\nMedindo tempo com threads:")
    start_time = time.time()
    gerar_todos_fractais()
    print(f"Tempo com threads: {time.time() - start_time:.2f} segundos")

    print("\nMedindo tempo sem threads:")
    start_time = time.time()
    # Gerando sem threads (executando sequencialmente)
    for fractal in [sierpinski, samambaia_barnsley, mandelbrot, julia]:
        pontos, titulo, cmap = fractal()
        salvar_imagem(pontos, titulo, cmap)
    print(f"Tempo sem threads: {time.time() - start_time:.2f} segundos")

# Executa a função principal
if __name__ == "__main__":
    medir_tempo()
