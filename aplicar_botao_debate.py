import json

# 1. Load catalog and build dictionary of debate URLs for each (day, sec_num)
cat = json.load(open("catalogo_geral_podcasts.json", encoding="utf-8"))
data = json.load(open("dados_interativos.json", encoding="utf-8"))

podcasts = []
for section, items in cat.items():
    part_day = "02/09" if "Parte 1" in section else ("03/09" if "Parte 2" in section else "04/09")
    part_folder = "" if part_day == "02/09" else ("Parte_2/" if part_day == "03/09" else "Parte_3/")
    base_rel = "Podcasts_Tematicos/Thalita_e_Francisca/" + part_folder
    for it in items:
        podcasts.append({
            "day": part_day,
            "filename": it["filename"],
            "url": base_rel + it["filename"],
            "is_full": it["is_full_chapter"]
        })

def get_best_podcast(day, sec_num, title):
    parts = str(sec_num).split(".")
    # 1. Direct Item_X_Y
    if len(parts) >= 2:
        pat = f"Item_{parts[0]}_{parts[1]}_"
        for p in podcasts:
            if p["day"] == day and pat in p["filename"]:
                return p["url"]

    # 2. Specific chapter matches
    try:
        c = int(parts[0])
        for p in podcasts:
            if p["day"] == day and (f"Capitulo_{c}_" in p["filename"] or f"Capitulos_{c}_" in p["filename"]):
                return p["url"]
    except:
        pass

    # 3. Special Dia 02
    if day == "02/09":
        try:
            c = int(parts[0])
            if c in [12, 14, 15]:
                for p in podcasts:
                    if p["day"] == day and "Capitulo_12" in p["filename"]:
                        return p["url"]
            if c in [13, 16, 17, 18, 19, 20]:
                for p in podcasts:
                    if p["day"] == day and "Capitulo_13" in p["filename"]:
                        return p["url"]
        except:
            pass

    # 4. Special Dia 03
    if day == "03/09":
        try:
            c = int(parts[0])
            if c in [10, 12, 13]:
                for p in podcasts:
                    if p["day"] == day and "Capitulo_10" in p["filename"]:
                        return p["url"]
            if c in [11, 14, 15, 16]:
                for p in podcasts:
                    if p["day"] == day and "Capitulo_11" in p["filename"]:
                        return p["url"]
        except:
            pass

    # 5. Special Dia 04
    if day == "04/09":
        try:
            c = int(parts[0])
            if c in [5, 6, 7]:
                for p in podcasts:
                    if p["day"] == day and "Capitulos_5_6_7" in p["filename"]:
                        return p["url"]
            if c in [8, 9, 10]:
                for p in podcasts:
                    if p["day"] == day and "Capitulos_8_9_10" in p["filename"]:
                        return p["url"]
            if c in [11, 14, 15, 16, 17]:
                for p in podcasts:
                    if p["day"] == day and "Capitulo_11" in p["filename"]:
                        return p["url"]
            if c in [12, 18, 19, 20, 21, 22, 23, 24]:
                for p in podcasts:
                    if p["day"] == day and "Capitulo_12" in p["filename"]:
                        return p["url"]
        except:
            pass

    for p in podcasts:
        if p["day"] == day and p["is_full"]:
            return p["url"]

    return None

debate_map = {}
for it in data:
    d = it.get("day", "")
    sec = str(it.get("sec_num", ""))
    u = get_best_podcast(d, sec, it.get("title", ""))
    debate_map[f"{d}_{sec}"] = u

print(f"Mapeamento de debate gerado: {len(debate_map)} itens")

# 2. Read existing player_interativo.html
with open("player_interativo.html", "r", encoding="utf-8") as f:
    content = f.read()

# CSS to inject
css_injection = """
        /* Botão e Estado de Reprodução de Debate Técnico (Thalita & Francisca) */
        .debate-btn {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            border: 1px solid #6366f1;
            padding: 5px 11px;
            border-radius: 5px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            box-shadow: 0 1px 3px rgba(79, 70, 229, 0.25);
            transition: all 0.15s ease;
        }
        .debate-btn:hover {
            background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
            transform: translateY(-1px);
            box-shadow: 0 3px 8px rgba(79, 70, 229, 0.35);
        }
        .debate-btn.is-playing {
            background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
            border-color: #34d399 !important;
            color: #ffffff !important;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.5) !important;
        }
        .item-card.playing-debate {
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.3), 0 8px 20px -4px rgba(124, 58, 237, 0.2) !important;
        }
"""

