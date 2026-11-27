"""Aplica a onda 2026-11-27_arthurwelle_entrada-2024: inclui a POF 2024-2025 no de-para (ADR 0011).

Diferente das ondas comuns (que movem células já existentes), esta onda ACRESCENTA as células de um ano novo.
Por isso é aplicada por este script, como as ondas v3/v4 e a inspeção geral, e não por `hp_onda.py fechar`.

Entrada: `fonte/2024/saida/decisoes_2024.csv`, gerado pelos scripts `fonte/2024/scripts/01..04` a partir dos
microdados e dos tradutores do IBGE de 2024 e do estado vigente da harmonização (commit ac864e8).
Cada linha é uma célula 2024 (código de 6 dígitos) com o grupo atribuído, a confiança e o motivo.

O que faz:
  1. acrescenta 5.538 linhas Ano=2024 a estado/depara.csv (uma por célula; Descri_Item = ITEM do tradutor IBGE);
  2. acrescenta os quadros de 2024 a estado/quadros.csv (Quadro_H = 3 primeiros dígitos do código:
     questionário + quadro, porque em 2024 a numeração dos quadros recomeça em cada questionário);
  3. grava ondas/<onda>/{escopo.json, plano.md, decisoes.csv, relatorio.md}: uma decisão ATRIBUIR por célula.
Recusa rodar se já houver linhas de 2024 no de-para.

Rodar da raiz do repositório:  python harmonizacao/fonte/2024/entrada_2024.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / ".claude/skills/harmoniza-pof/scripts"))
from hp_comum import (COLS_DECISOES, COLS_DEPARA, COLS_QUADROS, carrega_estado, dir_estado, dir_ondas,  # noqa: E402
                      grava_csv, grava_json, grava_texto, ordena_depara)

ONDA = "2026-11-27_arthurwelle_entrada-2024"
DATA = "2026-11-27"
FONTE = Path(__file__).resolve().parent

QUEST = {"1": "POF 1 (domicílio)", "2": "POF 2 (aquisição coletiva)", "3": "POF 3 (caderneta coletiva)",
         "4": "POF 4 (aquisição individual)", "5": "POF 5 (trabalho e rendimento)"}


def main() -> None:
    est = carrega_estado()
    dep, quad = est["depara"], est["quadros"]
    if (dep["Ano"] == "2024").any():
        sys.exit("ERRO: o de-para já tem linhas de 2024; esta onda já foi aplicada.")

    d = pd.read_csv(FONTE / "saida/decisoes_2024.csv", dtype=str, keep_default_na=False)
    assert d["Codigo"].is_unique and (d["para"] != "").all()
    grupos = set(est["grupos"].loc[est["grupos"]["status"] == "ativo", "Cod_harmo"])
    faltam = sorted(set(d["para"]) - grupos)
    if faltam:
        sys.exit(f"ERRO: grupos inexistentes ou extintos: {faltam}")

    # 1. de-para
    novo = pd.DataFrame({"Ano": "2024", "Quadro_H": d["Quadro_POF"], "Codigo": d["Codigo"],
                         "Descri_Item": d["Descri_Item"].str.strip(), "Cod_harmo": d["para"]})
    dep2 = ordena_depara(pd.concat([dep, novo], ignore_index=True))
    grava_csv(dep2, dir_estado() / "depara.csv", COLS_DEPARA)

    # 2. quadros
    q = (d.assign(q=d["Quadro_POF"]).groupby("q")["Descri_Item"]
           .agg(lambda s: "; ".join(list(dict.fromkeys(s.str.strip()))[:3])).reset_index())
    q["Desc_Quadro"] = q.apply(lambda r: f"{QUEST.get(r.q[0], 'POF ' + r.q[0])} · quadro {int(r.q[1:])} "
                                         f"(2024-2025). Ex.: {r.Descri_Item[:150]}", axis=1)
    quad2 = pd.concat([quad, pd.DataFrame({"Ano": "2024", "Quadro_H": q["q"], "Desc_Quadro": q["Desc_Quadro"]})],
                      ignore_index=True)
    grava_csv(quad2, dir_estado() / "quadros.csv", COLS_QUADROS)

    # 3. ledger da onda
    od = dir_ondas() / ONDA
    od.mkdir(parents=True, exist_ok=True)
    dec = pd.DataFrame({
        "id": [f"{ONDA}#a{i:04d}" for i in range(1, len(d) + 1)],
        "data": DATA, "tipo": "ATRIBUIR", "estrutural": "false",
        "celulas": "2024:" + d["Codigo"], "de": "", "para": d["para"],
        "movimentos": "2024:" + d["Codigo"] + ">" + d["para"],
        "confianca": d["confianca"].str.replace("MÉDIA", "MEDIA"),
        "regras_ref": "R6;R7", "evidencia": d["Descri_Item"].str.strip() + " · valor R$ " +
        d["valor_uc"].astype(float).round(2).astype(str) + "/UC",
        "motivo_ia": d["motivo"], "veredito": "aceita",
        "motivo_humano": "Arthur, 2026-11-27: 'Faça a harmonização de produtos' e, após o relatório, 'acato a "
                         "proposta ... leve para a harmonização, rode, faça upload na ferramenta'.",
        "revisor": "arthurwelle (decisões da IA aceitas em bloco)", "revoga": "", "pr": ""})
    grava_csv(dec, od / "decisoes.csv", COLS_DECISOES)
    grava_json({"onda": ONDA, "autor": "arthurwelle", "tipo": "entrada-de-ano", "grupos": sorted(set(d["para"])),
                "celulas": [], "pendencias": [], "aberta_em": DATA}, od / "escopo.json")

    conf = d.assign(v=d["valor_uc"].astype(float)).groupby("confianca").agg(celulas=("Codigo", "size"),
                                                                             valor=("v", "sum"))
    conf["pct_valor"] = (100 * conf["valor"] / conf["valor"].sum()).round(2)
    grava_texto(f"""# Plano — {ONDA}

