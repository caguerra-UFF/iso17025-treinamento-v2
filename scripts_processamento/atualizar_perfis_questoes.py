# -*- coding: utf-8 -*-
"""
Atualiza questoes_simulado.json adicionando o perfil profissional metrológico:
- 'tecnico': Corpo Técnico (Operação de Bancada, Equipamentos, Incerteza, Ensaios e Calibração)
- 'gerencial': Corpo Gerencial (Liderança, Governança, Imparcialidade, Riscos e Auditorias)
- 'geral': Geral / Institucional (Cultura da Qualidade, Ética, Sigilo, Ouvidoria e Conceitos Transversais)
"""

import json

PERFIS_MAP = {
    # 🛠️ CORPO TÉCNICO (22 questões)
    "Q_6.3_01": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Controle de condições ambientais, contaminação cruzada e infraestrutura de bancada."
    },
    "Q_6.4_01": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Critérios metrológicos de aceitação de calibração (|Erro| + U <= EMA)."
    },
    "Q_6.4_02": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Identificação e etiquetagem prática de status de calibração em bancada."
    },
    "Q_6.4_03": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Gestão de sobrecarga, isolamento de equipamento avariado e segregação física."
    },
    "Q_6.4_04": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Execução de checagens intermediárias para manutenção da confiança metrológica."
    },
    "Q_6.4_05": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Aplicação obrigatória de fatores e curvas de correção em cálculos analíticos."
    },
    "Q_6.4_06": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Intercambialidade de acessórios críticos e comprovação prévia de desempenho."
    },
    "Q_6.4_07": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Manutenção de prontuários históricos e registros de calibração de instrumentos."
    },
    "Q_6.5_01": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Cadeia ininterrupta de calibrações e rastreabilidade metrológica ao SI."
    },
    "Q_6.5_02": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Critérios técnicos para uso de Materiais de Referência Certificados (MRC) e validade."
    },
    "Q_7.2_01": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Diferença prática entre verificação de métodos normalizados e validação ampla."
    },
    "Q_7.3_01": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Execução de planos de amostragem representativa e registros de campo."
    },
    "Q_7.4_01": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Controle térmico de custódia, transporte e uso de frasco testemunha."
    },
    "Q_7.4_02": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Triagem e recepção de amostras com desvio e ressalva em registros primários."
    },
    "Q_7.5_01": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Contemporaneidade de anotações de bancada e rastreabilidade de emendas."
    },
    "Q_7.6_01": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Identificação de fontes e cálculo de componentes de incerteza de medição."
    },
    "Q_7.7_01": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Rotina de controle interno da qualidade, duplicatas cegas e padrões de checagem."
    },
    "Q_7.7_02": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Participação em Ensaios de Proficiência (PEP) segundo a NIT-DICLA-026."
    },
    "Q_7.7_03": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Interpretação e detecção de tendências analíticas em cartas-controle (Shewhart)."
    },
    "Q_7.8_03": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Aplicação da zona de dúvida e faixas de guarda na regra de decisão declarada."
    },
    "Q_7.8_04": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Segregação técnica entre resultados puros de ensaio e opiniões/interpretações."
    },
    "Q_7.11_01": {
        "perfil": "tecnico",
        "perfil_nome": "Corpo Técnico",
        "perfil_icone": "🛠️",
        "foco_perfil": "Validação de fórmulas, macros e bloqueio de células em planilhas Excel de cálculo."
    },

    # 👔 CORPO GERENCIAL (18 questões)
    "Q_4.1_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Blindagem da imparcialidade metrológica frente a pressões de prazos de clientes internos."
    },
    "Q_4.1_02": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Diretrizes de remuneração e mitigação de incentivos ligados a resultados de aprovação."
    },
    "Q_4.1_03": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Identificação contínua e mitigação documental de riscos à imparcialidade."
    },
    "Q_5.1_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Estrutura legal do laboratório e enquadramento institucional (NIT-DICLA-031)."
    },
    "Q_5.2_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Definição formal de responsabilidade geral e autoridade sobre as operações."
    },
    "Q_5.5_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Empoderamento funcional e autoridade para interromper ensaios com desvios."
    },
    "Q_5.7_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Gestão de mudanças estruturais sem perda de integridade do Sistema de Gestão."
    },
    "Q_6.2_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Política de autorização formal, monitoramento e qualificação de competências."
    },
    "Q_6.6_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Critérios de homologação e qualificação de fornecedores críticos e calibrações RBC."
    },
    "Q_7.1_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Análise crítica de pedidos e pactuação contratual prévia de regras de decisão."
    },
    "Q_7.9_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Garantia de independência na condução e aprovação do desfecho de reclamações."
    },
    "Q_7.10_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Gestão do trabalho não conforme e tomada de decisão sobre impacto retroativo."
    },
    "Q_7.10_02": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Critérios formais e competência designada para autorizar retomada de trabalhos."
    },
    "Q_8.1_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Arquitetura do sistema de gestão: distinção estratégica entre Opção A e Opção B."
    },
    "Q_8.5_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Abordagem baseada em riscos e oportunidades sem formalismo excessivo ou FMEA compulsório."
    },
    "Q_8.7_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Investigação da causa raiz de desvios e verificação mandatória de eficácia."
    },
    "Q_8.8_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Planejamento de auditorias internas e garantia de independência dos auditores."
    },
    "Q_8.9_01": {
        "perfil": "gerencial",
        "perfil_nome": "Corpo Gerencial",
        "perfil_icone": "👔",
        "foco_perfil": "Condução da análise crítica pela direção com avaliação mandatória de todas as entradas."
    },

    # 🌐 GERAL / INSTITUCIONAL (10 questões)
    "Q_4.1_04": {
        "perfil": "geral",
        "perfil_nome": "Geral / Institucional",
        "perfil_icone": "🌐",
        "foco_perfil": "Conscientização sobre canais seguros e proteção de ouvidoria (Fala.BR)."
    },
    "Q_4.2_01": {
        "perfil": "geral",
        "perfil_nome": "Geral / Institucional",
        "perfil_icone": "🌐",
        "foco_perfil": "Obrigações de confidencialidade e procedimentos para quebra de sigilo por força de lei."
    },
    "Q_4.2_02": {
        "perfil": "geral",
        "perfil_nome": "Geral / Institucional",
        "perfil_icone": "🌐",
        "foco_perfil": "Tratamento sigiloso de informações obtidas de terceiros e reguladores."
    },
    "Q_5.3_01": {
        "perfil": "geral",
        "perfil_nome": "Geral / Institucional",
        "perfil_icone": "🌐",
        "foco_perfil": "Abrangência das operações: instalações permanentes, móveis e atividades em campo."
    },
    "Q_7.8_01": {
        "perfil": "geral",
        "perfil_nome": "Geral / Institucional",
        "perfil_icone": "🌐",
        "foco_perfil": "Estrutura essencial e elementos obrigatórios de relatórios de ensaio e calibração."
    },
    "Q_7.8_02": {
        "perfil": "geral",
        "perfil_nome": "Geral / Institucional",
        "perfil_icone": "🌐",
        "foco_perfil": "Regras normativas para emissão de emendas e suplementos a relatórios já emitidos."
    },
    "Q_7.11_02": {
        "perfil": "geral",
        "perfil_nome": "Geral / Institucional",
        "perfil_icone": "🌐",
        "foco_perfil": "Segurança da informação, integridade de arquivos e testes periódicos de restauração de backup."
    },
    "Q_8.2_01": {
        "perfil": "geral",
        "perfil_nome": "Geral / Institucional",
        "perfil_icone": "🌐",
        "foco_perfil": "Políticas e objetivos da qualidade comunicados e compreendidos por toda a equipe."
    },
    "Q_MITOS_01": {
        "perfil": "geral",
        "perfil_nome": "Geral / Institucional",
        "perfil_icone": "🌐",
        "foco_perfil": "Desmistificação da norma: eliminação da exigência de Manual da Qualidade físico compulsório."
    },
    "Q_8.6_01": {
        "perfil": "geral",
        "perfil_nome": "Geral / Institucional",
        "perfil_icone": "🌐",
        "foco_perfil": "Cultura de melhoria contínua e escuta ativa de retroalimentação de clientes."
    }
}

def main():
    with open('questoes_simulado.json', 'r', encoding='utf-8') as f:
        questoes = json.load(f)

    atualizados = 0
    contagem_perfis = {"tecnico": 0, "gerencial": 0, "geral": 0}

    for q in questoes:
        qid = q["id"]
        if qid in PERFIS_MAP:
            info = PERFIS_MAP[qid]
            q["perfil"] = info["perfil"]
            q["perfil_nome"] = info["perfil_nome"]
            q["perfil_icone"] = info["perfil_icone"]
            q["foco_perfil"] = info["foco_perfil"]
            atualizados += 1
            contagem_perfis[info["perfil"]] += 1
        else:
            print(f"ALERTA: Questao {qid} nao encontrada no mapa de perfis!")

    with open('questoes_simulado.json', 'w', encoding='utf-8') as f:
        json.dump(questoes, f, ensure_ascii=False, indent=2)

    print(f"Sucesso: {atualizados}/{len(questoes)} questoes atualizadas com perfil.")
    print(f"Distribuicao: {contagem_perfis}")

if __name__ == '__main__':
    main()
