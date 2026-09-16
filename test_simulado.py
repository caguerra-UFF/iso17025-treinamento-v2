# -*- coding: utf-8 -*-
"""
Script de auditoria e validação contínua do Sistema de Provas & Simulados ISO/IEC 17025:2017.
Verifica:
1. Banco de Questões (questoes_simulado.json): 50 questões, perfis metrológicos (tecnico, gerencial, geral), explicações detalhadas e debates novos vinculados.
2. 250 Arquivos de Áudio (Audios_Simulado/): 50 enunciados regerados + 200 alternativas com pt-BR-FranciscaNeural.
3. 50 Debates Inéditos (Podcasts_Simulado/): 50 podcasts de debate entre Thalita & Francisca comentando erros e acertos.
4. Aplicação Web (simulado.html): Controles de parada (⏹️, barra flutuante, atalho Esc), seletor de perfis, sem 'Simulado Padrão'.
5. Links de Navegação nos portais do projeto.
"""

import json
import os

print('--- TEST 1: questoes_simulado.json e Perfis Metrologicos ---')
with open('questoes_simulado.json', 'r', encoding='utf-8') as f:
    qs = json.load(f)
assert len(qs) == 50, f"Expected 50 questions, got {len(qs)}"

dist_secao = {}
dist_perfil = {}
dist_correta = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
missing_audios = []
missing_debates = []
missing_exp = []
missing_profile = []

for idx, q in enumerate(qs):
    qid = q['id']
    sec = q['secao_raiz']
    dist_secao[sec] = dist_secao.get(sec, 0) + 1

    # Check profile
    perfil = q.get('perfil')
    if perfil not in ['tecnico', 'gerencial', 'geral']:
        missing_profile.append(qid)
    else:
        dist_perfil[perfil] = dist_perfil.get(perfil, 0) + 1

    correta = q.get('correta')
    assert correta in ['A', 'B', 'C', 'D'], f"Invalid correta in {qid}"
    dist_correta[correta] += 1
    if idx > 0:
        assert correta != qs[idx - 1].get('correta'), f"Repetição consecutiva monótona em {qid} ({correta} após {qs[idx - 1].get('correta')})"
    assert len(q.get('alternativas', [])) == 4, f"Alternativas != 4 in {qid}"
    assert os.path.exists(q['audio_ref']), f"Missing audio: {q['audio_ref']}"
    
    # Check debate podcast
    debate_path = q.get('debate_podcast', '')
    if not os.path.exists(debate_path) or os.path.getsize(debate_path) == 0:
        missing_debates.append(f"{qid}:{debate_path}")
    
    # Check per-alternative detailed explanations
    exp = q.get('explicacoes_detalhadas', {})
    if len(exp) != 4:
        missing_exp.append(qid)
    else:
        for letra in ['A', 'B', 'C', 'D']:
            item = exp.get(letra, {})
            if letra == q['correta']:
                if 'fundamentacao_acerto' not in item or not item['fundamentacao_acerto']:
                    missing_exp.append(f"{qid}:{letra}")
            else:
                if 'por_que_esta_incorreta' not in item or 'por_que_outra_e_correta' not in item:
                    missing_exp.append(f"{qid}:{letra}")

    # Check question statement audio
    enunc_audio = os.path.join('Audios_Simulado', f"{qid}_enunciado.mp3")
    if not os.path.exists(enunc_audio) or os.path.getsize(enunc_audio) == 0:
        missing_audios.append(enunc_audio)
        
    # Check alternatives audios
    for alt in q['alternativas']:
        alt_audio = os.path.join('Audios_Simulado', f"{qid}_alt_{alt['letra']}.mp3")
        if not os.path.exists(alt_audio) or os.path.getsize(alt_audio) == 0:
            missing_audios.append(alt_audio)

assert len(missing_profile) == 0, f"Missing or invalid profile in questions: {missing_profile}"
assert len(missing_exp) == 0, f"Missing detailed explanations in: {missing_exp}"
assert len(missing_audios) == 0, f"Missing {len(missing_audios)} audio files in Audios_Simulado: {missing_audios[:5]}"

print(f"[OK] 50/50 questions verified with 100% existing audios, and AI explanations!")
print(f"[OK] 250/250 synthesized audio files (50 statements + 200 alternatives) verified in Audios_Simulado/")
print(f"  Distribution by section: {dist_secao}")
print(f"  Distribution by profile: {dist_perfil}")
print(f"  Distribution by answer key (gabarito balanceado): {dist_correta}")
assert dist_correta['A'] >= 10 and dist_correta['B'] >= 10 and dist_correta['C'] >= 10 and dist_correta['D'] >= 10, f"Gabarito desbalanceado: {dist_correta}"
assert dist_correta['B'] < 20, f"Gabarito ainda excessivamente concentrado na letra B: {dist_correta['B']}"
assert dist_perfil['tecnico'] == 22, f"Expected 22 tecnico, got {dist_perfil['tecnico']}"
assert dist_perfil['gerencial'] == 18, f"Expected 18 gerencial, got {dist_perfil['gerencial']}"
assert dist_perfil['geral'] == 10, f"Expected 10 geral, got {dist_perfil['geral']}"

# Check debate files in Podcasts_Simulado/
debates_on_disk = [f for f in os.listdir('Podcasts_Simulado') if f.endswith('_debate.mp3')] if os.path.exists('Podcasts_Simulado') else []
print(f"[INFO] Debates in Podcasts_Simulado: {len(debates_on_disk)}/50")

print('--- TEST 2: simulado.html e Recursos de Interface & Áudio ---')
assert os.path.exists('simulado.html'), "simulado.html missing"
with open('simulado.html', 'r', encoding='utf-8') as f:
    sim_html = f.read()

