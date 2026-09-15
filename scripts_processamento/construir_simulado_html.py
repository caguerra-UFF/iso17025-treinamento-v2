# -*- coding: utf-8 -*-
"""
Construtor avançado do Simulado & Provas ISO/IEC 17025:2017.
Inclui:
- Divisão dos tipos de questões por perfis: Corpo Técnico, Corpo Gerencial e Geral / Institucional.
- Filtro dinâmico por Perfil com feedback em tempo real da quantidade de questões disponíveis.
- Seletor de quantidade sem o rótulo "Simulado Padrão".
- Manutenção dos filtros de Seção da Norma (4 a 8) e Modos de Avaliação (Estudo vs Prova Oficial).
- Ícone 🔊 após o enunciado e após cada alternativa para síntese de voz (pt-BR-FranciscaNeural).
- CONTROLE COMPLETO DE PARADA:
  * O ícone alterna para ⏹️ durante a reprodução, permitindo parar ao clicar nele novamente.
  * Barra flutuante inferior com botão em destaque [⏹️ Parar Áudio].
  * Atalho de teclado 'Escape' para interromper o áudio instantaneamente.
- Diagnóstico inédito e aprofundado para CADA erro e acerto por alternativa.
- 50 novos podcasts de debate entre Thalita e Francisca específicos para cada questão.
- Painel de desempenho duplo nos resultados: por Cláusula Normativa e por Perfil Profissional.
"""

import json

with open('questoes_simulado.json', 'r', encoding='utf-8') as f:
    questoes = json.load(f)

json_str = json.dumps(questoes, ensure_ascii=False)