## Por que esta onda agora
A primeira divulgação dos microdados da POF 2024-2025 saiu em novembro de 2026. O pipeline de `POF2024/` (scripts 1-4)
já reproduz os totais do IBGE. Falta o `Cod_harmo` para pôr 2024 na mesma série de 1987-2017.

## Motivo humano
Arthur (2026-11-27): avaliar se dá para copiar os códigos harmonizados de 2017 para 2024 e fazer a harmonização; depois,
"acato a proposta ... leve para a harmonização, rode, faça upload na ferramenta".

## Método
Ver `fonte/2024/plano_original.md` e `fonte/2024/relatorio_original.md`. Em resumo:
- célula 2024 = código de 6 dígitos (ADR 0011);
- casamento com 2017 pela descrição (exata ou aproximada), restrito ao quadro equivalente (mapa derivado dos dados) e
  conferido com o nível do tradutor do IBGE;
- as células sem correspondência clara foram decididas uma a uma ou por regra explícita (passo 4).
""", od / "plano.md")
    grava_texto(f"""# Relatório — {ONDA}

{len(d)} células de 2024 acrescentadas ao de-para, todas com grupo existente (tipo ATRIBUIR, não estrutural).
Grupos usados: {d['para'].nunique()}. Quadros de 2024: {len(q)}.

## Confiança (valor = gasto ou renda médio mensal por UC, ponderado)
```
{conf.to_string()}
```

## Quanto 2024 difere de 2017
88% das células de 2024 têm descrição idêntica à de 2017 (82% do valor). Das 5.122 com par direto, 5.119 apontam para
uma única célula de 2017. Há 134 divisões de células de 2017 em 2024 (sem efeito: herdam o mesmo grupo) e 3 junções.
Detalhes: `fonte/2024/relatorio_original.md`.

## Decisões estruturais
Ficam na onda seguinte, `2026-11-27_arthurwelle_entrada-2024-estruturais` (ADR 0012): grupo novo de apostas on-line,
exceções R1 de 2024 e correção de dois agregados da base.
""", od / "relatorio.md")
    print(f"OK: {len(novo)} linhas 2024 no de-para · {len(q)} quadros · {len(dec)} decisões em {od}")


if __name__ == "__main__":
    main()
