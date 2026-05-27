#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para adicionar coluna 'label' aos arquivos CSV que não a têm.
Uso: python add_labels.py <arquivo.csv> <label> [<arquivo2.csv> <label2> ...]
Exemplo: python add_labels.py teste_acelerometro.csv parado predict.csv correndo
"""

import sys
import pandas as pd
import os

def add_label_to_csv(file_path, label):
    """Adiciona coluna 'label' a um arquivo CSV se ela não existir."""
    if not os.path.exists(file_path):
        print("[ERRO] Arquivo nao encontrado: {}".format(file_path))
        return False
    
    try:
        df = pd.read_csv(file_path)
        
        # Se já tem label, não faz nada
        if 'label' in df.columns:
            print("[AVISO] {} ja tem coluna 'label'".format(os.path.basename(file_path)))
            return True
        
        # Adiciona label
        df['label'] = label
        
        # Salva o arquivo
        df.to_csv(file_path, index=False)
        print("[OK] {} - adicionada coluna 'label' com valor '{}'".format(
            os.path.basename(file_path), label))
        return True
    except Exception as e:
        print("[ERRO] Erro ao processar {}: {}".format(os.path.basename(file_path), e))
        return False

def main():
    if len(sys.argv) < 3 or len(sys.argv) % 2 == 0:
        print(__doc__)
        print("\nExemplo de uso batch (para adicionar label a multiplos arquivos):")
        print("python add_labels.py \\")
        print("  uploads/38b87887-ba40-4104-aa6f-c1aba74c4477/teste_acelerometro.csv parado \\")
        print("  uploads/15a543aa-2440-41f9-a58c-b162c8b9a904/predict.csv correndo")
        sys.exit(1)
    
    # Processa pares de arquivo/label
    for i in range(1, len(sys.argv), 2):
        file_path = sys.argv[i]
        label = sys.argv[i + 1]
        add_label_to_csv(file_path, label)
    
    print("\n[OK] Processo concluido!")

if __name__ == '__main__':
    main()
