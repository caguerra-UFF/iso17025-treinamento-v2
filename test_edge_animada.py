import asyncio
import edge_tts
import subprocess
import os

async def gen():
    d = [
        ("Thalita", "pt-BR-ThalitaMultilingualNeural", "+14%", "+4Hz", "Gente, vamos começar falando de uma das maiores dores de cabeça nos laboratórios: o controle de calibração e manutenção! O instrutor do curso trouxe uma visão super prática sobre isso no item 2.1."),
        ("Francisca", "pt-BR-FranciscaNeural", "+10%", "+2Hz", "Excelente ponto, Thalita! E convenhamos, o pessoal adora complicar, né? Já vi laboratório mantendo três controles completamente separados pra mesma máquina! O que o instrutor defendeu aqui foi direto ao ponto: não precisa inventar moda! Calibração, verificação intermediária e manutenção preventiva podem sim estar integradas no mesmo plano geral!"),
        ("Thalita", "pt-BR-ThalitaMultilingualNeural", "+14%", "+4Hz", "Nossa, isso facilita demais! Mas me diz uma coisa: e o avaliador da Cgcre, aceita isso numa boa? A norma não exige formulários separados?"),
        ("Francisca", "pt-BR-FranciscaNeural", "+10%", "+2Hz", "Aceita sim, com ressalva! Os requisitos 6.4.3 e 6.4.13 da ISO 17025 exigem que o plano exista e esteja sob controle rastreável! A força da evidência tá na rastreabilidade e no cumprimento das datas, e não na quantidade de planilhas que você inventou!"),
        ("Thalita", "pt-BR-ThalitaMultilingualNeural", "+14%", "+4Hz", "Perfeito! Menos burocracia de gaveta e muito mais controle real do que precisa ser feito no mês!")
    ]
    
    parts = []
    for i, (name, voice, rate, pitch, text) in enumerate(d):
        fn = f"_temp_edge_animada_{i}.mp3"
        parts.append(fn)
        c = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await c.save(fn)
        
    sil = "_silence_180ms.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "0.18", "-b:a", "192k", sil], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    lst = "_concat_edge_animada.txt"
    with open(lst, "w", encoding="utf-8") as f:
        for i, p in enumerate(parts):
            f.write(f"file '{p}'\n")
            if i < len(parts) - 1:
                f.write(f"file '{sil}'\n")
                
    out = "Comparacao_Item_2_1_EdgeTTS_Super_Animada.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:a", "libmp3lame", "-b:a", "192k", out], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for p in parts:
        if os.path.exists(p): os.remove(p)
    if os.path.exists(lst): os.remove(lst)
    print("SUCCESS Edge-TTS Super Animada:", out)

asyncio.run(gen())
