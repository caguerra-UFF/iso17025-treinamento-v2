# -*- coding: utf-8 -*-
"""
Gerador do banco de questoes estruturado: questoes_simulado.json
Baseado na ABNT NBR ISO/IEC 17025:2017, transcricoes da Eletronuclear,
guias tecnicos e debates de especialistas (Thalita & Francisca).
"""

import json
import os

# Carrega dados_normativos para buscar referencias exatas
with open('dados_normativos.json', 'r', encoding='utf-8') as f:
    normativos = json.load(f)

norm_map = {item['canonical_clause']: item for item in normativos}
norm_by_id = {item['item_id']: item for item in normativos}

def find_ref(clause, default_id=None):
    if default_id and default_id in norm_by_id:
        return default_id
    if clause in norm_map:
        return norm_map[clause]['item_id']
    for c, it in norm_map.items():
        if c.startswith(clause):
            return it['item_id']
    return normativos[0]['item_id']

questoes = [
    # =========================================================================
    # SEÇÃO 4: REQUISITOS GERAIS
    # =========================================================================
    {
        "id": "Q_4.1_01",
        "secao_raiz": "4",
        "clausula": "4.1",
        "clausula_nome": "4.1 Imparcialidade",
        "nivel": "Intermediário",
        "tema": "Pressão de Cliente Interno e Prazos Metrológicos",
        "enunciado": "A gerência de operação de uma central nuclear solicita que o laboratório de monitoramento ambiental antecipe a liberação do laudo de um ensaio microbiológico/físico-químico em 2 dias (reduzindo o tempo normatizado de incubação), sob a alegação de necessidade operacional urgente para liberação de um circuito. À luz da ABNT NBR ISO/IEC 17025:2017 (requisito 4.1.1 e 4.1.2):",
        "alternativas": [
            {"letra": "A", "texto": "O laboratório pode reduzir o tempo de incubação desde que a gerência de operação assine uma declaração de assunção de risco."},
            {"letra": "B", "texto": "A integridade técnica e a imparcialidade têm precedência sobre pressões de prazo internas, sendo vedado quebrar o método normatizado para atender exigências de clientes internos."},
            {"letra": "C", "texto": "Por se tratar de cliente interno pertencente à mesma pessoa jurídica, o laboratório é subordinado à gerência de produção e deve priorizar o cumprimento das metas fabris."},
            {"letra": "D", "texto": "O laudo pode ser emitido preliminarmente com base em estimativa matemática de crescimento biológico, regularizando-se posteriormente."}
        ],
        "correta": "B",
        "justificativa": "O requisito 4.1 da ISO/IEC 17025 determina que as atividades laboratoriais devem ser realizadas de forma imparcial e estruturadas contra pressões comerciais, financeiras ou operacionais. Demandas de clientes internos não justificam a quebra de requisitos técnicos de métodos normatizados.",
        "clausula_iso": "4.1.1 e 4.1.2",
        "item_id_referencia": "ISO_4.1_0409_8_4",
        "audio_ref": "Trechos_Aulas/Trecho_Item_001_ISO_4_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_8_4_Reclamacoes_Cliente_Interno_e_Limites_Tecnicos.mp3"
    },
    {
        "id": "Q_4.1_02",
        "secao_raiz": "4",
        "clausula": "4.1",
        "clausula_nome": "4.1 Imparcialidade",
        "nivel": "Auditoria / Avançado",
        "tema": "Remuneração Variável e Salvaguardas de Imparcialidade",
        "enunciado": "Um laboratório instituiu um programa de bonificação financeira para os químicos e analistas baseado em dois critérios: 1) número total de laudos liberados por mês e 2) índice de conformidade dos lotes ensaiados (maior bônus quanto menor o número de reprovações). Avaliando esta política frente ao requisito 4.1.3 da ISO/IEC 17025:2017:",
        "alternativas": [
            {"letra": "A", "texto": "A política é plenamente aceitável, pois incentiva a produtividade e a melhoria contínua da qualidade do produto."},
            {"letra": "B", "texto": "A bonificação por velocidade é válida, mas a bonificação atrelada a resultados conformes compromete diretamente a imparcialidade e o julgamento técnico dos analistas, constituindo não conformidade."},
            {"letra": "C", "texto": "A norma não faz qualquer restrição a modelos de remuneração ou bônus, deixando a política salarial a exclusivo critério corporativo."},
            {"letra": "D", "texto": "A política seria conforme somente se os analistas assinassem uma declaração de que o bônus financeiro não afeta sua ética profissional."}
        ],
        "correta": "B",
        "justificativa": "O requisito 4.1.3 estabelece que o laboratório não deve permitir que pressões comerciais, financeiras ou de outra natureza comprometam sua imparcialidade. Condicionar bônus a resultados 'conformes' cria um conflito de interesse direto e compromete a integridade dos laudos.",
        "clausula_iso": "4.1.3",
        "item_id_referencia": "ISO_4.1_1009_10_09_-_Parte_1_10_5",
        "audio_ref": "Trechos_Aulas/Trecho_Item_006_ISO_4_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_10_5_Salvaguardas_Pressoes_Comerciais.mp3"
    },
    {
        "id": "Q_4.1_03",
        "secao_raiz": "4",
        "clausula": "4.1",
        "clausula_nome": "4.1 Imparcialidade",
        "nivel": "Auditoria / Avançado",
        "tema": "Identificação Contínua de Riscos à Imparcialidade",
        "enunciado": "Durante uma auditoria externa da Cgcre, o avaliador constata que o laboratório possui uma Matriz de Riscos à Imparcialidade elaborada há dois anos, sem nenhuma revisão registrada, mesmo tendo contratado 4 novos analistas e inaugurado uma linha de ensaios com clientes externos. O laboratório argumenta que a planilha original foi aprovada pela Alta Direção. O posicionamento do auditor deve ser:",
        "alternativas": [
            {"letra": "A", "texto": "Aceitar a evidência, pois a ISO/IEC 17025 exige apenas que os riscos sejam identificados uma única vez no momento da implantação."},
            {"letra": "B", "texto": "Apontar não conformidade com o requisito 4.1.4, pois a identificação e o gerenciamento de riscos à imparcialidade devem ocorrer em uma base contínua."},
            {"letra": "C", "texto": "Aceitar a justificativa, desde que nenhum dos novos analistas possua processo judicial pendente."},
            {"letra": "D", "texto": "Recomendar que o laboratório substitua a matriz de riscos por uma apólice de seguro contra fraudes metrológicas."}
        ],
        "correta": "B",
        "justificativa": "O requisito 4.1.4 exige taxativamente que o laboratório identifique riscos à sua imparcialidade em uma base contínua (ongoing basis), abrangendo riscos decorrentes de suas atividades, relacionamentos e de seu pessoal.",
        "clausula_iso": "4.1.4",
        "item_id_referencia": "ISO_4.1_1009_10_09_-_Parte_1_10_6",
        "audio_ref": "Trechos_Aulas/Trecho_Item_007_ISO_4_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_10_6_Identificacao_Continua_Riscos_Imparcialidade.mp3"
    },
    {
        "id": "Q_4.2_01",
        "secao_raiz": "4",
        "clausula": "4.2",
        "clausula_nome": "4.2 Confidencialidade",
        "nivel": "Intermediário",
        "tema": "Divulgação Legal de Dados e Notificação ao Cliente",
        "enunciado": "Um órgão de fiscalização ambiental (ex: INEA / IBAMA) emite uma intimação oficial exigindo que o laboratório forneça os laudos brutos e o histórico analítico de efluentes de uma determinada empresa. De acordo com o requisito 4.2.2 da ISO/IEC 17025:2017:",
        "alternativas": [
            {"letra": "A", "texto": "O laboratório deve recusar o envio dos dados, pois o sigilo contratual é absoluto e intransponível frente a órgãos públicos."},
            {"letra": "B", "texto": "O laboratório deve fornecer as informações exigidas e notificar previamente o cliente sobre os dados fornecidos, a menos que tal notificação seja expressamente proibida por lei."},
            {"letra": "C", "texto": "O laboratório só pode repassar os dados caso o cliente autorize formalmente por escrito em até 30 dias."},
            {"letra": "D", "texto": "O laboratório entrega os dados em segredo absoluto, sendo terminantemente proibido alertar o cliente sob pena de infração ética."}
        ],
        "correta": "B",
        "justificativa": "Conforme o requisito 4.2.2, quando o laboratório for obrigado por lei ou autorizado por disposições contratuais a divulgar informações confidenciais, o cliente deve ser notificado sobre as informações fornecidas, a menos que seja proibido por lei.",
        "clausula_iso": "4.2.2",
        "item_id_referencia": "ISO_4.2_1009_10_09_-_Parte_2_10_11",
        "audio_ref": "Trechos_Aulas/Trecho_Item_011_ISO_4_2.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_10_11_Excecoes_Legais_Notificacao_Previa.mp3"
    },
    {
        "id": "Q_4.2_02",
        "secao_raiz": "4",
        "clausula": "4.2",
        "clausula_nome": "4.2 Confidencialidade",
        "nivel": "Intermediário",
        "tema": "Informações Obtidas de Terceiros e Sigilo",
        "enunciado": "O laboratório recebe de um reclamante ou de um órgão regulador informações desfavoráveis sobre um determinado cliente atendido pelo laboratório. Como o laboratório deve tratar essas informações recebidas de fontes externas, segundo a cláusula 4.2.3 da ISO 17025:2017?",
        "alternativas": [
            {"letra": "A", "texto": "Deve anexá-las imediatamente ao laudo público para alertar a sociedade."},
            {"letra": "B", "texto": "As informações obtidas sobre o cliente, a partir de fontes que não o próprio cliente, devem ser tratadas como confidenciais entre o cliente e o laboratório, mantendo sob sigilo a identidade do informante perante o cliente, a menos que acordado com a fonte."},
            {"letra": "C", "texto": "Deve convocar o cliente em audiência e revelar a identidade do informante para que ele possa tomar medidas judiciais."},
            {"letra": "D", "texto": "O laboratório não pode aceitar ou arquivar informações que não tenham sido enviadas formalmente pelo próprio cliente contratante."}
        ],
        "correta": "B",
        "justificativa": "O requisito 4.2.3 estipula que informações obtidas de outras fontes sobre o cliente devem ser tratadas como confidenciais, e a identidade da fonte não deve ser compartilhada com o cliente, a menos que haja concordância da fonte.",
        "clausula_iso": "4.2.3",
        "item_id_referencia": "ISO_4.2_1009_10_09_-_Parte_1_10_10",
        "audio_ref": "Trechos_Aulas/Trecho_Item_012_ISO_4_2.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_10_10_Clausula_4_2_Confidencialidade_Dever_Sigilo.mp3"
    },

    # =========================================================================
    # SEÇÃO 5: REQUISITOS DE ESTRUTURA
    # =========================================================================
    {
        "id": "Q_5.1_01",
        "secao_raiz": "5",
        "clausula": "5.1",
        "clausula_nome": "5.1 Personalidade Jurídica",
        "nivel": "Básico",
        "tema": "Responsabilidade Legal e Entidade Jurídica",
        "enunciado": "Um laboratório de monitoramento ambiental opera como departamento interno de uma grande empresa de energia (Eletronuclear). Para fins de acreditação na Cgcre conforme a ISO/IEC 17025:2017 e NIT-DICLA-031, qual é o requisito aplicável quanto à sua personalidade jurídica (Seção 5.1)?",
        "alternativas": [
            {"letra": "A", "texto": "O laboratório precisa abrir um CNPJ filial e constituir pessoa jurídica independente com capital social próprio."},
            {"letra": "B", "texto": "O laboratório deve ser uma entidade legal, ou parte definida de uma entidade legal, que seja legalmente responsável por suas atividades de laboratório."},
            {"letra": "C", "texto": "Laboratórios de primeira parte (internos) são isentos de comprovação de personalidade jurídica perante a Cgcre."},
            {"letra": "D", "texto": "A responsabilidade legal deve ser transferida individualmente para o CPF de cada químico e analista responsável."}
        ],
        "correta": "B",
        "justificativa": "O requisito 5.1 estabelece: 'O laboratório deve ser uma entidade legal, ou parte definida de uma entidade legal, que seja legalmente responsável por suas atividades de laboratório.' No caso de empresas como a Eletronuclear, a pessoa jurídica mantenedora responde legalmente pelas operações do laboratório.",
        "clausula_iso": "5.1",
        "item_id_referencia": "ISO_5.1_1009_10_09_-_Parte_2_10_12",
        "audio_ref": "Trechos_Aulas/Trecho_Item_013_ISO_5_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_10_12_Clausula_5_Personalidade_Juridica.mp3"
    },
    {
        "id": "Q_5.2_01",
        "secao_raiz": "5",
        "clausula": "5.2",
        "clausula_nome": "5.2 Identificação da Gerência",
        "nivel": "Intermediário",
        "tema": "Responsabilidade Geral pelo Laboratório",
        "enunciado": "A Cláusula 5.2 da ISO/IEC 17025:2017 exige a identificação da gerência que tenha a responsabilidade geral pelo laboratório. O principal propósito desta identificação formal é:",
        "alternativas": [
            {"letra": "A", "texto": "Definir quem será o único funcionário autorizado a assinar os laudos analíticos emitidos."},
            {"letra": "B", "texto": "Assegurar governança clara e autoridade executiva direta para a provisão de recursos necessários e sustentação contínua do Sistema de Gestão da Qualidade."},
            {"letra": "C", "texto": "Eliminar a necessidade de supervisão técnica nas bancadas analíticas."},
            {"letra": "D", "texto": "Cumprir uma exigência puramente cartorial sem qualquer reflexo prático na gestão operacional."}
        ],
        "correta": "B",
        "justificativa": "A identificação formal da gerência com responsabilidade geral (5.2) garante autoridade sobre a alocação de recursos financeiros, infraestrutura e pessoal, garantindo a sustentação e independência metrológica do laboratório.",
        "clausula_iso": "5.2",
        "item_id_referencia": "ISO_5.2_1009_10_09_-_Parte_2_10_12B",
        "audio_ref": "Trechos_Aulas/Trecho_Item_014_ISO_5_2.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_5_2_Identificacao_Gerencia_Geral.mp3"
    },
    {
        "id": "Q_5.5_01",
        "secao_raiz": "5",
        "clausula": "5.5",
        "clausula_nome": "5.5 Estrutura e Autoridade",
        "nivel": "Intermediário",
        "tema": "Autoridade para Interromper Ensaios com Desvios",
        "enunciado": "Um analista júnior nota que a temperatura do banho-maria de digestão ácida oscilou 8 °C acima da tolerância permitida pelo método normatizado. Ao consultar o requisito 5.6 da ISO/IEC 17025:2017, qual é a autoridade mandatória que o pessoal técnico do laboratório deve possuir?",
        "alternativas": [
            {"letra": "A", "texto": "Apenas a Diretoria Executiva da empresa tem autoridade para paralisar um lote analítico em andamento."},
            {"letra": "B", "texto": "O pessoal deve ter a autoridade e os recursos necessários para desempenhar suas funções, incluindo a autoridade de identificar e interromper desvios do sistema de gestão ou dos procedimentos de ensaio."},
            {"letra": "C", "texto": "O analista deve concluir o ensaio e omitir o desvio caso a amostra pertença a um cliente prioritário."},
            {"letra": "D", "texto": "O analista deve aplicar uma correção matemática informal e não documentar o desvio térmico."}
        ],
        "correta": "B",
        "justificativa": "O requisito 5.6 (alínea b) determina que o laboratório deve ter pessoal que, independentemente de outras responsabilidades, tenha a autoridade e os recursos necessários para identificar a ocorrência de desvios e iniciar ações para prevenir ou minimizar esses desvios.",
        "clausula_iso": "5.6",
        "item_id_referencia": "ISO_5.5_1009_10_09_-_Parte_2_10_12E",
        "audio_ref": "Trechos_Aulas/Trecho_Item_016_ISO_5_5.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_5_5_Organizacao_Responsabilidade_Autoridade.mp3"
    },
    {
        "id": "Q_5.7_01",
        "secao_raiz": "5",
        "clausula": "5.7",
        "clausula_nome": "5.7 Integridade do Sistema em Mudanças",
        "nivel": "Auditoria / Avançado",
        "tema": "Mudanças Organizacionais e Sustentação do SGQ",
        "enunciado": "Uma reestruturação corporativa transfere o laboratório para outra diretoria e substitui o software LIMS por uma plataforma integrada ERP. O requisito 5.7 da ISO/IEC 17025:2017 exige especificamente que a alta direção do laboratório assegure que:",
        "alternativas": [
            {"letra": "A", "texto": "Todas as análises sejam suspensas por 6 meses até que a transição corporativa termine."},
            {"letra": "B", "texto": "A integridade do sistema de gestão seja mantida quando mudanças no sistema de gestão forem planejadas e implementadas."},
            {"letra": "C", "texto": "Os manuais de qualidade antigos sejam descartados sem necessidade de retenção de histórico."},
            {"letra": "D", "texto": "A Cgcre seja solicitada a cancelar a acreditação e iniciar um processo de zero."}
        ],
        "correta": "B",
        "justificativa": "O requisito 5.7 estabelece: 'A alta direção do laboratório deve assegurar que: a) a comunicação seja estabelecida a respeito da eficácia do sistema de gestão (...); b) a integridade do sistema de gestão seja mantida quando mudanças no sistema de gestão forem planejadas e implementadas.'",
        "clausula_iso": "5.7",
        "item_id_referencia": "ISO_5.7_1009_10_09_-_Parte_2_10_13",
        "audio_ref": "Trechos_Aulas/Trecho_Item_018_ISO_5_7.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_5_7_Integridade_Sistema_Mudancas.mp3"
    },

    # =========================================================================
    # SEÇÃO 6: REQUISITOS DE RECURSOS
    # =========================================================================
    {
        "id": "Q_6.2_01",
        "secao_raiz": "6",
        "clausula": "6.2",
        "clausula_nome": "6.2 Pessoal",
        "nivel": "Intermediário",
        "tema": "Competência Técnica e Monitoramento Contínuo",
        "enunciado": "Um técnico recém-admitido apresenta currículo comprovando 10 anos de experiência em espectrometria de emissão óptica (ICP-OES) em outro laboratório. O laboratório pode colocá-lo imediatamente para emitir laudos oficiais no novo escopo sem avaliação interna? O que prescreve o requisito 6.2 da ISO/IEC 17025:2017?",
        "alternativas": [
            {"letra": "A", "texto": "Sim, a experiência pregressa comprovada em carteira de trabalho supre integralmente qualquer necessidade de comprovação interna."},
            {"letra": "B", "texto": "Não; o laboratório deve documentar os requisitos de competência, realizar a qualificação prática interna no seu método específico e autorizar formalmente o técnico antes de sua atuação na rotina."},
            {"letra": "C", "texto": "Sim, desde que o técnico possua registro ativo no Conselho Regional de Química (CRQ)."},
            {"letra": "D", "texto": "Não; a norma exige que todo novo funcionário passe por 2 anos de estágio supervisionado sem assinar nada."}
        ],
        "correta": "B",
        "justificativa": "O requisito 6.2.2 e 6.2.5 exige que o laboratório documente os requisitos de competência para cada função, avalie a eficácia do treinamento e autorize formalmente o pessoal para executar atividades laboratoriais específicas (métodos, equipamentos e emissão de laudos).",
        "clausula_iso": "6.2.2 e 6.2.5",
        "item_id_referencia": "ISO_6.2_1009_10_09_-_Parte_2_10_18",
        "audio_ref": "Trechos_Aulas/Trecho_Item_020_ISO_6_2.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_6_2_Competencia_Autorizacao_Pessoal.mp3"
    },
    {
        "id": "Q_6.3_01",
        "secao_raiz": "6",
        "clausula": "6.3",
        "clausula_nome": "6.3 Instalações e Condições Ambientais",
        "nivel": "Intermediário",
        "tema": "Contaminação Cruzada e Controle de Acesso",
        "enunciado": "Em um laboratório ambiental de monitoramento de usina nuclear, a sala de preparo de padrões de alta concentração de metais pesados divide a mesma bancada e o mesmo fluxo de ar com a sala de ensaios de nível ultra-traço em água desmineralizada. Sob a ótica do requisito 6.3 da ISO 17025:2017:",
        "alternativas": [
            {"letra": "A", "texto": "A prática é aceitável desde que o analista limpe a bancada com álcool 70% entre as preparações."},
            {"letra": "B", "texto": "O laboratório deve controlar e monitorar as instalações, assegurando separação eficaz entre áreas vizinhas nas quais haja atividades incompatíveis para evitar contaminação cruzada e invalidação dos resultados."},
            {"letra": "C", "texto": "A ISO 17025 só se preocupa com instalações de escritórios administrativos, não regulando o layout das bancadas."},
            {"letra": "D", "texto": "A contaminação é irrelevante, pois a incerteza analítica sempre absorve interferentes ambientais."}
        ],
        "correta": "B",
        "justificativa": "O requisito 6.3.4 determina que o laboratório deve controlar o acesso às áreas e que 'deve haver separação eficaz entre áreas vizinhas nas quais haja atividades incompatíveis', prevenindo contaminações que afetem a validade dos resultados.",
        "clausula_iso": "6.3.4",
        "item_id_referencia": "ISO_6.3_0209_1_9",
        "audio_ref": "Trechos_Aulas/Trecho_Item_022_ISO_6_3.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_1/Podcast_Parte1_Item_1_9_Cabines_Fluxo_Laminar.mp3"
    },
    {
        "id": "Q_6.4_01",
        "secao_raiz": "6",
        "clausula": "6.4",
        "clausula_nome": "6.4 Equipamentos",
        "nivel": "Auditoria / Avançado",
        "tema": "Critério de Aceitação de Calibração (|Erro| + U <= EMA)",
        "enunciado": "Um termômetro digital com resolução de 0,01 °C é utilizado em banho de DBO cuja especificação do método exige temperatura de (20,0 ± 0,5) °C (Erro Máximo Admissível = 0,5 °C). O certificado de calibração emitido por laboratório acreditado pela Cgcre informa: Erro Sistemático (Tendência) = +0,35 °C e Incerteza Expandida (k=2) = 0,10 °C. Aplicando a regra clássica de aceitação metrológica (|Erro| + U ≤ EMA):",
        "alternativas": [
            {"letra": "A", "texto": "O equipamento está reprovado, pois qualquer erro superior a 0,1 °C invalida o banho-maria."},
            {"letra": "B", "texto": "O equipamento está aprovado frente ao uso pretendido, pois |+0,35| + 0,10 = 0,45 °C, valor estritamente menor que o EMA de 0,5 °C."},
            {"letra": "C", "texto": "O equipamento só pode ser aprovado se o certificado trouxer um carimbo escrito 'APROVADO' colocado pelo calibrador externo."},
            {"letra": "D", "texto": "A incerteza não deve ser somada ao erro, bastando comparar o erro diretamente com a tolerância."}
        ],
        "correta": "B",
        "justificativa": "Para demonstrar que o equipamento atende aos requisitos do método (6.4.4 e 6.4.5), a análise crítica do certificado compara a soma da magnitude do erro com a incerteza expandida frente ao Erro Máximo Admissível do processo (|Erro| + U = 0,45 °C <= 0,50 °C), resultando em aprovação metrológica formal.",
        "clausula_iso": "6.4.4 e 6.4.5",
        "item_id_referencia": "ISO_6.4.5_0209_1_18",
        "audio_ref": "Trechos_Aulas/Trecho_Item_026_ISO_6_4_5.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_7_2_Formula_Aprovacao_Equipamentos.mp3"
    },
    {
        "id": "Q_6.4_02",
        "secao_raiz": "6",
        "clausula": "6.4",
        "clausula_nome": "6.4 Equipamentos",
        "nivel": "Intermediário",
        "tema": "Etiquetagem de Equipamentos e Mito de Auditoria",
        "enunciado": "Um avaliador afirma durante a auditoria interna: 'A etiqueta colada no equipamento DEVE obrigatoriamente conter a data do dia/mês/ano exato da próxima calibração, pois isso é uma exigência textual expressa da ISO 17025'. Como a equipe da qualidade deve responder tecnicamente a essa afirmação?",
        "alternativas": [
            {"letra": "A", "texto": "Concordar de imediato, pois a norma exige etiquetas físicas padronizadas com a data futura da calibração em todos os instrumentos."},
            {"letra": "B", "texto": "Esclarecer que a ISO 17025 (item 6.4.8) exige que os equipamentos sujeitos à calibração sejam rotulados, codificados ou de outra forma identificados para permitir que o usuário reconheça facilmente o status da calibração ou o período de validade; o formato exato da etiqueta ou controle via software é decisão do laboratório."},
            {"letra": "C", "texto": "Afirmar que a norma proíbe expressamente qualquer tipo de etiqueta física nos aparelhos."},
            {"letra": "D", "texto": "Informar que a data da próxima calibração deve ser definida pelo laboratório de calibração que emitiu o certificado, e nunca pelo usuário."}
        ],
        "correta": "B",
        "justificativa": "O requisito 6.4.8 da ISO/IEC 17025:2017 exige que o status de calibração seja identificável para permitir ao usuário saber se o equipamento está válido. Exigir um formato específico de etiqueta com data futura é um mito/generalização excessiva; o laboratório pode gerenciar o status via sistema informatizado ou etiquetas simplificadas.",
        "clausula_iso": "6.4.8",
        "item_id_referencia": "ISO_6.4.8_0209_1_21",
        "audio_ref": "Trechos_Aulas/Trecho_Item_032_ISO_6_4_8.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_1/Podcast_Parte1_Item_1_21_Etiqueta_Status_Equipamento.mp3"
    },
    {
        "id": "Q_6.4_03",
        "secao_raiz": "6",
        "clausula": "6.4",
        "clausula_nome": "6.4 Equipamentos",
        "nivel": "Intermediário",
        "tema": "Equipamento com Sobrecarga ou Defeito e Impacto Retroativo",
        "enunciado": "Uma balança analítica sofreu uma queda acidental de um frasco pesado e começou a apresentar leituras instáveis com deriva de 5 mg. De acordo com o requisito 6.4.9 da ISO/IEC 17025:2017, quais ações devem ser tomadas imediatamente pelo laboratório?",
        "alternativas": [
            {"letra": "A", "texto": "Apenas recalibrar a balança no final do mês sem parar a rotina."},
            {"letra": "B", "texto": "Retirar o equipamento de serviço, isolá-lo ou etiquetá-lo claramente como fora de uso e examinar o efeito do defeito ou desvio sobre os ensaios realizados anteriormente (requisito 7.10 de Trabalho Não Conforme)."},
            {"letra": "C", "texto": "Continuar usando a balança para pesagens que não exijam precisão sem registrar nada."},
            {"letra": "D", "texto": "Descartar a balança imediatamente no lixo para não deixar evidências em auditoria."}
        ],
        "correta": "B",
        "justificativa": "O item 6.4.9 determina que equipamentos submetidos a sobrecarga ou manuseio inadequado, ou que dêem resultados duvidosos, devem ser retirados de serviço, isolados/rotulados, e o laboratório deve examinar o efeito sobre ensaios anteriores conforme o procedimento de trabalho não conforme (7.10).",
        "clausula_iso": "6.4.9",
        "item_id_referencia": "ISO_6.4.9_0209_1_22",
        "audio_ref": "Trechos_Aulas/Trecho_Item_033_ISO_6_4_9.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_1/Podcast_Parte1_Item_1_22_Equipamento_Defeituoso_Retirada_Servico.mp3"
    },
    {
        "id": "Q_6.4_04",
        "secao_raiz": "6",
        "clausula": "6.4",
        "clausula_nome": "6.4 Equipamentos",
        "nivel": "Auditoria / Avançado",
        "tema": "Checagens Intermediárias vs Recalibração Completa",
        "enunciado": "Um pHmetro foi calibrado externamente por laboratório acreditado com validade estimada de 1 ano. Na rotina diária, os técnicos realizam a checagem com soluções tampão de pH 4,01, 7,00 e 10,01 antes de iniciar os ensaios. Sob o requisito 6.4.10 da ISO 17025:2017:",
        "alternativas": [
            {"letra": "A", "texto": "Essa prática é incorreta, pois checagens intermediárias substituem e dispensam a calibração periódica anual."},
            {"letra": "B", "texto": "Essa prática é plenamente conforme; quando forem necessárias checagens intermediárias para manter a confiança no desempenho do equipamento, essas checagens devem ser realizadas segundo um procedimento definido."},
            {"letra": "C", "texto": "A ISO 17025 proíbe que o próprio usuário faça checagens com tampões de pH."},
            {"letra": "D", "texto": "As checagens intermediárias só têm valor se forem realizadas na presença do avaliador da Cgcre."}
        ],
        "correta": "B",
        "justificativa": "O requisito 6.4.10 estabelece que checagens intermediárias devem ser planejadas e executadas para manter a confiança no desempenho metrológico dos equipamentos entre os ciclos formais de calibração.",
        "clausula_iso": "6.4.10",
        "item_id_referencia": "ISO_6.4.10_0209_1_23",
        "audio_ref": "Trechos_Aulas/Trecho_Item_034_ISO_6_4_10.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_1/Podcast_Parte1_Item_1_23_Checagens_Intermediarias.mp3"
    },
    {
        "id": "Q_6.5_01",
        "secao_raiz": "6",
        "clausula": "6.5",
        "clausula_nome": "6.5 Rastreabilidade Metrológica",
        "nivel": "Intermediário",
        "tema": "Cadeia Ininterrupta de Rastreabilidade ao SI",
        "enunciado": "Para demonstrar a rastreabilidade metrológica de suas medições ao Sistema Internacional de Unidades (SI) nos termos do requisito 6.5 da ISO 17025:2017, qual é a rota primária e amplamente reconhecida para os serviços de calibração?",
        "alternativas": [
            {"letra": "A", "texto": "Contratar qualquer oficina de manutenção que possua CNPJ ativo no ramo de conserto elétrico."},
            {"letra": "B", "texto": "Utilizar serviços de calibração providos por Institutos Nacionais de Metrologia (como INMETRO/BIPM) ou laboratórios de calibração acreditados por organismos signatários do acordo ILAC MRA (como os laboratórios da RBC acreditados pela Cgcre)."},
            {"letra": "C", "texto": "Comprar equipamentos importados que venham com certificado de fábrica em língua estrangeira sem menção à incerteza."},
            {"letra": "D", "texto": "Elaborar um certificado de calibração interno assinado pelo próprio gerente do laboratório de ensaios sem padrões de referência."}
        ],
        "correta": "B",
        "justificativa": "O requisito 6.5.2 e o Anexo A da ISO/IEC 17025 determinam que a rastreabilidade ao SI é assegurada por meio de calibração fornecida por laboratório competente (acreditado por organismo signatário do ILAC MRA, como a Cgcre/Inmetro) ou por Institutos Nacionais de Metrologia.",
        "clausula_iso": "6.5.2",
        "item_id_referencia": "ISO_6.5.1_0209_1_29",
        "audio_ref": "Trechos_Aulas/Trecho_Item_042_ISO_6_5_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_1/Podcast_Parte1_Item_1_29_Rastreabilidade_Metrologica_SI.mp3"
    },
    {
        "id": "Q_6.6_01",
        "secao_raiz": "6",
        "clausula": "6.6",
        "clausula_nome": "6.6 Produtos e Serviços Externos",
        "nivel": "Intermediário",
        "tema": "Qualificação de Fornecedores Críticos e Serviços Subcontratados",
        "enunciado": "O laboratório contrata um laboratório externo para realizar ensaios de radioquímica que não constam na sua capacidade imediata, e os resultados serão incorporados ao relatório entregue ao cliente. Conforme a Cláusula 6.6 da ISO/IEC 17025:2017:",
        "alternativas": [
            {"letra": "A", "texto": "O laboratório pode subcontratar qualquer entidade sem comunicar o cliente, pois o sigilo comercial protege essa relação."},
            {"letra": "B", "texto": "O laboratório deve ter procedimento para avaliar, selecionar e monitorar o desempenho do provedor externo, comunicar formalmente os requisitos técnicos e obter aprovação prévia do cliente para o uso de serviço externo."},
            {"letra": "C", "texto": "A responsabilidade pela qualidade do resultado passa a ser 100% do fornecedor contratado, isentando o laboratório primário de qualquer questionamento."},
            {"letra": "D", "texto": "A ISO 17025 proíbe sumariamente qualquer tipo de contratação de ensaios de provedores externos."}
        ],
        "correta": "B",
        "justificativa": "O requisito 6.6.2 exige que o laboratório defina critérios para qualificar, avaliar e monitorar provedores externos, comunicando claramente seus requisitos. Além disso, o requisito 7.1.1(c) e 7.8.2.1(p) determinam que o cliente seja informado e concorde quando atividades laboratoriais forem providas externamente.",
        "clausula_iso": "6.6.2",
        "item_id_referencia": "ISO_6.6.1_0209_1_35",
        "audio_ref": "Trechos_Aulas/Trecho_Item_048_ISO_6_6_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_1/Podcast_Parte1_Item_1_35_Provedores_Externos_Compras.mp3"
    },

    # =========================================================================
    # SEÇÃO 7: REQUISITOS DE PROCESSOS
    # =========================================================================
    {
        "id": "Q_7.1_01",
        "secao_raiz": "7",
        "clausula": "7.1",
        "clausula_nome": "7.1 Análise Crítica de Pedidos e Propostas",
        "nivel": "Intermediário",
        "tema": "Acordo Prévio sobre Regra de Decisão",
        "enunciado": "Um cliente solicita formalmente que o laboratório emita uma 'Declaração de Conformidade' no relatório de ensaio, atestando se a água desmineralizada atende à especificação nuclear de condutividade (< 0,1 µS/cm). De acordo com os requisitos 7.1.3 e 7.8.6 da ISO/IEC 17025:2017:",
        "alternativas": [
            {"letra": "A", "texto": "O laboratório deve recusar emitir qualquer declaração de conformidade, pois isso é atribuição exclusiva de organismos de certificação."},
            {"letra": "B", "texto": "A regra de decisão a ser empregada deve ser claramente definida, acordada previamente com o cliente e documentada antes da realização do ensaio, levando em consideração o nível de risco e a incerteza de medição associada."},
            {"letra": "C", "texto": "O laboratório pode aplicar qualquer critério próprio no momento de emitir o laudo sem necessidade de consulta ou acordo prévio com o cliente."},
            {"letra": "D", "texto": "A regra de decisão consiste apenas em verificar se o valor numérico é menor que 0,1, ignorando a incerteza."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.1.3 determina que, quando o cliente solicitar uma declaração de conformidade com uma especificação ou norma, a especificação e a regra de decisão devem ser claramente definidas e acordadas com o cliente antes do início dos trabalhos.",
        "clausula_iso": "7.1.3",
        "item_id_referencia": "ISO_7.1.3_0309_13_4",
        "audio_ref": "Trechos_Aulas/Trecho_Item_055_ISO_7_1_3.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_2/Podcast_Parte2_Item_13_4_Regra_de_Decisao_Acordo_Cliente.mp3"
    },
    {
        "id": "Q_7.2_01",
        "secao_raiz": "7",
        "clausula": "7.2",
        "clausula_nome": "7.2 Seleção e Verificação/Validação de Métodos",
        "nivel": "Auditoria / Avançado",
        "tema": "Verificação de Método Normalizado vs Validação de Método Interno",
        "enunciado": "Qual é a diferença metrológica fundamental perante a ISO/IEC 17025:2017 entre a 'verificação' de um método padronizado (ex: Standard Methods ou ASTM) e a 'validação' de um método desenvolvido internamente pelo laboratório?",
        "alternativas": [
            {"letra": "A", "texto": "Não há nenhuma diferença; os termos são sinônimos e exigem rigorosamente os mesmos ensaios e ensaios interlaboratoriais."},
            {"letra": "B", "texto": "A verificação (7.2.1.5) comprova que o laboratório tem capacidade de atingir o desempenho documentado no método normalizado antes de introduzi-lo; a validação (7.2.2) é a confirmação por exame e evidência objetiva de que os requisitos particulares para o uso pretendido são atendidos em métodos não normalizados ou modificados."},
            {"letra": "C", "texto": "Métodos normalizados dispensam qualquer tipo de comprovação experimental interna antes do uso rotineiro."},
            {"letra": "D", "texto": "Métodos internos só podem ser validados por peritos judiciais nomeados pela Cgcre."}
        ],
        "correta": "B",
        "justificativa": "O item 7.2.1.5 trata da verificação de métodos padronizados (comprovar que opera conforme especificado na norma). O item 7.2.2 estabelece a validação para métodos desenvolvidos pelo laboratório, métodos modificados ou métodos padronizados usados fora do escopo pretendido.",
        "clausula_iso": "7.2.1.5 e 7.2.2.1",
        "item_id_referencia": "ISO_7.2.1.5_0309_14_3",
        "audio_ref": "Trechos_Aulas/Trecho_Item_060_ISO_7_2_1_5.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_2/Podcast_Parte2_Item_14_3_Verificacao_de_Metodos_Normalizados.mp3"
    },
    {
        "id": "Q_7.4_01",
        "secao_raiz": "7",
        "clausula": "7.4",
        "clausula_nome": "7.4 Manuseio de Itens de Ensaio ou Calibração",
        "nivel": "Intermediário",
        "tema": "Controle de Temperatura no Transporte e Frasco Testemunha",
        "enunciado": "Amostras de efluente aquoso foram coletadas em campo e devem ser preservadas termicamente entre 2 °C e 6 °C durante o transporte até o laboratório. Qual é a prática metrológica recomendada no treinamento para comprovar a temperatura real da carga sem contaminar as amostras reais analisadas?",
        "alternativas": [
            {"letra": "A", "texto": "Abrir o frasco principal da amostra do cliente e inserir um termômetro de mercúrio comum diretamente no líquido."},
            {"letra": "B", "texto": "Utilizar um 'frasco testemunha' preenchido com água que viaja dentro da mesma caixa térmica no meio das amostras, medindo-se a temperatura desse frasco na recepção com termômetro calibrado."},
            {"letra": "C", "texto": "Apenas colocar a mão na caixa de isopor e assinar na ficha de amostragem que o gelo parecia frio."},
            {"letra": "D", "texto": "A temperatura de transporte é irrelevante, pois a amostra será climatizada no laboratório antes da análise."}
        ],
        "correta": "B",
        "justificativa": "O uso de frasco testemunha é a boa prática reconhecida para assegurar a rastreabilidade e integridade metrológica térmica no recebimento (7.4.3), permitindo aferição precisa sem perfurar lacres ou contaminar as amostras analíticas do cliente.",
        "clausula_iso": "7.4.1 e 7.4.3",
        "item_id_referencia": "ISO_7.4.1_0309_16_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_070_ISO_7_4_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_2/Podcast_Parte2_Item_16_1_Manuseio_Amostras_Frasco_Testemunha.mp3"
    },
    {
        "id": "Q_7.4_02",
        "secao_raiz": "7",
        "clausula": "7.4",
        "clausula_nome": "7.4 Manuseio de Itens de Ensaio",
        "nivel": "Auditoria / Avançado",
        "tema": "Recebimento de Amostra com Desvio e Ressalva no Laudo",
        "enunciado": "Uma amostra chega ao laboratório com o lacre rompido e volume abaixo do especificado. O laboratório avisa o cliente sobre a anomalia, mas o cliente insiste formalmente que o ensaio seja realizado mesmo assim. Segundo o requisito 7.4.3 da ISO/IEC 17025:2017:",
        "alternativas": [
            {"letra": "A", "texto": "O laboratório é obrigado a recusar e incinerar a amostra sem possibilidade de ensaio."},
            {"letra": "B", "texto": "O laboratório pode realizar o ensaio solicitado, mas deve incluir uma ressalva formal no relatório final indicando que a amostra apresentava desvio no recebimento e alertando que os resultados podem ter sua validade afetada por essa condição."},
            {"letra": "C", "texto": "O laboratório realiza o ensaio normalmente e omite o fato no laudo para não prejudicar o cliente perante a fiscalização."},
            {"letra": "D", "texto": "O cliente pode assinar um termo que apaga a responsabilidade da norma, tornando o laudo regular sem ressalvas."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.4.3 prevê expressamente: 'Quando o cliente exigir que o item seja ensaiado (...) reconhecendo o desvio das condições especificadas, o laboratório deve incluir uma ressalva no relatório indicando quais resultados podem ser afetados pelo desvio.'",
        "clausula_iso": "7.4.3",
        "item_id_referencia": "ISO_7.4.3_0309_16_3",
        "audio_ref": "Trechos_Aulas/Trecho_Item_072_ISO_7_4_3.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_2/Podcast_Parte2_Item_16_3_Amostra_Com_Desvio_Ressalva_Relatorio.mp3"
    },
    {
        "id": "Q_7.5_01",
        "secao_raiz": "7",
        "clausula": "7.5",
        "clausula_nome": "7.5 Registros Técnicos",
        "nivel": "Intermediário",
        "tema": "Correção de Registros e Contemporaneidade",
        "enunciado": "Durante a execução de uma titulação, o analista cometeu um engano de anotação na planilha de bancada em papel. Qual é o procedimento normativo correto para emenda de registros técnicos de acordo com a ISO/IEC 17025:2017 (item 7.5.2)?",
        "alternativas": [
            {"letra": "A", "texto": "Aplicar corretivo líquido branco sobre o número errado e escrever o correto por cima para deixar a folha limpa."},
            {"letra": "B", "texto": "Riscar o dado incorreto com um traço simples (mantendo o dado original legível), anotar o valor correto ao lado, datar e rubricar pelo responsável pela correção."},
            {"letra": "C", "texto": "Rasgar a folha de dados brutos e transcrever todos os dados a limpo em uma nova folha."},
            {"letra": "D", "texto": "Usar borracha para apagar totalmente o registro a lápis."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.5.2 determina que as emendas aos registros técnicos devem ser rastreáveis a versões anteriores ou a observações originais. Os dados originais e alterados devem ser mantidos legíveis, incluindo data de alteração, identificação dos dados alterados e pessoal responsável.",
        "clausula_iso": "7.5.2",
        "item_id_referencia": "ISO_7.5.2_0309_17_2",
        "audio_ref": "Trechos_Aulas/Trecho_Item_076_ISO_7_5_2.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_2/Podcast_Parte2_Item_17_2_Emendas_Registros_Tecnicos_Rastreabilidade.mp3"
    },
    {
        "id": "Q_7.6_01",
        "secao_raiz": "7",
        "clausula": "7.6",
        "clausula_nome": "7.6 Avaliação da Incerteza de Medição",
        "nivel": "Auditoria / Avançado",
        "tema": "Identificação de Contribuições Significativas de Incerteza",
        "enunciado": "Na avaliação da incerteza de medição para um ensaio cromatográfico quantitativo (requisito 7.6), um analista afirma: 'A única fonte de incerteza do método é o desvio-padrão de repetibilidade das injeções do cromatógrafo'. Por que essa afirmação é tecnicamente incompleta e incorreta perante a ISO 17025?",
        "alternativas": [
            {"letra": "A", "texto": "Porque ensaios químicos não possuem incerteza de medição, aplicando-se apenas a ensaios físicos."},
            {"letra": "B", "texto": "Porque o laboratório deve identificar todas as contribuições significativas para a incerteza de medição, incluindo incerteza dos padrões/MRC, balanças, vidrarias volumétricas, pureza de reagentes e efeitos de temperatura, não se limitando à repetibilidade."},
            {"letra": "C", "texto": "Porque a norma exige que a incerteza seja sempre fixada em 5% sem qualquer cálculo matemático."},
            {"letra": "D", "texto": "Porque a repetibilidade não faz parte do orçamento de incerteza."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.6.1 e 7.6.3 estabelece que o laboratório deve identificar todas as contribuições significativas para a incerteza de medição. A repetibilidade (Tipo A) é apenas uma componente; fontes sistemáticas como calibração de balanças, vidrarias, pureza e estabilidade de MRC (Tipo B) são essenciais.",
        "clausula_iso": "7.6.1 e 7.6.3",
        "item_id_referencia": "ISO_7.6.1_0309_18_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_078_ISO_7_6_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_2/Podcast_Parte2_Item_18_1_Incerteza_Medicao_Fontes_Significativas.mp3"
    },
    {
        "id": "Q_7.7_01",
        "secao_raiz": "7",
        "clausula": "7.7",
        "clausula_nome": "7.7 Garantia da Validade dos Resultados",
        "nivel": "Intermediário",
        "tema": "Mecanismos de Controle Interno da Qualidade (7.7.1)",
        "enunciado": "Para atender ao requisito 7.7.1 da ISO/IEC 17025:2017 (Garantia da Validade dos Resultados), o laboratório deve monitorar o desempenho de seus ensaios. Qual das alternativas lista EXCLUSIVAMENTE mecanismos válidos de monitoramento interno previstos na norma?",
        "alternativas": [
            {"letra": "A", "texto": "Uso de materiais de referência/padrões de checagem, ensaios em duplicata, amostras cegas e uso de cartas-controle com limites estatísticos definidos."},
            {"letra": "B", "texto": "Apenas conferir se a lâmpada do laboratório está acesa e o ar-condicionado ligado."},
            {"letra": "C", "texto": "Substituir todas as análises por uma declaração juramentada do gerente técnico."},
            {"letra": "D", "texto": "Aplicar sempre uma carta-controle manual sem limites de ação definidos."}
        ],
        "correta": "A",
        "justificativa": "O item 7.7.1 lista ferramentas como: uso de materiais de referência ou de controle da qualidade, checagens funcionais, uso de padrões de verificação com cartas de controle, ensaios repetidos com os mesmos métodos ou métodos diferentes, reensaio de itens retidos e correlação de resultados.",
        "clausula_iso": "7.7.1",
        "item_id_referencia": "ISO_7.7.1_0409_4_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_085_ISO_7_7_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_4_1_Cartas_Controle_Garantia_Validade.mp3"
    },
    {
        "id": "Q_7.7_02",
        "secao_raiz": "7",
        "clausula": "7.7",
        "clausula_nome": "7.7 Garantia da Validade dos Resultados",
        "nivel": "Auditoria / Avançado",
        "tema": "Ensaio de Proficiência (PEP) e NIT-DICLA-026",
        "enunciado": "Um laboratório postulante à acreditação Cgcre possui em seu escopo 40 ensaios físico-químicos e pretende participar de programa de ensaio de proficiência (PEP). Segundo as diretrizes da ISO 17025 (item 7.7.2) e a política brasileira da NIT-DICLA-026:",
        "alternativas": [
            {"letra": "A", "texto": "O laboratório precisa obrigatoriamente participar de PEP em todos os 40 ensaios todo mês."},
            {"letra": "B", "texto": "O laboratório deve planejar sua participação cobrindo uma parte significativa do escopo ao longo do ciclo de acreditação (com base em matriz de famílias de ensaios e análise de risco), e buscar alternativas de comparações interlaboratoriais quando não houver provedor disponível."},
            {"letra": "C", "texto": "A participação em PEP é puramente voluntária e não tem qualquer impacto no processo de acreditação da Cgcre."},
            {"letra": "D", "texto": "Resultados de PEP que resultem em 'Questionável' ou 'Insatisfatório' (|z| > 2) podem ser arquivados sem necessidade de investigação."}
        ],
        "correta": "B",
        "justificativa": "Conforme a ISO 7.7.2 e NIT-DICLA-026, o laboratório deve participar de ensaios de proficiência para uma parte significativa do seu escopo em ciclos quadrienais, fundamentado em gestão de risco e representatividade das matrizes/métodos.",
        "clausula_iso": "7.7.2",
        "item_id_referencia": "ISO_7.7.2_0409_5_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_090_ISO_7_7_2.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_5_1_PEP_Ensaio_Proficiencia_NIT26.mp3"
    },
    {
        "id": "Q_7.8_01",
        "secao_raiz": "7",
        "clausula": "7.8",
        "clausula_nome": "7.8 Relato de Resultados",
        "nivel": "Intermediário",
        "tema": "Requisitos Obrigatórios Comuns de Relatórios (7.8.2)",
        "enunciado": "Qual dos seguintes elementos NÃO é um requisito obrigatório da lista de requisitos comuns para relatórios de ensaio da ISO/IEC 17025:2017 (item 7.8.2.1)?",
        "alternativas": [
            {"letra": "A", "texto": "Identificação clara de que o relatório está concluído (por exemplo, indicação do total de páginas 'Página X de Y' e final do documento)."},
            {"letra": "B", "texto": "Identificação do método utilizado e descrição e identificação inequívoca do item ensaiado."},
            {"letra": "C", "texto": "A fotografia colorida de rosto do analista que realizou a pesagem da amostra."},
            {"letra": "D", "texto": "A identificação do(s) responsável(is) pela autorização da emissão do relatório."}
        ],
        "correta": "C",
        "justificativa": "O requisito 7.8.2.1 lista exaustivamente os itens obrigatórios: título, nome/endereço do laboratório, cliente, método, identificação das amostras, data, identificação de quem autoriza, paginação com total de páginas e demarcação clara do fim. Foto de rosto do analista não é requisito normativo.",
        "clausula_iso": "7.8.2.1",
        "item_id_referencia": "ISO_7.8.2.1_0409_6_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_098_ISO_7_8_2_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_6_1_Relato_Resultados_Requisitos_Obrigatorios.mp3"
    },
    {
        "id": "Q_7.8_02",
        "secao_raiz": "7",
        "clausula": "7.8",
        "clausula_nome": "7.8 Relato de Resultados",
        "nivel": "Auditoria / Avançado",
        "tema": "Emendas a Relatórios Já Emitidos (7.8.8)",
        "enunciado": "Um laudo de análise de água foi enviado ao cliente. No dia seguinte, detectou-se que a unidade de medida do cloreto foi digitada incorretamente como 'g/L' em vez de 'mg/L'. Como o laboratório deve proceder para corrigir esse laudo perante a cláusula 7.8.8 da ISO/IEC 17025:2017?",
        "alternativas": [
            {"letra": "A", "texto": "Basta abrir o arquivo PDF original no editor, trocar 'g/L' por 'mg/L' e mandar por WhatsApp com o mesmo número de relatório."},
            {"letra": "B", "texto": "Qualquer emenda deve ser emitida na forma de um novo documento ou adendo, conter identificação unívoca, referenciar claramente o relatório original que está sendo substituído e incluir uma declaração explicativa sobre a alteração realizada."},
            {"letra": "C", "texto": "Solicitar que o cliente rasure o laudo que tem em mãos e assine ao lado."},
            {"letra": "D", "texto": "Apagar o histórico do laudo no banco de dados para evitar auditoria de conformidade."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.8.8.1 e 7.8.8.2 estipula que emendas a relatórios emitidos devem ser feitas apenas na forma de um novo documento (ex: 'Suplemento ao Relatório X' ou 'Relatório X - Revisão 1') que identifique unicamente o documento substituído e descreva os motivos da alteração.",
        "clausula_iso": "7.8.8",
        "item_id_referencia": "ISO_7.8.8.1_0409_7_2",
        "audio_ref": "Trechos_Aulas/Trecho_Item_105_ISO_7_8_8_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_7_2_Emendas_Relatorios_Rastreabilidade.mp3"
    },
    {
        "id": "Q_7.9_01",
        "secao_raiz": "7",
        "clausula": "7.9",
        "clausula_nome": "7.9 Reclamações",
        "nivel": "Auditoria / Avançado",
        "tema": "Independência na Aprovação do Desfecho de Reclamações",
        "enunciado": "Um cliente contesta formalmente o resultado de teor de boro emitido pelo laboratório, afirmando que houve erro de titulação. O técnico Carlos, que executou a análise original, investiga o caso, refaz o cálculo e elabora a resposta técnica concluindo que o laudo original estava correto. De acordo com o requisito 7.9.6 da ISO 17025:2017, Carlos pode aprovar e assinar a decisão final de encerramento da reclamação?",
        "alternativas": [
            {"letra": "A", "texto": "Sim, pois ele é quem melhor domina a bancada e o método específico."},
            {"letra": "B", "texto": "Não; os resultados a serem comunicados ao reclamante devem ser elaborados por, ou revisados e aprovados por, indivíduo(s) não envolvido(s) nas atividades de laboratório originais em questão."},
            {"letra": "C", "texto": "Sim, desde que a contestação tenha vindo de cliente interno da empresa."},
            {"letra": "D", "texto": "A norma exige obrigatoriamente a contratação de um perito forense externo para aprovar qualquer reclamação."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.9.6 visa à salvaguarda da imparcialidade: quem aprova a resposta e a decisão final da reclamação não pode ser a mesma pessoa que executou ou esteve envolvida diretamente na atividade sob contestação.",
        "clausula_iso": "7.9.6",
        "item_id_referencia": "ISO_7.9.1_0409_8_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_108_ISO_7_9_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_8_2_Imparcialidade_Conclusao_Reclamacao.mp3"
    },
    {
        "id": "Q_7.10_01",
        "secao_raiz": "7",
        "clausula": "7.10",
        "clausula_nome": "7.10 Trabalho Não Conforme",
        "nivel": "Auditoria / Avançado",
        "tema": "Avaliação de Impacto Retroativo em Resultados Passados",
        "enunciado": "Descobriu-se que uma solução padrão de calibração usada há duas semanas em ensaios de absorção atômica estava com a concentração degradada por evaporação. O supervisor descarta a solução e prepara uma nova. Qual exigência essencial do requisito 7.10 da ISO/IEC 17025:2017 NÃO foi atendida nessa conduta?",
        "alternativas": [
            {"letra": "A", "texto": "A exigência de comprar padrões apenas de marcas europeias."},
            {"letra": "B", "texto": "A avaliação formal do impacto do desvio sobre os resultados já emitidos e liberados a clientes nas últimas duas semanas, incluindo a tomada de decisão sobre necessidade de cancelamento ou notificação aos clientes."},
            {"letra": "C", "texto": "A obrigatoriedade de punir os analistas envolvidos com advertência verbal."},
            {"letra": "D", "texto": "A necessidade de refazer todos os ensaios do laboratório desde o início do ano."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.10.1(b) determina que, ao ocorrer um trabalho não conforme, o laboratório deve realizar uma avaliação da significância do trabalho não conforme, incluindo uma análise de impacto sobre os resultados anteriores.",
        "clausula_iso": "7.10.1",
        "item_id_referencia": "ISO_7.10.1_0409_9_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_114_ISO_7_10_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_9_3_TNC_Impacto_Retroativo_Clientes.mp3"
    },
    {
        "id": "Q_7.11_01",
        "secao_raiz": "7",
        "clausula": "7.11",
        "clausula_nome": "7.11 Controle de Dados e Gestão da Informação",
        "nivel": "Intermediário",
        "tema": "Validação de Planilhas Eletrônicas (Excel) de Cálculo",
        "enunciado": "O laboratório desenvolveu uma planilha em Excel contendo fórmulas para cálculo automático de teor, diluição e incerteza de medição. Conforme o requisito 7.11.2 da ISO/IEC 17025:2017, quais cuidados são mandatórios antes de colocar a planilha em uso rotineiro?",
        "alternativas": [
            {"letra": "A", "texto": "Nenhum cuidado especial, pois softwares comerciais da Microsoft são presumidos 100% livres de erros de cálculo."},
            {"letra": "B", "texto": "Validar as fórmulas e funcionalidades da planilha comparando com cálculos manuais ou dados de referência conhecidos, proteger as células contra alterações acidentais e controlar a versão do arquivo."},
            {"letra": "C", "texto": "Apenas imprimir a planilha em papel e guardar na pasta da qualidade."},
            {"letra": "D", "texto": "A norma 17025 proíbe expressamente o uso de planilhas Excel em laboratórios acreditados."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.11.2 estipula que sistemas de gestão da informação (incluindo planilhas desenvolvidas internamente) devem ser validados quanto à sua funcionalidade antes de serem introduzidos para uso, protegidos contra alteração indevida e com integridade preservada.",
        "clausula_iso": "7.11.2",
        "item_id_referencia": "ISO_7.11.1_0409_10_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_120_ISO_7_11_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_10_2_Validacao_Planilhas_Excel_Protecao.mp3"
    },
    {
        "id": "Q_7.11_02",
        "secao_raiz": "7",
        "clausula": "7.11",
        "clausula_nome": "7.11 Controle de Dados e Gestão da Informação",
        "nivel": "Auditoria / Avançado",
        "tema": "Segurança de Dados e Teste Prático de Restauração de Backup",
        "enunciado": "O laboratório alega que cumpre plenamente o requisito de preservação de dados (7.11.4) porque seu servidor realiza backup diário automático para um disco rígido externo. Durante a auditoria, o auditor solicita a evidência do teste de restauração do backup, e a equipe admite que nunca tentou restaurar os arquivos. Qual é a fragilidade metrológica dessa situação?",
        "alternativas": [
            {"letra": "A", "texto": "Não há fragilidade, pois se a luz de gravação acende no disco rígido, a restauração é garantida."},
            {"letra": "B", "texto": "A cópia de segurança só é comprovadamente eficaz se o laboratório realizar testes periódicos de restauração (recovery test) comprovando que o banco de dados e arquivos brutos sobem íntegros sem corrupção em caso de desastre."},
            {"letra": "C", "texto": "O backup diário não é permitido pela ISO 17025, devendo ser feito exclusivamente a cada 5 anos."},
            {"letra": "D", "texto": "O auditor cometeu abuso de autoridade, pois backups não podem ser questionados em auditorias da Cgcre."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.11.4 e o guia técnico de implementação enfatizam que a manutenção de rotinas de backup sem testes de restauração documentados é uma falha crítica de integridade de dados; cópias corrompidas impedem a recuperação das evidências analíticas.",
        "clausula_iso": "7.11.4",
        "item_id_referencia": "ISO_7.11.2_0409_10_2",
        "audio_ref": "Trechos_Aulas/Trecho_Item_122_ISO_7_11_2.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_10_1_Backup_e_Restauracao_Sistemas_TI.mp3"
    },

    # =========================================================================
    # SEÇÃO 8: REQUISITOS DO SISTEMA DE GESTÃO
    # =========================================================================
    {
        "id": "Q_8.1_01",
        "secao_raiz": "8",
        "clausula": "8.1",
        "clausula_nome": "8.1 Opções de Sistema de Gestão",
        "nivel": "Básico",
        "tema": "Diferença entre Opção A e Opção B",
        "enunciado": "A Seção 8 da ABNT NBR ISO/IEC 17025:2017 oferece duas opções de implementação do Sistema de Gestão: Opção A e Opção B. Qual é a característica definidora da Opção B?",
        "alternativas": [
            {"letra": "A", "texto": "A Opção B isenta o laboratório de cumprir os requisitos técnicos das Seções 4, 5, 6 e 7."},
            {"letra": "B", "texto": "A Opção B aplica-se a laboratórios que integram uma organização que já possui e mantém um sistema de gestão certificado de acordo com a ISO 9001, desde que capaz de apoiar e demonstrar o cumprimento consistente dos requisitos das Seções 4 a 7 da 17025."},
            {"letra": "C", "texto": "A Opção B é reservada exclusivamente para laboratórios públicos e militares."},
            {"letra": "D", "texto": "A Opção B proíbe a realização de auditorias internas."}
        ],
        "correta": "B",
        "justificativa": "O requisito 8.1.3 (Opção B) permite que laboratórios que tenham estabelecido e mantenham um sistema de gestão conforme a ABNT NBR ISO 9001 atendam, pelo menos, aos requisitos dos itens 8.2 a 8.9, desde que apoiem consistentemente as seções 4 a 7.",
        "clausula_iso": "8.1.3",
        "item_id_referencia": "ISO_8.1_1009_10_09_-_Parte_2_10_20",
        "audio_ref": "Trechos_Aulas/Trecho_Item_125_ISO_8_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_8_1_Opcoes_A_e_B_Sistema_Gestao.mp3"
    },
    {
        "id": "Q_8.5_01",
        "secao_raiz": "8",
        "clausula": "8.5",
        "clausula_nome": "8.5 Ações para Abordar Riscos e Oportunidades",
        "nivel": "Intermediário",
        "tema": "Mentalidade de Risco sem Obrigatoriedade de Métodos Formais",
        "enunciado": "Um avaliador declara: 'O laboratório levou uma não conformidade porque não utilizou o método formal FMEA (Failure Mode and Effects Analysis) ou a norma ISO 31000 na sua planilha de gestão de riscos'. Essa exigência do avaliador é procedente perante a ISO 17025:2017?",
        "alternativas": [
            {"letra": "A", "texto": "Sim, a ISO 17025 adota compulsoriamente a metodologia FMEA para todos os processos laboratoriais."},
            {"letra": "B", "texto": "Não; embora o laboratório deva planejar ações para abordar riscos e oportunidades (item 8.5), a norma estabelece explicitamente que não há requisito para métodos formais de gestão de riscos ou processo documentado de gestão de riscos."},
            {"letra": "C", "texto": "Sim, mas somente se o laboratório possuir mais de 50 colaboradores."},
            {"letra": "D", "texto": "Não, pois a norma 17025 não menciona em nenhum ponto a palavra 'risco'."}
        ],
        "correta": "B",
        "justificativa": "A nota 1 do item 8.5.2 e as orientações da Cgcre esclarecem que o laboratório é responsável por decidir qual metodologia aplicar para identificar riscos; a ISO 17025 não exige o uso compulsório de FMEA nem certificação na ISO 31000.",
        "clausula_iso": "8.5.1 e 8.5.2",
        "item_id_referencia": "ISO_8.5_1009_10_09_-_Parte_3_10_26",
        "audio_ref": "Trechos_Aulas/Trecho_Item_132_ISO_8_5.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_8_5_Abordagem_de_Riscos_e_Oportunidades.mp3"
    },
    {
        "id": "Q_8.7_01",
        "secao_raiz": "8",
        "clausula": "8.7",
        "clausula_nome": "8.7 Ações Corretivas",
        "nivel": "Intermediário",
        "tema": "Investigação da Causa Raiz e Verificação de Eficácia",
        "enunciado": "Ao identificar uma não conformidade repetitiva de contaminação de amostras brancas de reagente, o laboratório limitou-se a descartar o lote contaminado. O auditor aponta desvio da Cláusula 8.7. Qual etapa fundamental do tratamento de não conformidades foi negligenciada?",
        "alternativas": [
            {"letra": "A", "texto": "A demissão dos funcionários que manipularam a amostra."},
            {"letra": "B", "texto": "A avaliação da necessidade de ação para eliminar a(s) causa(s) da não conformidade (análise de causa raiz), implementação de ações corretivas e análise crítica da eficácia de qualquer ação tomada para evitar repetição."},
            {"letra": "C", "texto": "O aumento imediato do preço cobrado pelo ensaio."},
            {"letra": "D", "texto": "Apenas a assinatura do diretor presidente no formulário de descarte."}
        ],
        "correta": "B",
        "justificativa": "Conforme o requisito 8.7.1, reagir à não conformidade (ação imediata/correção) não é suficiente; o laboratório deve avaliar a causa raiz (alínea b) e implementar ações para que a falha não volte a ocorrer, analisando a eficácia da ação corretiva tomada.",
        "clausula_iso": "8.7.1",
        "item_id_referencia": "ISO_8.7_0409_11_2",
        "audio_ref": "Trechos_Aulas/Trecho_Item_138_ISO_8_7.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_11_2_Causa_Raiz_e_Acao_Corretiva.mp3"
    },
    {
        "id": "Q_8.8_01",
        "secao_raiz": "8",
        "clausula": "8.8",
        "clausula_nome": "8.8 Auditorias Internas",
        "nivel": "Intermediário",
        "tema": "Independência do Auditor Interno",
        "enunciado": "Em um laboratório de pequeno porte, a responsável técnica pelo setor de ensaios físico-químicos foi designada para auditar internamente os procedimentos, registros e ensaios do seu próprio setor. Essa prática atende ao requisito 8.8.2 da ISO/IEC 17025:2017?",
        "alternativas": [
            {"letra": "A", "texto": "Sim, pois ninguém conhece melhor a rotina do setor do que a própria responsável técnica."},
            {"letra": "B", "texto": "Não; o laboratório deve assegurar que os auditores sejam qualificados e não auditem o seu próprio trabalho, garantindo a objetividade e a imparcialidade do processo de auditoria interna."},
            {"letra": "C", "texto": "Sim, desde que ela use luvas e jaleco durante a realização da auditoria interna."},
            {"letra": "D", "texto": "A norma 17025 não exige auditorias internas periódicas, apenas auditorias externas da Cgcre."}
        ],
        "correta": "B",
        "justificativa": "O item 8.8.2(c) estipula claramente: o laboratório deve 'selecionar auditores e conduzir auditorias para assegurar a objetividade e a imparcialidade do processo de auditoria'. O princípio basilar de auditoria determina que nenhum profissional audite as atividades pelas quais é diretamente responsável.",
        "clausula_iso": "8.8.2",
        "item_id_referencia": "ISO_8.8_1009_10_09_-_Parte_3_10_28",
        "audio_ref": "Trechos_Aulas/Trecho_Item_142_ISO_8_8.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_8_8_Auditorias_Internas_Independencia.mp3"
    },
    {
        "id": "Q_8.9_01",
        "secao_raiz": "8",
        "clausula": "8.9",
        "clausula_nome": "8.9 Análise Crítica pela Direção",
        "nivel": "Intermediário",
        "tema": "Entradas Obrigatórias da Reunião de Análise Crítica",
        "enunciado": "A alta direção do laboratório realiza a reunião anual de Análise Crítica pela Direção (item 8.9). De acordo com a ISO/IEC 17025:2017 (item 8.9.2), qual conjunto de tópicos constitui ENTRADAS obrigatórias que devem ser registradas e analisadas?",
        "alternativas": [
            {"letra": "A", "texto": "Resultados de auditorias internas/externas, retroalimentação de clientes, status de ações de análises anteriores, resultados de PEP, eficácia de ações implementadas para riscos e adequação de recursos."},
            {"letra": "B", "texto": "Apenas o demonstrativo de lucros e prejuízos comerciais da holding controladora."},
            {"letra": "C", "texto": "Apenas a lista de presença com os nomes dos diretores que tomaram café."},
            {"letra": "D", "texto": "Apenas os certificados de calibração emitidos no mês de dezembro."}
        ],
        "correta": "A",
        "justificativa": "O requisito 8.9.2 lista minuciosamente as entradas obrigatórias: cumprimento de objetivos, adequação de políticas/procedimentos, status de ações de reuniões anteriores, resultados de auditorias recentes, ações corretivas, PEPs, reclamações, recursos e identificação de riscos.",
        "clausula_iso": "8.9.2",
        "item_id_referencia": "ISO_8.9_1009_10_09_-_Parte_3_10_30",
        "audio_ref": "Trechos_Aulas/Trecho_Item_146_ISO_8_9.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_8_9_Analise_Critica_pela_Direcao.mp3"
    },

    # =========================================================================
    # QUESTÕES COMPLEMENTARES DE ALTO NÍVEL (METROLOGIA & CASOS ELETRONUCLEAR)
    # =========================================================================
    {
        "id": "Q_7.8_03",
        "secao_raiz": "7",
        "clausula": "7.8.6",
        "clausula_nome": "7.8.6 Relato de Declarações de Conformidade",
        "nivel": "Auditoria / Avançado",
        "tema": "Zona de Dúvida e Regra de Decisão com Faixa de Guarda",
        "enunciado": "Ao emitir um laudo com declaração de conformidade frente a um limite regulatório do CONAMA (ex: limite máximo = 40,0 mg/L), o laboratório obtém resultado analítico de 39,5 mg/L com incerteza expandida U = 1,0 mg/L (intervalo de 38,5 a 40,5 mg/L). Se a regra de decisão acordada prever aceitação binária estrita sem zona de guarda (zona de dúvida considerada conforme se média < limite):",
        "alternativas": [
            {"letra": "A", "texto": "O laboratório pode emitir conformidade sem citar a incerteza ou a regra adotada."},
            {"letra": "B", "texto": "O laboratório deve documentar a regra de decisão aplicada no relatório, levando em conta o nível de risco (falso aceite ou falsa rejeição), informando claramente ao cliente que a medição se sobrepõe ao limite de especificação."},
            {"letra": "C", "texto": "O laboratório altera a incerteza para 0,1 mg/L para não gerar questionamento no cliente."},
            {"letra": "D", "texto": "A norma impede qualquer laudo que apresente resultado a menos de 5% de distância do limite regulamentar."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.8.6.1 e 7.8.6.2 exige que o laboratório documente a regra de decisão empregada e identifique claramente a quais resultados a declaração se aplica e como o risco associado à incerteza foi considerado.",
        "clausula_iso": "7.8.6",
        "item_id_referencia": "ISO_7.8.6.1_0409_6_3",
        "audio_ref": "Trechos_Aulas/Trecho_Item_101_ISO_7_8_6_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_6_3_Declaracao_Conformidade_Regra_Decisao.mp3"
    },
    {
        "id": "Q_6.4_05",
        "secao_raiz": "6",
        "clausula": "6.4.11",
        "clausula_nome": "6.4.11 Dados de Referência e Fatores de Correção",
        "nivel": "Auditoria / Avançado",
        "tema": "Aplicação Obrigatória de Fatores de Correção em Cálculos",
        "enunciado": "Um certificado de calibração informa que um termopar de mufla apresenta erro sistemático de +6,0 °C na faixa de 600 °C (fator de correção = -6,0 °C). Os analistas continuam anotando a leitura direta do display e usando o valor sem aplicar a correção no cálculo de cinzas. Qual é o requisito da ISO 17025 violado?",
        "alternativas": [
            {"letra": "A", "texto": "Nenhum, pois fatores de correção são opcionais e servem apenas como sugestão técnica."},
            {"letra": "B", "texto": "O requisito 6.4.11, que exige que quando a calibração originar fatores de correção, o laboratório deve assegurar que esses fatores sejam atualizados e aplicados apropriadamente nos cálculos e sistemas informatizados."},
            {"letra": "C", "texto": "Apenas o requisito de compras e almoxarifado."},
            {"letra": "D", "texto": "O requisito de iluminação da bancada de queima."}
        ],
        "correta": "B",
        "justificativa": "O requisito 6.4.11 afirma categoricamente: 'Quando a calibração e os dados de materiais de referência derem origem a fatores de referência ou fatores de correção, o laboratório deve assegurar que os fatores de referência e de correção sejam atualizados e aplicados apropriadamente para atender aos requisitos especificados.'",
        "clausula_iso": "6.4.11",
        "item_id_referencia": "ISO_6.4.11_0209_1_25",
        "audio_ref": "Trechos_Aulas/Trecho_Item_036_ISO_6_4_11.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_1/Podcast_Parte1_Item_1_25_Fatores_Correcao_Atualizacao.mp3"
    },
    {
        "id": "Q_7.3_01",
        "secao_raiz": "7",
        "clausula": "7.3",
        "clausula_nome": "7.3 Amostragem",
        "nivel": "Intermediário",
        "tema": "Plano e Registros de Amostragem",
        "enunciado": "Quando o laboratório de monitoramento ambiental realiza a amostragem de água no canal de descarga da usina para ensaio posterior, quais informações devem obrigatoriamente constar nos registros de amostragem de acordo com o item 7.3.3 da ISO/IEC 17025:2017?",
        "alternativas": [
            {"letra": "A", "texto": "Apenas o nome do motorista do veículo de transporte."},
            {"letra": "B", "texto": "Referência ao método de amostragem, data e hora da coleta, identificação inequívoca do ponto/local, identificação do amostrador, condições ambientais relevantes (ex: maré, chuva) e diagrama/plano estatístico quando aplicável."},
            {"letra": "C", "texto": "Apenas a quantidade de garrafas plásticas utilizadas."},
            {"letra": "D", "texto": "Amostragem em campo não precisa de registro documentado, bastando etiquetar as garrafas."}
        ],
        "correta": "B",
        "justificativa": "O item 7.3.3 determina que o laboratório deve reter registros dos dados de amostragem contendo: método usado, data/hora, identificação do local, pessoal que executou, equipamentos usados, condições ambientais e diagramas de localização.",
        "clausula_iso": "7.3.3",
        "item_id_referencia": "ISO_7.3.1_0309_15_2",
        "audio_ref": "Trechos_Aulas/Trecho_Item_065_ISO_7_3_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_2/Podcast_Parte2_Item_15_2_Plano_de_Amostragem_Registros_Campo.mp3"
    },
    {
        "id": "Q_6.5_02",
        "secao_raiz": "6",
        "clausula": "6.5",
        "clausula_nome": "6.5 Rastreabilidade Metrológica",
        "nivel": "Auditoria / Avançado",
        "tema": "Uso de Material de Referência Certificado (MRC) Vencido",
        "enunciado": "Um padrão primário de condutividade elétrica certificado (MRC emitido sob a ISO 17034) atingiu o prazo de validade indicado no frasco. Um analista propõe: 'Podemos continuar usando esse frasco como MRC rastreável válido para calibrar nossa célula de condutividade, pois ele sempre esteve guardado no escuro'. Qual é a orientação técnica correta do Guia Técnico e da ISO 17025?",
        "alternativas": [
            {"letra": "A", "texto": "A proposta é plenamente aceita sem qualquer restrição, pois MRCs químicos não perdem a estabilidade metrológica."},
            {"letra": "B", "texto": "Item vencido não pode ser utilizado como MRC válido para estabelecer rastreabilidade metrológica nem calibrar equipamentos oficiais; se for mantido para estudos qualitativos ou treino interno, deve ser expressamente segregado e rotulado como 'NÃO UTILIZAR PARA CALIBRAÇÃO/RASTREABILIDADE'."},
            {"letra": "C", "texto": "Basta multiplicar o valor certificado por 1,1 para compensar a idade do padrão."},
            {"letra": "D", "texto": "O laboratório pode revalidar o MRC vencido por mais 10 anos apenas medindo com uma fita tornassol."}
        ],
        "correta": "B",
        "justificativa": "Conforme amplamente destacado nas aulas e no Guia Técnico (Item 12 do Dia 02), um padrão de referência com prazo de validade expirado perde a garantia da rastreabilidade metrológica de seu certificado; seu uso como MRC em ensaios acreditados gera não conformidade grave.",
        "clausula_iso": "6.5.3",
        "item_id_referencia": "ISO_6.5.3_0209_1_33",
        "audio_ref": "Trechos_Aulas/Trecho_Item_046_ISO_6_5_3.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_1/Podcast_Parte1_Item_1_33_Materiais_Referencia_Certificados_MRC.mp3"
    },
    {
        "id": "Q_7.8_04",
        "secao_raiz": "7",
        "clausula": "7.8",
        "clausula_nome": "7.8.7 Opiniões e Interpretações",
        "nivel": "Intermediário",
        "tema": "Distinção entre Resultados do Ensaio e Pareceres Técnicos",
        "enunciado": "Ao emitir um relatório de análise da água de refrigeração da central nuclear, o laboratório insere um comentário: 'Os resultados indicam possível corrosão galvânica na tubulação de condensação e recomendam a troca dos ânodos de sacrifício'. Perante o requisito 7.8.7 da ISO/IEC 17025:2017:",
        "alternativas": [
            {"letra": "A", "texto": "Essa declaração é proibida e invalida o relatório de ensaio."},
            {"letra": "B", "texto": "Quando forem emitidas opiniões e interpretações, o laboratório deve assegurar que apenas pessoal autorizado formalmente para isso emita o parecer, e o relatório deve identificar com clareza quais partes constituem opiniões e interpretações, fundamentando a base técnica que as originou."},
            {"letra": "C", "texto": "Opiniões e interpretações não precisam de autorização prévia e podem ser redigidas por qualquer estagiário."},
            {"letra": "D", "texto": "A ISO 17025 só permite que pareceres sejam emitidos por advogados constituídos da empresa."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.8.7.1 e 6.2.6 estabelece que apenas pessoal autorizado e competente pode emitir opiniões e interpretações, devendo o laudo diferenciar claramente os dados objetivos de medição das opiniões emitidas.",
        "clausula_iso": "7.8.7",
        "item_id_referencia": "ISO_7.8.7.1_0409_7_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_103_ISO_7_8_7_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_7_1_Opinioes_e_Interpretacoes_Relatorio.mp3"
    },
    {
        "id": "Q_MITOS_01",
        "secao_raiz": "8",
        "clausula": "8.3",
        "clausula_nome": "8.3 Controle de Documentos",
        "nivel": "Básico",
        "tema": "Mitos da Norma: Formato de Procedimentos e Manuais",
        "enunciado": "Um avaliador de qualidade argumenta que um procedimento operacional padrão (POP) do laboratório não pode ser elaborado em formato de fluxograma visual colorido, exigindo que todo procedimento seja obrigatoriamente um texto dissertativo digitado com no mínimo 10 seções padrão. De acordo com os fundamentos modernos da ISO/IEC 17025:2017:",
        "alternativas": [
            {"letra": "A", "texto": "O avaliador está correto, pois a norma prescreve a formatação ABNT padrão em papel para todos os POPs."},
            {"letra": "B", "texto": "O avaliador está equivocado; a ISO 17025 não impõe formato específico de documento (podendo ser fluxograma, vídeo, infográfico, digital ou texto), exigindo apenas controle de versão, identificação unívoca, aprovação por pessoal autorizado e disponibilidade onde necessário."},
            {"letra": "C", "texto": "Fluxogramas só são válidos se forem impressos em tamanho A1 plastificado."},
            {"letra": "D", "texto": "A norma exige que todos os documentos sejam escritos em língua inglesa."}
        ],
        "correta": "B",
        "justificativa": "A versão 2017 da ISO/IEC 17025 desmistificou o excesso burocrático de formatos documentais: o foco é a eficácia, controle de versão e acessibilidade ao pessoal técnico no ponto de uso.",
        "clausula_iso": "8.3.1 e 8.3.2",
        "item_id_referencia": "ISO_8.3_0309_5_2",
        "audio_ref": "Trechos_Aulas/Trecho_Item_128_ISO_8_3.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_2/Podcast_Parte2_Item_5_2_Procedimentos_em_Fluxograma.mp3"
    },
    {
        "id": "Q_4.1_04",
        "secao_raiz": "4",
        "clausula": "4.1",
        "clausula_nome": "4.1 Imparcialidade",
        "nivel": "Intermediário",
        "tema": "Canais Seguros de Comunicação e Ouvidoria",
        "enunciado": "Para salvaguardar a imparcialidade frente a potenciais conflitos de interesse, qual mecanismo corporativo é citado no treinamento da Eletronuclear como ferramenta de proteção ao analista para relatar pressões indevidas sem medo de retaliação (requisito 4.1)?",
        "alternativas": [
            {"letra": "A", "texto": "Discussão informal na copa durante o intervalo de café."},
            {"letra": "B", "texto": "Canais formais e protegidos de ouvidoria interna e plataformas federais como o Fala.BR com garantia de anonimato e apuração independente."},
            {"letra": "C", "texto": "Publicação anônima em redes sociais corporativas abertas."},
            {"letra": "D", "texto": "Envio de carta impressa sem remetente para a portaria da empresa."}
        ],
        "correta": "B",
        "justificativa": "Conforme abordado na aula de 10/09 pela instrutora Luciana, a existência de canais formais de ouvidoria (como ouvidoria interna e o Fala.BR da CGU) é uma salvaguarda essencial para que colaboradores reportem potenciais conflitos de interesse ou pressões hierárquicas sobre resultados analíticos.",
        "clausula_iso": "4.1.4 e 4.1.5",
        "item_id_referencia": "ISO_4.1_1009_10_09_-_Parte_1_10_7",
        "audio_ref": "Trechos_Aulas/Trecho_Item_008_ISO_4_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_10_7_Eliminacao_Minimizacao_Riscos_Imparcialidade.mp3"
    },
    {
        "id": "Q_5.3_01",
        "secao_raiz": "5",
        "clausula": "5.3",
        "clausula_nome": "5.3 Escopo das Atividades Laboratoriais",
        "nivel": "Intermediário",
        "tema": "Locais de Realização das Atividades (Fixas, Móveis e em Campo)",
        "enunciado": "O laboratório realiza ensaios físico-químicos em sua sede física permanente e também opera uma unidade móvel que mede parâmetros in situ nas praias vizinhas à central nuclear. Segundo o requisito 5.3 da ISO/IEC 17025:2017:",
        "alternativas": [
            {"letra": "A", "texto": "A norma 17025 só pode ser aplicada ao prédio sede, sendo proibido acreditar ensaios realizados em instalações móveis ou de campo."},
            {"letra": "B", "texto": "O laboratório deve definir e documentar o escopo das atividades laboratoriais em conformidade com a norma, abrangendo atividades realizadas em instalações permanentes, móveis, temporárias ou no cliente/campo."},
            {"letra": "C", "texto": "Ensaios de campo não precisam cumprir os requisitos de calibração ou controle da qualidade."},
            {"letra": "D", "texto": "A unidade móvel precisa ter uma personalidade jurídica separada com outro CNPJ."}
        ],
        "correta": "B",
        "justificativa": "O requisito 5.3 exige que o laboratório defina e documente a amplitude de suas atividades em conformidade com a norma, e a nota do item 5.3 e 6.3.1 esclarece que o escopo abrange instalações permanentes, móveis, associadas ou instalações temporárias de clientes.",
        "clausula_iso": "5.3",
        "item_id_referencia": "ISO_5.3_1009_10_09_-_Parte_2_10_12C",
        "audio_ref": "Trechos_Aulas/Trecho_Item_015_ISO_5_3.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_5_3_Escopo_Atividades_Instalacoes_Moveis.mp3"
    },
    {
        "id": "Q_6.4_06",
        "secao_raiz": "6",
        "clausula": "6.4.4",
        "clausula_nome": "6.4 Equipamentos",
        "nivel": "Auditoria / Avançado",
        "tema": "Troca de Sonda/Console e Comprovação de Desempenho",
        "enunciado": "Um técnico substitui o eletrodo de vidro de um pHmetro por uma sonda sobressalente nova do mesmo fabricante. O auditor interno questiona: 'A troca de qualquer sonda exige obrigatoriamente uma recalibração externa imediata por laboratório acreditado'. Qual é a análise técnica correta (requisito 6.4.4)?",
        "alternativas": [
            {"letra": "A", "texto": "O auditor tem razão, pois sondas e consoles nunca podem ser trocados sem certificado de calibração RBC do par acoplado."},
            {"letra": "B", "texto": "A exigência do auditor é um mito conservador; o requisito 6.4.4 exige verificar e comprovar que o equipamento atende aos requisitos especificados antes de colocá-lo em serviço, o que pode ser demonstrado por calibração com MRCs e checagem de linearidade/desempenho documentada internamente."},
            {"letra": "C", "texto": "Sondas de reposição não precisam de nenhuma verificação, bastando conectar no aparelho."},
            {"letra": "D", "texto": "O laboratório é obrigado a comprar consoles novos a cada troca de sonda."}
        ],
        "correta": "B",
        "justificativa": "Conforme detalhado no Guia Técnico do Treinamento (Item 12 do Dia 02) e debatido por Thalita & Francisca, a exigência de recalibração externa para toda troca de sonda não está no texto da ISO 17025. O que a norma exige é demonstrar e documentar que a nova configuração atende aos critérios de exatidão e linearidade do método.",
        "clausula_iso": "6.4.4 e 6.4.11",
        "item_id_referencia": "ISO_6.4.4_0209_1_17",
        "audio_ref": "Trechos_Aulas/Trecho_Item_025_ISO_6_4_4.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_1/Podcast_Parte1_Item_1_17_Sondas_Consoles_Recalibracao.mp3"
    },
    {
        "id": "Q_7.7_03",
        "secao_raiz": "7",
        "clausula": "7.7.1",
        "clausula_nome": "7.7.1 Monitoramento da Validade dos Resultados",
        "nivel": "Auditoria / Avançado",
        "tema": "Análise de Tendências em Cartas-Controle",
        "enunciado": "Na carta-controle de um ensaio de espectrofotometria UV-Vis, os últimos 7 pontos consecutivos de uma solução padrão de controle caíram todos abaixo da linha média (tendência sistemática unilateral), porém todos ainda dentro dos Limites de Ação (± 3s). Conforme as diretrizes metrológicas de 7.7.1:",
        "alternativas": [
            {"letra": "A", "texto": "Como nenhum ponto ultrapassou os limites de ação de ± 3s, o analista não precisa fazer nada e deve ignorar o gráfico."},
            {"letra": "B", "texto": "Os dados de monitoramento devem ser registrados de maneira que as tendências sejam detectáveis; 7 pontos consecutivos do mesmo lado da média indicam perda de aleatoriedade e exigem investigação preventiva de causa antes que o limite de ação seja violado."},
            {"letra": "C", "texto": "A carta-controle deve ser reiniciada do zero para apagar os pontos baixos."},
            {"letra": "D", "texto": "A norma 17025 proíbe o registro de pontos abaixo da média."}
        ],
        "correta": "B",
        "justificativa": "O requisito 7.7.1 estabelece que os dados resultantes do monitoramento devem ser registrados de modo que as tendências sejam detectáveis e, onde praticável, técnicas estatísticas devem ser aplicadas para a análise crítica dos resultados, acionando ações planejadas quando fora de critérios pré-definidos.",
        "clausula_iso": "7.7.1",
        "item_id_referencia": "ISO_7.7.1_0409_4_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_085_ISO_7_7_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_4_1_Cartas_Controle_Garantia_Validade.mp3"
    },
    {
        "id": "Q_7.10_02",
        "secao_raiz": "7",
        "clausula": "7.10.3",
        "clausula_nome": "7.10 Trabalho Não Conforme",
        "nivel": "Intermediário",
        "tema": "Autorização para Retomada das Atividades",
        "enunciado": "Após a identificação e contenção de um Trabalho Não Conforme em um ensaio cromatográfico, quem deve possuir a responsabilidade e autoridade definida para autorizar a retomada formal dos ensaios na rotina (item 7.10.1)?",
        "alternativas": [
            {"letra": "A", "texto": "Qualquer operador que chegue mais cedo no dia seguinte."},
            {"letra": "B", "texto": "Profissionais formalmente designados com responsabilidades e autoridades definidas no procedimento documentado de trabalho não conforme do laboratório."},
            {"letra": "C", "texto": "Apenas o auditor fiscal do Ministério do Trabalho."},
            {"letra": "D", "texto": "O cliente que solicitou a análise mais rápida."}
        ],
        "correta": "B",
        "justificativa": "O item 7.10.1(a) da ISO/IEC 17025:2017 estabelece que as responsabilidades e autoridades para a gestão de trabalho não conforme devem ser definidas, incluindo expressamente a definição de quem tem a autoridade para autorizar a retomada do trabalho.",
        "clausula_iso": "7.10.1 e 7.10.3",
        "item_id_referencia": "ISO_7.10.1_0409_9_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_114_ISO_7_10_1.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_9_3_TNC_Impacto_Retroativo_Clientes.mp3"
    },
    {
        "id": "Q_8.2_01",
        "secao_raiz": "8",
        "clausula": "8.2",
        "clausula_nome": "8.2 Documentação do Sistema de Gestão",
        "nivel": "Básico",
        "tema": "Políticas e Objetivos da Qualidade",
        "enunciado": "A Alta Direção do laboratório deve estabelecer, documentar e manter políticas e objetivos para o cumprimento do propósito da ISO/IEC 17025:2017 (requisito 8.2.1 e 8.2.2). Quais compromissos devem ser explicitamente assegurados nessas políticas?",
        "alternativas": [
            {"letra": "A", "texto": "Compromisso de obter lucro comercial a qualquer custo analítico."},
            {"letra": "B", "texto": "Compromisso com a competência técnica, imparcialidade e operação consistente do laboratório, assegurando que as políticas sejam compreendidas e implementadas em todos os níveis da organização."},
            {"letra": "C", "texto": "Compromisso de emitir laudos sempre idênticos aos do ano anterior."},
            {"letra": "D", "texto": "Compromisso de não contratar auditorias externas."}
        ],
        "correta": "B",
        "justificativa": "O requisito 8.2.2 determina: 'As políticas e os objetivos devem abordar a competência, a imparcialidade e a operação consistente do laboratório', sendo a alta direção responsável por comprovar o comprometimento com o desenvolvimento e implementação do SGQ.",
        "clausula_iso": "8.2.1 e 8.2.2",
        "item_id_referencia": "ISO_8.2_1009_10_09_-_Parte_2_10_21",
        "audio_ref": "Trechos_Aulas/Trecho_Item_126_ISO_8_2.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_4/Podcast_Parte4_Item_8_2_Politica_Objetivos_Qualidade.mp3"
    },
    {
        "id": "Q_8.6_01",
        "secao_raiz": "8",
        "clausula": "8.6",
        "clausula_nome": "8.6 Melhoria",
        "nivel": "Básico",
        "tema": "Retroalimentação de Clientes e Melhoria Contínua",
        "enunciado": "O requisito 8.6.2 da ISO/IEC 17025:2017 aborda a retroalimentação (feedback) de clientes. Como o laboratório deve tratar esse feedback?",
        "alternativas": [
            {"letra": "A", "texto": "Deve ignorar avaliações negativas e divulgar apenas os elogios no mural da empresa."},
            {"letra": "B", "texto": "O laboratório deve buscar retroalimentação, tanto positiva quanto negativa, de seus clientes. A retroalimentação deve ser analisada e utilizada para melhorar o sistema de gestão, as atividades de laboratório e o atendimento ao cliente."},
            {"letra": "C", "texto": "A pesquisa de satisfação deve ser anônima e destruída logo após o preenchimento."},
            {"letra": "D", "texto": "O laboratório não pode solicitar opinião de clientes para não expor vulnerabilidades."}
        ],
        "correta": "B",
        "justificativa": "O requisito 8.6.2 preconiza a busca ativa e a análise crítica da retroalimentação (positiva e negativa) dos clientes como insumo fundamental para a melhoria contínua dos serviços e do sistema de gestão.",
        "clausula_iso": "8.6.1 e 8.6.2",
        "item_id_referencia": "ISO_8.6_0409_11_1",
        "audio_ref": "Trechos_Aulas/Trecho_Item_136_ISO_8_6.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_3/Podcast_Parte3_Item_11_1_Melhoria_Retroalimentacao_Clientes.mp3"
    },
    {
        "id": "Q_6.4_07",
        "secao_raiz": "6",
        "clausula": "6.4.13",
        "clausula_nome": "6.4.13 Registros de Equipamentos",
        "nivel": "Intermediário",
        "tema": "Dossiê Histórico e Registros de Equipamentos",
        "enunciado": "O requisito 6.4.13 da ISO/IEC 17025:2017 exige a retenção de registros para equipamentos que possam influenciar as atividades do laboratório. Quais elementos devem constar obrigatoriamente nesse dossiê?",
        "alternativas": [
            {"letra": "A", "texto": "Apenas a nota fiscal de compra e a foto do vendedor."},
            {"letra": "B", "texto": "Identificação do equipamento e software/firmware, instruções do fabricante, verificação de conformidade com os requisitos, localização atual, datas e relatórios de calibrações, plano de manutenção e histórico de qualquer dano ou reparo."},
            {"letra": "C", "texto": "Apenas o comprovante de pagamento da energia elétrica do laboratório."},
            {"letra": "D", "texto": "Equipamentos analíticos modernos não exigem guarda de registros históricos."}
        ],
        "correta": "B",
        "justificativa": "O item 6.4.13 elenca de forma detalhada o conteúdo do prontuário do equipamento (alíneas a a h), assegurando rastreabilidade total de manutenções, calibrações, checagens e modificações ao longo de toda a vida útil do instrumento.",
        "clausula_iso": "6.4.13",
        "item_id_referencia": "ISO_6.4.13_0209_1_27",
        "audio_ref": "Trechos_Aulas/Trecho_Item_038_ISO_6_4_13.mp3",
        "debate_podcast": "Podcasts_Tematicos/Thalita_e_Francisca/Parte_1/Podcast_Parte1_Item_1_27_Registros_Equipamentos_Dossie.mp3"
    }
]

# Validar se todos os IDs e caminhos de audio existem ou mapeiam corretamente
print(f"Total de questoes geradas: {len(questoes)}")

# Estatisticas por secao
dist = {}
for q in questoes:
    sec = q['secao_raiz']
    dist[sec] = dist.get(sec, 0) + 1
print("Distribuicao das questoes por secao:", dist)

# Salvar o banco de dados
output_path = 'questoes_simulado.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(questoes, f, ensure_ascii=False, indent=2)

print(f"Arquivo '{output_path}' salvo com sucesso!")
