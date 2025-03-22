import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading
import time

def buscar_palavra_no_site(url_inicial, palavra, profundidade_maxima=3):
    urls_visitados = set()
    resultados = {}
    lock = threading.Lock()
    threads = []
    
    def buscar_recursivo(url_atual, profundidade_atual):
        if profundidade_atual > profundidade_maxima:
            return
        
        with lock:
            if url_atual in urls_visitados:
                return
            urls_visitados.add(url_atual)
        
        try:
            print(f"Buscando em: {url_atual} (Profundidade: {profundidade_atual})")
            response = requests.get(url_atual, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            conteudo = soup.get_text().lower()
            palavra_encontrada = palavra.lower() in conteudo
            
            with lock:
                resultados[url_atual] = palavra_encontrada
            
            links = soup.find_all('a', href=True)
            for link in links:
                url_completa = urljoin(url_inicial, link['href'])
                if url_completa.startswith(url_inicial):
                    thread = threading.Thread(target=buscar_recursivo, args=(url_completa, profundidade_atual + 1))
                    threads.append(thread)
                    thread.start()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {url_atual}: {e}")
    
    inicio = time.time()
    buscar_recursivo(url_inicial, profundidade_atual=1)
    
    for thread in threads:
        thread.join()
    
    fim = time.time()
    print(f"Tempo de execução: {fim - inicio:.2f} segundos")
    
    return resultados

if __name__ == "__main__":
    url_inicial = input("Digite a URL inicial do site (ex.: https://www.exemplo.com): ")
    palavra = input("Digite a palavra a ser buscada: ")
    
    resultados = buscar_palavra_no_site(url_inicial, palavra)
    print("\nResultados da busca:")
    for url, encontrada in resultados.items():
        status = "Encontrada" if encontrada else "Não encontrada"
        print(f"{url}: Palavra '{palavra}' {status}")
