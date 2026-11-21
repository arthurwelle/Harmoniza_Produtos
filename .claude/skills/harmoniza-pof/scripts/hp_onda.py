"""Ciclo de vida de uma onda.

Uso:
  python hp_onda.py status
  python hp_onda.py abrir --escopo cirurgia --tipo familia --grupos 36005,36006 [--celulas 2017:42026]
                          [--pendencias base#q3] [--autor nome] [--sem-branch]
  python hp_onda.py propostas ONDA          # valida propostas.json e gera onda.json (para a página)
  python hp_onda.py importar-db ONDA --dir PASTA_DO_READ_DB [--revisor nome]
  python hp_onda.py fechar ONDA             # aplica decisões, valida, escreve relatorio.md
  python hp_onda.py consolidar [--onda ONDA --pr N]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

import hp_cobertura
import hp_familias
import hp_validar
from hp_comum import (ANOS, COLS_DECISOES, COLS_DEPARA, COLS_GRUPOS, COLS_PENDENCIAS, COLS_QUADROS,
                      COLS_REGRAS, CONFIANCAS, TIPOS_DECISAO, TIPOS_ESTRUTURAIS, TIPOS_REGRA, VEREDITOS,
                      agora, autor_git, carrega_decisoes_todas, carrega_estado, celulas_df, cod5, dir_estado,
                      dir_h, dir_ondas, git, grava_csv, grava_json, grava_texto, hoje, junta, le_csv,
                      le_json, matriz_cobertura, movimentos_txt, ordena_depara, padrao, separa, slug,
                      txt_movimentos)

ESTADO_ARQS = {"depara": COLS_DEPARA, "quadros": COLS_QUADROS, "grupos": COLS_GRUPOS,
               "regras": COLS_REGRAS, "pendencias": COLS_PENDENCIAS}


def pasta(onda: str) -> Path:
    p = dir_ondas() / onda
    if not p.exists():
        sys.exit(f"ERRO: onda não existe: {p}")
    return p


def conf_norm(c: str) -> str:
    return (c or "").upper().replace("É", "E")


# ------------------------------------------------------------------ status

def cmd_status(a) -> None:
    est = carrega_estado()
    A = hp_validar.Achados()
    gc = hp_validar.valida_estado(est, A)
    hp_validar.valida_ledger(gc, A)
    print(f"Branch atual: {git('branch', '--show-current') or '?'}")
    ondas = sorted(p.name for p in dir_ondas().glob("*") if p.is_dir())
    print(f"Ondas no repo: {len(ondas)} (últimas: {', '.join(ondas[-5:])})")
    pen = est["pendencias"]
    ab = pen[pen["status"].isin(["aberta", "em_onda"])]
    print(f"Pendências abertas: {len(ab)} " + str(dict(Counter(ab["origem"]))))
    print(f"Validação: ERRO {len(A.erros)} | ALERTA {sum(i[0] == 'ALERTA' for i in A.itens)}")

    print("\nCandidatas à próxima onda (ONDAS.md):")
    n = 1
    for nivel, cod, msg, ex in A.itens:
        if nivel == "ERRO":
            print(f"  {n}. [erro {cod}] {msg} — ex.: {', '.join(ex[:5])}"); n += 1
    for r in ab.sort_values("id").head(8).itertuples():
        print(f"  {n}. [pendência {r.id} {r.origem}] {r.descricao[:110]} "
              f"{('células ' + r.celulas[:60]) if r.celulas else ''}"); n += 1
    au = hp_cobertura.ausencias(est)
    if len(au):
        au = au[au["vazios_nao_justificados"] != ""]
        g = est["grupos"].set_index("Cod_harmo")
        au["nivel1"] = au["Cod_harmo"].map(lambda c: g.loc[c, "nivel1"] if c in g.index else "")
        for n1, sub in au.groupby("nivel1"):
            print(f"  {n}. [ausência A01 · {n1 or 'sem nível'}] {len(sub)} grupos: "
                  f"{', '.join(sub['Cod_harmo'])}"); n += 1
    m = matriz_cobertura(est["depara"], None, "itens")
    big = m.sum(axis=1).sort_values(ascending=False).head(3)
    print(f"  {n}. [balde] maiores: " + ", ".join(f"{k} ({v} itens)" for k, v in big.items())); n += 1
    tipos = []
    for p in sorted(dir_ondas().glob("*/escopo.json")):
        tipos.append(le_json(p).get("tipo"))
    locais = 0
    for t in reversed(tipos):
        if t in ("global", "taxonomia", "base"):
            break
        locais += 1
    if locais >= 3:
        print(f"  {n}. [global] {locais} ondas locais desde a última global ⇒ sugerir onda global")


# ------------------------------------------------------------------ abrir

def escopos_outras_branches(onda_atual: str) -> list[dict]:
    git("fetch", "--quiet")
    refs = git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/onda", "refs/heads/onda")
    out = []
    for ref in refs.splitlines():
        nome = ref.split("onda/", 1)[-1]
        if nome == onda_atual:
            continue
        txt = git("show", f"{ref}:harmonizacao/ondas/{nome}/escopo.json")
        if txt:
            try:
                out.append({"ref": ref, **json.loads(txt)})
            except json.JSONDecodeError:
                pass
    return out


def cmd_abrir(a) -> None:
    autor = slug(a.autor) if a.autor else autor_git()
    onda = f"{hoje()}_{autor}_{slug(a.escopo)}"
    od = dir_ondas() / onda
    if od.exists():
        sys.exit(f"ERRO: onda já existe: {od}")
    grupos = [cod5(g) for g in re.split(r"[,;]", a.grupos or "") if g.strip()]
    celulas = [c.strip() for c in re.split(r"[,;]", a.celulas or "") if c.strip()]
    pend = [p.strip() for p in (a.pendencias or "").split(",") if p.strip()]

    est = carrega_estado()
    cel = celulas_df(est["depara"])
    alvo = set(cel.loc[cel["grupos"].isin(grupos), "cel"]) | set(celulas)
    faltam = [c for c in celulas if c not in set(cel["cel"])]
    if faltam:
        sys.exit(f"ERRO: células inexistentes: {faltam}")

    for o in escopos_outras_branches(onda):
        g2, c2 = set(o.get("grupos", [])), set(o.get("celulas", []))
        inter_g = sorted(set(grupos) & g2)
        inter_c = sorted(set(celulas) & c2)
        if inter_g or inter_c:
            print(f"AVISO: escopo cruza com {o['ref']} (autor {o.get('autor')}): "
                  f"grupos {inter_g} células {inter_c[:10]}. Combine antes de seguir.")

    if not a.sem_branch:
        if git("status", "--porcelain", "--untracked-files=no"):
            print("AVISO: há mudanças não commitadas; a branch nova as carrega.")
        r = git("switch", "-c", f"onda/{onda}")
        print(f"branch onda/{onda} criada" if git("branch", "--show-current") == f"onda/{onda}"
              else "AVISO: não consegui criar a branch; siga manualmente.")

    grava_json({"onda": onda, "autor": autor, "tipo": a.tipo, "grupos": grupos, "celulas": celulas,
                "pendencias": pend, "aberta_em": hoje()}, od / "escopo.json")
    grava_texto(f"""# Plano — {onda}