if ".debate-btn" not in content:
    content = content.replace(".norma-btn:hover {", css_injection + "\n        .norma-btn:hover {")

# Header link to podcast player
header_link = '<a href="Player_Podcasts_Thalita_e_Francisca.html" target="_blank" class="pdf-btn" style="background: linear-gradient(135deg, #6366f1, #a855f7); color: white; border: none; font-weight: 700;" title="Abrir a Estação Dedicada de Podcasts com busca e velocidade">🎙️ Podcasts (154 Faixas)</a>'
if "Player_Podcasts_Thalita_e_Francisca.html" not in content:
    content = content.replace('<div class="pdf-links">', '<div class="pdf-links">\n                    ' + header_link)

# Inject debateMap into JavaScript
js_map = f"        const debateMap = {json.dumps(debate_map, ensure_ascii=False)};\n        let isDebatePlaying = false;\n"
if "const debateMap =" not in content:
    content = content.replace("const audioPaths = {", js_map + "\n        const audioPaths = {")

# Inject playDebate function and update stopAudio
play_debate_fn = """
        // Função para Tocar o Debate Técnico do Item (Thalita & Francisca)
        function playDebate(day, secNum, cardId, btn = null) {
            const key = `${day}_${secNum}`;
            const debateUrl = debateMap[key];
            if (!debateUrl) {
                alert("Debate não disponível para este item específico.");
                return;
            }

            const currentCard = document.getElementById(cardId);

            // Toggle pause/play se já estiver tocando este mesmo debate
            if (activeCardId === cardId && isDebatePlaying && !player.paused) {
                player.pause();
                return;
            }

            if (activeCardId) {
                const prev = document.getElementById(activeCardId);
                if (prev) {
                    prev.classList.remove('playing');
                    prev.classList.remove('playing-debate');
                }
            }

            document.querySelectorAll('.debate-btn').forEach(b => {
                b.innerHTML = '🎙️ Debate (Thalita & Francisca)';
                b.classList.remove('is-playing');
            });

            activeCardId = cardId;
            isDebatePlaying = true;
            if (currentCard) {
                currentCard.classList.add('playing');
                currentCard.classList.add('playing-debate');
            }

            if (btn) {
                btn.innerHTML = '⏸️ Ouvindo Debate...';
                btn.classList.add('is-playing');
            }

            trackBadge.textContent = 'DEBATE';
            trackBadge.style.background = 'linear-gradient(135deg, #7c3aed, #4f46e5)';
            trackName.textContent = `🎙️ Debate Especialista: Item ${secNum} (Thalita & Francisca)`;

            const fullSrc = getAudioPrefix() + debateUrl;
            if (!audioSource.src.endsWith(debateUrl)) {
                audioSource.src = fullSrc;
                player.load();
            }
            player.currentTime = 0;
            player.play();
        }
"""

if "function playDebate" not in content:
    content = content.replace("// Função para Parar a Reprodução de Áudio", play_debate_fn + "\n        // Função para Parar a Reprodução de Áudio")

# Modify stopAudio to clean up debate states
old_stop_audio = """        function stopAudio(cardId = null) {
            player.pause();
            if (activeCardId) {
                const prev = document.getElementById(activeCardId);
                if (prev) prev.classList.remove('playing');
                activeCardId = null;
            }
        }"""

new_stop_audio = """        function stopAudio(cardId = null) {
            player.pause();
            if (activeCardId) {
                const prev = document.getElementById(activeCardId);
                if (prev) {
                    prev.classList.remove('playing');
                    prev.classList.remove('playing-debate');
                }
                activeCardId = null;
            }
            isDebatePlaying = false;
            document.querySelectorAll('.debate-btn').forEach(b => {
                b.innerHTML = '🎙️ Debate (Thalita & Francisca)';
                b.classList.remove('is-playing');
            });
        }"""

content = content.replace(old_stop_audio, new_stop_audio)

# Update pause listener to also reset debate buttons
old_pause_listener = """        player.addEventListener('pause', () => {
            if (activeCardId) {
                const cur = document.getElementById(activeCardId);
                if (cur) cur.classList.remove('playing');
            }
        });"""

new_pause_listener = """        player.addEventListener('pause', () => {
            if (activeCardId) {
                const cur = document.getElementById(activeCardId);
                if (cur) {
                    cur.classList.remove('playing');
                    cur.classList.remove('playing-debate');
                }
            }
            document.querySelectorAll('.debate-btn').forEach(b => {
                b.innerHTML = '🎙️ Debate (Thalita & Francisca)';
                b.classList.remove('is-playing');
            });
        });"""

