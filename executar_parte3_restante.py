# -*- coding: utf-8 -*-
import subprocess
import sys

json_files = [
    'dialogos_parte3_cap4.json',
    'dialogos_parte3_cap5_6_7.json',
    'dialogos_parte3_cap8_9_10.json',
    'dialogos_parte3_cap11_especial.json',
    'dialogos_parte3_cap12_especial.json',
]

print('Iniciando execucao em lote da Parte 3...')
for jf in json_files:
    print('=' * 60)
    print(f'Executando: {jf}')
    print('=' * 60)
    ret = subprocess.run([sys.executable, 'gerar_podcast_por_json.py', jf])
    if ret.returncode != 0:
        print(f'ERRO ao executar {jf} (codigo {ret.returncode})')
        sys.exit(ret.returncode)

print('=' * 60)
print('TODOS OS CAPITULOS DA PARTE 3 FORAM GERADOS COM SUCESSO!')
print('=' * 60)