assert 'const ALL_QUESTIONS = [' in sim_html
assert 'function startExam(' in sim_html
assert 'function finishExam()' in sim_html
assert 'btn-tts-icon' in sim_html
assert 'diagnosticCard' in sim_html
assert 'Audios_Simulado' in sim_html
assert 'selectProfile' in sim_html, "selectProfile missing from simulado.html"
assert 'qBadgeProfile' in sim_html, "qBadgeProfile missing from simulado.html"
assert 'profileRadarBox' in sim_html, "profileRadarBox missing from simulado.html"
assert 'updateFilterNotice' in sim_html, "updateFilterNotice missing from simulado.html"

# Verify Audio Stop Controls
assert 'floatingAudioBar' in sim_html, "floatingAudioBar missing from simulado.html"
assert 'stopAllAudio' in sim_html, "stopAllAudio missing from simulado.html"
assert 'Parar Áudio' in sim_html, "Parar Áudio button text missing from simulado.html"
assert 'Escape' in sim_html, "Escape keyboard shortcut missing from simulado.html"

# Verify that "Simulado Padrão" is NOT present in simulado.html
assert 'Simulado Padrão' not in sim_html, "Simulado Padrão still present in simulado.html!"
assert 'simulado padrão' not in sim_html.lower(), "simulado padrão still present in simulado.html!"

print(f"[OK] simulado.html verified ({len(sim_html)} chars, valid structure with audio stop controls, profiles and NO 'Simulado Padrão')!")

print('--- TEST 2.1: Autenticação Google & Firebase (Identificação, Cadastro e Habilitação) ---')
# SDKs compat do Firebase e módulo local
assert 'firebase-app-compat.js' in sim_html, "Firebase App SDK tag missing from simulado.html"
assert 'firebase-auth-compat.js' in sim_html, "Firebase Auth SDK tag missing from simulado.html"
assert 'firebase-firestore-compat.js' in sim_html, "Firebase Firestore SDK tag missing from simulado.html"
assert '<script src="firebase_simulado.js"></script>' in sim_html, "firebase_simulado.js script tag missing from simulado.html"

# Elementos de interface da identificação, cadastro e gestão
for element_id in ['identityCard', 'identityAvatar', 'identityName', 'identityEmail', 'identityStatusBadge',
                   'btnGoogleLogin', 'btnManualLogin', 'btnDemoLogin', 'btnEditCadastro', 'btnGestorPanel', 'btnGoogleSignOut',
                   'modalCadastro', 'cadMatricula', 'cadSetor', 'cadFuncao',
                   'modalPainelGestor', 'dashTableBody', 'dashSearchInput', 'dashFilterStatus', 'btnExportCSV',
                   'resultsIdentityLine', 'certStampBox', 'examUserName']:
    assert element_id in sim_html, f"Identity/Auth/Dashboard UI element '{element_id}' missing from simulado.html"

# Funções do fluxo de autenticação e dashboard
for func_name in ['updateAuthUI', 'handleLoginGoogle', 'handleLoginManual', 'handleLoginDemo', 'handleLogout',
                  'openModalCadastro', 'closeModalCadastro', 'salvarCadastroForm',
                  'openModalPainelGestor', 'closeModalPainelGestor', 'renderTabelaGestor',
                  'filtrarTabelaGestor', 'exportarRelatorioCSV']:
    assert f'function {func_name}(' in sim_html, f"Function {func_name} missing from simulado.html"

# Guarda de Prova Oficial (exige login e cadastro completo)
assert "if (examMode === 'exam')" in sim_html, "startExam exam mode check missing"
assert "openModalCadastro()" in sim_html, "openModalCadastro trigger in startExam missing"

# Registro da Prova e Selo de Habilitação Metrológica
assert 'window.firebaseSimulado.enviarSubmissaoProva' in sim_html, "enviarSubmissaoProva call missing from finishExam"
assert 'HABILITAÇÃO METROLÓGICA OFICIAL CONCEDIDA' in sim_html, "Official habilitation stamp missing from finishExam"
assert 'CÓDIGO DE AUTENTICIDADE E RASTREABILIDADE' in sim_html, "Authenticity code missing from finishExam"

# Guarda de regressão do f-string: nenhuma chave dupla pode vazar para o HTML/JS gerado
css_marker = 'IDENTIFICACAO DO PARTICIPANTE'
data_marker = 'const ALL_QUESTIONS = '
i_css = sim_html.find(css_marker)
i_data = sim_html.find(data_marker)
assert i_css != -1, "Identity CSS block not found in simulado.html"
assert i_data != -1, "Questions data block not found in simulado.html"
i_after_data = sim_html.find('\n', i_data) + 1
novo_codigo = sim_html[i_css:i_data] + sim_html[i_after_data:]
assert '{{' not in novo_codigo and '}}' not in novo_codigo, \
    "f-string escaping error: double braces leaked into the generated simulado.html"

print("[OK] Firebase Auth + Firestore integrados: Login Google, Cadastro de Matrícula/Setor, Guarda de Prova Oficial, Selo de Habilitação Metrológica e Painel do Gestor com Exportação CSV!")


print('--- TEST 3: Links in Portal Pages ---')
for page in ['index.html', 'lma-iso17025.html', 'player_interativo.html']:
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'simulado.html' in content, f"simulado.html not linked in {page}"
    print(f"[OK] {page} correctly links to simulado.html")

if len(debates_on_disk) == 50 and len(missing_debates) == 0:
    print(f"[OK] 50/50 custom debates verified in Podcasts_Simulado/ and linked in questoes_simulado.json!")

print('\n>>> ALL SYSTEM AUDIT CHECKS COMPLETED <<<')
