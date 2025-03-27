from PIL import Image
from tkinter import Tk, filedialog
import threading

# Função para calcular a luminância e converter um pixel em tons de cinza
def luminance(r, g, b):
    return int(0.299 * r + 0.587 * g + 0.114 * b)

# Função que processa uma faixa horizontal de pixels
def process_row(start_row, end_row, imagem, imagem_preto_branco, lock):
    largura, altura = imagem.size
    for y in range(start_row, end_row):
        for x in range(largura):
            r, g, b = imagem.getpixel((x, y))
            luminancia_valor = luminance(r, g, b)
            with lock:  # Acesso exclusivo para modificar a imagem
                imagem_preto_branco.putpixel((x, y), luminancia_valor)

# Função principal para converter a imagem em preto e branco com threads
def converter_para_preto_e_branco_manual():
    try:
        root = Tk()
        root.withdraw()
        caminho_imagem = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.gif"), ("Todos os arquivos", "*.*")]
        )
        if not caminho_imagem:
            print("Nenhuma imagem foi selecionada.")
            return
        
        imagem = Image.open(caminho_imagem)
        imagem = imagem.convert("RGB")  # Garante que a imagem esteja no modo RGB
        largura, altura = imagem.size
        imagem_preto_branco = Image.new("L", (largura, altura))
        
        # Dividir a imagem em faixas horizontais e atribuir para threads
        num_threads = 4  # Número de threads a ser usado
        threads = []
        lock = threading.Lock()  # Garantir acesso exclusivo ao imagem_preto_branco
        rows_per_thread = altura // num_threads
        
        # Criar e iniciar as threads
        for i in range(num_threads):
            start_row = i * rows_per_thread
            end_row = (i + 1) * rows_per_thread if i < num_threads - 1 else altura
            thread = threading.Thread(target=process_row, args=(start_row, end_row, imagem, imagem_preto_branco, lock))
            threads.append(thread)
            thread.start()

        # Aguardar todas as threads terminarem
        for thread in threads:
            thread.join()

        # Solicitar o caminho para salvar a imagem
        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar imagem em preto e branco",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("Todos os arquivos", "*.*")]
        )
        if not caminho_saida:
            print("Operação de salvamento cancelada.")
            return

        # Salvar a imagem em preto e branco no caminho especificado
        imagem_preto_branco.save(caminho_saida)
        print(f"Imagem convertida com sucesso! Salva em: {caminho_saida}")

    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")

# Exemplo de uso
if __name__ == "__main__":
    converter_para_preto_e_branco_manual()