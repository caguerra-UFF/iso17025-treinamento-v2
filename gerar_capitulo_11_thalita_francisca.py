# -*- coding: utf-8 -*-
import asyncio
import os
import sys
import subprocess
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import edge_tts

OUTPUT_DIR = Path(r"F:\Transcricoes_Consolidadas\Podcasts_Tematicos\Thalita_e_Francisca")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VOZ_THALITA = "pt-BR-ThalitaMultilingualNeural"
VOZ_FRANCISCA = "pt-BR-FranciscaNeural"

EPISODIOS_SEC11 = [
    {
        "id": "11.1",
        "filename": "Podcast_Item_11_1_Produtor_Competente_e_ISO_17034.mp3",
        "title": "Item 11.1 - Produtor Competente de MRC e a ISO 17034",
        "dialogue": [
            ("Thalita", "Francisca, entramos no Capítulo 11: o universo dos Materiais de Referência Certificados, os famosos MRCs. No treinamento, a instrutora enfatizou muito a busca pelo credenciamento na ISO 17034. Todo padrão usado pelo laboratório precisa obrigatoriamente ter o selo da ISO 17034?"),
            ("Francisca", "Essa é uma nuance técnica importantíssima, Thalita! A classificação técnica dessa fala é Confirmado com Ressalva. A ISO 17025, na Nota 1 do requisito 6.4.1 e no item 6.5.2, diz que o laboratório deve usar materiais de referência de produtores competentes, e reconhece que produtores sob a ISO 17034 são considerados competentes."),
            ("Thalita", "Mas a norma internacional fecha as portas para outros produtores?"),
            ("Francisca", "O texto internacional fala em demonstrar competência. A acreditação na ISO 17034 é a rota de ouro, a forma mais robusta e direta de comprovar rastreabilidade perante auditorias da Cgcre. Porém, para padrões de institutos nacionais primários como o Inmetro ou o NIST, a competência é inerente. É fundamental consultar a política de rastreabilidade nacional."),
            ("Thalita", "Excelente distinção! A ISO 17034 dá segurança jurídica máxima, mas entender o texto da norma evita exigências descabidas.")
        ]
    },
    {
        "id": "11.2",
        "filename": "Podcast_Item_11_2_Incerteza_do_MRC_Compativel_com_Uso.mp3",
        "title": "Item 11.2 - Incerteza do MRC Compatível com o Uso",
        "dialogue": [
            ("Thalita", "No Item 11.2, vem uma advertência matemática crucial: não adianta comprar um padrão certificado se a incerteza dele for do mesmo tamanho da tolerância do seu método. Por que isso é um tiro no pé, Francisca?"),
            ("Francisca", "Porque a incerteza do material de referência entra diretamente na composição da incerteza global do seu ensaio, Thalita! Se o seu cliente ou a legislação exige uma tolerância máxima de um décimo e o padrão que você comprou tem incerteza de quase um décimo, sua margem de erro permitida já foi quase toda consumida antes de começar a análise!"),
            ("Thalita", "E qual é a orientação prática que a metrologia recomenda ao escolher o MRC?"),
            ("Francisca", "A regra prática consagrada é que a incerteza expandida do padrão de referência seja de um terço a um décimo da tolerância admitida para o processo. Assim, a contribuição do padrão fica insignificante no balanço final de incerteza do laudo."),
            ("Thalita", "Aula pura de compatibilidade metrológica: comprar padrão não é só olhar o nome do reagente, é dimensionar a incerteza dele para o método!")
        ]
    },
    {
        "id": "11.3",
        "filename": "Podcast_Item_11_3_Lote_Validade_e_Condicoes_do_Certificado.mp3",
        "title": "Item 11.3 - Lote, Validade e Condições: O Perigo dos Valores Informativos",
        "dialogue": [
            ("Thalita", "Chegamos ao Item 11.3 com um caso real que acontece todo dia nos laboratórios: um certificado de tampão traz o valor de pH certificado a vinte e cinco graus Celsius, mas traz também uma tabelinha com valores a vinte e a trinta graus. O analista pode usar esses outros valores no cálculo do ensaio, Francisca?"),
            ("Francisca", "Alerta vermelho para essa prática, Thalita! A documentação técnica é explícita: o valor só é certificado na temperatura e condição em que o produtor declarou a incerteza! Aquela tabelinha impressa em outras temperaturas é apenas informativa e não possui valor metrológico atestado."),
            ("Thalita", "E o que acontece se o laboratório usar esse valor informativo como se fosse certificado?"),
            ("Francisca", "Você quebra a cadeia de rastreabilidade metrológica! A ISO 17025 exige que o laboratório opere rigorosamente dentro das condições sob as quais o valor foi certificado. Promover valor meramente informativo a padrão de calibração é não conformidade grave na certa."),
            ("Thalita", "Recado claríssimo: tabela informativa não é certificado metrológico. Se o certificado crava vinte e cinco graus, a sua medição tem que respeitar essa condição.")
        ]
    },
    {
        "id": "11.4",
        "filename": "Podcast_Item_11_4_Temperatura_20C_vs_25C_para_pH.mp3",
        "title": "Item 11.4 - Temperatura de 20 °C versus 25 °C para pH",
        "dialogue": [
            ("Thalita", "No Item 11.4, o treinamento discutiu o embate entre calibrar pH a vinte graus versus vinte e cinco graus Celsius. Francisca, a ISO 17025 define alguma temperatura universal obrigatória para a medição de pH?"),
            ("Francisca", "A ISO 17025 não impõe nem vinte nem vinte e cinco graus, Thalita! A temperatura de referência depende exclusivamente do método analítico que o laboratório adotou, como o Standard Methods ou a Farmacopeia, e das especificações do seu equipamento."),
            ("Thalita", "E onde o laboratório costuma escorregar nessa questão de temperatura?"),
            ("Francisca", "O erro está em comprar um padrão com valor certificado para vinte graus quando o seu procedimento operacional exige calibração a vinte e cinco graus! O laboratório precisa alinhar três pontas: o método de ensaio, o certificado do padrão e a curva de compensação do pHmetro. Coerência entre método e material é a chave."),
            ("Thalita", "Perfeito! A norma dá a regra de consistência, quem dá os graus Celsius é o método normalizado.")
        ]
    },
    {
        "id": "11.5",
        "filename": "Podcast_Item_11_5_Quantidade_Minima_de_Amostra_do_MRC.mp3",
        "title": "Item 11.5 - Quantidade Mínima de Amostra: Alerta sobre Homogeneidade",
        "dialogue": [
            ("Thalita", "No Item 11.5, temos uma correção técnica importante feita pelo guia. No curso foi dito que se o certificado não especificar a quantidade mínima de amostra a ser usada, qualquer quantidade pode ser retirada. Isso é seguro, Francisca?"),
            ("Francisca", "Cuidado absoluto com essa conclusão, Thalita! A nossa equipe técnica marcou esse trecho com Atenção e Correção. A quantidade mínima descrita no certificado é exatamente a fração de massa ou volume para a qual o produtor comprovou estatisticamente a homogeneidade do lote."),
            ("Thalita", "E se o certificado não trouxer essa informação explícita no texto?"),
            ("Francisca", "A omissão dessa informação não autoriza o analista a presumir que qualquer microquantidade é homogênea! Em matrizes sólidas, pós ou suspensões, se você retirar uma fração minúscula de alguns miligramas, você corre o risco de pegar uma amostra não representativa. É dever do laboratório consultar as instruções técnicas do produtor antes de fracionar."),
            ("Thalita", "Excelente esclarecimento! Presumir homogeneidade sem respaldo do produtor é um risco invisível para o ensaio.")
        ]
    },
    {
        "id": "11.6",
        "filename": "Podcast_Item_11_6_Validade_Apos_Abertura.mp3",
        "title": "Item 11.6 - Validade Após Abertura: A Vida Útil Real do Padrão",
        "dialogue": [
            ("Thalita", "No Item 11.6, surge outra dúvida que tira o sono dos analistas de bancada: se o certificado não indicar um prazo de validade após a abertura do frasco, o laboratório pode continuar usando o padrão até o vencimento original do lacre?"),
            ("Francisca", "Outro ponto marcado com Atenção e Correção técnica, Thalita! A ISO 17025 exige controle rigoroso de prazos e preservação das características dos padrões. Mas ela não autoriza a suposição de que um frasco aberto dura anos só porque o lacre venceria dali a três anos!"),
            ("Thalita", "E qual é o perigo químico real de manter um frasco aberto por muito tempo?"),
            ("Francisca", "Pense num tampão de pH dez: em contato com o ar ambiente, ele absorve dióxido de carbono imediatamente, alterando o pH em poucas semanas! Soluções voláteis evaporam o solvente e concentram o soluto. Quando o fabricante não declara a validade pós-abertura, o laboratório tem que estabelecer um procedimento interno de controle, descarte ou monitoramento de estabilidade."),
            ("Thalita", "Visão impecável! O lacre protege o lote fechado; depois que o frasco é aberto na bancada, a responsabilidade pela integridade passa para o laboratório.")
        ]
    },
    {
        "id": "11.7",
        "filename": "Podcast_Item_11_7_Uso_de_Reagente_ou_Material_Vencido.mp3",
        "title": "Item 11.7 - Uso de Reagente ou Material Vencido: O Veredito Definitivo",
        "dialogue": [
            ("Thalita", "Pra fechar a Seção 11 e todo o primeiro dia de treinamento, o Item 11.7 traz a polêmica suprema: o laboratório pode usar um reagente ou padrão vencido se fizer um teste de comparação interna e demonstrar que ele ainda atende?"),
            ("Francisca", "Veredito técnico categórico, Thalita: para fins de calibração e rastreabilidade metrológica, material de referência certificado vencido perde o status de certificado! A ISO 17025 não possui nenhuma permissão genérica para extensão informal de validade de MRC por conta própria."),
            ("Thalita", "Mas e para reagentes comuns ou materiais auxiliares, existe alguma brecha em auditoria?"),
            ("Francisca", "A conversa no treinamento mostrou divergências sérias entre avaliadores e restrições legais da Anvisa e órgãos reguladores! Um material vencido pode no máximo, em condições controladas, ser usado para treinamento interno de novos analistas ou testes qualitativos didáticos. Mas nesse caso, o frasco precisa estar fisicamente segregado e com etiqueta vermelha gigante: proibido usar para ensaios e calibrações!"),
            ("Thalita", "Sensacional, Francisca! Uma resposta que protege o laboratório contra autuações e fecha com chave de ouro a metrologia de equipamentos e padrões.")
        ]
    }
]

