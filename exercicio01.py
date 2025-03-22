import random
import threading
import time

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]
    
    left_sorted = []
    right_sorted = []
    
    # Criando ara ordenar as sublistas
    left_thread = threading.Thread(target=lambda: left_sorted.extend(quicksort(left)))
    right_thread = threading.Thread(target=lambda: right_sorted.extend(quicksort(right)))
    
    left_thread.start()
    right_thread.start()
    
    left_thread.join()
    right_thread.join()
    
    return left_sorted + [pivot] + right_sorted

def gerar_numeros_aleatorios(n=100, min_val=1, max_val=200):
    return [random.randint(min_val, max_val) for _ in range(n)]

def main():
    tamanhos = [100, 1000, 5000, 10000]  # Teste com diferentes tamanhos de lista
    for tamanho in tamanhos:
        numeros = gerar_numeros_aleatorios(tamanho)
        print(f"\nTamanho da lista: {tamanho}")
        print("Primeiros 10 números antes da ordenação:", numeros[:10])
        
        # Medindo tempo sem threads
        inicio_seq = time.time()
        numeros_ordenados_seq = sorted(numeros)
        fim_seq = time.time()
        print("Tempo de execução (sem threads):", fim_seq - inicio_seq)
        
        # Medindo tempo com threads
        inicio_thread = time.time()
        numeros_ordenados_thread = quicksort(numeros)
        fim_thread = time.time()
        print("Tempo de execução (com threads):", fim_thread - inicio_thread)
        
        print("Primeiros 10 números após a ordenação:", numeros_ordenados_thread[:10])

if __name__ == "__main__":
    main()