content = content.replace(old_pause_listener, new_pause_listener)

# Now update renderCards to include the debate button on EVERY card
old_render_card_block = """                let quoteHtml = '';
                if (item.quote) {
                    quoteHtml = `
                        <div class="quote-box" onclick="playTrecho('${item.day}', ${item.timestamp}, '${item.cardId}')" title="Clique para ouvir este exato momento no áudio">
                            <div class="quote-header-line">
                                <span>💬 ${item.quote_header || 'Trecho da Gravação'}</span>
                                <span>⏱️ ${item.timestamp_str}</span>
                            </div>
                            <div class="quote-text">“${item.quote}”</div>
                            <div class="card-actions-row">
                                <button class="quote-btn" onclick="event.stopPropagation(); playTrecho('${item.day}', ${item.timestamp}, '${item.cardId}')">
                                    ▶️ Ouvir no Áudio (${item.timestamp_str})
                                </button>
                                <button class="stop-btn" onclick="event.stopPropagation(); stopAudio('${item.cardId}')" title="Parar reprodução de áudio imediatamente">
                                    ⏹️ Parar
                                </button>
                                <button class="norma-btn" onclick="event.stopPropagation(); openNormaViewer(${normaPage})">
                                    📖 Ver na Norma (Pág. ${normaPage}${normaClause})
                                </button>
                            </div>
                        </div>
                    `;
                }"""

new_render_card_block = """                const debateUrl = debateMap[`${item.day}_${item.sec_num}`] || '';
                const debateBtnHtml = debateUrl ? `
                    <button class="debate-btn" id="debate-btn-${item.cardId}" onclick="event.stopPropagation(); playDebate('${item.day}', '${item.sec_num}', '${item.cardId}', this)" title="Ouvir o debate técnico deste item com Thalita e Francisca">
                        🎙️ Debate (Thalita & Francisca)
                    </button>
                ` : '';

                const actionsRowHtml = `
                    <div class="card-actions-row">
                        ${item.timestamp ? `<button class="quote-btn" onclick="event.stopPropagation(); playTrecho('${item.day}', ${item.timestamp}, '${item.cardId}')">▶️ Ouvir no Áudio (${item.timestamp_str})</button>` : ''}
                        ${debateBtnHtml}
                        <button class="stop-btn" onclick="event.stopPropagation(); stopAudio('${item.cardId}')" title="Parar reprodução de áudio imediatamente">⏹️ Parar</button>
                        <button class="norma-btn" onclick="event.stopPropagation(); openNormaViewer(${normaPage})">📖 Ver na Norma (Pág. ${normaPage}${normaClause})</button>
                    </div>
                `;

                let quoteHtml = '';
                if (item.quote) {
                    quoteHtml = `
                        <div class="quote-box" onclick="playTrecho('${item.day}', ${item.timestamp}, '${item.cardId}')" title="Clique para ouvir este exato momento no áudio original">
                            <div class="quote-header-line">
                                <span>💬 ${item.quote_header || 'Trecho da Gravação'}</span>
                                <span>⏱️ ${item.timestamp_str}</span>
                            </div>
                            <div class="quote-text">“${item.quote}”</div>
                            ${actionsRowHtml}
                        </div>
                    `;
                } else {
                    quoteHtml = actionsRowHtml;
                }"""

content = content.replace(old_render_card_block, new_render_card_block)

# Also update playTrecho to reset isDebatePlaying and reset debate buttons
old_play_trecho_start = """            activeCardId = cardId;
            const currentCard = document.getElementById(cardId);
            if (currentCard) currentCard.classList.add('playing');"""

new_play_trecho_start = """            activeCardId = cardId;
            isDebatePlaying = false;
            document.querySelectorAll('.debate-btn').forEach(b => {
                b.innerHTML = '🎙️ Debate (Thalita & Francisca)';
                b.classList.remove('is-playing');
            });
            const currentCard = document.getElementById(cardId);
            if (currentCard) {
                currentCard.classList.add('playing');
                currentCard.classList.remove('playing-debate');
            }"""

content = content.replace(old_play_trecho_start, new_play_trecho_start)

# Write back to player_interativo.html
with open("player_interativo.html", "w", encoding="utf-8") as f:
    f.write(content)

print("player_interativo.html atualizado com sucesso!")