Tipo: `{a.tipo}` · grupos: {', '.join(grupos) or '—'} · células extras: {', '.join(celulas) or '—'}
· pendências: {', '.join(pend) or '—'} · total de células no escopo: {len(alvo)}

## Por que esta onda agora (IA)
_preencher: sinal que motivou (alerta, pendência, balde), alternativas consideradas._

## Por que esta onda agora (humano)
_preencher com o motivo dado pelo autor ao confirmar o escopo._

## Hipóteses iniciais
_preencher antes de ler o contexto; confrontar no diagnóstico._
""", od / "plano.md")
    txt = hp_familias.contexto(est, grupos, celulas, 3, 10, 12)
    grava_texto(txt, od / "contexto.md")
    print(f"OK onda {onda}\n  {od}\n  contexto.md: {len(txt)} caracteres, {len(alvo)} células")
    print("Próximo: preencher plano.md, ler contexto.md, escrever propostas.json, rodar `propostas`.")


# ------------------------------------------------------------------ propostas

def simula(dep: pd.DataFrame, movs: list[dict]) -> pd.DataFrame:
    d = dep.copy()
    chave = d["Ano"] + ":" + d["Codigo"]
    for m in movs:
        d.loc[chave.isin(m["celulas"]), "Cod_harmo"] = m["para"]
    return d


def cobertura_de(dep: pd.DataFrame, grupos: set[str]) -> dict[str, list[int]]:
    sub = dep[dep["Cod_harmo"].isin(grupos)]
    m = matriz_cobertura(sub) if len(sub) else pd.DataFrame(columns=ANOS)
    return {g: [int(m.loc[g, a]) if g in m.index else 0 for a in ANOS] for g in sorted(grupos)}


def valida_propostas(P: dict, est: dict) -> tuple[list[str], list[str]]:
    erros, avisos = [], []
    dep, grp = est["depara"], est["grupos"]
    cels_ok = set(dep["Ano"] + ":" + dep["Codigo"])
    ativos = set(grp.loc[grp["status"] == "ativo", "Cod_harmo"])
    todos_cod = set(grp["Cod_harmo"])
    regras_ids = set(est["regras"]["id"])
    decs_ids = set(carrega_decisoes_todas()["id"])
    vistos, cel_uso = set(), Counter()
    for p in P.get("propostas", []):
        pid = p.get("id", "?")
        if pid in vistos:
            erros.append(f"{pid}: id repetido")
        vistos.add(pid)
        t = p.get("tipo")
        if t not in TIPOS_DECISAO:
            erros.append(f"{pid}: tipo inválido {t}")
            continue
        conf = conf_norm(p.get("confianca"))
        if conf not in {"ALTA", "MEDIA", "BAIXA"}:
            erros.append(f"{pid}: confiança inválida {p.get('confianca')}")
        if not (p.get("motivo_ia") or "").strip():
            erros.append(f"{pid}: motivo_ia vazio")
        movs = p.get("movimentos") or []
        novos = p.get("novos_grupos") or {}
        if t in {"MOVER", "UNIR", "DIVIDIR", "CRIAR"}:
            if not movs:
                erros.append(f"{pid}: {t} sem movimentos")
            if not p.get("regras_ref"):
                erros.append(f"{pid}: {t} precisa citar regra (regras_ref)")
            if conf == "BAIXA":
                erros.append(f"{pid}: confiança BAIXA não pode ser {t}; use REVISAR (CONSTITUICAO)")
        if t in {"MANTER", "REVISAR"} and movs:
            erros.append(f"{pid}: {t} não deve ter movimentos")
        for m in movs:
            for c in m.get("celulas", []):
                if c not in cels_ok:
                    erros.append(f"{pid}: célula inexistente {c}")
                cel_uso[c] += 1
            para = m.get("para", "")
            if para.startswith("NOVO:"):
                if para[5:] not in novos:
                    erros.append(f"{pid}: {para} sem definição em novos_grupos")
            elif cod5(para) not in ativos:
                erros.append(f"{pid}: destino {para} não é grupo ativo")
        for s, g in novos.items():
            if not g.get("nome"):
                erros.append(f"{pid}: novo grupo {s} sem nome")
            cs = g.get("codigo_sugerido", "")
            if cs and cod5(cs) in todos_cod:
                avisos.append(f"{pid}: codigo_sugerido {cs} já existe (será realocado no fechar)")
        if t == "UNIR" and not p.get("extinguir"):
            avisos.append(f"{pid}: UNIR sem 'extinguir' (grupos absorvidos ficarão ativos e vazios)")
        for g in p.get("extinguir", []) or []:
            if cod5(g) not in ativos:
                erros.append(f"{pid}: extinguir {g} não é grupo ativo")
        if t == "RENOMEAR":
            for g in (p.get("renomear") or {}):
                if cod5(g) not in ativos:
                    erros.append(f"{pid}: renomear {g} não é grupo ativo")
            if not p.get("renomear"):
                erros.append(f"{pid}: RENOMEAR sem campo renomear")
        if t == "REGRA":
            rn = p.get("regra_nova") or {}
            if rn.get("tipo") not in TIPOS_REGRA:
                erros.append(f"{pid}: regra_nova.tipo inválido")
            if not rn.get("enunciado"):
                erros.append(f"{pid}: regra_nova sem enunciado")
        for r in p.get("revoga", []) or []:
            if r not in regras_ids and r not in decs_ids:
                erros.append(f"{pid}: revoga id desconhecido {r}")
        if p.get("conflito") and not isinstance(p["conflito"], dict):
            erros.append(f"{pid}: conflito deve ser objeto")
    for c, n in cel_uso.items():
        if n > 1:
            avisos.append(f"célula {c} movida por {n} propostas (a última aceita vence)")
    return erros, avisos


def cmd_propostas(a) -> None:
    od = pasta(a.onda)
    P = le_json(od / "propostas.json")
    est = carrega_estado()
    erros, avisos = valida_propostas(P, est)
    for w in avisos:
        print("AVISO", w)
    if erros:
        for e in erros:
            print("ERRO", e)
        sys.exit(1)

    dep, grp = est["depara"], est["grupos"]
    cel = celulas_df(dep).set_index("cel")
    g = grp.set_index("Cod_harmo")
    nomes = {k: {"nome": r["nome"], "nivel1": r["nivel1"], "nivel2": r["nivel2"], "status": r["status"]}
             for k, r in g.iterrows()}
    for p in P["propostas"]:
        movs = p.get("movimentos") or []
        cels = list(dict.fromkeys([c for m in movs for c in m["celulas"]] + (p.get("celulas_analisadas") or [])))
        p["estrutural"] = p["tipo"] in TIPOS_ESTRUTURAIS
        p["contexto_celulas"] = [{
            "cel": c, "ano": c.split(":")[0], "codigo": c.split(":")[1],
            "quadro": cel.loc[c, "Quadro_H"], "grupo": cel.loc[c, "grupos"], "n_itens": int(cel.loc[c, "n_itens"]),
            "itens": cel.loc[c, "itens"].split(" | ")[:40]} for c in cels if c in cel.index]
        envolvidos = {x["grupo"] for x in p["contexto_celulas"]} | {m["para"] for m in movs}
        envolvidos |= {cod5(x) for x in p.get("extinguir", []) or []}
        reais = {x for x in envolvidos if not x.startswith("NOVO:")}
        p["cobertura_antes"] = cobertura_de(dep, reais)
        p["cobertura_depois"] = cobertura_de(simula(dep, movs), envolvidos)
    reg = est["regras"]
    onda_json = {**P, "gerado_em": agora(), "anos": ANOS, "grupos": nomes,
                 "regras_ativas": reg[reg["status"] == "ativa"].to_dict("records"),
                 "escopo": le_json(od / "escopo.json")}
    grava_json(onda_json, od / "onda.json")
    t = Counter(p["tipo"] for p in P["propostas"])
    print(f"OK {len(P['propostas'])} propostas {dict(t)} · estruturais: "
          f"{sum(p['estrutural'] for p in P['propostas'])}\n  gerado {od / 'onda.json'}")


# ------------------------------------------------------------------ importar-db

def cmd_importar_db(a) -> None:
    od = pasta(a.onda)
    base = Path(a.dir)
    arqs = sorted(base.rglob("*.json"))
    if not arqs:
        sys.exit(f"ERRO: nenhum JSON em {base}")
    decs = {}
    for f in arqs:
        doc = json.loads(f.read_text(encoding="utf-8"))
        if isinstance(doc, dict) and isinstance(doc.get("data"), dict) and "veredito" not in doc:
            doc = doc["data"]
        pid = doc.get("pid") or f.stem
        if doc.get("onda") and doc["onda"] != a.onda:
            continue
        decs[pid] = {k: doc.get(k) for k in ("veredito", "motivo", "revisor", "ts", "movimentos")}
        if a.revisor and not decs[pid].get("revisor"):
            decs[pid]["revisor"] = a.revisor
    grava_json({"onda": a.onda, "modo": "artifact", "importado_em": agora(), "decisoes": decs},
               od / "decisoes.json")
    print(f"OK {len(decs)} decisões → {od / 'decisoes.json'} {dict(Counter(d['veredito'] for d in decs.values()))}")


# ------------------------------------------------------------------ fechar

def aloca_codigo(sugerido: str, prefixo_ref: str, usados: set[str]) -> str:
    s = cod5(sugerido) if sugerido else ""
    if re.fullmatch(r"\d{5}", s) and s not in usados:
        return s
    pref = (s or cod5(prefixo_ref))[:3]
    for ll in range(1, 99):
        c = f"{pref}{ll:02d}"
        if c not in usados:
            return c
    sys.exit(f"ERRO: sem código livre no prefixo {pref}")


def cmd_fechar(a) -> None:
    od = pasta(a.onda)
    P = le_json(od / "propostas.json")
    D = le_json(od / "decisoes.json").get("decisoes", {})
    est = carrega_estado()
    erros, _ = valida_propostas(P, est)
    if erros:
        sys.exit("ERRO: propostas.json inválido; rode `propostas`.\n" + "\n".join(erros))
    faltam = [p["id"] for p in P["propostas"] if p["id"] not in D]
    if faltam:
        sys.exit(f"ERRO: propostas sem veredito: {faltam}")
    for pid, d in D.items():
        if d.get("veredito") not in VEREDITOS:
            sys.exit(f"ERRO: {pid} veredito inválido {d.get('veredito')}")
        if d["veredito"] != "aceita" and not (d.get("motivo") or "").strip():
            sys.exit(f"ERRO: {pid} veredito '{d['veredito']}' exige motivo humano")

    originais = {k: (dir_estado() / f"{k}.csv").read_bytes() for k in ESTADO_ARQS}
    dep, grp, reg, pen = est["depara"], est["grupos"], est["regras"], est["pendencias"]
    dep_antes = dep.copy()
    chave = dep["Ano"] + ":" + dep["Codigo"]
    grupo_de = dict(zip(chave, dep["Cod_harmo"]))
    usados = set(grp["Cod_harmo"])
    linhas_dec, novas_regras, novas_pend, resolvidas = [], [], [], []
    tocados: set[str] = set()

    for p in P["propostas"]:
        d = D[p["id"]]
        ver = d["veredito"]
        movs = d.get("movimentos") if ver == "modificada" and d.get("movimentos") else (p.get("movimentos") or [])
        movs = [{"celulas": list(m["celulas"]), "para": m["para"]} for m in movs]
        cels = list(dict.fromkeys([c for m in movs for c in m["celulas"]] + (p.get("celulas_analisadas") or [])))
        de = sorted({grupo_de.get(c, "") for c in cels} - {""})
        did = f"{a.onda}#{p['id']}"
        aplicar = ver in ("aceita", "modificada")

        if aplicar:
            mapa_novo = {}
            for s, gdef in (p.get("novos_grupos") or {}).items():
                ref = gdef.get("codigo_sugerido") or (de[0] if de else "00000")
                c = aloca_codigo(gdef.get("codigo_sugerido", ""), ref, usados)
                usados.add(c)
                mapa_novo[f"NOVO:{s}"] = c
                grp = pd.concat([grp, pd.DataFrame([{
                    "Cod_harmo": c, "nome": gdef["nome"], "nivel1": gdef.get("nivel1", ""),
                    "nivel2": gdef.get("nivel2", ""), "status": "ativo", "criado_em": a.onda,
                    "extinto_em": "", "substituido_por": "", "nome_original": ""}])], ignore_index=True)
            for m in movs:
                m["para"] = mapa_novo.get(m["para"], cod5(m["para"]))
                dep.loc[chave.isin(m["celulas"]), "Cod_harmo"] = m["para"]
                for c in m["celulas"]:
                    grupo_de[c] = m["para"]
                tocados.add(m["para"])
            tocados.update(de)
            for gcod, ren in (p.get("renomear") or {}).items():
                ix = grp["Cod_harmo"] == cod5(gcod)
                for campo in ("nome", "nivel1", "nivel2"):
                    if ren.get(campo):
                        grp.loc[ix, campo] = ren[campo]
                tocados.add(cod5(gcod))
            dest = movs[-1]["para"] if movs else ""
            for gcod in p.get("extinguir", []) or []:
                ix = grp["Cod_harmo"] == cod5(gcod)
                grp.loc[ix, ["status", "extinto_em", "substituido_por"]] = ["extinto", a.onda, dest]
            if p["tipo"] == "REGRA" and p.get("regra_nova"):
                rn = p["regra_nova"]
                novas_regras.append({
                    "id": f"{a.onda}#r{len(novas_regras) + 1}", "tipo": rn["tipo"], "enunciado": rn["enunciado"],
                    "celulas": junta(rn.get("celulas", [])), "grupos": junta(cod5(x) for x in rn.get("grupos", [])),
                    "anos": junta(rn.get("anos", [])), "evidencia": rn.get("evidencia", p.get("evidencia", "")),
                    "autor": f"IA+{d.get('revisor', '')}", "onda": a.onda, "status": "ativa", "revogada_por": ""})
            for rid in p.get("revoga", []) or []:
                ix = reg["id"] == rid
                reg.loc[ix, ["status", "revogada_por"]] = ["revogada", did]

        if ver in ("aceita", "modificada", "rejeitada"):
            resolvidas += p.get("pendencias", []) or []
        if p["tipo"] == "REVISAR" and ver in ("aceita", "modificada"):
            novas_pend.append({"id": f"{a.onda}#q{len(novas_pend) + 1}", "data": hoje(), "origem": "IA",
                               "descricao": f"{p.get('titulo', '')}: {p.get('motivo_ia', '')} "
                                            f"[humano: {d.get('motivo', '')}]",
                               "celulas": junta(cels), "grupos": junta(de), "onda_alvo": "",
                               "status": "aberta", "resolvida_em": ""})

        linhas_dec.append({
            "id": did, "data": hoje(), "tipo": p["tipo"], "estrutural": str(p["tipo"] in TIPOS_ESTRUTURAIS).lower(),
            "celulas": junta(cels), "de": junta(de), "para": junta(dict.fromkeys(m["para"] for m in movs)),
            "movimentos": movimentos_txt(movs), "confianca": conf_norm(p.get("confianca")),
            "regras_ref": junta(p.get("regras_ref", []) or []), "evidencia": p.get("evidencia", ""),
            "motivo_ia": p.get("motivo_ia", ""), "veredito": ver, "motivo_humano": d.get("motivo", "") or "",
            "revisor": d.get("revisor", "") or "", "revoga": junta(p.get("revoga", []) or []), "pr": ""})

    if novas_regras:
        reg = pd.concat([reg, pd.DataFrame(novas_regras)], ignore_index=True)
    if resolvidas:
        ix = pen["id"].isin(resolvidas)
        pen.loc[ix, ["status", "resolvida_em"]] = ["resolvida", a.onda]
    if novas_pend:
        pen = pd.concat([pen, pd.DataFrame(novas_pend)], ignore_index=True)

    grava_csv(ordena_depara(dep), dir_estado() / "depara.csv", COLS_DEPARA)
    grava_csv(grp.sort_values("Cod_harmo").reset_index(drop=True), dir_estado() / "grupos.csv", COLS_GRUPOS)
    grava_csv(reg, dir_estado() / "regras.csv", COLS_REGRAS)
    grava_csv(pen, dir_estado() / "pendencias.csv", COLS_PENDENCIAS)
    dec_path = od / "decisoes.csv"
    dec_antigo = dec_path.read_bytes() if dec_path.exists() else None
    grava_csv(pd.DataFrame(linhas_dec), dec_path, COLS_DECISOES)

    est2 = carrega_estado()
    A = hp_validar.Achados()
    gc = hp_validar.valida_estado(est2, A)
    hp_validar.valida_ledger(gc, A)
    if A.erros:
        for k, b in originais.items():
            (dir_estado() / f"{k}.csv").write_bytes(b)
        if dec_antigo is None:
            dec_path.unlink()
        else:
            dec_path.write_bytes(dec_antigo)
        print(A.md(False))
        sys.exit("ERRO: validação falhou; estado restaurado. Corrija (ADR? propostas?) e rode `fechar` de novo.")

    tocados = {t for t in tocados if t}
    cob_a = cobertura_de(dep_antes, tocados)
    cob_d = cobertura_de(est2["depara"], tocados)
    nomes = dict(zip(est2["grupos"]["Cod_harmo"], est2["grupos"]["nome"]))
    cov_rows = "\n".join(
        f"| {g} | {nomes.get(g, '')[:50]} | {' '.join(map(str, cob_a.get(g, [0] * 5)))} | "
        f"{' '.join(map(str, cob_d.get(g, [0] * 5)))} |" for g in sorted(tocados))
    dec_rows = "\n".join(
        f"| {r['id'].split('#')[1]} | {r['tipo']} | **{r['veredito']}** | {len(separa(r['celulas']))} | "
        f"{r['de']} → {r['para']} | {r['motivo_ia'][:160]} | {r['motivo_humano'][:160]} | {r['revisor']} |"
        for r in linhas_dec)
    n_mud = int((dep_antes.reset_index(drop=True)["Cod_harmo"] != dep["Cod_harmo"].reset_index(drop=True)).sum())
    estr = [r["id"] for r in linhas_dec if r["estrutural"] == "true" and r["veredito"] in ("aceita", "modificada")]
    vc = Counter(r["veredito"] for r in linhas_dec)
    escopo = le_json(od / "escopo.json")
    grava_texto(f"""# Relatório — {a.onda}

