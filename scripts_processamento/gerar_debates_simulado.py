# -*- coding: utf-8 -*-
"""
Gerador de Debates Inéditos para o Simulado ISO/IEC 17025:2017.
Produz 50 podcasts dinâmicos entre Thalita e Francisca analisando
a questão, as armadilhas das alternativas incorretas e o fundamento da correta.
Salva em Podcasts_Simulado/{qid}_debate.mp3 com vozes neurais e concatenação ffmpeg.
Aplica regras fonéticas aprovadas:
- Standard Methods -> stán-derd mé-thadz
- Cgcre / CGCRE -> Sêgécre
- Atualização dinâmica da letra correta e da letra distratora.
"""

import asyncio
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
import edge_tts

OUTPUT_DIR = Path("Podcasts_Simulado")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VOZ_THALITA = "pt-BR-ThalitaMultilingualNeural"
VOZ_FRANCISCA = "pt-BR-FranciscaNeural"

def phonetize_text(text: str) -> str:
    """Aplica regras fonéticas aprovadas."""
    text = re.sub(r'\bStandard Methods\b', 'stán-derd mé-thadz', text, flags=re.IGNORECASE)
    text = re.sub(r'\bStandard Method\b', 'stán-derd mé-thad', text, flags=re.IGNORECASE)
    text = text.replace("ISO/IEC", "ISO").replace("ISO 17025:2017", "ISO 17025")
    # Cgcre -> Sêgécre (pronúncia correta solicitada)
    text = re.sub(r'\bCgcre\b', 'Sêgécre', text, flags=re.IGNORECASE)
    text = re.sub(r'\bCGCRE\b', 'Sêgécre', text, flags=re.IGNORECASE)
    return text

def clean_summary(text: str, max_words: int = 25) -> str:
    """Resume sentenças longas para fluidez de conversa em podcast."""
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."

def build_dialogue_turns(q: dict):
    clausula = q.get('clausula', '')
    tema = phonetize_text(q.get('tema', ''))
    correta = q.get('correta', 'A')
    
    # Encontrar texto da correta e uma incorreta principal
    alt_correta_obj = next((a for a in q['alternativas'] if a['letra'] == correta), None)
    texto_correta = clean_summary(alt_correta_obj['texto'] if alt_correta_obj else '', 20)
    
    incorretas = [a for a in q['alternativas'] if a['letra'] != correta]
    alt_errada = incorretas[0] if incorretas else None
    letra_errada = alt_errada['letra'] if alt_errada else 'A'
    texto_errada = clean_summary(alt_errada['texto'] if alt_errada else '', 18)
    
    # Extrair diagnósticos
    exp_map = q.get('explicacoes_detalhadas', {})
    exp_errada = exp_map.get(letra_errada, {})
    pq_errada = clean_summary(exp_errada.get('por_que_esta_incorreta', 'essa interpretação não tem respaldo na norma.'), 24)
    
    exp_correta = exp_map.get(correta, {})
    fund_acerto = clean_summary(exp_correta.get('fundamentacao_acerto', q.get('justificativa', '')), 26)

    # 4 turnos dinâmicos e naturais com fonética aplicada
    dialogue = [
        ("Thalita", phonetize_text(
            f"Francisca, vamos analisar essa questão do Requisito {clausula} sobre {tema}. "
            f"O que torna esse tema tão propenso a dúvidas na rotina do laboratório?"
        )),
        ("Francisca", phonetize_text(
            f"Essa é clássica, Thalita! A maior pegadinha aqui costuma ser a alternativa {letra_errada}: '{texto_errada}'. "
            f"Muitos avaliados marcam essa opção por hábito, mas isso é um erro porque {pq_errada}"
        )),
        ("Thalita", phonetize_text(
            f"Exatamente! E a resposta certa é a alternativa {correta}, porque diz com precisão que '{texto_correta}'."
        )),
        ("Francisca", phonetize_text(
            f"Perfeito, Thalita! A fundamentação metrológica é clara: {fund_acerto}. "
            f"Na rotina dos laboratórios da Eletronuclear e em auditorias da Cgcre, ter esse domínio evita não conformidades sérias."
        ))
    ]
    return dialogue

async def synthesize_turn(text: str, voice: str, rate: str, pitch: str) -> bytes:
    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    data = bytearray()
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            data.extend(chunk["data"])
    return bytes(data)

async def gerar_debate_questao(q: dict, silence_file: Path, force=False):
    qid = q['id']
    out_file = OUTPUT_DIR / f"{qid}_debate.mp3"
    
    if not force and out_file.exists() and out_file.stat().st_size > 5000:
        return out_file  # Já gerado
        
    dialogue = build_dialogue_turns(q)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        concat_txt = tmp_path / "concat.txt"
        lines = []
        
        for idx, (speaker, text) in enumerate(dialogue):
            voz = VOZ_THALITA if speaker == "Thalita" else VOZ_FRANCISCA
            rate = "+14%" if speaker == "Thalita" else "+10%"
            pitch = "+4Hz" if speaker == "Thalita" else "+2Hz"
            
            audio = await synthesize_turn(text, voz, rate, pitch)
            cfile = tmp_path / f"turn_{idx:02d}.mp3"
            cfile.write_bytes(audio)
            
            lines.append(f"file '{cfile.resolve().as_posix()}'")
            lines.append(f"file '{silence_file.resolve().as_posix()}'")
            
        concat_txt.write_text("\n".join(lines), encoding="utf-8")
        
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_file)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
    return out_file

async def main():
    print("==========================================================")
    print(" GERANDO 50 DEBATES INÉDITOS DO SIMULADO - THALITA & FRANCISCA")
    print(" (Com nova distribuição de gabarito e pronúncia Sêgécre)     ")
    print("==========================================================")
    
    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    with open('questoes_simulado.json', 'r', encoding='utf-8') as f:
        questoes = json.load(f)
        
    print(f"Total de questões para gerar debates: {len(questoes)}")
    
    # Processar em lotes controlados
    batch_size = 5
    for i in range(0, len(questoes), batch_size):
        chunk = questoes[i:i + batch_size]
        tasks = [gerar_debate_questao(q, silence_file, force=True) for q in chunk]
        results = await asyncio.gather(*tasks)
        print(f"Progresso: {min(i + batch_size, len(questoes))}/{len(questoes)} debates gerados...")
        
    # Atualizar questoes_simulado.json com o caminho dos novos debates
    for q in questoes:
        qid = q['id']
        q['debate_podcast'] = f"Podcasts_Simulado/{qid}_debate.mp3"
        
    with open('questoes_simulado.json', 'w', encoding='utf-8') as f:
        json.dump(questoes, f, ensure_ascii=False, indent=2)
        
    print("\n[OK] Todos os 50 debates inéditos foram gerados e vinculados em questoes_simulado.json!")

if __name__ == '__main__':
    asyncio.run(main())
