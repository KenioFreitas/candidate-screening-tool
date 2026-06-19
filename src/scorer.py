"""
Candidate Screening Scorer
--------------------------
Calcula o score de aderência de um candidato com base em 4 perguntas rápidas.
Os pesos foram calibrados a partir de dados reais de recrutamento bancário (2020)
e podem ser ajustados para qualquer mercado.

Uso:
    from scorer import calcular_score
    resultado = calcular_score(
        idade="entre 21 e 25 anos",
        perfil="comunicativo",
        oportunidade="atendimento",
        certificacao="cpa10"
    )
    print(resultado)
"""

# ─────────────────────────────────────────────
# PESOS DAS QUESTÕES (soma = 1.0)
# Ajuste esses valores para calibrar ao seu mercado
# ─────────────────────────────────────────────
PESOS = {
    "q1_idade":        0.15,
    "q2_perfil":       0.25,
    "q3_oportunidade": 0.35,
    "q4_certificacao": 0.25,
}

# ─────────────────────────────────────────────
# SCORES POR RESPOSTA (0.0 a 1.0)
# Calibrados a partir de dados reais de 90 candidatos
# ─────────────────────────────────────────────

# Q1 — Idade
SCORES_IDADE = {
    "entre 21 e 25 anos": 1.00,
    "entre 31 e 35 anos": 0.90,
    "acima de 36 anos":   0.80,
    "entre 26 e 30 anos": 0.70,
    "menos de 21 anos":   0.30,
}

# Q2 — Como você se descreve?
SCORES_PERFIL = {
    "comunicativo": 1.00,   # "Gosto de falar muito, sou comunicativo..."
    "executor":     0.80,   # "Sou orientado a execução..."
    "ambicioso":    0.70,   # "Sou ambicioso, sei onde quero chegar..."
    "analitico":    0.40,   # "Tenho boa capacidade analítica..."
    "inovador":     0.20,   # "Sou orientado a inovação..."
}

# Q3 — Qual oportunidade mais se encaixa nas suas expectativas?
SCORES_OPORTUNIDADE = {
    "atendimento": 1.00,   # "Atendimento ao público / Posso Ajudar?"
    "caixa":       0.70,   # "Caixa / Área interna"
    "estrategia":  0.40,   # "Estratégias, definição e acompanhamento de metas"
    "analise":     0.10,   # "Análise de informações..."
}

# Q4 — Certificação ANBIMA
SCORES_CERTIFICACAO = {
    "cpa20":    1.00,
    "cpa10":    0.80,
    "cea":      0.80,
    "nenhuma":  0.20,
}

# ─────────────────────────────────────────────
# FAIXAS DE CLASSIFICAÇÃO
# ─────────────────────────────────────────────
CLASSIFICACOES = [
    (0.70, "Alto Alinhamento",  "Perfil muito alinhado ao que buscamos. Recomendamos avançar no processo."),
    (0.50, "Alinhamento Médio", "Perfil com bom potencial. Vale aprofundar a conversa."),
    (0.30, "Alinhamento Baixo", "Perfil com algumas divergências. Avaliar com cautela."),
    (0.00, "Fora do Perfil",    "Perfil fora do alvo neste momento. Manteremos seu contato para futuras oportunidades."),
]


def calcular_score(idade: str, perfil: str, oportunidade: str, certificacao: str) -> dict:
    """
    Calcula o score de aderência de um candidato.

    Parâmetros
    ----------
    idade : str
        Chave de idade. Ex: "entre 21 e 25 anos"
    perfil : str
        Chave de perfil. Ex: "comunicativo", "analitico", "inovador", "executor", "ambicioso"
    oportunidade : str
        Chave de oportunidade. Ex: "atendimento", "caixa", "estrategia", "analise"
    certificacao : str
        Chave de certificação. Ex: "cpa10", "cpa20", "cea", "nenhuma"

    Retorna
    -------
    dict com score (0-1), classificação e mensagem
    """
    scores_individuais = {
        "q1_idade":        SCORES_IDADE.get(idade.lower(), 0.5),
        "q2_perfil":       SCORES_PERFIL.get(perfil.lower(), 0.5),
        "q3_oportunidade": SCORES_OPORTUNIDADE.get(oportunidade.lower(), 0.5),
        "q4_certificacao": SCORES_CERTIFICACAO.get(certificacao.lower(), 0.5),
    }

    score_final = sum(
        scores_individuais[q] * PESOS[q]
        for q in PESOS
    )

    classificacao, mensagem = "Indefinido", ""
    for limite, classe, msg in CLASSIFICACOES:
        if score_final >= limite:
            classificacao = classe
            mensagem = msg
            break

    return {
        "score": round(score_final, 4),
        "score_pct": f"{score_final * 100:.1f}%",
        "classificacao": classificacao,
        "mensagem": mensagem,
        "detalhes": scores_individuais,
    }


# ─────────────────────────────────────────────
# EXEMPLOS DE USO
# ─────────────────────────────────────────────
if __name__ == "__main__":
    exemplos = [
        {
            "label": "Candidato A — Perfil ideal",
            "idade": "entre 21 e 25 anos",
            "perfil": "comunicativo",
            "oportunidade": "atendimento",
            "certificacao": "cpa20",
        },
        {
            "label": "Candidato B — Perfil analítico",
            "idade": "entre 26 e 30 anos",
            "perfil": "analitico",
            "oportunidade": "analise",
            "certificacao": "nenhuma",
        },
        {
            "label": "Candidato C — Perfil intermediário",
            "idade": "entre 31 e 35 anos",
            "perfil": "ambicioso",
            "oportunidade": "caixa",
            "certificacao": "cpa10",
        },
    ]

    for ex in exemplos:
        label = ex.pop("label")
        resultado = calcular_score(**ex)
        print(f"\n{'─'*50}")
        print(f"  {label}")
        print(f"{'─'*50}")
        print(f"  Score:          {resultado['score_pct']}")
        print(f"  Classificação:  {resultado['classificacao']}")
        print(f"  Mensagem:       {resultado['mensagem']}")
        print(f"  Detalhes:       {resultado['detalhes']}")