Tipo `{escopo.get('tipo')}` · autor {escopo.get('autor')} · fechada em {hoje()}

{P.get('resumo', '')}

## Decisões ({len(linhas_dec)}: {', '.join(f'{k} {v}' for k, v in vc.items())})
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
{dec_rows}

## Efeito
- Itens do de-para que mudaram de grupo: {n_mud}
- Regras novas: {len(novas_regras)} · pendências resolvidas: {len(set(resolvidas))} · pendências criadas: {len(novas_pend)}
- Decisões estruturais aplicadas: {', '.join(estr) or 'nenhuma'}{' ⇒ PR com label `estrutural` e aprovação de outro membro' if estr else ''}

## Cobertura dos grupos tocados (células {' '.join(ANOS)})
| grupo | nome | antes | depois |
|---|---|---|---|
{cov_rows or '| — | | | |'}

## Validação após fechar
{A.md(False)}
## Commit sugerido
`onda {a.onda}: {len(linhas_dec)} decisões ({', '.join(f'{k} {v}' for k, v in vc.items())})`
""", od / "relatorio.md")
    print(f"OK onda fechada: {len(linhas_dec)} decisões, {n_mud} itens mudaram de grupo.\n  {od / 'relatorio.md'}")


# ------------------------------------------------------------------ consolidar

def cmd_consolidar(a) -> None:
    if a.onda and a.pr:
        p = pasta(a.onda) / "decisoes.csv"
        d = le_csv(p, COLS_DECISOES)
        d["pr"] = str(a.pr)
        grava_csv(d, p, COLS_DECISOES)
        for adr in (dir_h() / "adr").glob("*.md"):
            t = adr.read_text(encoding="utf-8")
            if a.onda in t and f"PR #{a.pr}" not in t:
                grava_texto(t.rstrip() + f"\n\nMesclado via PR #{a.pr}.\n", adr)
    est = carrega_estado()
    dec = carrega_decisoes_todas()
    grava_csv(dec.drop(columns=["_ordem"]), dir_h() / "decisoes_todas.csv", ["onda", *COLS_DECISOES])

    grp, dep, reg = est["grupos"], est["depara"], est["regras"]
    m = matriz_cobertura(dep, grp)
    cel = celulas_df(dep)
    out = ["# Documentação da harmonização de produtos POF 1987–2017",
           "_Gerado por `hp_onda.py consolidar`. Não editar à mão._", "",
           "Método: `.claude/skills/harmoniza-pof/CONSTITUICAO.md`. Histórico completo: `decisoes_todas.csv`.", "",
           "## Ondas", "| onda | tipo | decisões | aplicadas | PR |", "|---|---|---|---|---|"]
    for p in sorted(dir_ondas().glob("*/escopo.json")):
        e = le_json(p)
        sub = dec[dec["onda"] == p.parent.name]
        apl = sub["veredito"].isin(["aceita", "modificada"]).sum()
        prs = junta(sorted(set(sub["pr"]) - {""}))
        out.append(f"| {p.parent.name} | {e.get('tipo')} | {len(sub)} | {apl} | {prs} |")
    out += ["", "## Regras ativas", "| id | tipo | enunciado | grupos | anos |", "|---|---|---|---|---|"]
    for r in reg[reg["status"] == "ativa"].itertuples():
        out.append(f"| {r.id} | {r.tipo} | {r.enunciado} | {r.grupos} | {r.anos} |")
    out += ["", f"## Grupos ({(grp['status'] == 'ativo').sum()} ativos, {(grp['status'] == 'extinto').sum()} extintos)"]
    for nivel1, bloco in grp.groupby("nivel1", sort=False):
        out.append(f"\n### {nivel1 or '(sem nível 1)'}")
        for g in bloco.itertuples():
            cov = m.loc[g.Cod_harmo] if g.Cod_harmo in m.index else pd.Series({x: 0 for x in ANOS})
            out.append(f"\n#### {g.Cod_harmo} — {g.nome}")
            out.append(f"{g.nivel2} · status **{g.status}** · criado em {g.criado_em}"
                       + (f" · extinto em {g.extinto_em} → {g.substituido_por}" if g.status == "extinto" else ""))
            out.append("Células por ano: " + " · ".join(f"{x}: {cov[x]}" for x in ANOS) + f" (padrão {padrao(cov)})")
            regs = reg[reg["grupos"].map(lambda s: g.Cod_harmo in separa(s))]
            for r in regs.itertuples():
                out.append(f"- Regra {r.id} ({r.tipo}, {r.status}): {r.enunciado}")
            cels_g = set(cel.loc[cel["grupos"] == g.Cod_harmo, "cel"])
            for r in dec.itertuples():
                movs = txt_movimentos(r.movimentos)
                if g.Cod_harmo in separa(r.de) or g.Cod_harmo in separa(r.para) or cels_g & set(separa(r.celulas)):
                    mov = f" ({r.de} → {r.para})" if r.para else ""
                    out.append(f"- Decisão {r.id} {r.tipo} **{r.veredito}**{mov}. "
                               f"IA: {r.motivo_ia} Humano ({r.revisor}): {r.motivo_humano or '—'}"
                               + (f" PR #{r.pr}" if r.pr else ""))
    grava_texto("\n".join(out) + "\n", dir_h() / "DOCUMENTACAO.md")
    print(f"OK DOCUMENTACAO.md e decisoes_todas.csv ({len(dec)} decisões)")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    s = sub.add_parser("abrir")
    s.add_argument("--escopo", required=True)
    s.add_argument("--tipo", required=True, choices=["familia", "pendencia", "balde", "global", "taxonomia"])
    s.add_argument("--grupos", default="")
    s.add_argument("--celulas", default="")
    s.add_argument("--pendencias", default="")
    s.add_argument("--autor")
    s.add_argument("--sem-branch", action="store_true")
    s = sub.add_parser("propostas"); s.add_argument("onda")
    s = sub.add_parser("importar-db"); s.add_argument("onda"); s.add_argument("--dir", required=True)
    s.add_argument("--revisor")
    s = sub.add_parser("fechar"); s.add_argument("onda")
    s = sub.add_parser("consolidar"); s.add_argument("--onda"); s.add_argument("--pr", type=int)
    a = p.parse_args()
    {"status": cmd_status, "abrir": cmd_abrir, "propostas": cmd_propostas, "importar-db": cmd_importar_db,
     "fechar": cmd_fechar, "consolidar": cmd_consolidar}[a.cmd](a)


if __name__ == "__main__":
    main()
