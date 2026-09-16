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

        /* ==================================================================
           IDENTIFICACAO DO PARTICIPANTE (LOGIN GOOGLE - GOOGLE IDENTITY SERVICES)
           ================================================================== */
        .identity-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
            border: 1px solid var(--border-dark);
            border-left: 5px solid var(--accent);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .identity-info {{
            display: flex;
            align-items: center;
            gap: 14px;
            min-width: 260px;
        }}

        .identity-avatar {{
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background: var(--primary-light);
            border: 2px solid var(--border-dark);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            overflow: hidden;
            flex-shrink: 0;
        }}

        .identity-avatar img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .identity-title {{
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: var(--text-muted);
        }}

        .identity-name {{
            font-size: 16px;
            font-weight: 800;
            color: var(--primary-dark);
            line-height: 1.25;
        }}

        .identity-email {{
            font-size: 12.5px;
            color: var(--text-muted);
        }}

        .identity-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        #googleSignInButton {{
            min-height: 40px;
            display: flex;
            align-items: center;
        }}

        .google-config-notice {{
            display: none;
            font-size: 12px;
            font-weight: 600;
            line-height: 1.5;
            color: #92400e;
            background: var(--warning-light);
            border: 1px solid #fcd34d;
            border-radius: 8px;
            padding: 10px 14px;
            margin: -8px 0 18px 0;
        }}

        .results-identity-line {{
            margin-top: 10px;
            font-size: 13px;
            font-weight: 700;
            color: var(--primary-dark);
        }}

        .exam-user-badge {{
            font-size: 12px;
            font-weight: 700;
            color: var(--primary-dark);
            border-left: 1px solid var(--border-dark);
            padding-left: 10px;
        }}

        /* Badges de Status de Habilitação */
        .badge-status {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 3px 9px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }}
        .badge-habilitado {{
            background: #dcfce7;
            color: #15803d;
            border: 1px solid #86efac;
        }}
        .badge-pendente {{
            background: #fef3c7;
            color: #b45309;
            border: 1px solid #fde68a;
        }}

        /* Botões de Ação de Autenticação */
        .btn-google-login {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #ffffff;
            color: #374151;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 8px 14px;
            font-size: 13.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}
        .btn-google-login:hover {{
            background: #f9fafb;
            border-color: #9ca3af;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .btn-gestor-panel {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: linear-gradient(135deg, #0f4c81, #1e3a8a);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 8px 14px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .btn-gestor-panel:hover {{
            opacity: 0.92;
            transform: translateY(-1px);
        }}

        /* Estilos dos Modais (Cadastro e Painel Gestor) */
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(4px);
            z-index: 9999;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 16px;
        }}
        .modal-box {{
            background: #ffffff;
            border-radius: 14px;
            width: 100%;
            max-width: 580px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            max-height: 90vh;
        }}
        .modal-box.modal-large {{
            max-width: 980px;
        }}
        .modal-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: #ffffff;
            padding: 16px 22px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .modal-header h3 {{
            font-size: 16px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .modal-close {{
            background: none;
            border: none;
            color: #ffffff;
            font-size: 20px;
            cursor: pointer;
            opacity: 0.85;
        }}
        .modal-close:hover {{
            opacity: 1;
        }}
        .modal-body {{
            padding: 22px;
            overflow-y: auto;
        }}
        .modal-footer {{
            padding: 14px 22px;
            background: #f8fafc;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }}
        .form-group-modal {{
            margin-bottom: 14px;
        }}
        .form-group-modal label {{
            display: block;
            font-size: 12.5px;
            font-weight: 700;
            color: #334155;
            margin-bottom: 5px;
        }}
        .form-input-modal, .form-select-modal {{
            width: 100%;
            padding: 9px 12px;
            border: 1px solid var(--border-dark);
            border-radius: 8px;
            font-size: 13.5px;
            color: #1e293b;
            background: #ffffff;
            outline: none;
            box-sizing: border-box;
        }}
        .form-input-modal:focus, .form-select-modal:focus {{
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }}
        .form-input-modal[readonly] {{
            background: #f1f5f9;
            color: #64748b;
            cursor: not-allowed;
        }}

        /* Painel do Gestor */
        .dash-metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 10px;
            margin-bottom: 18px;
        }}
        .dash-stat-card {{
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px;
            text-align: center;
        }}
        .dash-stat-val {{
            font-size: 22px;
            font-weight: 800;
            color: var(--primary);
        }}
        .dash-stat-lbl {{
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
        }}
        .dash-filters-bar {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 14px;
            align-items: center;
            justify-content: space-between;
        }}
        .dash-table-wrap {{
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow-x: auto;
            background: #ffffff;
            max-height: 400px;
        }}
        .dash-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12.5px;
            text-align: left;
        }}
        .dash-table th {{
            background: #f1f5f9;
            color: #475569;
            font-weight: 700;
            padding: 9px 12px;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 2;
        }}
        .dash-table td {{
            padding: 9px 12px;
            border-bottom: 1px solid #f1f5f9;
            color: #334155;
        }}
        .dash-table tr:hover td {{
            background: #f8fafc;
        }}

        /* Carimbo de Habilitação no Laudo */
        .cert-stamp-box {{
            margin-top: 18px;
            padding: 16px 20px;
            border-radius: 10px;
            border: 2px dashed;
            display: flex;
            align-items: center;
            gap: 16px;
            background: #ffffff;
        }}
        .cert-stamp-box.apto {{
            border-color: #16a34a;
            background: #f0fdf4;
            color: #166534;
        }}
        .cert-stamp-box.pendente {{
            border-color: #d97706;
            background: #fffbeb;
            color: #92400e;
        }}
        .cert-stamp-icon {{
            font-size: 34px;
            flex-shrink: 0;
        }}
        .cert-stamp-title {{
            font-size: 14.5px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-bottom: 4px;
        }}
        .cert-stamp-meta {{
            font-size: 12.5px;
            opacity: 0.9;
        }}
    </style>

    <!-- Firebase SDKs (Compat v9/v10 - Vanilla HTML/JS) -->
    <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-auth-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore-compat.js"></script>
    <script src="firebase_simulado.js"></script>
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
                    Personalize seu simulado por perfil profissional, seção da norma e formato de aplicação.
                </p>

                <!-- Identificação do Participante (Login Google + Firebase) -->
                <div id="identityCard" class="identity-card">
                    <div class="identity-info">
                        <div id="identityAvatar" class="identity-avatar">👤</div>
                        <div>
                            <div class="identity-title">
                                Identificação Funcional do Participante
                                <span id="identityStatusBadge" class="badge-status badge-pendente" style="margin-left: 6px;">Não Autenticado</span>
                            </div>
                            <div id="identityName" class="identity-name">Visitante / Convidado</div>
                            <div id="identityEmail" class="identity-email">
                                Entre com sua Conta Google para registrar sua avaliação e habilitar seu perfil perante a ISO/IEC 17025.
                            </div>
                        </div>
                    </div>
                    <div class="identity-actions">
                        <button id="btnGoogleLogin" class="btn-google-login" onclick="handleLoginGoogle()">
                            <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
                            <span>Entrar com Google</span>
                        </button>
                        <button id="btnDemoLogin" class="btn-nav" style="display: inline-flex;" onclick="handleLoginDemo()" title="Simula usuário para testes rápidos">
                            <span>⚡ Modo Teste</span>
                        </button>
                        <button id="btnEditCadastro" class="btn-nav" style="display: none;" onclick="openModalCadastro()">
                            <span>👤 Meu Cadastro</span>
                        </button>
                        <button id="btnGestorPanel" class="btn-gestor-panel" style="display: none;" onclick="openModalPainelGestor()">
                            <span>📊 Painel do Gestor</span>
                        </button>
                        <button id="btnGoogleSignOut" class="btn-nav" style="display: none;" onclick="handleLogout()">
                            <span>🚪 Sair</span>
                        </button>
                    </div>
                </div>
                <div id="googleConfigNotice" class="google-config-notice"></div>

                <div class="config-grid">
                    <!-- 1. Modo de Exame -->
                    <div class="config-group">
                        <label class="group-title">1. Modo de Avaliação</label>
                        <div class="option-radio">
                            <label class="radio-card">
                                <input type="radio" name="examMode" value="study" checked>
                                <div class="radio-info">
                                    <strong>Modo Estudo</strong>
                                    <span>Gabarito, diagnóstico do erro e debate comentados na hora.</span>
                                </div>
                            </label>
                            <label class="radio-card">
                                <input type="radio" name="examMode" value="exam">
                                <div class="radio-info">
                                    <strong>Modo Prova</strong>
                                    <span>Cronometrado, sem consulta e com laudo de desempenho ao final.</span>
                                </div>
                            </label>
                        </div>
                    </div>

                    <!-- 2. Perfil do Avaliado -->
                    <div class="config-group">
                        <label class="group-title">2. Perfil Profissional</label>
                        <select id="selectProfile" class="select-custom" onchange="updateFilterNotice()">
                            <option value="all" selected>🌐 Todos os Perfis (Visão Global)</option>
                            <option value="tecnico">🛠️ Corpo Técnico (Bancada e Métodos)</option>
                            <option value="gerencial">👔 Corpo Gerencial (Gestão e Riscos)</option>
                            <option value="geral">🌐 Geral / Institucional (Cultura e Sigilo)</option>
                        </select>
                        <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 8px;">
                            Questões direcionadas à sua rotina de trabalho.
                        </p>
                    </div>

                    <!-- 3. Seção da Norma -->
                    <div class="config-group">
                        <label class="group-title">3. Seção da Norma</label>
                        <select id="selectScope" class="select-custom" onchange="updateFilterNotice()">
                            <option value="all" selected>Todas as Seções (Norma Completa)</option>
                            <option value="4">Seção 4: Requisitos Gerais (Imparcialidade e Sigilo)</option>
                            <option value="5">Seção 5: Estrutura Organizacional</option>
                            <option value="6">Seção 6: Recursos (Pessoal, Equipamentos e Metrologia)</option>
                            <option value="7">Seção 7: Processos (Ensaios, Métodos e Incerteza)</option>
                            <option value="8">Seção 8: Gestão (Riscos e Auditorias)</option>
                        </select>
                    </div>

                    <!-- 4. Quantidade de Questões -->
                    <div class="config-group">
                        <label class="group-title">4. Quantidade de Questões</label>
                        <select id="selectCount" class="select-custom" onchange="updateFilterNotice()">
                            <option value="10">10 Questões (~15 min)</option>
                            <option value="20" selected>20 Questões (~30 min)</option>
                            <option value="30">30 Questões (~45 min)</option>
                            <option value="all">Todas as Questões do Filtro</option>
                        </select>
                        <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 8px;">
                            Tempo no Modo Prova: 1,5 min/questão.
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
                    <span class="exam-user-badge">
                        👤 <span id="examUserName">—</span>
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

                <div id="resultsIdentityLine" class="results-identity-line">
                    <!-- Preenchido via JavaScript -->
                </div>

                <!-- Selo de Habilitação Metrológica Oficial -->
                <div id="certStampBox" class="cert-stamp-box" style="display: none;"></div>

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

        <!-- ==============================================================
             MODAL 1: CADASTRO SIMPLES DO PARTICIPANTE (PRIMEIRO ACESSO)
             ============================================================== -->
        <div id="modalCadastro" class="modal-overlay">
            <div class="modal-box">
                <div class="modal-header">
                    <h3><span>👤</span> Cadastro Funcional do Participante</h3>
                    <button class="modal-close" onclick="closeModalCadastro()">✕</button>
                </div>
                <form id="formCadastroSimples" onsubmit="salvarCadastroForm(event)">
                    <div class="modal-body">
                        <p style="font-size: 13px; color: #64748b; margin-bottom: 16px;">
                            Preencha seus dados funcionais da Eletronuclear para emissão do <strong>Laudo Oficial de Habilitação Metrológica (ISO/IEC 17025)</strong>.
                        </p>

                        <div class="form-group-modal">
                            <label for="cadNome">Nome Completo (como constará no Laudo/Certificado)</label>
                            <input type="text" id="cadNome" class="form-input-modal" required placeholder="Seu nome completo">
                        </div>

                        <div class="form-group-modal">
                            <label for="cadEmail">E-mail Institucional / Conta Google</label>
                            <input type="email" id="cadEmail" class="form-input-modal" readonly>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                            <div class="form-group-modal">
                                <label for="cadMatricula">Matrícula / Reg. Funcional *</label>
                                <input type="text" id="cadMatricula" class="form-input-modal" required placeholder="Ex: EN-10492">
                            </div>
                            <div class="form-group-modal">
                                <label for="cadSetor">Setor / Laboratório *</label>
                                <select id="cadSetor" class="form-select-modal" required>
                                    <option value="">Selecione o setor...</option>
                                    <option value="LMA - Laboratório de Monitoramento Ambiental">LMA - Lab. Monitoramento Ambiental</option>
                                    <option value="Química Analítica e Ensaios Físico-Químicos">Química Analítica / Físico-Química</option>
                                    <option value="Radiometria e Proteção Radiológica">Radiometria / Proteção Radiológica</option>
                                    <option value="Garantia da Qualidade e Metrologia">Garantia da Qualidade / SGQ</option>
                                    <option value="Operação e Apoio de Usinas (Angra 1 e 2)">Operação / Usinas (Angra 1 e 2)</option>
                                    <option value="Meio Ambiente e Licenciamento">Meio Ambiente e Licenciamento</option>
                                    <option value="Outro Setor">Outro Setor da Eletronuclear</option>
                                </select>
                            </div>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                            <div class="form-group-modal">
                                <label for="cadFuncao">Cargo / Função</label>
                                <input type="text" id="cadFuncao" class="form-input-modal" placeholder="Ex: Químico, Técnico, Supervisor">
                            </div>
                            <div class="form-group-modal">
                                <label for="cadPerfilMetrologico">Perfil Metrológico Principal</label>
                                <select id="cadPerfilMetrologico" class="form-select-modal">
                                    <option value="geral">Geral / Institucional</option>
                                    <option value="tecnico">Corpo Técnico (Execução e Métodos)</option>
                                    <option value="gerencial">Corpo Gerencial / SGQ</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn-nav" onclick="closeModalCadastro()">Cancelar</button>
                        <button type="submit" class="btn-action-primary" style="padding: 9px 20px;">
                            <span>💾</span> Salvar Cadastro
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- ==============================================================
             MODAL 2: PAINEL DO GESTOR / INSTRUTOR (WHITELIST PROTEGIDA)
             ============================================================== -->
        <div id="modalPainelGestor" class="modal-overlay">
            <div class="modal-box modal-large">
                <div class="modal-header">
                    <h3><span>📊</span> Painel do Gestor e Instrutor • Habilitações ISO/IEC 17025</h3>
                    <button class="modal-close" onclick="closeModalPainelGestor()">✕</button>
                </div>
                <div class="modal-body">
                    <!-- Métricas Rápidas -->
                    <div class="dash-metrics-grid">
                        <div class="dash-stat-card">
                            <div id="dashTotalUsers" class="dash-stat-val">0</div>
                            <div class="dash-stat-lbl">Participantes</div>
                        </div>
                        <div class="dash-stat-card">
                            <div id="dashTotalHabilitados" class="dash-stat-val" style="color: var(--success);">0</div>
                            <div class="dash-stat-lbl">Habilitados (Aptos)</div>
                        </div>
                        <div class="dash-stat-card">
                            <div id="dashTaxaAprovacao" class="dash-stat-val">0%</div>
                            <div class="dash-stat-lbl">Taxa de Habilitação</div>
                        </div>
                        <div class="dash-stat-card">
                            <div id="dashMediaNota" class="dash-stat-val">0%</div>
                            <div class="dash-stat-lbl">Média de Pontuação</div>
                        </div>
                    </div>

                    <!-- Barra de Filtros e Busca -->
                    <div class="dash-filters-bar">
                        <input type="text" id="dashSearchInput" class="form-input-modal" style="max-width: 260px;" placeholder="🔍 Buscar por nome ou matrícula..." oninput="filtrarTabelaGestor()">
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            <select id="dashFilterStatus" class="form-select-modal" style="width: auto;" onchange="filtrarTabelaGestor()">
                                <option value="all">Todos os Status</option>
                                <option value="apto">Apenas Habilitados (Aptos)</option>
                                <option value="pendente">Apenas Em Treinamento</option>
                            </select>
                            <button id="btnExportCSV" class="btn-action-primary" style="padding: 8px 14px; font-size: 13px;" onclick="exportarRelatorioCSV()">
                                <span>📥</span> Exportar CSV / Excel
                            </button>
                        </div>
                    </div>

                    <!-- Tabela de Alunos -->
                    <div class="dash-table-wrap">
                        <table class="dash-table">
                            <thead>
                                <tr>
                                    <th>Participante</th>
                                    <th>Matrícula & Setor</th>
                                    <th>Status Metrológico</th>
                                    <th>Melhor Nota</th>
                                    <th>Tentativas</th>
                                    <th>Data Habilitação / Avaliação</th>
                                </tr>
                            </thead>
                            <tbody id="dashTableBody">
                                <tr>
                                    <td colspan="6" style="text-align: center; padding: 24px; color: #64748b;">
                                        Carregando registros do banco de dados...
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn-action-secondary" onclick="closeModalPainelGestor()">Fechar Painel</button>
                </div>
            </div>
        </div>
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

        // ==================================================================
        // AUTENTICAÇÃO FIREBASE E IDENTIFICAÇÃO DO PARTICIPANTE
        // ==================================================================
        let currentUser = null;
        let currentProfile = null;
        let gestorAlunosLista = [];

        function updateAuthUI(user, profile) {{
            currentUser = user;
            currentProfile = profile;

            const avatar = document.getElementById('identityAvatar');
            const nameEl = document.getElementById('identityName');
            const emailEl = document.getElementById('identityEmail');
            const statusBadge = document.getElementById('identityStatusBadge');
            const btnGoogle = document.getElementById('btnGoogleLogin');
            const btnDemo = document.getElementById('btnDemoLogin');
            const btnEdit = document.getElementById('btnEditCadastro');
            const btnGestor = document.getElementById('btnGestorPanel');
            const btnOut = document.getElementById('btnGoogleSignOut');
            const examUser = document.getElementById('examUserName');

            if (user) {{
                // Usuário logado
                if (avatar) {{
                    avatar.innerHTML = user.photoURL 
                        ? `<img src="${{user.photoURL}}" alt="Foto" referrerpolicy="no-referrer">` 
                        : '👤';
                }}
                if (nameEl) {{
                    nameEl.textContent = (profile && profile.nome) || user.displayName || 'Participante';
                }}
                if (emailEl) {{
                    const matText = (profile && profile.matricula) ? ` • Matrícula: ${{profile.matricula}}` : '';
                    const setCol = (profile && profile.setor) ? ` • ${{profile.setor}}` : '';
                    emailEl.textContent = `${{user.email || 'Conta vinculada'}}${{matText}}${{setCol}}`;
                }}
                if (statusBadge) {{
                    if (profile && profile.isHabilitado) {{
                        statusBadge.className = 'badge-status badge-apto';
                        statusBadge.textContent = '✓ Habilitado (Apto)';
                    }} else if (profile && profile.matricula) {{
                        statusBadge.className = 'badge-status badge-pendente';
                        statusBadge.textContent = 'Em Treinamento';
                    }} else {{
                        statusBadge.className = 'badge-status badge-pendente';
                        statusBadge.textContent = 'Cadastro Pendente';
                    }}
                }}
                if (btnGoogle) btnGoogle.style.display = 'none';
                if (btnDemo) btnDemo.style.display = 'none';
                if (btnEdit) btnEdit.style.display = 'inline-flex';
                if (btnOut) btnOut.style.display = 'inline-flex';
                if (examUser) examUser.textContent = (profile && profile.nome) || user.displayName || user.email;

                // Verificar permissão de instrutor / gestor
                if (btnGestor && window.firebaseSimulado) {{
                    btnGestor.style.display = window.firebaseSimulado.isInstrutor() ? 'inline-flex' : 'none';
                }}

                // Se o usuário logou pela primeira vez e não tem matrícula, abrir modal de cadastro suavemente
                if (profile && !profile.matricula && !sessionStorage.getItem('iso17025_modal_shown')) {{
                    sessionStorage.setItem('iso17025_modal_shown', '1');
                    openModalCadastro();
                }}
            }} else {{
                // Visitante deslogado
                if (avatar) avatar.innerHTML = '👤';
                if (nameEl) nameEl.textContent = 'Visitante / Não Autenticado';
                if (emailEl) emailEl.textContent = 'Entre com sua Conta Google para registrar sua avaliação e habilitar seu perfil perante a ISO/IEC 17025.';
                if (statusBadge) {{
                    statusBadge.className = 'badge-status badge-pendente';
                    statusBadge.textContent = 'Não Autenticado';
                }}
                if (btnGoogle) btnGoogle.style.display = 'inline-flex';
                if (btnDemo) btnDemo.style.display = 'inline-flex';
                if (btnEdit) btnEdit.style.display = 'none';
                if (btnGestor) btnGestor.style.display = 'none';
                if (btnOut) btnOut.style.display = 'none';
                if (examUser) examUser.textContent = '—';
            }}
        }}

        async function handleLoginGoogle() {{
            if (!window.firebaseSimulado) return;
            try {{
                const res = await window.firebaseSimulado.loginGoogle();
                if (res && res.user) {{
                    updateAuthUI(res.user, res.profile);
                }}
            }} catch (err) {{
                console.error('Falha no login Google:', err);
            }}
        }}

        function handleLoginDemo() {{
            if (!window.firebaseSimulado) return;
            const res = window.firebaseSimulado._loginMockDemo();
            updateAuthUI(res.user, res.profile);
        }}

        async function handleLogout() {{
            if (!window.firebaseSimulado) return;
            if (confirm('Deseja realmente sair da sua conta?')) {{
                await window.firebaseSimulado.logout();
                updateAuthUI(null, null);
            }}
        }}

        // Modal de Cadastro
        function openModalCadastro() {{
            const modal = document.getElementById('modalCadastro');
            if (!modal) return;

            const nameInp = document.getElementById('cadNome');
            const emailInp = document.getElementById('cadEmail');
            const matInp = document.getElementById('cadMatricula');
            const setorSel = document.getElementById('cadSetor');
            const funcInp = document.getElementById('cadFuncao');
            const perfilSel = document.getElementById('cadPerfilMetrologico');

            if (currentUser) {{
                if (nameInp) nameInp.value = (currentProfile && currentProfile.nome) || currentUser.displayName || '';
                if (emailInp) emailInp.value = currentUser.email || '';
                if (matInp) matInp.value = (currentProfile && currentProfile.matricula) || '';
                if (setorSel) setorSel.value = (currentProfile && currentProfile.setor) || '';
                if (funcInp) funcInp.value = (currentProfile && currentProfile.funcao) || '';
                if (perfilSel) perfilSel.value = (currentProfile && currentProfile.perfilMetrologico) || 'geral';
            }}

            modal.classList.add('active');
        }}

        function closeModalCadastro() {{
            const modal = document.getElementById('modalCadastro');
            if (modal) modal.classList.remove('active');
        }}

        async function salvarCadastroForm(e) {{
            e.preventDefault();
            if (!currentUser) {{
                alert('Você precisa estar autenticado para salvar seus dados cadastrais.');
                return;
            }}

            const matricula = document.getElementById('cadMatricula').value.trim();
            const setor = document.getElementById('cadSetor').value;
            const funcao = document.getElementById('cadFuncao').value.trim();
            const nome = document.getElementById('cadNome').value.trim();
            const perfilMetrologico = document.getElementById('cadPerfilMetrologico').value;

            if (!matricula || !setor) {{
                alert('Por favor, informe a Matrícula e o Setor de atuação.');
                return;
            }}

            try {{
                const dados = {{ nome, matricula, setor, funcao, perfilMetrologico }};
                const updated = await window.firebaseSimulado.salvarCadastro(dados);
                currentProfile = updated;
                updateAuthUI(currentUser, currentProfile);
                closeModalCadastro();
                alert('✓ Cadastro funcional salvo com sucesso!');
            }} catch (err) {{
                console.error('Erro ao salvar cadastro:', err);
                alert('Erro ao salvar os dados. Tente novamente.');
            }}
        }}

        // Painel do Gestor / Instrutor
        async function openModalPainelGestor() {{
            const modal = document.getElementById('modalPainelGestor');
            if (!modal) return;

            modal.classList.add('active');
            const tbody = document.getElementById('dashTableBody');
            if (tbody) {{
                tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 24px; color: #64748b;">Carregando dados dos participantes...</td></tr>';
            }}

            try {{
                gestorAlunosLista = await window.firebaseSimulado.carregarPainelGestor();
                renderTabelaGestor(gestorAlunosLista);
            }} catch (err) {{
                console.error('Erro ao carregar painel:', err);
                if (tbody) {{
                    tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 24px; color: var(--danger);">Erro ao carregar dados do banco de dados.</td></tr>';
                }}
            }}
        }}

        function closeModalPainelGestor() {{
            const modal = document.getElementById('modalPainelGestor');
            if (modal) modal.classList.remove('active');
        }}

        function renderTabelaGestor(lista) {{
            const tbody = document.getElementById('dashTableBody');
            if (!tbody) return;

            const total = lista.length;
            const habilitados = lista.filter(u => u.isHabilitado).length;
            const taxa = total > 0 ? Math.round((habilitados / total) * 100) : 0;
            const somaNotas = lista.reduce((acc, u) => acc + (u.melhorNota || 0), 0);
            const media = total > 0 ? Math.round(somaNotas / total) : 0;

            const elTotal = document.getElementById('dashTotalUsers');
            const elHab = document.getElementById('dashTotalHabilitados');
            const elTaxa = document.getElementById('dashTaxaAprovacao');
            const elMedia = document.getElementById('dashMediaNota');

            if (elTotal) elTotal.textContent = total;
            if (elHab) elHab.textContent = habilitados;
            if (elTaxa) elTaxa.textContent = taxa + '%';
            if (elMedia) elMedia.textContent = media + '%';

            if (lista.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 24px; color: #64748b;">Nenhum participante encontrado com os filtros aplicados.</td></tr>';
                return;
            }}

            tbody.innerHTML = lista.map(u => {{
                const statusBadge = u.isHabilitado 
                    ? '<span class="badge-status badge-apto">✓ Habilitado (Apto)</span>' 
                    : '<span class="badge-status badge-pendente">Em Treinamento</span>';
                
                const dataFormatada = u.dataHabilitacao 
                    ? new Date(u.dataHabilitacao).toLocaleDateString('pt-BR', {{ day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }})
                    : (u.ultimaAtividade ? new Date(u.ultimaAtividade).toLocaleDateString('pt-BR') : '—');

                return `
                    <tr>
                        <td>
                            <strong>${{u.nome || 'Participante'}}</strong>
                            <div style="font-size: 11px; color: #64748b;">${{u.email || '—'}}</div>
                        </td>
                        <td>
                            <strong style="color: var(--primary);">${{u.matricula || 'Sem matrícula'}}</strong>
                            <div style="font-size: 11px; color: #475569;">${{u.setor || 'Setor não informado'}}</div>
                        </td>
                        <td>${{statusBadge}}</td>
                        <td>
                            <strong style="color: ${{ (u.melhorNota || 0) >= 70 ? 'var(--success)' : 'var(--danger)' }}; font-size: 14px;">
                                ${{u.melhorNota || 0}}%
                            </strong>
                        </td>
                        <td style="text-align: center;">${{u.totalTentativas || 0}}</td>
                        <td style="font-size: 12px; color: #475569;">${{dataFormatada}}</td>
                    </tr>
                `;
            }}).join('');
        }}

        function filtrarTabelaGestor() {{
            const search = (document.getElementById('dashSearchInput').value || '').toLowerCase().trim();
            const statusFilter = document.getElementById('dashFilterStatus').value;

            let filtrados = [...gestorAlunosLista];

            if (statusFilter === 'apto') {{
                filtrados = filtrados.filter(u => u.isHabilitado);
            }} else if (statusFilter === 'pendente') {{
                filtrados = filtrados.filter(u => !u.isHabilitado);
            }}

            if (search) {{
                filtrados = filtrados.filter(u => 
                    (u.nome && u.nome.toLowerCase().includes(search)) ||
                    (u.matricula && u.matricula.toLowerCase().includes(search)) ||
                    (u.email && u.email.toLowerCase().includes(search)) ||
                    (u.setor && u.setor.toLowerCase().includes(search))
                );
            }}

            renderTabelaGestor(filtrados);
        }}

        function exportarRelatorioCSV() {{
            if (!gestorAlunosLista || gestorAlunosLista.length === 0) {{
                alert('Não há dados disponíveis para exportação.');
                return;
            }}

            const headers = ['Nome Completo', 'E-mail', 'Matrícula', 'Setor / Laboratório', 'Função', 'Status ISO 17025', 'Melhor Nota (%)', 'Total Avaliações', 'Data Habilitação / Última Prova'];
            const rows = gestorAlunosLista.map(u => [
                `"${{(u.nome || '').replace(/"/g, '""')}}"`,
                `"${{(u.email || '').replace(/"/g, '""')}}"`,
                `"${{(u.matricula || '').replace(/"/g, '""')}}"`,
                `"${{(u.setor || '').replace(/"/g, '""')}}"`,
                `"${{(u.funcao || '').replace(/"/g, '""')}}"`,
                `"${{u.isHabilitado ? 'Habilitado (Apto - ISO 17025)' : 'Em Treinamento (Não Habilitado)'}}"`,
                u.melhorNota || 0,
                u.totalTentativas || 0,
                `"${{u.dataHabilitacao || u.ultimaAtividade || ''}}"`
            ]);

            const csvContent = '\\uFEFF' + [headers.join(';'), ...rows.map(r => r.join(';'))].join('\\r\\n');
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `relatorio_habilitacoes_iso17025_${{new Date().toISOString().slice(0, 10)}}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            renderUserStats();
            setupKeyboardShortcuts();
            updateFilterNotice();

            // Integração Firebase Simulado
            if (window.firebaseSimulado) {{
                window.firebaseSimulado.onAuthChange((user, profile) => {{
                    updateAuthUI(user, profile);
                }});
            }}

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
            examMode = document.querySelector('input[name="examMode"]:checked').value;

            // Se for Modo Prova Oficial, exige identificação e matrícula preenchida
            if (examMode === 'exam') {{
                if (!currentUser) {{
                    alert('Identificação Obrigatória: Para realizar a Prova Oficial de Habilitação da ISO/IEC 17025, faça login com sua Conta Google (ou utilize o Modo Teste).');
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                    return;
                }}
                if (!currentProfile || !currentProfile.matricula) {{
                    alert('Cadastro Incompleto: Por favor, informe sua Matrícula e Setor antes de iniciar a Prova Oficial.');
                    openModalCadastro();
                    return;
                }}
            }}

            stopAllAudio();
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
                    passed: passed,
                    user_name: currentUser ? currentUser.name : null,
                    user_email: currentUser ? currentUser.email : null,
                    user_sub: currentUser ? currentUser.sub : null
                }});
                localStorage.setItem('iso17025_exam_history', JSON.stringify(hist.slice(0, 30)));
            }} catch (e) {{
                console.log('Notice:', e);
            }}

            // Identidade do participante no laudo de desempenho
            const identityLine = document.getElementById('resultsIdentityLine');
            if (identityLine) {{
                if (currentUser) {{
                    const matInfo = (currentProfile && currentProfile.matricula) ? ` • Matrícula: ${{currentProfile.matricula}} (${{currentProfile.setor || 'SGQ'}})` : '';
                    identityLine.innerHTML = `👤 Avaliação realizada por <strong>${{ (currentProfile && currentProfile.nome) || currentUser.displayName || 'Participante' }}</strong> — ${{currentUser.email || ''}}${{matInfo}}`;
                }} else {{
                    identityLine.innerHTML = '👤 Avaliação realizada em modo visitante / não autenticado.';
                }}
            }}

            // Selo de Habilitação Metrológica Oficial (quando logado)
            const certBox = document.getElementById('certStampBox');
            if (certBox) {{
                if (currentUser && passed) {{
                    const certCode = window.firebaseSimulado ? window.firebaseSimulado._gerarCodigoAutenticidade(currentUser.uid, percent) : `ISO17025-${{Date.now()}}`;
                    certBox.style.display = 'flex';
                    certBox.innerHTML = `
                        <div class="cert-stamp-icon">🛡️</div>
                        <div class="cert-stamp-content">
                            <h4>HABILITAÇÃO METROLÓGICA OFICIAL CONCEDIDA (ISO/IEC 17025:2017)</h4>
                            <p>O participante <strong>${{ (currentProfile && currentProfile.nome) || currentUser.displayName || 'Participante' }}</strong> (Matrícula: <strong>${{ (currentProfile && currentProfile.matricula) || 'EN-REG' }}</strong>) atingiu índice de conformidade de <strong>${{percent}}%</strong>, estando formalmente <strong>HABILITADO / APTO</strong> perante os requisitos normativos do laboratório.</p>
                            <div class="cert-stamp-hash">CÓDIGO DE AUTENTICIDADE E RASTREABILIDADE: ${{certCode}}</div>
                        </div>
                    `;
                }} else if (currentUser && !passed) {{
                    certBox.style.display = 'flex';
                    certBox.style.background = '#fff1f2';
                    certBox.style.borderColor = '#fca5a5';
                    certBox.innerHTML = `
                        <div class="cert-stamp-icon">⚠️</div>
                        <div class="cert-stamp-content">
                            <h4 style="color: var(--danger);">EM TREINAMENTO • NECESSITA REVISÃO DOS REQUISITOS</h4>
                            <p>Aproveitamento de <strong>${{percent}}%</strong> (Corte: 70%). Conforme diretrizes da qualidade, o participante deverá revisar os itens apontados no diagnóstico e repetir o exame para emissão do registro de aptidão.</p>
                        </div>
                    `;
                }} else {{
                    certBox.style.display = 'none';
                }}
            }}

            // Envio e Registro da Avaliação no Firebase Firestore
            if (window.firebaseSimulado && currentUser) {{
                const submissaoPayload = {{
                    percent: percent,
                    totalQuestions: total,
                    correctCount: correctCount,
                    wrongCount: total - correctCount,
                    examMode: examMode,
                    timeSpentSeconds: timeSpentSeconds,
                    profileFilter: document.getElementById('selectProfile').value,
                    scopeFilter: document.getElementById('selectScope').value,
                    radarProfile: profileScores,
                    radarSection: sectionScores,
                    answersSummary: activeQuestions.map(q => ({{
                        id: q.id,
                        clausula: q.clausula,
                        resposta: userAnswers[q.id] || null,
                        correta: q.correta,
                        acertou: userAnswers[q.id] === q.correta
                    }}))
                }};
                window.firebaseSimulado.enviarSubmissaoProva(submissaoPayload)
                    .then(doc => {{
                        console.log('[Simulado] Prova registrada com sucesso no Firestore:', doc ? doc.submissaoId : 'OK');
                    }})
                    .catch(err => {{
                        console.warn('[Simulado] Registro salvo localmente. Falha no envio Firestore:', err);
                    }});
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
