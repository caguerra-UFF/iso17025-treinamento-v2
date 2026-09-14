html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparador de Vozes: Padrão vs. Super Animada | Item 2.1</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0f172a;
            --surface: #1e293b;
            --border: #334155;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --accent-eleven: #a855f7;
            --accent-edge: #06b6d4;
            --accent-fire: #f59e0b;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
        body { background: var(--bg); color: var(--text); padding: 32px 20px; min-height: 100vh; display: flex; flex-direction: column; align-items: center; }
        .container { max-width: 1000px; width: 100%; }
        header { text-align: center; margin-bottom: 28px; }
        header h1 { font-size: 1.8rem; font-weight: 800; background: linear-gradient(90deg, #f59e0b, #ec4899, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        header p { color: var(--text-muted); font-size: 0.95rem; margin-top: 6px; }
        
        .section-title { font-size: 1.1rem; font-weight: 700; margin: 24px 0 14px 0; display: flex; align-items: center; gap: 8px; color: #f1f5f9; }
        .comparison-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
        @media (max-width: 768px) { .comparison-cards { grid-template-columns: 1fr; } }
        
        .card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 12px; position: relative; }
        .card.featured { border: 2px solid #ec4899; box-shadow: 0 0 20px rgba(236, 72, 153, 0.15); }
        .card.edge-anim { border-top: 4px solid var(--accent-fire); }
        .card.eleven-anim { border-top: 4px solid #ec4899; }
        .card.edge-std { border-top: 4px solid var(--accent-edge); }
        .card.eleven-std { border-top: 4px solid var(--accent-eleven); }
        
        .card-header { display: flex; justify-content: space-between; align-items: center; }
        .badge { font-size: 0.725rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; text-transform: uppercase; }
        .badge.fire { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
        .badge.pink { background: rgba(236, 72, 153, 0.2); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.4); }
        .badge.edge { background: rgba(6, 182, 212, 0.15); color: #38bdf8; }
        .badge.eleven { background: rgba(139, 92, 246, 0.15); color: #c084fc; }
        
        .card-title { font-size: 1.05rem; font-weight: 700; }
        .card-specs { font-size: 0.8rem; color: var(--text-muted); line-height: 1.5; }
        
        audio { width: 100%; margin-top: 6px; border-radius: 8px; }
        
        .dialogue-box { background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border); border-radius: 10px; padding: 20px; margin-top: 30px; }
        .dialogue-title { font-size: 0.85rem; font-weight: 700; color: #cbd5e1; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.05em; }
        .turn { margin-bottom: 12px; font-size: 0.875rem; line-height: 1.5; }
        .turn-speaker { font-weight: 700; }
        .speaker-host { color: #38bdf8; }
        .speaker-guest { color: #f472b6; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔥 Comparador de Energia & Ritmo</h1>
            <p>Teste do <strong>Item 2.1 — Plano de Manutenção e Calibração</strong> com diferentes níveis de animação e entonação</p>
        </header>

        <div class="section-title">⚡ Versões SUPER ANIMADAS (Alto Entusiasmo, Pausas Curtas & Ritmo Vibrante):</div>
        <div class="comparison-cards">
            <!-- Card 1: ElevenLabs Super Animada -->
            <div class="card featured eleven-anim">
                <div class="card-header">
                    <div class="card-title">🔥 1. ElevenLabs — Super Animada</div>
                    <span class="badge pink">Muito Expressiva</span>
                </div>
                <div class="card-specs">
                    <div>👭 <strong>Vozes:</strong> Laura (Enthusiast/Sassy) & Jessica (Playful/Warm)</div>
                    <div>⚡ <strong>Ajustes:</strong> Estabilidade reduzida (0.28), Estilo acentuado (+45%), Pausas 180ms</div>
                    <div>⏱️ <strong>Duração:</strong> 1m 19s (79s) • 192 kbps MP3</div>
                </div>
                <audio controls src="Comparacao_Item_2_1_ElevenLabs_Super_Animada.mp3"></audio>
            </div>

            <!-- Card 2: Edge-TTS Super Animada -->
            <div class="card edge-anim">
                <div class="card-header">
                    <div class="card-title">⚡ 2. Edge-TTS — Super Animada</div>
                    <span class="badge fire">Ágil / Rádio Jovem</span>
                </div>
                <div class="card-specs">
                    <div>👭 <strong>Vozes:</strong> Thalita & Francisca (Neural)</div>
                    <div>⚡ <strong>Ajustes:</strong> Velocidade acelerada (+14%), Pitch mais alto (+4Hz), Pausas 180ms</div>
                    <div>⏱️ <strong>Duração:</strong> 1m 06s (66s) • 192 kbps MP3</div>
                </div>
                <audio controls src="Comparacao_Item_2_1_EdgeTTS_Super_Animada.mp3"></audio>
            </div>
        </div>

        <div class="section-title" style="margin-top: 32px;">🎙️ Versões MODERADAS (Tom Clássico / Formal):</div>
        <div class="comparison-cards">
            <!-- Card 3: ElevenLabs Padrão -->
            <div class="card eleven-std">
                <div class="card-header">
                    <div class="card-title">3. ElevenLabs — Tom Moderado</div>
                    <span class="badge eleven">Sarah & Alice</span>
                </div>
                <div class="card-specs">
                    <div>👭 <strong>Vozes:</strong> Sarah & Alice (Multilingual v2)</div>
                    <div>⚡ <strong>Ajustes:</strong> Estabilidade padrão (0.50), Pausas 250ms</div>
                    <div>⏱️ <strong>Duração:</strong> 1m 22s (82s) • 192 kbps MP3</div>
                </div>
                <audio controls src="Comparacao_Item_2_1_ElevenLabs_Sarah_e_Alice.mp3"></audio>
            </div>

            <!-- Card 4: Edge-TTS Padrão Atual -->
            <div class="card edge-std">
                <div class="card-header">
                    <div class="card-title">4. Edge-TTS — Tom Moderado</div>
                    <span class="badge edge">Produção Atual</span>
                </div>
                <div class="card-specs">
                    <div>👭 <strong>Vozes:</strong> Thalita & Francisca (Neural Padrão)</div>
                    <div>⚡ <strong>Ajustes:</strong> Velocidade normal, Pausas 250ms</div>
                    <div>⏱️ <strong>Duração:</strong> 1m 14s (74s) • 160 kbps MP3</div>
                </div>
                <audio controls src="Podcasts_Tematicos/Thalita_e_Francisca/Podcast_Item_2_1_Plano_de_Manutencao_e_Calibracao.mp3"></audio>
            </div>
        </div>

        <div class="dialogue-box">
            <div class="dialogue-title">📜 Roteiro Falado no Trecho:</div>
            <div class="turn">
                <span class="turn-speaker speaker-host">Apresentadora:</span>
                <span>"Gente, vamos começar falando de uma das maiores dores de cabeça nos laboratórios: o controle de calibração e manutenção! O instrutor do curso trouxe uma visão super prática sobre isso no item 2.1."</span>
            </div>
            <div class="turn">
                <span class="turn-speaker speaker-guest">Especialista:</span>
                <span>"Excelente ponto! E convenhamos, o pessoal adora complicar isso, né? Já vi laboratório mantendo três controles completamente separados pra mesma máquina! O que o instrutor defendeu aqui foi direto ao ponto: não precisa inventar moda! Calibração, verificação intermediária e manutenção preventiva podem sim estar integradas no mesmo plano geral!"</span>
            </div>
            <div class="turn">
                <span class="turn-speaker speaker-host">Apresentadora:</span>
                <span>"Nossa, isso facilita demais a vida! Mas me diz uma coisa: e o avaliador da Cgcre, aceita isso numa boa? A norma não exige formulários separados?"</span>
            </div>
            <div class="turn">
                <span class="turn-speaker speaker-guest">Especialista:</span>
                <span>"Aceita sim, com ressalva! Os requisitos 6.4.3 e 6.4.13 da ISO 17025 exigem que o plano exista e esteja sob controle rastreável! A força da evidência tá na rastreabilidade e no cumprimento das datas, e não na quantidade de planilhas que você inventou!"</span>
            </div>
            <div class="turn">
                <span class="turn-speaker speaker-host">Apresentadora:</span>
                <span>"Perfeito! Menos burocracia de gaveta e muito mais controle real do que realmente precisa ser feito no mês!"</span>
            </div>
        </div>
    </div>
</body>
</html>"""

with open("Comparador_Audio_EdgeTTS_vs_ElevenLabs.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Comparador_Audio_EdgeTTS_vs_ElevenLabs.html atualizado!")
