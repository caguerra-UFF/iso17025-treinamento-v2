# -*- coding: utf-8 -*-
"""
Síntese de Áudio para o Simulado ISO/IEC 17025:2017:
Regenera enunciados e alternativas com a introdução natural profissional:
- "Pergunta sobre o Requisito [Cláusula], [Tema]. [Enunciado]"
- Alternativas com prefixo "Alternativa [Letra]: [Texto]"
- Pronúncia fonética corrigida para:
  * "Standard Methods" -> "stán-derd mé-thadz"
  * "Cgcre" / "CGCRE" -> "Sêgécre"
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
    
    # Cgcre -> Sêgécre (pronúncia oficial solicitada)
    text = re.sub(r'\bCgcre\b', 'Sêgécre', text, flags=re.IGNORECASE)
    text = re.sub(r'\bCGCRE\b', 'Sêgécre', text, flags=re.IGNORECASE)
    
    return text

async def synthesize_file(text: str, output_path: Path, force=False):
    if not force and output_path.exists() and output_path.stat().st_size > 500:
        return  # Já existe
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(str(output_path))
    except Exception as e:
        print(f"Erro ao sintetizar {output_path.name}: {e}")

async def process_batch(items, batch_size=10):
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
        raw_tema = q.get('tema', '')
        raw_enunciado = q['enunciado']
        
        tema = phonetize_text(raw_tema)
        enunciado = phonetize_text(raw_enunciado)

        # Se o enunciado ou tema contiver Cgcre ou Standard Methods, forçar regeração
        has_special = bool(re.search(r'\b(cgcre|standard method)\b', raw_tema + " " + raw_enunciado, re.IGNORECASE))

        # Enunciado com introdução natural
        text_enunciado = f"Pergunta sobre o Requisito {clausula}, {tema}. {enunciado}"
        work_items.append((text_enunciado, OUTPUT_DIR / f"{qid}_enunciado.mp3", has_special))

        # Todas as 4 alternativas de cada questão (forçar regeração devido ao novo mapeamento A/B/C/D)
        for alt in q['alternativas']:
            letra = alt['letra']
            alt_text = phonetize_text(alt['texto'])
            text_alt = f"Alternativa {letra}: {alt_text}"
            alt_path = OUTPUT_DIR / f"{qid}_alt_{letra}.mp3"
            work_items.append((text_alt, alt_path, True))

    print(f"Total de faixas para sintetizar com a voz {VOICE}: {len(work_items)}")
    await process_batch(work_items, batch_size=10)
    print("Síntese das faixas concluída com sucesso com nova distribuição de alternativas e pronúncia Sêgécre!")

if __name__ == '__main__':
    asyncio.run(main())
