#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste para validar que os arquivos foram corrigidos corretamente.
Simula o fluxo de treinamento para verificar se tudo funciona.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import load_file_as_array, extract_features_from_array
from app import detect_label_from_file
import pandas as pd
import numpy as np

def test_files():
    """Testa a detecção e extração de features para arquivos de treinamento."""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    uploads_dir = os.path.join(base_dir, 'uploads')
    
    # Arquivos para testar
    test_files = [
        'uploads/38b87887-ba40-4104-aa6f-c1aba74c4477/teste_acelerometro.csv',
        'uploads/3a6d1e80-1a22-4f18-9298-42f31a00ff1f/train_1.csv',
        'uploads/3a6d1e80-1a22-4f18-9298-42f31a00ff1f/train_2.csv',
        'uploads/0775fdf6-a18d-40d6-acd3-8951ac22a122/teste_acelerometro.csv',
    ]
    
    print("=" * 70)
    print("TESTE DE VALIDACAO - Arquivos CSV Corrigidos")
    print("=" * 70)
    
    total_files = 0
    files_with_labels = 0
    files_with_features = 0
    
    for rel_path in test_files:
        full_path = os.path.join(base_dir, rel_path)
        
        if not os.path.exists(full_path):
            print("[ERRO] Arquivo nao existe: {}".format(rel_path))
            continue
        
        total_files += 1
        print("\nArquivo: {}".format(os.path.basename(full_path)))
        
        # Testar detecção de label
        label = detect_label_from_file(full_path, {})
        if label:
            print("  [OK] Label detectado: '{}'".format(label))
            files_with_labels += 1
        else:
            print("  [ERRO] Label nao detectado")
            continue
        
        # Testar carregamento de array
        arr = load_file_as_array(full_path)
        if arr is None:
            print("  [ERRO] Falha ao carregar array")
            continue
        
        print("  [OK] Array carregado: {} amostras x {} features".format(arr.shape[0], arr.shape[1]))
        
        # Testar extração de features
        features = extract_features_from_array(arr)
        if features:
            print("  [OK] Features extraidas: {} features".format(len(features)))
            files_with_features += 1
        else:
            print("  [ERRO] Falha ao extrair features")
    
    print("\n" + "=" * 70)
    print("RESUMO DO TESTE:")
    print("=" * 70)
    print("Total de arquivos testados: {}".format(total_files))
    print("Arquivos com label detectado: {}".format(files_with_labels))
    print("Arquivos com features extraidas: {}".format(files_with_features))
    
    if files_with_features >= 2:
        print("\n[OK] Teste aprovado! O sistema esta pronto para treinamento.")
        return True
    else:
        print("\n[ERRO] Teste falhou. Verificar arquivos.")
        return False

if __name__ == '__main__':
    success = test_files()
    sys.exit(0 if success else 1)
