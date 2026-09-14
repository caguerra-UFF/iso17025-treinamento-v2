# -*- coding: utf-8 -*-
import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'F:\Transcricoes_Consolidadas\Podcasts_Tematicos\Thalita_e_Francisca'
dirs = {
    'Parte 1 (02/09/2026) - Equipamentos, Calibração e Gestão de Fornecedores': base_dir,
    'Parte 2 (03/09/2026) - Requisitos de Processo: 7.1 a 7.6': os.path.join(base_dir, 'Parte_2'),
    'Parte 3 (04/09/2026) - Garantia da Validade, Laudos, Metrologia e Gestão': os.path.join(base_dir, 'Parte_3')
}

catalog = {}
total_files = 0
total_bytes = 0

for section, folder in dirs.items():
    if not os.path.exists(folder):
        continue
    files = [f for f in os.listdir(folder) if f.endswith('.mp3') and not f.startswith('_')]
    catalog[section] = []
    for f in sorted(files):
        path = os.path.join(folder, f)
        size = os.path.getsize(path)
        total_files += 1
        total_bytes += size
        is_full = 'Completo' in f or 'Capitulo_1' in f
        catalog[section].append({
            'filename': f,
            'size_kb': round(size / 1024, 1),
            'size_mb': round(size / (1024 * 1024), 2),
            'is_full_chapter': is_full
        })

print(f'Total de Faixas: {total_files}')
print(f'Tamanho Total: {total_bytes / (1024 * 1024):.2f} MB')

with open(r'F:\Transcricoes_Consolidadas\catalogo_geral_podcasts.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print('catalogo_geral_podcasts.json gerado com sucesso!')
