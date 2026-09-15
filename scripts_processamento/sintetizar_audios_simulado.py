# -*- coding: utf-8 -*-
"""
Síntese de Áudio para o Simulado ISO/IEC 17025:2017:
Regenera enunciados com a introdução natural profissional:
"Pergunta sobre o Requisito [Cláusula], [Tema]. [Enunciado]"
e pronúncia fonética corrigida para "Standard Methods" -> "stán-derd mé-thadz".
"""

import asyncio
import json
import os
import re
from pathlib import Path
import edge_tts

VOICE = "pt-BR-FranciscaNeural"
OUTPUT_DIR = Path("Audios_Simulado")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def phonetize_text(text: str) -> str:
    """Aplica ajustes fonéticos para pronúncia natural em pt-BR."""
    # Standard Methods -> stán-derd mé-thadz
    text = re.sub(r'\bStandard Methods\b', 'stán-derd mé-thadz', text, flags=re.IGNORECASE)
    text = re.sub(r'\bStandard Method\b', 'stán-derd mé-thad', text, flags=re.IGNORECASE)
    return text

async def synthesize_file(text: str, output_path: Path, force=False):
    if not force and output_path.exists() and output_path.stat().st_size > 500:
        return  # Já existe
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(str(output_path))
    except Exception as e:
        print(f"Erro ao sintetizar {output_path.name}: {e}")

async def process_batch(items, batch_size=8):
    for i in range(0, len(items), batch_size):
        chunk = items[i:i + batch_size]
        tasks = [synthesize_file(text, path, force=force) for text, path, force in chunk]
        await asyncio.gather(*tasks)
        print(f"Progresso: {min(i + batch_size, len(items))}/{len(items)} faixas concluídas...")

async def main():
    with open('questoes_simulado.json', 'r', encoding='utf-8') as f:
        qs = json.load(f)

    work_items = []
    for q in qs:
        qid = q['id']
        clausula = q.get('clausula', '')
        tema = phonetize_text(q.get('tema', ''))
        enunciado = phonetize_text(q['enunciado'])

        # Nova introdução natural: "Pergunta sobre o Requisito [Cláusula], [Tema]. [Enunciado]"
        text_enunciado = f"Pergunta sobre o Requisito {clausula}, {tema}. {enunciado}"
        work_items.append((text_enunciado, OUTPUT_DIR / f"{qid}_enunciado.mp3", True))

        # Alternativas (garantir fonética)
        for alt in q['alternativas']:
            letra = alt['letra']
            alt_text = phonetize_text(alt['texto'])
            text_alt = f"Alternativa {letra}: {alt_text}"
            alt_path = OUTPUT_DIR / f"{qid}_alt_{letra}.mp3"
            # Se a alternativa continha Standard Methods, force=True
            has_std = 'standard method' in alt['texto'].lower()
            work_items.append((text_alt, alt_path, has_std))

    print(f"Total de faixas para sintetizar com a voz {VOICE}: {len(work_items)}")
    await process_batch(work_items, batch_size=10)
    print("Síntese dos enunciados concluída com sucesso com nova introdução e fonética!")

if __name__ == '__main__':
    asyncio.run(main())