async def sintetizar(texto: str, voz: str, rate: str = "+0%", pitch: str = "+0Hz") -> bytes:
    comm = edge_tts.Communicate(texto, voz, rate=rate, pitch=pitch)
    chunks = []
    async for ch in comm.stream():
        if ch["type"] == "audio":
            chunks.append(ch["data"])
    return b"".join(chunks)

async def gerar_episodio(ep: dict, silence_path: Path) -> Path:
    out_file = OUTPUT_DIR / ep["filename"]
    t_title = ep["title"]
    print(f"\n[Seção 11 - Thalita & Francisca] Processando: {t_title}...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        concat_txt = tmp_path / "concat.txt"
        lines = []
        for idx, (speaker, text) in enumerate(ep["dialogue"]):
            voz = VOZ_THALITA if speaker == "Thalita" else VOZ_FRANCISCA
            print(f"   [{speaker}]: \"{text[:55]}...\"")
            rate = "+14%" if speaker == "Thalita" else "+10%"
            pitch = "+4Hz" if speaker == "Thalita" else "+2Hz"
            audio = await sintetizar(text, voz, rate=rate, pitch=pitch)
            cfile = tmp_path / f"turn_{idx:02d}.mp3"
            cfile.write_bytes(audio)
            lines.append(f"file '{cfile.as_posix()}'")
            lines.append(f"file '{silence_path.as_posix()}'")

        concat_txt.write_text("\n".join(lines), encoding="utf-8")
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(out_file)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print(f"[OK] Gerado com sucesso: {out_file.name} ({out_file.stat().st_size // 1024} KB)")
    return out_file

async def main():
    print("==========================================================")
    print(" GERANDO SEÇÃO 11 (ITENS 11.1 A 11.7) - THALITA & FRANCISCA")
    print("==========================================================")

    silence_file = OUTPUT_DIR / "_silence_180ms.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "0.18", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_file)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    gerados = []
    for ep in EPISODIOS_SEC11:
        caminho = await gerar_episodio(ep, silence_file)
        gerados.append(caminho)

    print("\n[Capítulo 11 Completo] Unindo os itens 11.1 a 11.7 em um único áudio...")
    ep_completo = OUTPUT_DIR / "Podcast_Capitulo_11_Itens_11_1_a_11_7_Completo_Thalita_e_Francisca.mp3"
    silence_1s = OUTPUT_DIR / "_silence_1s.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
        "-t", "1.0", "-q:a", "9", "-acodec", "libmp3lame",
        str(silence_1s)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        linhas_full = []
        for g in gerados:
            linhas_full.append(f"file '{g.as_posix()}'")
            linhas_full.append(f"file '{silence_1s.as_posix()}'")
        f.write("\n".join(linhas_full))
        concat_full = f.name

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_full,
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(ep_completo)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    try:
        silence_file.unlink(missing_ok=True)
        silence_1s.unlink(missing_ok=True)
        os.remove(concat_full)
    except Exception:
        pass

    print(f"\n[Sucesso] Todos os episódios da Seção 11 foram salvos em: {OUTPUT_DIR}")

if __name__ == "__main__":
    asyncio.run(main())