html_template = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulado & Provas Interativas | ISO/IEC 17025:2017</title>
    <style>
        :root {{
            --primary: #0f4c81;
            --primary-dark: #092c4d;
            --primary-light: #e8f0fe;
            --accent: #2563eb;
            --accent-hover: #1d4ed8;
            --success: #16a34a;
            --success-light: #dcfce7;
            --warning: #d97706;
            --warning-light: #fef3c7;
            --danger: #dc2626;
            --danger-light: #fee2e2;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --border-dark: #cbd5e1;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
            --shadow: 0 4px 6px -1px rgba(0,0,0,0.08), 0 2px 4px -2px rgba(0,0,0,0.06);
            --shadow-lg: 0 10px 25px -5px rgba(0,0,0,0.12), 0 8px 10px -6px rgba(0,0,0,0.08);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        /* Header Superior */
        header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 14px 24px;
            box-shadow: var(--shadow);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .header-wrap {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .header-title {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .header-title h1 {{
            font-size: 19px;
            font-weight: 700;
            letter-spacing: -0.3px;
        }}
        .header-title p {{
            font-size: 12px;
            color: #cbd5e1;
        }}
        .header-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .btn-header {{
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            text-decoration: none;
            padding: 7px 14px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .btn-header:hover {{
            background: rgba(255, 255, 255, 0.28);
            border-color: rgba(255, 255, 255, 0.5);
            transform: translateY(-1px);
        }}

        /* Container Principal */
        main {{
            max-width: 1100px;
            width: 100%;
            margin: 24px auto;
            padding: 0 16px;
            flex: 1;
        }}

        /* Views */
        .view-section {{
            display: none;
        }}
        .view-section.active {{
            display: block;
            animation: fadeIn 0.25s ease;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* ====================================================================
           ÍCONE DE ÁUDIO TTS (APENAS O ÍCONE) E CONTROLES DE STOP
           ==================================================================== */
        .btn-tts-icon {{
            background: #f1f5f9;
            border: 1px solid var(--border-dark);
            color: var(--primary);
            width: 28px;
            height: 28px;
            border-radius: 50%;
            font-size: 13px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            margin-left: 8px;
            vertical-align: middle;
            flex-shrink: 0;
            box-shadow: var(--shadow-sm);
            line-height: 1;
        }}
        .btn-tts-icon:hover {{
            background: #e0e7ff;
            border-color: #6366f1;
            color: #4f46e5;
            transform: scale(1.12);
        }}
        .btn-tts-icon.is-playing {{
            background: #fee2e2;
            border-color: #ef4444;
            color: #b91c1c;
            animation: audioPulseStop 0.9s infinite alternate;
        }}
        @keyframes audioPulseStop {{
            0% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.5); }}
            100% {{ transform: scale(1.18); box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }}
        }}

        /* Barra Flutuante de Controle e Parada de Áudio */
        .floating-audio-bar {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(8px);
            color: white;
            padding: 10px 18px;
            border-radius: 50px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            display: flex;
            align-items: center;
            gap: 14px;
            z-index: 1000;
            animation: slideUp 0.25s ease;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        @keyframes slideUp {{
            from {{ transform: translateY(20px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        .floating-audio-info {{
            display: flex;
            align-items: center;
            gap: 8px;
            max-width: 320px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-size: 13px;
            font-weight: 600;
        }}
        .btn-stop-audio {{
            background: #ef4444;
            color: white;
            border: none;
            padding: 7px 16px;
            border-radius: 30px;
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
        }}
        .btn-stop-audio:hover {{
            background: #dc2626;
            transform: scale(1.06);
        }}

        /* ====================================================================
           TELA 1: CONFIGURAÇÃO DO SIMULADO
           ==================================================================== */
        .config-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            box-shadow: var(--shadow);
            padding: 32px;
            margin-bottom: 24px;
        }}
        .config-title {{
            font-size: 22px;
            font-weight: 800;
            color: var(--primary-dark);
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .config-desc {{
            color: var(--text-muted);
            font-size: 14px;
            margin-bottom: 24px;
            line-height: 1.6;
        }}

        .config-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 18px;
            margin-bottom: 20px;
        }}
        .config-group {{
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px 18px;
        }}
        .config-group label.group-title {{
            font-size: 12.5px;
            font-weight: 700;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: block;
            margin-bottom: 10px;
        }}

        .option-radio {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .radio-card {{
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 9px 10px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: white;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .radio-card:hover {{
            border-color: var(--accent);
            background: #f0f7ff;
        }}
        .radio-card input[type="radio"] {{
            margin-top: 3px;
            cursor: pointer;
        }}
        .radio-info strong {{
            display: block;
            font-size: 13px;
            color: var(--text-main);
        }}
        .radio-info span {{
            font-size: 11.5px;
            color: var(--text-muted);
            line-height: 1.3;
        }}

        .select-custom {{
            width: 100%;
            padding: 10px 12px;
            border: 1px solid var(--border-dark);
            border-radius: 8px;
            font-size: 13.5px;
            background: white;
            color: var(--text-main);
            outline: none;
            cursor: pointer;
        }}
        .select-custom:focus {{
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }}

        /* Banner Informativo de Filtro */
        .filter-summary-card {{
            background: #eef2ff;
            border: 1px solid #c7d2fe;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            font-size: 13.5px;
            color: #1e40af;
        }}
        .filter-summary-card strong {{
            font-weight: 800;
        }}
        .badge-count-avail {{
            background: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 800;
            font-size: 12px;
            border: 1px solid #c7d2fe;
            color: var(--primary);
            box-shadow: var(--shadow-sm);
        }}

        .btn-start-exam {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            border: none;
            padding: 16px 32px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            width: 100%;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        .btn-start-exam:hover {{
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
        }}

        /* Histórico de Desempenho */
        .stats-summary-card {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            box-shadow: var(--shadow-sm);
            display: flex;
            justify-content: space-around;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .stat-item {{
            text-align: center;
        }}
        .stat-val {{
            font-size: 24px;
            font-weight: 800;
            color: var(--primary);
        }}
        .stat-lbl {{
            font-size: 11.5px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }}

        /* ====================================================================
           TELA 2: AMBIENTE DO EXAME
           ==================================================================== */
        .exam-header-bar {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px 20px;
            margin-bottom: 16px;
            box-shadow: var(--shadow-sm);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .exam-status-info {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}
        .timer-badge {{
            background: #f1f5f9;
            color: var(--primary-dark);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border: 1px solid var(--border);
        }}
        .timer-badge.urgent {{
            background: var(--danger-light);
            color: var(--danger);
            border-color: #fca5a5;
            animation: pulse 1s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}

        .progress-bar-wrap {{
            flex: 1;
            max-width: 320px;
            margin: 0 16px;
        }}
        .progress-bar-bg {{
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
        }}
        .progress-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #2563eb, #16a34a);
            width: 0%;
            transition: width 0.3s ease;
        }}
        .progress-label {{
            font-size: 11.5px;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            margin-top: 4px;
        }}

        /* Grade de Navegação das Questões */
        .question-nav-grid {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            box-shadow: var(--shadow-sm);
        }}
        .q-nav-btn {{
            width: 34px;
            height: 34px;
            border-radius: 6px;
            border: 1px solid var(--border-dark);
            background: #f8fafc;
            color: var(--text-main);
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}
        .q-nav-btn:hover {{
            background: #e2e8f0;
            transform: scale(1.05);
        }}
        .q-nav-btn.active {{
            border-color: var(--accent);
            outline: 2px solid var(--accent);
            outline-offset: 1px;
            font-weight: 800;
        }}
        .q-nav-btn.answered {{
            background: #dbeafe;
            border-color: #93c5fd;
            color: #1e40af;
        }}
        .q-nav-btn.flagged::after {{
            content: "🚩";
            position: absolute;
            top: -6px;
            right: -6px;
            font-size: 10px;
        }}
        .q-nav-btn.correct-study {{
            background: #dcfce7;
            border-color: #86efac;
            color: #166534;
        }}
        .q-nav-btn.incorrect-study {{
            background: #fee2e2;
            border-color: #fca5a5;
            color: #991b1b;
        }}

        /* Card da Questão Ativa */
        .question-box {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 28px 32px;
            box-shadow: var(--shadow);
            margin-bottom: 24px;
        }}
        .q-meta-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .q-badges {{
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
        }}

        /* Badges de Perfil */
        .badge-profile {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            padding: 3px 9px;
            border-radius: 6px;
        }}
        .badge-profile-tecnico {{
            background: #e0f2fe;
            color: #0369a1;
            border: 1px solid #bae6fd;
        }}
        .badge-profile-gerencial {{
            background: #f3e8ff;
            color: #7e22ce;
            border: 1px solid #e9d5ff;
        }}
        .badge-profile-geral {{
            background: #ecfdf5;
            color: #047857;
            border: 1px solid #a7f3d0;
        }}

        .badge-clause {{
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            color: #1d4ed8;
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
        }}
        .badge-level {{
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            color: #475569;
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }}
        .badge-theme {{
            background: #fef3c7;
            border: 1px solid #fde68a;
            color: #92400e;
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }}

        .btn-flag {{
            background: transparent;
            border: 1px solid var(--border-dark);
            color: var(--text-muted);
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s;
        }}
        .btn-flag:hover {{
            background: #fffbeb;
            color: #b45309;
            border-color: #fde68a;
        }}
        .btn-flag.active {{
            background: #fef3c7;
            color: #b45309;
            border-color: #f59e0b;
        }}
        .btn-debate-header {{
            background: #f5f3ff;
            border: 1px solid #ddd6fe;
            color: #6d28d9;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s;
        }}
        .btn-debate-header:hover {{
            background: #ede9fe;
            border-color: #8b5cf6;
            color: #5b21b6;
            transform: scale(1.03);
        }}
        .btn-debate-header.is-playing {{
            background: #fee2e2;
            border-color: #ef4444;
            color: #b91c1c;
            animation: audioPulseStop 0.9s infinite alternate;
        }}

        .q-statement-box {{
            font-size: 16px;
            font-weight: 600;
            line-height: 1.6;
            margin-bottom: 24px;
            color: var(--primary-dark);
            display: flex;
            align-items: flex-start;
            gap: 4px;
        }}
        .q-statement-text {{
            flex: 1;
        }}

        /* Alternativas */
        .alternatives-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }}
        .alt-card {{
            border: 1.5px solid var(--border);
            border-radius: 10px;
            padding: 14px 18px;
            background: #f8fafc;
            cursor: pointer;
            transition: all 0.15s;
            display: flex;
            align-items: flex-start;
            gap: 14px;
            position: relative;
        }}
        .alt-card:hover:not(.disabled) {{
            background: #f0f7ff;
            border-color: var(--accent);
            transform: translateX(2px);
        }}
        .alt-card.selected {{
            background: #eff6ff;
            border-color: var(--accent);
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
        }}
        .alt-letter {{
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: white;
            border: 1px solid var(--border-dark);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 13px;
            color: var(--text-muted);
            flex-shrink: 0;
            transition: all 0.15s;
        }}
        .alt-card.selected .alt-letter {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }}
        .alt-body {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            flex: 1;
        }}
        .alt-text {{
            font-size: 14.5px;
            color: var(--text-main);
            line-height: 1.5;
            flex: 1;
        }}

        /* Destaques de Acerto/Erro */
        .alt-card.correct-ans {{
            background: var(--success-light) !important;
            border-color: var(--success) !important;
        }}
        .alt-card.correct-ans .alt-letter {{
            background: var(--success) !important;
            color: white !important;
            border-color: var(--success) !important;
        }}
        .alt-card.wrong-ans {{
            background: var(--danger-light) !important;
            border-color: var(--danger) !important;
        }}
        .alt-card.wrong-ans .alt-letter {{
            background: var(--danger) !important;
            color: white !important;
            border-color: var(--danger) !important;
        }}

        /* ====================================================================
           PAINEL DE DIAGNÓSTICO DO ERRO / ACERTO (PERSONALIZADO POR ALTERNATIVA)
           ==================================================================== */
        .diagnostic-card {{
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            display: none;
            animation: fadeIn 0.25s ease;
            box-shadow: var(--shadow-sm);
        }}
        .diagnostic-card.show {{
            display: block;
        }}
        .diagnostic-card.is-correct {{
            background: #f0fdf4;
            border: 1px solid #86efac;
            border-left: 6px solid var(--success);
        }}
        .diagnostic-card.is-wrong {{
            background: #fef2f2;
            border: 1px solid #fca5a5;
            border-left: 6px solid var(--danger);
        }}
        .diag-title-row {{
            font-size: 14.5px;
            font-weight: 800;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .is-correct .diag-title-row {{
            color: var(--success);
        }}
        .is-wrong .diag-title-row {{
            color: var(--danger);
        }}

        .diag-section {{
            margin-bottom: 12px;
            background: white;
            padding: 12px 14px;
            border-radius: 8px;
            border: 1px solid rgba(0, 0, 0, 0.06);
        }}
        .diag-label {{
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .is-wrong .label-erro {{
            color: #b91c1c;
        }}
        .is-wrong .label-correta {{
            color: #15803d;
        }}
        .is-correct .label-acerto {{
            color: #15803d;
        }}
        .diag-text {{
            font-size: 13.5px;
            line-height: 1.55;
            color: #334155;
        }}

        .diag-actions {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 14px;
            padding-top: 12px;
            border-top: 1px dashed rgba(0, 0, 0, 0.12);
        }}
        .btn-feedback-audio {{
            background: white;
            border: 1px solid var(--border-dark);
            color: var(--primary);
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .btn-feedback-audio:hover {{
            background: var(--primary-light);
            border-color: var(--accent);
            color: var(--accent);
        }}

        /* Barra Inferior de Navegação */
        .exam-bottom-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .btn-nav {{
            background: white;
            border: 1px solid var(--border-dark);
            color: var(--text-main);
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .btn-nav:hover:not(:disabled) {{
            background: #f1f5f9;
            border-color: #94a3b8;
        }}
        .btn-nav:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .btn-finish-exam {{
            background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 2px 8px rgba(22, 163, 74, 0.3);
        }}
        .btn-finish-exam:hover {{
            background: #15803d;
            transform: translateY(-1px);
        }}

        /* ====================================================================
           TELA 3: RESULTADOS E DASHBOARD
           ==================================================================== */
        .results-hero {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 32px;
            text-align: center;
            box-shadow: var(--shadow);
            margin-bottom: 24px;
        }}
        .score-circle {{
            width: 130px;
            height: 130px;
            border-radius: 50%;
            margin: 0 auto 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: #f8fafc;
            border: 6px solid var(--border);
            box-shadow: var(--shadow-sm);
        }}
        .score-circle.passed {{
            border-color: var(--success);
            background: #f0fdf4;
        }}
        .score-circle.failed {{
            border-color: var(--danger);
            background: #fef2f2;
        }}
        .score-val {{
            font-size: 34px;
            font-weight: 900;
            line-height: 1;
        }}
        .score-circle.passed .score-val {{
            color: var(--success);
        }}
        .score-circle.failed .score-val {{
            color: var(--danger);
        }}
        .score-sub {{
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .results-title {{
            font-size: 24px;
            font-weight: 800;
            margin-bottom: 6px;
        }}
        .results-sub {{
            font-size: 14px;
            color: var(--text-muted);
            max-width: 600px;
            margin: 0 auto 24px;
            line-height: 1.5;
        }}

        .results-metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            max-width: 800px;
            margin: 0 auto 28px;
        }}
        .metric-box {{
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 14px;
            text-align: center;
        }}
        .metric-box strong {{
            display: block;
            font-size: 20px;
            font-weight: 800;
            color: var(--primary-dark);
        }}
        .metric-box span {{
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
        }}

        /* Radars de Desempenho */
        .section-radar-box {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-sm);
        }}
        .section-radar-title {{
            font-size: 16px;
            font-weight: 800;
            color: var(--primary-dark);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .radar-list {{
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}
        .radar-item-row {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}
        .radar-label {{
            width: 240px;
            font-size: 13px;
            font-weight: 700;
            color: var(--text-main);
            flex-shrink: 0;
        }}
        .radar-bar-bg {{
            flex: 1;
            height: 12px;
            background: #e2e8f0;
            border-radius: 6px;
            overflow: hidden;
        }}
        .radar-bar-fill {{
            height: 100%;
            border-radius: 6px;
            transition: width 0.5s ease;
        }}
        .radar-perc {{
            width: 90px;
            text-align: right;
            font-size: 13px;
            font-weight: 800;
            flex-shrink: 0;
        }}

        .results-actions-row {{
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 30px;
        }}
        .btn-action-primary {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14.5px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
            transition: all 0.2s;
        }}
        .btn-action-primary:hover {{
            background: #1d4ed8;
            transform: translateY(-1px);
        }}
        .btn-action-secondary {{
            background: white;
            color: var(--text-main);
            border: 1px solid var(--border-dark);
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14.5px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }}
        .btn-action-secondary:hover {{
            background: #f1f5f9;
            border-color: #94a3b8;
        }}

        /* Seção de Revisão das Questões */
        .review-filter-bar {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px 20px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .review-filter-buttons {{
            display: flex;
            gap: 8px;
        }}
        .btn-filter {{
            background: #f8fafc;
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .btn-filter.active {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }}

        .review-cards-list {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        .review-card {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            box-shadow: var(--shadow-sm);
        }}
        .review-card.status-correct {{
            border-left: 5px solid var(--success);
        }}
        .review-card.status-wrong {{
            border-left: 5px solid var(--danger);
        }}

        @media print {{
            header, .exam-header-bar, .question-nav-grid, .results-actions-row, .review-filter-bar, .btn-tts-icon, .floating-audio-bar {{
                display: none !important;
            }}
            body {{
                background: white;
            }}
            .results-hero, .section-radar-box, .review-card {{
                box-shadow: none !important;
                border: 1px solid #ccc !important;
            }}
        }}
    </style>
</head>
<body>

    <!-- Header Principal -->
    <header>
        <div class="header-wrap">
            <div class="header-title">
                <span style="font-size: 26px;">📝</span>
                <div>
                    <h1>Sistema de Provas & Simulados | ABNT NBR ISO/IEC 17025:2017</h1>
                    <p>Treinamento Especializado • Laboratórios da Eletronuclear • Perfis Técnico, Gerencial e Geral</p>
                </div>
            </div>
            <div class="header-actions">
                <a href="index.html" class="btn-header" title="Voltar à Estação de Estudos e Transcrições">
                    📘 Voltar ao Treinamento
                </a>
            </div>
        </div>
    </header>

    <main>
        <!-- ==================================================================
             TELA 1: CONFIGURAÇÃO DO SIMULADO
             ================================================================== -->
        <section id="viewConfig" class="view-section active">
            <div class="config-card">
                <div class="config-title">
                    <span>🎯</span> Configurar Avaliação Metrológica
                </div>
                <p class="config-desc">
                    Escolha o perfil profissional para direcionar o foco das questões (Corpo Técnico, Gerencial ou Geral), 
                    a seção da norma desejada, o modo de realização e a quantidade de perguntas.
                    Todas as questões contam com narração oficial por voz (ícone 🔊), controle de parada imediata (⏹️) e diagnóstico inédito por alternativa.
                </p>

                <div class="config-grid">
                    <!-- 1. Modo de Exame -->
                    <div class="config-group">
                        <label class="group-title">1. Modo de Avaliação</label>
                        <div class="option-radio">
                            <label class="radio-card">
                                <input type="radio" name="examMode" value="study" checked>
                                <div class="radio-info">
                                    <strong>Modo Estudo (Diagnóstico Imediato)</strong>
                                    <span>Ao marcar uma alternativa, você visualiza na hora o porquê daquele erro e por que a outra é a correta.</span>
                                </div>
                            </label>
                            <label class="radio-card">
                                <input type="radio" name="examMode" value="exam">
                                <div class="radio-info">
                                    <strong>Modo Prova Oficial (Cronometrado)</strong>
                                    <span>Simulação de avaliação com contagem regressiva e laudo com radar de competências ao final.</span>
                                </div>
                            </label>
                        </div>
                    </div>

                    <!-- 2. Perfil do Avaliado -->
                    <div class="config-group">
                        <label class="group-title">2. Perfil do Avaliado (Foco da Prova)</label>
                        <select id="selectProfile" class="select-custom" onchange="updateFilterNotice()">
                            <option value="all" selected>🌐 Todos os Perfis (Avaliação Global da Norma - 50 Questões)</option>
                            <option value="tecnico">🛠️ Corpo Técnico (Bancada, Equipamentos, Incerteza & Métodos)</option>
                            <option value="gerencial">👔 Corpo Gerencial (Liderança, Riscos, SGQ & Tomada de Decisão)</option>
                            <option value="geral">🌐 Geral / Institucional (Cultura da Qualidade, Sigilo & Diretrizes)</option>
                        </select>
                        <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 8px;">
                            Adapta as questões à sua atuação profissional na Eletronuclear.
                        </p>
                    </div>

                    <!-- 3. Seção da Norma -->
                    <div class="config-group">
                        <label class="group-title">3. Seção da Norma</label>
                        <select id="selectScope" class="select-custom" onchange="updateFilterNotice()">
                            <option value="all" selected>Todas as Seções (Cláusulas 4 a 8)</option>
                            <option value="4">Seção 4: Requisitos Gerais (4.1 Imparcialidade & 4.2 Confidencialidade)</option>
                            <option value="5">Seção 5: Requisitos de Estrutura (5.1 a 5.7)</option>
                            <option value="6">Seção 6: Requisitos de Recursos (Pessoal, Instalações, Calibração, Compras)</option>
                            <option value="7">Seção 7: Requisitos de Processos (Validação, Amostragem, Incerteza, PEP, Relatórios)</option>
                            <option value="8">Seção 8: Requisitos de Gestão (Opções A/B, Riscos, Ações Corretivas, Auditoria)</option>
                        </select>
                        <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 8px;">
                            Permite treinar uma cláusula específica da ABNT NBR ISO/IEC 17025.
                        </p>
                    </div>

                    <!-- 4. Quantidade de Questões -->
                    <div class="config-group">
                        <label class="group-title">4. Quantidade de Questões</label>
                        <select id="selectCount" class="select-custom" onchange="updateFilterNotice()">
                            <option value="10">10 Questões (Aprox. 15 min)</option>
                            <option value="20" selected>20 Questões (Aprox. 30 min)</option>
                            <option value="30">30 Questões (Aprox. 45 min)</option>
                            <option value="all">Todas as Questões Disponíveis no Filtro</option>
                        </select>
                        <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 8px;">
                            No Modo Prova, o tempo limite é proporcional (1,5 min por questão).
                        </p>
                    </div>
                </div>

                <!-- Banner Informativo de Filtro Dinâmico -->
                <div id="filterNoticeBox" class="filter-summary-card">
                    <span id="filterNoticeText">🔍 Carregando escopo...</span>
                    <span id="filterCountBadge" class="badge-count-avail">50 Questões Disponíveis</span>
                </div>

                <button class="btn-start-exam" onclick="startExam()">
                    <span>🚀</span> Iniciar Avaliação Agora
                </button>
            </div>

            <!-- Resumo Histórico de Tentativas -->
            <div class="stats-summary-card" id="userStatsCard">
                <div class="stat-item">
                    <div class="stat-val" id="statCompleted">0</div>
                    <div class="stat-lbl">Simulados Concluídos</div>
                </div>
                <div class="stat-item">
                    <div class="stat-val" id="statAvgScore">0%</div>
                    <div class="stat-lbl">Média de Acertos</div>
                </div>
                <div class="stat-item">
                    <div class="stat-val" id="statBestScore">0%</div>
                    <div class="stat-lbl">Melhor Nota</div>
                </div>
                <div class="stat-item">
                    <button class="btn-nav" style="padding: 6px 12px; font-size: 11px;" onclick="clearHistory()">
                        🗑️ Limpar Histórico
                    </button>
                </div>
            </div>
        </section>

        <!-- ==================================================================
             TELA 2: AMBIENTE DO EXAME
             ================================================================== -->
        <section id="viewExam" class="view-section">
            <!-- Barra Superior do Exame -->
            <div class="exam-header-bar">
                <div class="exam-status-info">
                    <div id="examTimerBadge" class="timer-badge">
                        <span>⏱️</span> <span id="timerDisplay">30:00</span>
                    </div>
                    <span id="examModeBadge" style="font-size: 12px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">
                        MODO ESTUDO
                    </span>
                </div>

                <div class="progress-bar-wrap">
                    <div class="progress-bar-bg">
                        <div id="progressBarFill" class="progress-bar-fill"></div>
                    </div>
                    <div class="progress-label">
                        <span id="progressText">Questão 1 de 20</span>
                        <span id="answeredCountText">0 respondidas</span>
                    </div>
                </div>

                <button class="btn-finish-exam" onclick="confirmFinishExam()">
                    <span>✓</span> Entregar Avaliação
                </button>
            </div>

            <!-- Grade Navegadora de Questões -->
            <div class="question-nav-grid" id="questionNavGrid">
                <!-- Preenchido via JavaScript -->
            </div>

            <!-- Card da Questão Ativa -->
            <div class="question-box">
                <div class="q-meta-row">
                    <div class="q-badges">
                        <span id="qBadgeProfile" class="badge-profile badge-profile-tecnico">🛠️ Corpo Técnico</span>
                        <span id="qBadgeClause" class="badge-clause">Requisito 7.8</span>
                        <span id="qBadgeLevel" class="badge-level">Intermediário</span>
                        <span id="qBadgeTheme" class="badge-theme">Relato de Resultados</span>
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <button id="btnDebateHeader" class="btn-debate-header" onclick="playQuestionAudio('debate')" title="Ouvir debate de especialistas (Thalita & Francisca) sobre esta questão">
                            <span>🎙️</span> Ouvir Debate
                        </button>
                        <button id="btnFlagQuestion" class="btn-flag" onclick="toggleFlagCurrentQuestion()" title="Marcar para revisar antes de entregar">
                            <span>🚩</span> Revisar depois
                        </button>
                    </div>
                </div>

                <!-- Enunciado com Ícone 🔊 após o texto (alterna para ⏹️ ao tocar) -->
                <div class="q-statement-box">
                    <span id="qStatement" class="q-statement-text">Enunciado da questão...</span>
                    <button id="btnTTSStatement" class="btn-tts-icon" onclick="playStatementAudio()" title="Ouvir pergunta com a voz Francisca (ou clique para parar)" aria-label="Ouvir pergunta">🔊</button>
                </div>

                <!-- Lista de Alternativas com Ícone 🔊 após cada uma -->
                <div class="alternatives-list" id="alternativesList">
                    <!-- Preenchido via JavaScript -->
                </div>

                <!-- Painel de Diagnóstico do Erro / Acerto por Alternativa -->
                <div class="diagnostic-card" id="diagnosticCard">
                    <div class="diag-title-row">
                        <span id="diagTitle">Diagnóstico Metrológico</span>
                        <span id="diagBadge" style="font-size: 12px; font-weight: 700; text-transform: uppercase;"></span>
                    </div>

                    <div id="diagBody">
                        <!-- Preenchido dinamicamente com os motivos do erro e da correta -->
                    </div>

                    <div class="diag-actions">
                        <button id="btnPlayAula" class="btn-feedback-audio" onclick="playQuestionAudio('aula')">
                            🎧 Trecho da Aula
                        </button>
                        <button id="btnPlayDebate" class="btn-feedback-audio" onclick="playQuestionAudio('debate')">
                            🎙️ Debate de Especialistas (Thalita & Francisca)
                        </button>
                        <a id="linkVerTreinamento" href="index.html" target="_blank" class="btn-feedback-audio" style="text-decoration: none;">
                            📄 Ver no Treinamento
                        </a>
                    </div>
                </div>
            </div>

            <!-- Barra Inferior de Navegação -->
            <div class="exam-bottom-bar">
                <button id="btnPrev" class="btn-nav" onclick="prevQuestion()">
                    ← Questão Anterior
                </button>
                <div style="font-size: 13px; color: var(--text-muted);">
                    Clique no ícone <strong>🔊</strong> para ouvir e em <strong>⏹️</strong> para parar (ou tecle <strong>Esc</strong>)
                </div>
                <button id="btnNext" class="btn-nav" onclick="nextQuestion()">
                    Próxima Questão →
                </button>
            </div>
        </section>

        <!-- ==================================================================
             TELA 3: RESULTADOS E DASHBOARD
             ================================================================== -->
        <section id="viewResults" class="view-section">
            <div class="results-hero">
                <div id="scoreCircle" class="score-circle passed">
                    <span id="scorePercentage" class="score-val">85%</span>
                    <span class="score-sub">APROVEITAMENTO</span>
                </div>
                <h2 id="resultsStatusTitle" class="results-title">Parabéns! Você foi Aprovado!</h2>
                <p id="resultsStatusDesc" class="results-sub">
                    Você demonstrou excelente compreensão metrológica dos requisitos da ABNT NBR ISO/IEC 17025:2017 e das práticas da Eletronuclear.
                </p>

                <div class="results-metrics-grid">
                    <div class="metric-box">
                        <strong id="metricScoreFraction">17 / 20</strong>
                        <span>Questões Corretas</span>
                    </div>
                    <div class="metric-box">
                        <strong id="metricWrong">3</strong>
                        <span>Erros</span>
                    </div>
                    <div class="metric-box">
                        <strong id="metricTimeSpent">18 min</strong>
                        <span>Tempo Total</span>
                    </div>
                    <div class="metric-box">
                        <strong id="metricCutoff">70%</strong>
                        <span>Nota de Corte</span>
                    </div>
                </div>
            </div>

            <!-- Radar de Competências por Perfil Profissional -->
            <div class="section-radar-box" id="profileRadarBox">
                <div class="section-radar-title">
                    <span>👥</span> Desempenho por Perfil Profissional
                </div>
                <div class="radar-list" id="profileRadarList">
                    <!-- Preenchido via JavaScript -->
                </div>
            </div>

            <!-- Radar de Competências por Seção Normativa -->
            <div class="section-radar-box">
                <div class="section-radar-title">
                    <span>📊</span> Domínio Normativo por Cláusula da ISO/IEC 17025:2017
                </div>
                <div class="radar-list" id="sectionRadarList">
                    <!-- Preenchido via JavaScript -->
                </div>
            </div>

            <!-- Ações da Tela de Resultados -->
            <div class="results-actions-row">
                <button class="btn-action-primary" onclick="restartWithSameConfig()">
                    <span>🔄</span> Fazer Novo Simulado
                </button>
                <button id="btnRetryErrors" class="btn-action-secondary" onclick="retryOnlyErrors()">
                    <span>🎯</span> Refazer Apenas as Questões Erradas
                </button>
                <button class="btn-action-secondary" onclick="window.print()">
                    <span>🖨️</span> Imprimir Relatório de Desempenho
                </button>
                <button class="btn-action-secondary" onclick="goToConfig()">
                    <span>⚙️</span> Alterar Configurações
                </button>
            </div>

            <!-- Revisão Detalhada das Questões -->
            <div class="review-filter-bar">
                <h3 style="font-size: 16px; font-weight: 800; color: var(--primary-dark);">
                    📝 Gabarito Comentado e Diagnóstico das Alternativas
                </h3>
                <div class="review-filter-buttons">
                    <button class="btn-filter active" onclick="filterReviewList('all', this)">Todas (<span id="countRevAll">0</span>)</button>
                    <button class="btn-filter" onclick="filterReviewList('errors', this)">Apenas Erros (<span id="countRevErrors">0</span>)</button>
                    <button class="btn-filter" onclick="filterReviewList('correct', this)">Apenas Acertos (<span id="countRevCorrect">0</span>)</button>
                </div>
            </div>

            <div class="review-cards-list" id="reviewCardsList">
                <!-- Preenchido via JavaScript -->
            </div>
        </section>
    </main>

    <!-- Barra Flutuante de Controle e Parada de Áudio -->
    <div id="floatingAudioBar" class="floating-audio-bar" style="display: none;">
        <div class="floating-audio-info">
            <span style="font-size: 16px;">🔊</span>
            <span id="floatingAudioTitle">Reproduzindo áudio...</span>
        </div>
        <button class="btn-stop-audio" onclick="stopAllAudio()" title="Parar reprodução (ou aperte Esc)">
            <span>⏹️</span> Parar Áudio
        </button>
    </div>

    <!-- Áudio Player Centralizado -->
    <audio id="audioPlayer" preload="none"></audio>

    <script>
        // BANCO DE QUESTÕES COMPLETO COM ÁUDIOS E EXPLICAÇÕES POR ALTERNATIVA
        const ALL_QUESTIONS = {json_str};

        // Estado da Aplicação
        let activeQuestions = [];
        let currentIndex = 0;
        let userAnswers = {{}};
        let flaggedQuestions = new Set();
        let examMode = 'study';
        let timerInterval = null;
        let secondsRemaining = 0;
        let totalSecondsAllocated = 0;
        let startTime = null;

        const audioPlayer = document.getElementById('audioPlayer');
        let currentPlayingBtn = null;

        window.addEventListener('DOMContentLoaded', () => {{
            renderUserStats();
            setupKeyboardShortcuts();
            updateFilterNotice();

            audioPlayer.addEventListener('ended', resetTTSButtons);
            audioPlayer.addEventListener('pause', () => {{
                if (audioPlayer.currentTime === audioPlayer.duration) resetTTSButtons();
            }});
        }});

        // Atualização Dinâmica do Banner de Filtro
        function updateFilterNotice() {{
            const profile = document.getElementById('selectProfile').value;
            const scope = document.getElementById('selectScope').value;

            let pool = ALL_QUESTIONS;
            if (profile !== 'all') pool = pool.filter(q => q.perfil === profile);
            if (scope !== 'all') pool = pool.filter(q => q.secao_raiz === scope);

            const available = pool.length;
            const badge = document.getElementById('filterCountBadge');
            const text = document.getElementById('filterNoticeText');

            let profileLabel = "Todos os Perfis";
            if (profile === 'tecnico') profileLabel = "🛠️ Corpo Técnico";
            else if (profile === 'gerencial') profileLabel = "👔 Corpo Gerencial";
            else if (profile === 'geral') profileLabel = "🌐 Geral / Institucional";

            let scopeLabel = "Todas as Seções";
            if (scope !== 'all') scopeLabel = `Seção ${{scope}}`;

            text.innerHTML = `Filtro ativo: <strong>${{profileLabel}}</strong> • <strong>${{scopeLabel}}</strong>`;
            badge.textContent = `${{available}} Questões Disponíveis`;

            if (available === 0) {{
                badge.style.color = 'var(--danger)';
                text.innerHTML += ' <span style="color: var(--danger); font-weight: 700;">(Sem questões nesta combinação. Selecione "Todas as Seções")</span>';
            }} else {{
                badge.style.color = 'var(--primary)';
            }}
        }}

        // Gerenciamento e Controle de Áudio (Com Parada Imediata)
        function stopAllAudio() {{
            if (audioPlayer) {{
                audioPlayer.pause();
                audioPlayer.currentTime = 0;
            }}
            if (window.speechSynthesis) {{
                window.speechSynthesis.cancel();
            }}
            resetTTSButtons();
        }}

        function playTTS(btn, audioSrc, fallbackText, trackTitle) {{
            // Se o botão já está tocando, para a reprodução
            if (currentPlayingBtn === btn && !audioPlayer.paused) {{
                stopAllAudio();
                return;
            }}

            stopAllAudio();
            currentPlayingBtn = btn;
            if (btn) {{
                btn.classList.add('is-playing');
                btn.innerHTML = '⏹️';
                btn.title = 'Clique para parar o áudio (ou aperte Esc)';
            }}

            showFloatingAudioBar(trackTitle || "Leitura com voz oficial...");

            if (audioSrc) {{
                audioPlayer.src = audioSrc;
                audioPlayer.play().catch(err => {{
                    console.warn('Erro ao tocar arquivo MP3, acionando fallback por voz do navegador:', err);
                    playBrowserTTS(fallbackText, btn);
                }});
            }} else {{
                playBrowserTTS(fallbackText, btn);
            }}
        }}

        function playBrowserTTS(text, btn) {{
            if (!window.speechSynthesis) return;
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = 'pt-BR';
            utter.rate = 1.0;
            utter.onend = resetTTSButtons;
            utter.onerror = resetTTSButtons;
            window.speechSynthesis.speak(utter);
        }}

        function resetTTSButtons() {{
            document.querySelectorAll('.btn-tts-icon').forEach(btn => {{
                btn.classList.remove('is-playing');
                btn.innerHTML = '🔊';
                btn.title = 'Ouvir com voz oficial';
            }});
            const btnDebate = document.getElementById('btnDebateHeader');
            if (btnDebate) {{
                btnDebate.classList.remove('is-playing');
                btnDebate.innerHTML = '<span>🎙️</span> Ouvir Debate';
            }}
            const btnDiagDebate = document.getElementById('btnPlayDebate');
            if (btnDiagDebate) {{
                btnDiagDebate.innerHTML = '🎙️ Debate de Especialistas (Thalita & Francisca)';
            }}
            const bar = document.getElementById('floatingAudioBar');
            if (bar) bar.style.display = 'none';
            currentPlayingBtn = null;
        }}

        function showFloatingAudioBar(title) {{
            const bar = document.getElementById('floatingAudioBar');
            const txt = document.getElementById('floatingAudioTitle');
            if (bar && txt) {{
                txt.textContent = title;
                bar.style.display = 'flex';
            }}
        }}

        function playStatementAudio() {{
            const q = activeQuestions[currentIndex];
            const btn = document.getElementById('btnTTSStatement');
            const audioSrc = `Audios_Simulado/${{q.id}}_enunciado.mp3`;
            const title = `Pergunta • Requisito ${{q.clausula}}: ${{q.tema || ''}}`;
            playTTS(btn, audioSrc, q.enunciado, title);
        }}

        function playAlternativeAudio(letra) {{
            const q = activeQuestions[currentIndex];
            const btn = document.getElementById(`btnTTSAlt_${{letra}}`);
            const altObj = q.alternativas.find(a => a.letra === letra);
            const audioSrc = altObj ? altObj.audio_alt : `Audios_Simulado/${{q.id}}_alt_${{letra}}.mp3`;
            const text = altObj ? altObj.texto : '';
            const title = `Alternativa ${{letra}} • Requisito ${{q.clausula}}`;
            playTTS(btn, audioSrc, `Alternativa ${{letra}}: ${{text}}`, title);
        }}

        function playQuestionAudio(type) {{
            const q = activeQuestions[currentIndex];
            const src = (type === 'debate') ? q.debate_podcast : q.audio_ref;
            const title = (type === 'debate') ? `🎙️ Debate: Questão ${{q.id.replace('Q_', '')}} • Thalita & Francisca (ISO 17025)` : `🎧 Aula • Requisito ${{q.clausula}}`;
            const btn = (type === 'debate') ? document.getElementById('btnDebateHeader') : null;
            playSingleAudio(src, title, btn);
        }}

        function playSingleAudio(src, title, btn = null) {{
            if (!src) {{
                alert('Áudio não disponível.');
                return;
            }}
            if (!audioPlayer.paused && audioPlayer.src.includes(src)) {{
                stopAllAudio();
                return;
            }}
            stopAllAudio();
            currentPlayingBtn = btn;
            if (btn) {{
                btn.classList.add('is-playing');
                btn.innerHTML = '<span>⏹️</span> Parar Debate';
            }}
            showFloatingAudioBar(title || "Reproduzindo áudio...");
            audioPlayer.src = src;
            audioPlayer.play().catch(e => console.log('Notice:', e));
        }}

        // Estatísticas Locais
        function renderUserStats() {{
            const raw = localStorage.getItem('iso17025_exam_history');
            const statCompleted = document.getElementById('statCompleted');
            const statAvgScore = document.getElementById('statAvgScore');
            const statBestScore = document.getElementById('statBestScore');

            if (!raw) {{
                statCompleted.textContent = '0';
                statAvgScore.textContent = '0%';
                statBestScore.textContent = '0%';
                return;
            }}

            const history = JSON.parse(raw);
            if (history.length === 0) {{
                statCompleted.textContent = '0';
                statAvgScore.textContent = '0%';
                statBestScore.textContent = '0%';
                return;
            }}

            const totalExams = history.length;
            const avg = Math.round(history.reduce((acc, h) => acc + h.percent, 0) / totalExams);
            const best = Math.max(...history.map(h => h.percent));

            statCompleted.textContent = totalExams;
            statAvgScore.textContent = avg + '%';
            statBestScore.textContent = best + '%';
        }}

        function clearHistory() {{
            if (confirm('Deseja realmente apagar o histórico de simulados salvos neste navegador?')) {{
                localStorage.removeItem('iso17025_exam_history');
                renderUserStats();
            }}
        }}

        // Iniciar Simulado com Filtro por Perfil e Seção
        function startExam(customQuestions = null) {{
            stopAllAudio();
            examMode = document.querySelector('input[name="examMode"]:checked').value;
            const profileChoice = document.getElementById('selectProfile').value;
            const scope = document.getElementById('selectScope').value;
            const countChoice = document.getElementById('selectCount').value;

            if (customQuestions) {{
                activeQuestions = customQuestions;
            }} else {{
                let pool = [...ALL_QUESTIONS];
                if (profileChoice !== 'all') {{
                    pool = pool.filter(q => q.perfil === profileChoice);
                }}
                if (scope !== 'all') {{
                    pool = pool.filter(q => q.secao_raiz === scope);
                }}

                if (pool.length === 0) {{
                    alert('Nenhuma questão encontrada para a combinação de Perfil e Seção selecionada. Por favor, ajuste os filtros na tela de configuração.');
                    return;
                }}

                pool.sort(() => Math.random() - 0.5);

                if (countChoice !== 'all') {{
                    const qty = parseInt(countChoice);
                    pool = pool.slice(0, Math.min(qty, pool.length));
                }}
                activeQuestions = pool;
            }}

            if (activeQuestions.length === 0) {{
                alert('Nenhuma questão encontrada para este filtro.');
                return;
            }}

            currentIndex = 0;
            userAnswers = {{}};
            flaggedQuestions.clear();
            startTime = new Date();

            clearInterval(timerInterval);
            const timerBadge = document.getElementById('examTimerBadge');
            const modeBadge = document.getElementById('examModeBadge');

            if (examMode === 'exam') {{
                totalSecondsAllocated = activeQuestions.length * 90;
                secondsRemaining = totalSecondsAllocated;
                timerBadge.style.display = 'flex';
                modeBadge.textContent = 'MODO PROVA OFICIAL';
                modeBadge.style.color = 'var(--primary)';
                updateTimerDisplay();
                timerInterval = setInterval(tickTimer, 1000);
            }} else {{
                timerBadge.style.display = 'none';
                modeBadge.textContent = 'MODO ESTUDO (DIAGNÓSTICO IMEDIATO)';
                modeBadge.style.color = 'var(--success)';
            }}

            switchView('viewExam');
            renderQuestionNav();
            loadQuestion(0);
        }}

        function tickTimer() {{
            secondsRemaining--;
            updateTimerDisplay();

            if (secondsRemaining <= 0) {{
                clearInterval(timerInterval);
                alert('Tempo limite esgotado! Sua prova será entregue agora.');
                finishExam();
            }}
        }}

        function updateTimerDisplay() {{
            const timerDisplay = document.getElementById('timerDisplay');
            const timerBadge = document.getElementById('examTimerBadge');

            const mins = Math.floor(secondsRemaining / 60);
            const secs = secondsRemaining % 60;
            timerDisplay.textContent = `${{String(mins).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;

            if (secondsRemaining <= 300) {{
                timerBadge.classList.add('urgent');
            }} else {{
                timerBadge.classList.remove('urgent');
            }}
        }}

        function renderQuestionNav() {{
            const grid = document.getElementById('questionNavGrid');
            grid.innerHTML = '';

            activeQuestions.forEach((q, idx) => {{
                const btn = document.createElement('button');
                btn.className = 'q-nav-btn';
                btn.id = `navBtn_${{idx}}`;
                btn.textContent = idx + 1;
                btn.onclick = () => loadQuestion(idx);
                grid.appendChild(btn);
            }});
            updateQuestionNavStates();
        }}

        function updateQuestionNavStates() {{
            activeQuestions.forEach((q, idx) => {{
                const btn = document.getElementById(`navBtn_${{idx}}`);
                if (!btn) return;

                btn.classList.toggle('active', idx === currentIndex);
                const hasAnswer = userAnswers[q.id] !== undefined;
                btn.classList.toggle('answered', hasAnswer);
                btn.classList.toggle('flagged', flaggedQuestions.has(q.id));

                if (examMode === 'study' && hasAnswer) {{
                    const isCorrect = userAnswers[q.id] === q.correta;
                    btn.classList.toggle('correct-study', isCorrect);
                    btn.classList.toggle('incorrect-study', !isCorrect);
                }}
            }});

            const answeredCount = Object.keys(userAnswers).length;
            document.getElementById('progressText').textContent = `Questão ${{currentIndex + 1}} de ${{activeQuestions.length}}`;
            document.getElementById('answeredCountText').textContent = `${{answeredCount}} respondidas`;
            const perc = (answeredCount / activeQuestions.length) * 100;
            document.getElementById('progressBarFill').style.width = `${{perc}}%`;
        }}

        // Carregar Questão Ativa
        function loadQuestion(idx) {{
            if (idx < 0 || idx >= activeQuestions.length) return;
            stopAllAudio();
            currentIndex = idx;
            const q = activeQuestions[currentIndex];

            // Renderizar Badges de Perfil e Requisito
            const badgeProfile = document.getElementById('qBadgeProfile');
            if (badgeProfile) {{
                const p = q.perfil || 'geral';
                badgeProfile.className = `badge-profile badge-profile-${{p}}`;
                badgeProfile.innerHTML = `${{q.perfil_icone || '🌐'}} ${{q.perfil_nome || 'Geral'}}`;
                badgeProfile.title = q.foco_perfil || '';
            }}

            document.getElementById('qBadgeClause').textContent = `Requisito ${{q.clausula}}`;
            document.getElementById('qBadgeLevel').textContent = q.nivel;
            document.getElementById('qBadgeTheme').textContent = q.tema;
            document.getElementById('qStatement').textContent = q.enunciado;

            const btnFlag = document.getElementById('btnFlagQuestion');
            btnFlag.classList.toggle('active', flaggedQuestions.has(q.id));

            const btnDebate = document.getElementById('btnDebateHeader');
            if (btnDebate) {{
                btnDebate.innerHTML = '<span>🎙️</span> Ouvir Debate';
                btnDebate.classList.remove('is-playing');
                btnDebate.title = `Ouvir debate de especialistas (Thalita & Francisca) sobre a Questão do Requisito ${{q.clausula}}`;
                btnDebate.style.display = (examMode === 'study') ? 'inline-flex' : 'none';
            }}

            // Renderizar Alternativas com Ícone 🔊
            const list = document.getElementById('alternativesList');
            list.innerHTML = '';

            const selectedLetter = userAnswers[q.id];
            const isAnswered = selectedLetter !== undefined;

            q.alternativas.forEach(alt => {{
                const card = document.createElement('div');
                card.className = 'alt-card';
                if (selectedLetter === alt.letra) card.classList.add('selected');

                if (examMode === 'study' && isAnswered) {{
                    card.classList.add('disabled');
                    if (alt.letra === q.correta) {{
                        card.classList.add('correct-ans');
                    }} else if (selectedLetter === alt.letra) {{
                        card.classList.add('wrong-ans');
                    }}
                }}

                card.onclick = () => selectAlternative(alt.letra);

                card.innerHTML = `
                    <div class="alt-letter">${{alt.letra}}</div>
                    <div class="alt-body">
                        <div class="alt-text">${{alt.texto}}</div>
                        <button id="btnTTSAlt_${{alt.letra}}" class="btn-tts-icon" onclick="event.stopPropagation(); playAlternativeAudio('${{alt.letra}}')" title="Ouvir alternativa ${{alt.letra}} (ou clique para parar)" aria-label="Ouvir alternativa ${{alt.letra}}">🔊</button>
                    </div>
                `;
                list.appendChild(card);
            }});

            // Diagnóstico Exclusivo no Modo Estudo
            renderDiagnosticBox(q, selectedLetter);

            document.getElementById('btnPrev').disabled = (currentIndex === 0);
            document.getElementById('btnNext').disabled = (currentIndex === activeQuestions.length - 1);

            updateQuestionNavStates();
        }}

        // Renderizar Painel de Diagnóstico do Erro/Acerto
        function renderDiagnosticBox(q, selectedLetter) {{
            const card = document.getElementById('diagnosticCard');
            if (examMode !== 'study' || !selectedLetter) {{
                card.classList.remove('show');
                return;
            }}

            const isCorrect = (selectedLetter === q.correta);
            const expMap = q.explicacoes_detalhadas || {{}};
            const chosenExp = expMap[selectedLetter];

            card.className = `diagnostic-card show ${{isCorrect ? 'is-correct' : 'is-wrong'}}`;
            const badge = document.getElementById('diagBadge');
            const title = document.getElementById('diagTitle');
            const body = document.getElementById('diagBody');

            if (isCorrect) {{
                badge.textContent = 'RESPOSTA CORRETA';
                badge.style.color = 'var(--success)';
                title.textContent = `✓ Excelente! Alternativa [${{selectedLetter}}] está Correta`;

                const fund = chosenExp ? chosenExp.fundamentacao_acerto : q.justificativa;
                body.innerHTML = `
                    <div class="diag-section">
                        <div class="diag-label label-acerto">📘 Fundamentação Metrológica (Requisito ${{q.clausula_iso || q.clausula}}):</div>
                        <div class="diag-text">${{fund}}</div>
                    </div>
                `;
            }} else {{
                badge.textContent = 'ALTERNATIVA INCORRETA';
                badge.style.color = 'var(--danger)';
                title.textContent = `✖ Análise do Erro: Alternativa [${{selectedLetter}}] Incorreta`;

                const pqErrada = chosenExp ? chosenExp.por_que_esta_incorreta : 'Alternativa incorreta.';
                const pqCerta = chosenExp ? chosenExp.por_que_outra_e_correta : `A alternativa correta é a [${{q.correta}}]. ${{q.justificativa}}`;

                body.innerHTML = `
                    <div class="diag-section">
                        <div class="diag-label label-erro">❌ Por que a alternativa [${{selectedLetter}}] é um erro:</div>
                        <div class="diag-text">${{pqErrada}}</div>
                    </div>
                    <div class="diag-section">
                        <div class="diag-label label-correta">✔️ Por que a alternativa [${{q.correta}}] é a correta:</div>
                        <div class="diag-text">${{pqCerta}}</div>
                    </div>
                `;
            }}

            const linkNorma = document.getElementById('linkVerTreinamento');
            linkNorma.href = `index.html#${{q.item_id_referencia || ''}}`;
        }}

        function selectAlternative(letra) {{
            const q = activeQuestions[currentIndex];
            if (examMode === 'study' && userAnswers[q.id] !== undefined) return;

            userAnswers[q.id] = letra;
            loadQuestion(currentIndex);
        }}

        function toggleFlagCurrentQuestion() {{
            const q = activeQuestions[currentIndex];
            if (flaggedQuestions.has(q.id)) {{
                flaggedQuestions.delete(q.id);
            }} else {{
                flaggedQuestions.add(q.id);
            }}
            loadQuestion(currentIndex);
        }}

        function nextQuestion() {{
            if (currentIndex < activeQuestions.length - 1) {{
                loadQuestion(currentIndex + 1);
            }}
        }}

        function prevQuestion() {{
            if (currentIndex > 0) {{
                loadQuestion(currentIndex - 1);
            }}
        }}

        function confirmFinishExam() {{
            const answeredCount = Object.keys(userAnswers).length;
            const total = activeQuestions.length;

            if (answeredCount < total) {{
                const missing = total - answeredCount;
                if (!confirm(`Você ainda possui ${{missing}} questão(ões) sem resposta! Deseja realmente entregar a avaliação agora?`)) {{
                    return;
                }}
            }} else if (flaggedQuestions.size > 0) {{
                if (!confirm(`Você marcou ${{flaggedQuestions.size}} questão(ões) para revisar. Deseja entregar assim mesmo?`)) {{
                    return;
                }}
            }}
            finishExam();
        }}

        // Finalizar e Gerar Dashboard
        function finishExam() {{
            clearInterval(timerInterval);
            stopAllAudio();

            let correctCount = 0;
            const sectionScores = {{
                '4': {{ c: 0, t: 0 }},
                '5': {{ c: 0, t: 0 }},
                '6': {{ c: 0, t: 0 }},
                '7': {{ c: 0, t: 0 }},
                '8': {{ c: 0, t: 0 }}
            }};

            const profileScores = {{
                'tecnico': {{ c: 0, t: 0, nome: '🛠️ Corpo Técnico', desc: 'Bancada, equipamentos, calibração e incerteza' }},
                'gerencial': {{ c: 0, t: 0, nome: '👔 Corpo Gerencial', desc: 'Liderança, riscos, imparcialidade e auditorias' }},
                'geral': {{ c: 0, t: 0, nome: '🌐 Geral / Institucional', desc: 'Cultura da qualidade, sigilo e diretrizes gerais' }}
            }};

            activeQuestions.forEach(q => {{
                const userAns = userAnswers[q.id];
                const isCorrect = userAns === q.correta;

                if (isCorrect) correctCount++;

                const sec = q.secao_raiz;
                if (sectionScores[sec]) {{
                    sectionScores[sec].t++;
                    if (isCorrect) sectionScores[sec].c++;
                }}

                const p = q.perfil || 'geral';
                if (!profileScores[p]) profileScores[p] = {{ c: 0, t: 0, nome: p, desc: '' }};
                profileScores[p].t++;
                if (isCorrect) profileScores[p].c++;
            }});

            const total = activeQuestions.length;
            const percent = Math.round((correctCount / total) * 100);
            const passed = percent >= 70;

            const timeSpentSeconds = Math.round((new Date() - startTime) / 1000);
            const minsSpent = Math.max(1, Math.round(timeSpentSeconds / 60));

            // Salvar no Histórico
            try {{
                const raw = localStorage.getItem('iso17025_exam_history') || '[]';
                const hist = JSON.parse(raw);
                hist.unshift({{
                    date: new Date().toISOString(),
                    mode: examMode,
                    score: correctCount,
                    total: total,
                    percent: percent,
                    passed: passed
                }});
                localStorage.setItem('iso17025_exam_history', JSON.stringify(hist.slice(0, 30)));
            }} catch (e) {{
                console.log('Notice:', e);
            }}

            // Preencher Hero de Resultados
            const scoreCircle = document.getElementById('scoreCircle');
            scoreCircle.className = `score-circle ${{passed ? 'passed' : 'failed'}}`;
            document.getElementById('scorePercentage').textContent = percent + '%';

            const statusTitle = document.getElementById('resultsStatusTitle');
            const statusDesc = document.getElementById('resultsStatusDesc');

            if (passed) {{
                statusTitle.textContent = '🎉 Parabéns! Você foi Aprovado!';
                statusTitle.style.color = 'var(--success)';
                statusDesc.textContent = `Você superou a nota de corte (70%) com aproveitamento de ${{percent}}%. Seus conhecimentos sobre os requisitos da ABNT NBR ISO/IEC 17025:2017 estão sólidos.`;
            }} else {{
                statusTitle.textContent = '⚠️ Necessita Revisão Normativa';
                statusTitle.style.color = 'var(--danger)';
                statusDesc.textContent = `Seu aproveitamento foi de ${{percent}}% (nota de corte: 70%). Analise o diagnóstico das alternativas abaixo para compreender cada erro cometido.`;
            }}

            document.getElementById('metricScoreFraction').textContent = `${{correctCount}} / ${{total}}`;
            document.getElementById('metricWrong').textContent = `${{total - correctCount}}`;
            document.getElementById('metricTimeSpent').textContent = `${{minsSpent}} min`;

            // Radar de Desempenho por Perfil Profissional
            const profileRadarList = document.getElementById('profileRadarList');
            profileRadarList.innerHTML = '';
            for (const [key, data] of Object.entries(profileScores)) {{
                if (data.t === 0) continue;
                const pPerc = Math.round((data.c / data.t) * 100);
                const row = document.createElement('div');
                row.className = 'radar-item-row';
                row.innerHTML = `
                    <div class="radar-label">${{data.nome}}</div>
                    <div class="radar-bar-bg">
                        <div class="radar-bar-fill" style="width: ${{pPerc}}%; background: ${{pPerc >= 70 ? 'var(--success)' : (pPerc >= 50 ? 'var(--warning)' : 'var(--danger)')}};"></div>
                    </div>
                    <div class="radar-perc" style="color: ${{pPerc >= 70 ? 'var(--success)' : 'var(--danger)'}};">${{pPerc}}% (${{data.c}}/${{data.t}})</div>
                `;
                profileRadarList.appendChild(row);
            }}

            // Radar de Desempenho por Seção da Norma
            const sectionNames = {{
                '4': 'Seção 4: Requisitos Gerais (4.1 e 4.2)',
                '5': 'Seção 5: Requisitos de Estrutura (5.1 a 5.7)',
                '6': 'Seção 6: Requisitos de Recursos (6.1 a 6.6)',
                '7': 'Seção 7: Requisitos de Processos (7.1 a 7.11)',
                '8': 'Seção 8: Sistema de Gestão (8.1 a 8.9)'
            }};

            const radarList = document.getElementById('sectionRadarList');
            radarList.innerHTML = '';

            for (const sec of ['4', '5', '6', '7', '8']) {{
                const data = sectionScores[sec];
                if (!data || data.t === 0) continue;

                const secPerc = Math.round((data.c / data.t) * 100);
                const row = document.createElement('div');
                row.className = 'radar-item-row';
                row.innerHTML = `
                    <div class="radar-label">${{sectionNames[sec]}}</div>
                    <div class="radar-bar-bg">
                        <div class="radar-bar-fill" style="width: ${{secPerc}}%; background: ${{secPerc >= 70 ? 'var(--success)' : (secPerc >= 50 ? 'var(--warning)' : 'var(--danger)')}};"></div>
                    </div>
                    <div class="radar-perc" style="color: ${{secPerc >= 70 ? 'var(--success)' : 'var(--danger)'}};">${{secPerc}}% (${{data.c}}/${{data.t}})</div>
                `;
                radarList.appendChild(row);
            }}

            renderReviewList();

            const btnRetry = document.getElementById('btnRetryErrors');
            btnRetry.style.display = (total - correctCount > 0) ? 'inline-flex' : 'none';

            switchView('viewResults');
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        // Renderizar Lista de Revisão com Diagnóstico Inédito
        function renderReviewList(filter = 'all') {{
            const list = document.getElementById('reviewCardsList');
            list.innerHTML = '';

            let correctTotal = 0;
            let errorsTotal = 0;

            activeQuestions.forEach((q, idx) => {{
                const userAns = userAnswers[q.id];
                const isCorrect = userAns === q.correta;

                if (isCorrect) correctTotal++;
                else errorsTotal++;

                if (filter === 'errors' && isCorrect) return;
                if (filter === 'correct' && !isCorrect) return;

                const card = document.createElement('div');
                card.className = `review-card ${{isCorrect ? 'status-correct' : 'status-wrong'}}`;

                let altsHtml = '';
                q.alternativas.forEach(alt => {{
                    let altStyle = '';
                    let tag = '';
                    if (alt.letra === q.correta) {{
                        altStyle = 'color: var(--success); font-weight: 700;';
                        tag = ' <strong style="color: var(--success);">(Gabarito Correto)</strong>';
                    }} else if (alt.letra === userAns) {{
                        altStyle = 'color: var(--danger); text-decoration: line-through;';
                        tag = ' <strong style="color: var(--danger);">(Sua Escolha)</strong>';
                    }}

                    altsHtml += `
                        <div style="font-size: 13.5px; margin-bottom: 4px; ${{altStyle}}">
                            <strong>${{alt.letra}})</strong> ${{alt.texto}} ${{tag}}
                        </div>
                    `;
                }});

                const expMap = q.explicacoes_detalhadas || {{}};
                const chosenExp = expMap[userAns];

                let diagSectionHtml = '';
                if (isCorrect) {{
                    const fund = chosenExp ? chosenExp.fundamentacao_acerto : q.justificativa;
                    diagSectionHtml = `
                        <div style="background: #f0fdf4; border: 1px solid #86efac; border-left: 4px solid var(--success); padding: 10px 14px; border-radius: 6px; margin-top: 10px;">
                            <div style="font-size: 12px; font-weight: 800; color: #15803d; text-transform: uppercase;">📘 Por que seu acerto é correto:</div>
                            <div style="font-size: 13px; color: #334155; margin-top: 4px;">${{fund}}</div>
                        </div>
                    `;
                }} else if (userAns) {{
                    const pqErrada = chosenExp ? chosenExp.por_que_esta_incorreta : 'Alternativa incorreta.';
                    const pqCerta = chosenExp ? chosenExp.por_que_outra_e_correta : `A alternativa correta é a [${{q.correta}}].`;
                    diagSectionHtml = `
                        <div style="background: #fef2f2; border: 1px solid #fca5a5; border-left: 4px solid var(--danger); padding: 10px 14px; border-radius: 6px; margin-top: 10px;">
                            <div style="font-size: 12px; font-weight: 800; color: #b91c1c; text-transform: uppercase;">❌ Por que sua escolha [${{userAns}}] está incorreta:</div>
                            <div style="font-size: 13px; color: #334155; margin-top: 4px; margin-bottom: 8px;">${{pqErrada}}</div>
                            <div style="font-size: 12px; font-weight: 800; color: #15803d; text-transform: uppercase;">✔️ Por que a alternativa [${{q.correta}}] é a correta:</div>
                            <div style="font-size: 13px; color: #334155; margin-top: 4px;">${{pqCerta}}</div>
                        </div>
                    `;
                }} else {{
                    diagSectionHtml = `
                        <div style="background: #fffbeb; border: 1px solid #fde68a; border-left: 4px solid var(--warning); padding: 10px 14px; border-radius: 6px; margin-top: 10px;">
                            <div style="font-size: 12px; font-weight: 800; color: #b45309; text-transform: uppercase;">⚠️ Questão Não Respondida:</div>
                            <div style="font-size: 13px; color: #334155; margin-top: 4px;">Gabarito oficial é a letra <strong>[${{q.correta}}]</strong>. ${{q.justificativa}}</div>
                        </div>
                    `;
                }}

                const p = q.perfil || 'geral';
                const pTag = `<span class="badge-profile badge-profile-${{p}}" style="margin-right: 8px;">${{q.perfil_icone || ''}} ${{q.perfil_nome || ''}}</span>`;

                card.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;">
                        <div style="display: flex; align-items: center;">
                            ${{pTag}}
                            <span style="font-weight: 800; color: var(--primary);">Questão ${{idx + 1}} • Requisito ${{q.clausula}}</span>
                        </div>
                        <span style="font-weight: 800; color: ${{isCorrect ? 'var(--success)' : 'var(--danger)'}};">
                            ${{isCorrect ? '✓ ACERTOU' : (userAns ? '✖ ERROU' : '⚠️ EM BRANCO')}}
                        </span>
                    </div>
                    <div style="font-size: 14.5px; font-weight: 600; margin-bottom: 12px;">${{q.enunciado}}</div>
                    <div style="background: #f8fafc; padding: 12px; border-radius: 8px; margin-bottom: 8px;">${{altsHtml}}</div>
                    ${{diagSectionHtml}}
                    <div style="display: flex; gap: 8px; margin-top: 12px; flex-wrap: wrap;">
                        <button class="btn-feedback-audio" onclick="playSingleAudio('${{q.audio_ref}}', 'Aula • Requisito ${{q.clausula}}')">
                            🎧 Ouvir Aula
                        </button>
                        <button class="btn-feedback-audio" onclick="playSingleAudio('${{q.debate_podcast}}', 'Debate • Requisito ${{q.clausula}}')">
                            🎙️ Ouvir Debate
                        </button>
                        <a href="index.html#${{q.item_id_referencia || ''}}" target="_blank" class="btn-feedback-audio" style="text-decoration: none;">
                            📄 Ver no Treinamento
                        </a>
                    </div>
                `;
                list.appendChild(card);
            }});

            document.getElementById('countRevAll').textContent = activeQuestions.length;
            document.getElementById('countRevErrors').textContent = errorsTotal;
            document.getElementById('countRevCorrect').textContent = correctTotal;
        }}

        function filterReviewList(mode, btn) {{
            document.querySelectorAll('.btn-filter').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderReviewList(mode);
        }}

        function retryOnlyErrors() {{
            const errorQuestions = activeQuestions.filter(q => userAnswers[q.id] !== q.correta);
            if (errorQuestions.length === 0) return;
            startExam(errorQuestions);
        }}

        function restartWithSameConfig() {{
            startExam();
        }}

        function goToConfig() {{
            clearInterval(timerInterval);
            stopAllAudio();
            switchView('viewConfig');
        }}

        function switchView(viewId) {{
            document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
            document.getElementById(viewId).classList.add('active');
        }}

        function setupKeyboardShortcuts() {{
            document.addEventListener('keydown', (e) => {{
                if (e.key === 'Escape') {{
                    stopAllAudio();
                    return;
                }}
                if (!document.getElementById('viewExam').classList.contains('active')) return;

                if (['1', 'a', 'A'].includes(e.key)) selectAlternative('A');
                else if (['2', 'b', 'B'].includes(e.key)) selectAlternative('B');
                else if (['3', 'c', 'C'].includes(e.key)) selectAlternative('C');
                else if (['4', 'd', 'D'].includes(e.key)) selectAlternative('D');
                else if (e.key === 'ArrowRight') nextQuestion();
                else if (e.key === 'ArrowLeft') prevQuestion();
                else if (['f', 'F', 'r', 'R'].includes(e.key)) toggleFlagCurrentQuestion();
            }});
        }}
    </script>
</body>
</html>
'''

with open('simulado.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("simulado.html reconstruido com sucesso com parada de audio e controles aprimorados!")
