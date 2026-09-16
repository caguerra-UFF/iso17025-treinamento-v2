# -*- coding: utf-8 -*-
"""
Script para alternar e distribuir de forma balanceada o gabarito das 50 questões do Simulado.
Elimina o vício de 'B' sempre correta (que antes ocorria em 47 de 50 questões), distribuindo:
- 13 questões com gabarito A
- 12 questões com gabarito B
- 13 questões com gabarito C
- 12 questões com gabarito D
Garante:
1. Nenhuma repetição consecutiva de gabarito (0 repetições de mesma letra em sequência).
2. Presença de todas as 4 letras em todas as seções da norma (4, 5, 6, 7 e 8).
3. Reorganização perfeita das alternativas A, B, C, D e seus diagnósticos em explicacoes_detalhadas.
4. Atualização dos caminhos de áudio das alternativas.
"""

import json
from pathlib import Path
from collections import Counter

JSON_PATH = Path("questoes_simulado.json")

# Distribuição balanceada por seção garantindo variedade contínua
DIST_POR_SECAO = {
    '4': ['C', 'A', 'D', 'B', 'A', 'C'],                                              # 6 questões
    '5': ['B', 'D', 'A', 'C', 'B'],                                                   # 5 questões
    '6': ['D', 'A', 'B', 'C', 'A', 'D', 'B', 'C', 'D', 'A', 'C', 'B'],               # 12 questões
    '7': ['A', 'D', 'B', 'C', 'D', 'A', 'C', 'B', 'A', 'C', 'D', 'B', 'C', 'A', 'B', 'D', 'C', 'A', 'D'], # 19 questões
    '8': ['B', 'D', 'A', 'C', 'B', 'D', 'A', 'C']                                    # 8 questões
}

LETTERS = ['A', 'B', 'C', 'D']

def reordenar_questoes():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        questoes = json.load(f)

    # Coletar a lista linear de metas
    targets = []
    for sec in ['4', '5', '6', '7', '8']:
        targets.extend(DIST_POR_SECAO[sec])

    assert len(targets) == len(questoes), f"Tamanho incompatível: {len(targets)} metas vs {len(questoes)} questões"

    print("=== DISTRIBUIÇÃO PLANEJADA ===")
    print(Counter(targets))

    modificadas = 0
    for idx, q in enumerate(questoes):
        qid = q['id']
        old_correta = q['correta']
        target_correta = targets[idx]
        target_idx = LETTERS.index(target_correta)

        alts = q['alternativas']
        correct_alt = next(a for a in alts if a['letra'] == old_correta)
        distractor_alts = [a for a in alts if a['letra'] != old_correta]

        # Posiciona a alternativa correta na posição alvo
        new_alts = [None, None, None, None]
        new_alts[target_idx] = correct_alt

        # Preenche os outros slots com os distratores
        empty_slots = [i for i in range(4) if i != target_idx]
        for slot_idx, distractor in zip(empty_slots, distractor_alts):
            new_alts[slot_idx] = distractor

        old_exps = q.get('explicacoes_detalhadas', {})
        new_exps = {}

        for j in range(4):
            new_letter = LETTERS[j]
            old_letter = new_alts[j]['letra']
            old_exp = old_exps.get(old_letter, {})

            clausula_ref = q.get('clausula_iso', q.get('clausula', ''))
            alt_texto = new_alts[j]['texto']

            if new_letter == target_correta:
                fund = old_exp.get('fundamentacao_acerto', q.get('justificativa', ''))
                # Substituir referências à letra anterior pela nova letra
                fund = fund.replace(f'[{old_correta}]', f'[{target_correta}]')
                fund = fund.replace(f'Alternativa {old_correta}', f'Alternativa {target_correta}')
                fund = fund.replace(f'alternativa {old_correta}', f'alternativa {target_correta}')

                new_exps[new_letter] = {
                    'tipo': 'correta',
                    'letra': new_letter,
                    'titulo': f'✓ Resposta Correta (Alternativa {new_letter})',
                    'fundamentacao_acerto': fund,
                    'texto_leitura': f"Alternativa {new_letter}: {alt_texto}. Resposta correta conforme o requisito {clausula_ref} da norma."
                }
            else:
                pq_incorreta = old_exp.get('por_que_esta_incorreta', 'Essa alternativa adota uma premissa contrária aos requisitos normativos.')
                pq_outra = old_exp.get('por_que_outra_e_correta', f"A alternativa [{target_correta}] é a correta.")
                # Atualizar a menção da correta
                pq_outra = pq_outra.replace(f'[{old_correta}]', f'[{target_correta}]')
                pq_outra = pq_outra.replace(f'Alternativa {old_correta}', f'Alternativa {target_correta}')
                pq_outra = pq_outra.replace(f'alternativa {old_correta}', f'alternativa {target_correta}')

                new_exps[new_letter] = {
                    'tipo': 'incorreta',
                    'letra': new_letter,
                    'titulo': f'✖ Atenção: Alternativa {new_letter} Incorreta',
                    'por_que_esta_incorreta': pq_incorreta,
                    'por_que_outra_e_correta': pq_outra,
                    'gabarito_correto': target_correta,
                    'texto_leitura': f"Alternativa {new_letter}: {alt_texto}. Esta alternativa está incorreta. A resposta correta é a letra {target_correta}."
                }

            # Atualiza o objeto de alternativa com a nova letra e novo áudio
            new_alts[j]['letra'] = new_letter
            new_alts[j]['audio_alt'] = f"Audios_Simulado/{qid}_alt_{new_letter}.mp3"

        q['alternativas'] = new_alts
        q['correta'] = target_correta
        q['explicacoes_detalhadas'] = new_exps
        modificadas += 1

    # Salvar o banco de questões atualizado
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(questoes, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Todas as {modificadas} questões foram balanceadas e reordenadas com sucesso em {JSON_PATH}!")

if __name__ == '__main__':
    reordenar_questoes()
