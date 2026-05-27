#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exemplos práticos de uso da função extract_accelerometer_features
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from utils import extract_accelerometer_features

def exemplo_1_dados_simples():
    """Exemplo 1: Extrair features de dados simples"""
    print("\n" + "="*70)
    print("EXEMPLO 1: Dados Simples")
    print("="*70)
    
    # Dados brutos
    data = {
        'x': [0.05, -0.03, 0.01, 0.02, -0.04],
        'y': [0.02, -0.04, 0.00, -0.01, 0.03],
        'z': [9.79, 9.83, 9.78, 9.82, 9.80],
        'label': ['parado', 'parado', 'parado', 'parado', 'parado']
    }
    
    df = pd.DataFrame(data)
    print("\nDados de entrada (5 amostras):")
    print(df)
    
    # Extrair features
    features = extract_accelerometer_features(df)
    
    print("\nFeatures extraidas (1 linha, 19 colunas):")
    print(features)
    
    print("\nAlgumas features especificas:")
    print("  x_mean: {:.6f}".format(features['x_mean'].values[0]))
    print("  z_energy: {:.6f}".format(features['z_energy'].values[0]))
    print("  magnitude_mean: {:.6f}".format(features['magnitude_mean'].values[0]))


def exemplo_2_numpy_array():
    """Exemplo 2: Converter NumPy array para features"""
    print("\n" + "="*70)
    print("EXEMPLO 2: NumPy Array")
    print("="*70)
    
    # Dados como array
    arr = np.array([
        [0.05, 0.02, 9.79],
        [-0.03, -0.04, 9.83],
        [0.01, 0.00, 9.78],
        [0.02, -0.01, 9.82],
        [-0.04, 0.03, 9.80]
    ])
    
    print("\nArray de entrada (5x3):")
    print("  Linhas: 5 amostras")
    print("  Colunas: x, y, z")
    
    # Extrair features
    features = extract_accelerometer_features(arr)
    
    print("\nFeatures extraidas:")
    print("  Forma: {}".format(features.shape))
    print("  Total de features: {}".format(features.shape[1]))


def exemplo_3_arquivo_csv():
    """Exemplo 3: Carregar CSV e extrair features"""
    print("\n" + "="*70)
    print("EXEMPLO 3: Arquivo CSV")
    print("="*70)
    
    # Usar arquivo de teste criado anteriormente
    csv_path = os.path.join(os.path.dirname(__file__), 'test_input.csv')
    
    if os.path.exists(csv_path):
        print("\nCarregando arquivo: {}".format(csv_path))
        df = pd.read_csv(csv_path)
        
        print("Dados originais:")
        print(df)
        
        # Extrair features
        features = extract_accelerometer_features(df)
        
        print("\nFeatures extraidas:")
        print(features)
    else:
        print("Arquivo de teste nao encontrado. Pulando este exemplo.")


def exemplo_4_multiplos_arquivos():
    """Exemplo 4: Processar múltiplos arquivos"""
    print("\n" + "="*70)
    print("EXEMPLO 4: Multiplos Arquivos")
    print("="*70)
    
    # Simular 3 arquivos com dados diferentes
    datasets = [
        {'name': 'Parado', 'data': np.array([
            [0.01, 0.00, 9.80],
            [0.00, 0.01, 9.81],
            [-0.01, 0.00, 9.79]
        ])},
        {'name': 'Correndo', 'data': np.array([
            [0.5, 0.3, 9.5],
            [0.4, 0.2, 9.6],
            [0.6, 0.4, 9.4]
        ])},
        {'name': 'Andando', 'data': np.array([
            [0.2, 0.1, 9.8],
            [0.1, 0.2, 9.9],
            [0.3, 0.0, 9.7]
        ])}
    ]
    
    todos_features = []
    
    for dataset in datasets:
        print("\nProcessando: {}".format(dataset['name']))
        features = extract_accelerometer_features(dataset['data'])
        features['activity'] = dataset['name']  # Adicionar label
        todos_features.append(features)
        print("  x_mean: {:.6f}".format(features['x_mean'].values[0]))
        print("  magnitude_mean: {:.6f}".format(features['magnitude_mean'].values[0]))
    
    # Combinar todos os resultados
    df_combined = pd.concat(todos_features, ignore_index=True)
    print("\n" + "-"*70)
    print("Combinado (3 atividades):")
    print(df_combined[['activity', 'x_mean', 'magnitude_mean']])


def exemplo_5_calculos_detalhados():
    """Exemplo 5: Entender os calculos"""
    print("\n" + "="*70)
    print("EXEMPLO 5: Calculos Detalhados")
    print("="*70)
    
    # Dados simples para verificacao manual
    data = {
        'x': [1.0, 2.0, 3.0],
        'y': [0.0, 0.0, 0.0],
        'z': [0.0, 0.0, 0.0]
    }
    
    df = pd.DataFrame(data)
    features = extract_accelerometer_features(df)
    
    print("\nDados de entrada:")
    print(df)
    
    print("\nCalculos manuais para verificacao:")
    print("  x: [1.0, 2.0, 3.0]")
    print("  x_mean = (1 + 2 + 3) / 3 = {:.6f}".format(features['x_mean'].values[0]))
    print("  x_std = desvio padrao = {:.6f}".format(features['x_std'].values[0]))
    print("  x_min = {:.6f}".format(features['x_min'].values[0]))
    print("  x_max = {:.6f}".format(features['x_max'].values[0]))
    print("  x_energy = 1^2 + 2^2 + 3^2 = {:.6f}".format(features['x_energy'].values[0]))
    
    print("\nMagnitude = sqrt(x^2 + y^2 + z^2):")
    print("  magnitude_mean = sqrt(1^2 + 2^2 + 3^2) / 3 = {:.6f}".format(
        features['magnitude_mean'].values[0]))


def exemplo_6_lista_todas_features():
    """Exemplo 6: Listar todas as features calculadas"""
    print("\n" + "="*70)
    print("EXEMPLO 6: Todas as Features")
    print("="*70)
    
    data = {
        'x': np.random.randn(100),
        'y': np.random.randn(100),
        'z': 9.8 + np.random.randn(100) * 0.1
    }
    
    df = pd.DataFrame(data)
    features = extract_accelerometer_features(df)
    
    print("\nTodas as {} features calculadas:".format(features.shape[1]))
    print("-" * 70)
    
    # Agrupar por eixo
    for axis in ['x', 'y', 'z']:
        print("\nEixo '{}':".format(axis))
        for stat in ['mean', 'std', 'var', 'min', 'max', 'energy']:
            col_name = '{}_{}'.format(axis, stat)
            value = features[col_name].values[0]
            print("  {}: {:.6f}".format(col_name, value))
    
    print("\nGlobal:")
    print("  magnitude_mean: {:.6f}".format(features['magnitude_mean'].values[0]))


if __name__ == '__main__':
    print("\n" + "#"*70)
    print("# EXEMPLOS PRATICOS - extract_accelerometer_features")
    print("#"*70)
    
    exemplo_1_dados_simples()
    exemplo_2_numpy_array()
    exemplo_3_arquivo_csv()
    exemplo_4_multiplos_arquivos()
    exemplo_5_calculos_detalhados()
    exemplo_6_lista_todas_features()
    
    print("\n" + "#"*70)
    print("# FIM DOS EXEMPLOS")
    print("#"*70)
    print("\nPara mais informacoes, veja FEATURE_EXTRACTION_GUIDE.md")
