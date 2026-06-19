# Candidate Screening Tool — Triagem Inteligente por Aderência de Perfil

> **Problema:** No mercado atual, candidatar-se a uma vaga virou commodity. As pessoas se inscrevem em dezenas de vagas por dia e desistem ao primeiro sinal de formulário longo. Como triamos candidatos com precisão sem afugentá-los antes mesmo da primeira conversa?

> **Solução:** Um formulário de 4 perguntas com mecânica de "iscas progressivas" — o candidato sente que está avançando no processo a cada resposta, enquanto o sistema calcula silenciosamente o score de aderência ao perfil desejado.

---

## O Problema Real

Durante um período de **expansão acelerada no setor bancário**, precisávamos contratar dezenas de profissionais para atendimento ao público em curto prazo. Os desafios eram:

- Alto volume de inscrições com perfis muito díspares
- Tempo escasso dos gestores para triagem manual
- Candidatos que abandonavam formulários longos antes de completar
- Dificuldade em identificar rapidamente quem tinha fit com o perfil de **atendimento e relacionamento** (não de análise ou estratégia)

## A Solução: Progressive Screening com Scoring de Aderência

O formulário foi desenhado com 3 princípios centrais:

### 1. Mínimo de perguntas, máximo de informação
4 perguntas cuidadosamente escolhidas que revelam perfil comportamental, motivação, qualificação técnica e janela de carreira — sem perguntar diretamente nada disso.

### 2. Mecânica de iscas progressivas (Progressive Bait)
Cada resposta gera um feedback positivo: *"Você avançou para a próxima etapa"*. O candidato percebe que está progredindo num processo seletivo, o que reduz a taxa de abandono e aumenta a qualidade das respostas (as pessoas respondem com mais cuidado quando sentem que estão sendo avaliadas).

### 3. Captura de lead como recompensa
A promessa de um **"diagnóstico gratuito de perfil"** ao final captura email e WhatsApp organicamente. O candidato recebe valor percebido; o recrutador recebe o contato qualificado.

---

## Arquitetura do Projeto

```
candidate-screening-tool/
│
├── README.md                    ← Este arquivo
│
├── form/
│   └── index.html               ← Formulário interativo (roda direto no browser)
│
├── src/
│   └── scorer.py                ← Motor de scoring em Python (configurável)
│
├── data/
│   └── sample_responses.csv     ← 90 respostas reais anonimizadas (dataset de calibração)
│
└── notebooks/
    └── analysis.ipynb           ← Análise exploratória e calibração dos pesos
```

---

## Como Funciona o Scoring

O score final é uma **média ponderada** das 4 respostas, cada uma com pesos calibrados a partir de dados reais:

| Pergunta | Peso | Lógica |
|---|---|---|
| Idade | 15% | Janela ideal de carreira para o mercado-alvo |
| Como você se descreve? | 25% | Perfil comportamental (comunicativo > analítico para front-line) |
| Qual oportunidade te atrai? | 35% | Motivação real: atendimento vs. análise vs. estratégia |
| Certificação ANBIMA | 25% | Comprometimento com o mercado financeiro |

**Score final:** 0.0 a 1.0

| Faixa | Classificação | Ação sugerida |
|---|---|---|
| ≥ 0.70 | Alto Alinhamento | Avançar imediatamente |
| 0.50 – 0.69 | Alinhamento Médio | Entrevista exploratória |
| 0.30 – 0.49 | Alinhamento Baixo | Manter em base |
| < 0.30 | Fora do Perfil | Descarte gentil |

---

## Quick Start

### Formulário (sem instalação)
Abra `form/index.html` direto no navegador. Funciona offline, sem servidor.

### Scorer Python
```python
from src.scorer import calcular_score

resultado = calcular_score(
    idade="entre 21 e 25 anos",
    perfil="comunicativo",
    oportunidade="atendimento",
    certificacao="cpa10"
)
print(resultado)
# {'score': 0.8275, 'score_pct': '82.8%', 'classificacao': 'Alto Alinhamento', ...}
```

### Análise dos dados
```bash
pip install pandas matplotlib jupyter
jupyter notebook notebooks/analysis.ipynb
```

---

## Adaptando para Outros Mercados

O modelo foi criado para o setor bancário (perfil de atendimento e vendas), mas a **metodologia é agnóstica ao mercado**. Para adaptar:

1. **Reescreva as perguntas** para o contexto do seu setor
2. **Ajuste os pesos** em `src/scorer.py` → variável `PESOS`
3. **Recalibre os scores por resposta** com base nos seus dados históricos ou nas competências que você prioriza
4. **Personalize os textos de feedback** no formulário HTML

Exemplos de adaptação:
- **Varejo:** substituir ANBIMA por experiência com metas de vendas
- **Saúde:** substituir certificação por CRM/EHR e perfil por empatia/atenção a detalhes
- **TI:** substituir oportunidade por stack preferida e certificações técnicas

---

## Sobre o Projeto

Este projeto foi desenvolvido em **2020** durante um processo de expansão acelerada no setor financeiro, com necessidade de contratação em massa para agências bancárias. O formulário foi veiculado via link direto (SurveyMonkey/Typeform), e os dados foram exportados e analisados em Excel para calibração dos pesos.

Os **90 registros reais foram anonimizados** antes da publicação neste repositório. Nenhum dado pessoal identificável foi mantido.

**Stack original:** Google Forms / SurveyMonkey → Excel (scoring) → análise manual  
**Stack remakeada:** Python + HTML puro (sem dependências externas)

---

## Autor

**Kenio Freitas** — Business Analytics | Data Analytics | BI | Lean Six Sigma  
[LinkedIn](https://linkedin.com/in/kenio-freitas) · keniomf@gmail.com
