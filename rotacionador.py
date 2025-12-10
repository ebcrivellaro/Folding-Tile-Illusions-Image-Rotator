# Esse é o código do Rotacionador.py, ao ser executado, ele processa as imagens das obras e gera os novos arquivos na pasta 'saida'

import os
import cv2
import numpy as np
from pathlib import Path

def determinar_rotacao(cols, linhas, i, j, cell_num):
    """Determina a direção de rotação com base no padrão especificado"""
    if cols == 4 and linhas == 4:
        # Padrão específico para 4x4
        padrao = [
            ['h', 'ah', 'h', 'ah'],
            ['ah', 'h', 'ah', 'h'],
            ['h', 'ah', 'h', 'ah'],
            ['ah', 'h', 'ah', 'h']
        ]
        return padrao[j][i]
    else:
        # Padrão original para outras grades
        if cell_num % 2 != 0:
            return 'ah'
        else:
            return 'h'

def processar_imagem(caminho_entrada, caminho_saida, cols, linhas):
    """Processa imagens de uma pasta com grade específica"""
    Path(caminho_saida).mkdir(parents=True, exist_ok=True)
    
    # Processar cada imagem na pasta de entrada
    for arquivo in os.listdir(caminho_entrada):
        if arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Carregar imagem
            img_path = os.path.join(caminho_entrada, arquivo)
            img = cv2.imread(img_path)
            
            if img is None:
                print(f"Erro ao carregar {arquivo}, pulando...")
                continue
            
            # Criar imagem de saída com o mesmo tamanho da original
            altura, largura = img.shape[:2]
            img_saida = np.zeros_like(img)
            
            # Calcular dimensões das células
            cell_largura = largura // cols
            cell_altura = altura // linhas
            
            for i in range(cols):
                for j in range(linhas):
                    # Calcular coordenadas da célula
                    x1 = i * cell_largura
                    x2 = (i + 1) * cell_largura
                    y1 = j * cell_altura
                    y2 = (j + 1) * cell_altura
                    
                    # Extrair região da célula
                    cell = img[y1:y2, x1:x2]
                    
                    # Calcular número da célula (1-N)
                    cell_num = i + j * cols + 1
                    
                    # Determinar direção de rotação
                    rotacao = determinar_rotacao(cols, linhas, i, j, cell_num)
                    
                    # Aplicar rotação conforme especificado
                    if rotacao == 'h':
                        cell = cv2.rotate(cell, cv2.ROTATE_90_CLOCKWISE)
                    else:
                        cell = cv2.rotate(cell, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    
                    # Colocar célula rotacionada de volta na imagem
                    img_saida[y1:y1+cell.shape[0], x1:x1+cell.shape[1]] = cell
            
            # Salvar imagem processada
            nome_base = os.path.splitext(arquivo)[0]
            caminho_saida_arquivo = os.path.join(
                caminho_saida, 
                f"{nome_base}_rot_{cols}x{linhas}.png"
            )
            cv2.imwrite(caminho_saida_arquivo, img_saida)
            print(f"Imagem processada salva em: {caminho_saida_arquivo}")

def processar_todas_pastas():
    """Processa todas as pastas de entrada com suas respectivas grades"""
    # Configurar pastas de entrada e saída
    pastas_entrada = {
        "entrada3x4": (3, 4),
        "entrada4x3": (4, 3),
        "entrada3x3": (3, 3),
        "entrada4x4": (4, 4)
    }
    saida_dir = "saida"
    
    # Processar cada pasta de entrada
    for pasta, (cols, linhas) in pastas_entrada.items():
        if os.path.exists(pasta):
            print(f"\nProcessando pasta: {pasta} com grade {cols}x{linhas}")
            processar_imagem(pasta, saida_dir, cols, linhas)
        else:
            print(f"Pasta {pasta} não encontrada, pulando...")
    
    print("\nProcessamento concluído!")

if __name__ == "__main__":
    # Iniciar processamento de todas as pastas
    processar_todas_pastas()