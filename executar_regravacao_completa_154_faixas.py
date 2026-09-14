# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)

BASE_DIR = r'F:\Transcricoes_Consolidadas'

parte1_scripts = [
    'gerar_capitulo_3_thalita_francisca.py',
    'gerar_capitulo_4_thalita_francisca.py',
    'gerar_capitulo_5_thalita_francisca.py',
    'gerar_capitulo_6_thalita_francisca.py',
    'gerar_capitulo_7_thalita_francisca.py',
    'gerar_capitulo_8_thalita_francisca.py',
    'gerar_capitulo_9_thalita_francisca.py',
    'gerar_capitulo_10_thalita_francisca.py',
    'gerar_capitulo_11_thalita_francisca.py',
    'gerar_capitulo_12_thalita_francisca.py',
    'gerar_capitulo_13_thalita_francisca.py'
]

parte2_jsons = [
    'dialogos_parte2_cap2.json',
    'dialogos_parte2_cap3.json',
    'dialogos_parte2_cap4.json',
    'dialogos_parte2_cap5.json',
    'dialogos_parte2_cap6.json',
    'dialogos_parte2_cap7.json',
    'dialogos_parte2_cap8.json',
    'dialogos_parte2_cap9.json',
    'dialogos_parte2_cap10_especial.json',
    'dialogos_parte2_cap11_especial.json'
]

parte3_jsons = [
    'dialogos_parte3_cap2.json',
    'dialogos_parte3_cap3.json',
    'dialogos_parte3_cap4.json',
    'dialogos_parte3_cap5_6_7.json',
    'dialogos_parte3_cap8_9_10.json',
    'dialogos_parte3_cap11_especial.json',
    'dialogos_parte3_cap12_especial.json'
]

total_steps = len(parte1_scripts) + len(parte2_jsons) + len(parte3_jsons)
current = 0
start_time = time.time()

print('=' * 70)
print('🚀 INICIANDO REGRAVACAO COMPLETA NO MODO SUPER ANIMADO')
print(f'Total de modulos a executar: {total_steps}')
print('=' * 70)

# 1. Parte 1
print('\n>>> [FASE 1/3] REGRAVANDO PARTE 1 (Capitulos 3 ao 13)...')
for s in parte1_scripts:
    current += 1
    print(f'\n[{current}/{total_steps}] Executando: {s}...')
    ret = subprocess.run([sys.executable, os.path.join(BASE_DIR, s)], cwd=BASE_DIR)
    if ret.returncode != 0:
        print(f'❌ ERRO ao executar {s} (codigo {ret.returncode})')
        sys.exit(ret.returncode)

# 2. Parte 2
print('\n>>> [FASE 2/3] REGRAVANDO PARTE 2 (Capitulos 2 ao 11)...')
for j in parte2_jsons:
    current += 1
    print(f'\n[{current}/{total_steps}] Executando: {j}...')
    ret = subprocess.run([sys.executable, os.path.join(BASE_DIR, 'gerar_podcast_por_json.py'), j], cwd=BASE_DIR)
    if ret.returncode != 0:
        print(f'❌ ERRO ao executar {j} (codigo {ret.returncode})')
        sys.exit(ret.returncode)

# 3. Parte 3
print('\n>>> [FASE 3/3] REGRAVANDO PARTE 3 (Capitulos 2 ao 12)...')
for j in parte3_jsons:
    current += 1
    print(f'\n[{current}/{total_steps}] Executando: {j}...')
    ret = subprocess.run([sys.executable, os.path.join(BASE_DIR, 'gerar_podcast_por_json.py'), j], cwd=BASE_DIR)
    if ret.returncode != 0:
        print(f'❌ ERRO ao executar {j} (codigo {ret.returncode})')
        sys.exit(ret.returncode)

# 4. Atualizar catalogo e players
print('\n>>> [FASE FINAL] REINDEXANDO CATALOGO E ATUALIZANDO PLAYERS...')
subprocess.run([sys.executable, os.path.join(BASE_DIR, 'gerar_catalogo_completo_audios.py')], cwd=BASE_DIR, check=True)
subprocess.run([sys.executable, os.path.join(BASE_DIR, 'gerar_player.py')], cwd=BASE_DIR, check=True)

elapsed = (time.time() - start_time) / 60
print('\n' + '=' * 70)
print(f'🎉 REGRAVACAO DE TODAS AS 154 FAIXAS CONCLUIDA COM SUCESSO EM {elapsed:.1f} MINUTOS!')
print('=' * 70)
