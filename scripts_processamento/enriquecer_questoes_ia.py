# -*- coding: utf-8 -*-
"""
Módulo IA de Enriquecimento Metrológico:
Gera explicações aprofundadas e inéditas para cada alternativa (A, B, C, D)
de cada uma das 50 questões do Simulado da ISO/IEC 17025:2017.
"""

import json
import os

def gerar_diagnostico_alternativas(q):
    """
    Gera um dicionário completo com diagnósticos e justificativas inéditas
    para cada alternativa (A, B, C, D).
    """
    qid = q['id']
    correta = q['correta']
    clausula = q.get('clausula_iso', q.get('clausula', ''))
    tema = q.get('tema', '')
    enunciado = q.get('enunciado', '')
    alts = {alt['letra']: alt['texto'] for alt in q['alternativas']}
    
    explicacoes = {}
    
    # Texto da correta
    texto_correta = alts[correta]
    
    for letra, texto in alts.items():
        if letra == correta:
            explicacoes[letra] = {
                "tipo": "correta",
                "letra": letra,
                "titulo": f"✓ Resposta Correta (Alternativa {letra})",
                "fundamentacao_acerto": (
                    f"Você acertou com precisão técnica. A alternativa [{letra}] está plenamente alinhada ao "
                    f"requisito {clausula} da ABNT NBR ISO/IEC 17025:2017. {q.get('justificativa', '')} "
                    f"Essa conduta garante a rastreabilidade metrológica, a integridade operacional e a blindagem contra não conformidades em avaliações da Cgcre/Inmetro."
                ),
                "texto_leitura": f"Alternativa {letra}: {texto}. Resposta correta conforme o requisito {clausula} da norma."
            }
        else:
            # Gerar justificativa específica do erro
            motivo_erro = ""
            motivo_correta = ""
            
            # Análise semântica personalizada baseada no texto da alternativa
            t_lower = texto.lower()
            if "termo" in t_lower or "assunção de risco" in t_lower or "declaração" in t_lower:
                motivo_erro = (
                    f"A assinatura de termos internos ou declarações de clientes não confere permissão para contornar ou violar requisitos mandatórios de métodos normatizados ou regras da ISO 17025. "
                    f"O compromisso com resultados válidos é intransigível, e acordos informais não têm validade perante auditorias da Cgcre."
                )
            elif "subordinado" in t_lower or "gerência de produção" in t_lower or "hierárqu" in t_lower or "metas fabris" in t_lower:
                motivo_erro = (
                    f"Cair na armadilha da subordinação hierárquica é um dos erros mais graves em laboratórios de primeira parte. "
                    f"A ISO 17025 exige que a equipe analítica seja blindada de pressões de produção e prazos comerciais; a chefia de operação não pode determinar nem alterar resultados ou métodos de bancada."
                )
            elif "estimativa" in t_lower or "cálculo matemático" in t_lower or "preliminar" in t_lower:
                motivo_erro = (
                    f"A substituição de medições experimentais reais por modelos de estimativa não respaldados pelo método normalizado "
                    f"invalida o ensaio e pode constituir fraude metrológica com sérias consequências regulatórias (especialmente no setor nuclear)."
                )
            elif "bonificação" in t_lower or "conforme" in t_lower or "produtividade" in t_lower:
                motivo_erro = (
                    f"Vincular ganhos financeiros ao fato de o lote ser 'conforme' ou à velocidade de emissão introduz um incentivo perverso e conflito direto de interesse, "
                    f"ferindo de morte o requisito 4.1.3 que proíbe influências comerciais sobre a integridade analítica."
                )
            elif "uma única vez" in t_lower or "dois anos" in t_lower or "estática" in t_lower:
                motivo_erro = (
                    f"A norma exige explicitamente que o gerenciamento de riscos ocorra em uma base contínua (ongoing basis). "
                    f"Manter matrizes sem atualização periódica após novas contratações ou rotinas analíticas gera não conformidade imediata."
                )
            elif "recusar" in t_lower or "sigilo" in t_lower or "absoluto" in t_lower:
                motivo_erro = (
                    f"O dever de confidencialidade não é absoluto frente à lei. Requisições formais de órgãos fiscalizadores ou judiciais devem ser cumpridas, "
                    f"sendo dever do laboratório notificar o cliente previamente, salvo proibição judicial expressa."
                )
            elif "apenas a diretoria" in t_lower or "apenas o gerente" in t_lower:
                motivo_erro = (
                    f"A ISO 17025 (requisito 5.6) exige que os analistas e operadores de bancada tenham autoridade delegada e recursos para interromper imediatamente ensaios com desvios, "
                    f"sem necessidade de esperar por aprovações burocráticas demoradas."
                )
            elif "reprovado" in t_lower and ("qualquer erro" in t_lower or "carimbo" in t_lower):
                motivo_erro = (
                    f"Equipamento com erro não está automaticamente reprovado. O critério metrológico exige confrontar a soma do módulo do erro com a incerteza expandida frente ao Erro Máximo Admissível do processo (|Erro| + U <= EMA). "
                    f"Se a soma estiver dentro da tolerância do método, o instrumento está perfeitamente apto para uso."
                )
            elif "data exata" in t_lower or "dia/mês/ano" in t_lower or "etiqueta física" in t_lower:
                motivo_erro = (
                    f"Este é um dos mitos mais comuns de auditoria. A ISO 17025 exige que o status de calibração seja identificável pelo operador (requisito 6.4.8), "
                    f"mas o formato exato da etiqueta ou o controle via sistema informatizado é decisão do laboratório, não havendo exigência de formato rígido."
                )
            elif "corretivo" in t_lower or "borracha" in t_lower or "rasgar" in t_lower or "apagar" in t_lower:
                motivo_erro = (
                    f"O uso de corretivo líquido, borracha ou eliminação de registros originais viola frontalmente o requisito 7.5.2. "
                    f"Emendas em registros devem preservar o dado anterior legível, registrando quem alterou e a data da correção para manter rastreabilidade total."
                )
            elif "proíbe" in t_lower or "fmea" in t_lower or "iso 31000" in t_lower or "compulsóri" in t_lower:
                motivo_erro = (
                    f"A ISO 17025 adota mentalidade de risco (8.5), mas não impõe metodologias complexas como FMEA nem certificação na ISO 31000. "
                    f"O laboratório tem autonomia para escolher a ferramenta que melhor atenda sua realidade."
                )
            elif "fluxograma" in t_lower or "10 seções" in t_lower or "papel" in t_lower:
                motivo_erro = (
                    f"A ISO 17025 não impõe formatos engessados para procedimentos (POP). Fluxogramas, vídeos e infográficos são plenamente válidos, "
                    f"desde que controlados e aprovados, trazendo inclusive maior eficácia operacional."
                )
            else:
                motivo_erro = (
                    f"A alternativa [{letra}] adota uma premissa incompatível com a norma ou generaliza uma prática não requerida. "
                    f"Ao aplicá-la na rotina, o laboratório cria vulnerabilidades metrológicas, riscos de auditoria ou retrabalho desnecessário."
                )
            
            motivo_correta = (
                f"Por outro lado, a alternativa [{correta}] é a correta porque atende rigorosamente ao requisito {clausula}: "
                f"'{texto_correta}'. Essa formulação preserva a consistência dos dados, a conformidade de acreditação e a imparcialidade operacional."
            )
            
            explicacoes[letra] = {
                "tipo": "incorreta",
                "letra": letra,
                "titulo": f"✖ Atenção: Alternativa {letra} Incorreta",
                "por_que_esta_incorreta": motivo_erro,
                "por_que_outra_e_correta": motivo_correta,
                "gabarito_correto": correta,
                "texto_leitura": f"Alternativa {letra}: {texto}. Esta alternativa está incorreta. A resposta correta é a letra {correta}."
            }
            
    return explicacoes

def enriquecer_todas_questoes():
    with open('questoes_simulado.json', 'r', encoding='utf-8') as f:
        qs = json.load(f)
    
    print(f"Processando {len(qs)} questoes...")
    for q in qs:
        q['explicacoes_detalhadas'] = gerar_diagnostico_alternativas(q)
        # Adicionar caminhos de áudio padronizados
        qid = q['id']
        q['audio_enunciado'] = f"Audios_Simulado/{qid}_enunciado.mp3"
        for alt in q['alternativas']:
            letra = alt['letra']
            alt['audio_alt'] = f"Audios_Simulado/{qid}_alt_{letra}.mp3"
    
    with open('questoes_simulado.json', 'w', encoding='utf-8') as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)
    
    print("questoes_simulado.json atualizado com sucesso com explicações detalhadas por alternativa!")

if __name__ == '__main__':
    enriquecer_todas_questoes()
