"""Utilidades compartilhadas pelos scripts harmoniza-pof."""
from __future__ import annotations

import csv
import io
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

ANOS = ["1987", "1995", "2002", "2008", "2017"]

COLS_DEPARA = ["Ano", "Quadro_H", "Codigo", "Descri_Item", "Cod_harmo"]
COLS_QUADROS = ["Ano", "Quadro_H", "Desc_Quadro"]
COLS_GRUPOS = ["Cod_harmo", "nome", "nivel1", "nivel2", "status", "criado_em",
               "extinto_em", "substituido_por", "nome_original"]
COLS_REGRAS = ["id", "tipo", "enunciado", "celulas", "grupos", "anos", "evidencia",
               "autor", "onda", "status", "revogada_por"]
COLS_PENDENCIAS = ["id", "data", "origem", "descricao", "celulas", "grupos",
                   "onda_alvo", "status", "resolvida_em"]
COLS_DECISOES = ["id", "data", "tipo", "estrutural", "celulas", "de", "para", "movimentos",
                 "confianca", "regras_ref", "evidencia", "motivo_ia", "veredito",
                 "motivo_humano", "revisor", "revoga", "pr"]

TIPOS_DECISAO = ["MANTER", "MOVER", "RENOMEAR", "UNIR", "DIVIDIR", "CRIAR", "REGRA", "REVISAR"]
TIPOS_ESTRUTURAIS = {"UNIR", "DIVIDIR", "CRIAR", "REGRA"}
TIPOS_REGRA = ["inseparavel", "ausencia_estrutural", "manter_separado", "equivalencia", "convencao"]
CONFIANCAS = ["ALTA", "MEDIA", "MÉDIA", "BAIXA"]
VEREDITOS = ["aceita", "rejeitada", "modificada", "adiada"]

for _fluxo in (sys.stdout, sys.stderr):
    if hasattr(_fluxo, "reconfigure"):
        _fluxo.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------- caminhos

def raiz_repo() -> Path:
    """Raiz do repositório: HP_ROOT, ou primeiro ancestral com .git a partir do cwd/script."""
    if os.environ.get("HP_ROOT"):
        return Path(os.environ["HP_ROOT"]).resolve()
    for inicio in (Path.cwd(), Path(__file__).resolve().parent):
        for p in [inicio, *inicio.parents]:
            if (p / ".git").exists():
                return p
    sys.exit("ERRO: não achei a raiz do repo (.git). Defina HP_ROOT.")


def dir_h() -> Path:
    return raiz_repo() / "harmonizacao"


def dir_estado() -> Path:
    return dir_h() / "estado"


def dir_ondas() -> Path:
    return dir_h() / "ondas"


# ---------------------------------------------------------------- texto e códigos

def limpa(v) -> str:
    """Valor de célula Excel/CSV -> texto limpo ('9109.0' -> '9109', NaN -> '')."""
    if v is None:
        return ""
    if isinstance(v, float):
        if pd.isna(v):
            return ""
        if v.is_integer():
            return str(int(v))
    s = str(v).strip()
    if s.lower() == "nan":
        return ""
    if re.fullmatch(r"-?\d+\.0+", s):
        s = s.split(".")[0]
    return s


def cod5(v) -> str:
    """Cod_harmo em 5 dígitos texto ('1101' -> '01101'). Não numérico passa como está."""
    s = limpa(v)
    return s.zfill(5) if s.isdigit() else s


def norm_texto(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s).lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def cel(ano, codigo) -> str:
    return f"{limpa(ano)}:{limpa(codigo)}"


def parse_cel(c: str) -> tuple[str, str]:
    ano, _, codigo = c.partition(":")
    return ano.strip(), codigo.strip()


def junta(xs) -> str:
    return ";".join(str(x) for x in xs if str(x) != "")


def separa(s) -> list[str]:
    s = limpa(s)
    return [x.strip() for x in s.split(";") if x.strip()] if s else []


def chave_codigo(s: str):
    s = limpa(s)
    return (0, int(s), "") if s.isdigit() else (1, 0, s)


def hoje() -> str:
    return date.today().isoformat()


def agora() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", norm_texto(s)).strip("-")[:40]


# ---------------------------------------------------------------- CSV

def le_csv(path: Path, colunas: list[str] | None = None) -> pd.DataFrame:
    if not path.exists():
        if colunas is None:
            sys.exit(f"ERRO: arquivo não existe: {path}")
        return pd.DataFrame(columns=colunas)
    try:
        df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8")
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=colunas or [])
    if colunas:
        for c in colunas:
            if c not in df.columns:
                df[c] = ""
        df = df[colunas + [c for c in df.columns if c not in colunas]]
    return df


def grava_csv(df: pd.DataFrame, path: Path, colunas: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if colunas:
        for c in colunas:
            if c not in df.columns:
                df[c] = ""
        df = df[colunas]
    buf = io.StringIO()
    df.to_csv(buf, index=False, quoting=csv.QUOTE_MINIMAL)
    texto = buf.getvalue().replace("\r\n", "\n")
    path.write_bytes(texto.encode("utf-8"))


def ordena_depara(df: pd.DataFrame) -> pd.DataFrame:
    k = df["Codigo"].map(chave_codigo)
    df = df.assign(_a=df["Ano"], _k0=k.map(lambda t: t[0]), _k1=k.map(lambda t: t[1]),
                   _k2=k.map(lambda t: t[2]))
    df = df.sort_values(["_a", "_k0", "_k1", "_k2", "Descri_Item", "Cod_harmo"], kind="mergesort")
    return df.drop(columns=["_a", "_k0", "_k1", "_k2"]).reset_index(drop=True)


def le_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def grava_json(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def grava_texto(texto: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(texto.replace("\r\n", "\n").encode("utf-8"))


# ---------------------------------------------------------------- estado

def carrega_estado() -> dict[str, pd.DataFrame]:
    e = dir_estado()
    return {
        "depara": le_csv(e / "depara.csv", COLS_DEPARA),
        "quadros": le_csv(e / "quadros.csv", COLS_QUADROS),
        "grupos": le_csv(e / "grupos.csv", COLS_GRUPOS),
        "regras": le_csv(e / "regras.csv", COLS_REGRAS),
        "pendencias": le_csv(e / "pendencias.csv", COLS_PENDENCIAS),
    }


def celulas_df(depara: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por célula (Ano, Codigo) com grupo(s), nº de itens e itens."""
    g = depara.groupby(["Ano", "Codigo"], sort=False)
    out = g.agg(Quadro_H=("Quadro_H", "first"),
                grupos=("Cod_harmo", lambda s: junta(sorted(set(s)))),
                n_itens=("Descri_Item", "size"),
                itens=("Descri_Item", lambda s: " | ".join(dict.fromkeys(s)))).reset_index()
    out["cel"] = out["Ano"] + ":" + out["Codigo"]
    return out


def matriz_cobertura(depara: pd.DataFrame, grupos: pd.DataFrame | None = None,
                     medida: str = "celulas") -> pd.DataFrame:
    """Grupo x ano: nº de células (default) ou itens. Inclui grupos ativos sem membros."""
    if medida == "celulas":
        base = depara.drop_duplicates(["Ano", "Codigo", "Cod_harmo"])
    else:
        base = depara
    m = base.groupby(["Cod_harmo", "Ano"]).size().unstack(fill_value=0)
    for a in ANOS:
        if a not in m.columns:
            m[a] = 0
    m = m[ANOS]
    if grupos is not None and len(grupos):
        ativos = grupos.loc[grupos["status"] == "ativo", "Cod_harmo"]
        m = m.reindex(sorted(set(m.index) | set(ativos)), fill_value=0)
    m.index.name = "Cod_harmo"
    return m.astype(int)


def padrao(linha) -> str:
    return "".join("1" if int(linha[a]) > 0 else "0" for a in ANOS)


def ausencias_justificadas(regras: pd.DataFrame) -> set[tuple[str, str]]:
    ok = set()
    if regras.empty:
        return ok
    r = regras[(regras["tipo"] == "ausencia_estrutural") & (regras["status"] == "ativa")]
    for _, row in r.iterrows():
        for g in separa(row["grupos"]):
            for a in separa(row["anos"]):
                ok.add((cod5(g), a))
    return ok


def nome_grupo(grupos: pd.DataFrame) -> dict[str, str]:
    return dict(zip(grupos["Cod_harmo"], grupos["nome"]))


# ---------------------------------------------------------------- decisões

def movimentos_txt(movs: list[dict]) -> str:
    """[{'celulas': [...], 'para': 'X'}] -> '2017:1;2017:2>X|...'"""
    return "|".join(f"{junta(m.get('celulas', []))}>{m.get('para', '')}" for m in movs or [])


def txt_movimentos(s: str) -> list[dict]:
    out = []
    for parte in limpa(s).split("|"):
        if ">" not in parte:
            continue
        cels, _, para = parte.rpartition(">")
        out.append({"celulas": separa(cels), "para": para.strip()})
    return out


def carrega_decisoes_todas() -> pd.DataFrame:
    """Concatena ondas/*/decisoes.csv em ordem de onda (id começa com data)."""
    dfs = []
    for p in sorted(dir_ondas().glob("*/decisoes.csv")):
        d = le_csv(p, COLS_DECISOES)
        d.insert(0, "onda", p.parent.name)
        d["_ordem"] = range(len(d))
        dfs.append(d)
    if not dfs:
        return pd.DataFrame(columns=["onda", *COLS_DECISOES, "_ordem"])
    return pd.concat(dfs, ignore_index=True)


# ---------------------------------------------------------------- git

def git(*args, check=False) -> str:
    r = subprocess.run(["git", *args], cwd=raiz_repo(), capture_output=True, text=True,
                       encoding="utf-8")
    if check and r.returncode != 0:
        sys.exit(f"ERRO git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip() if r.returncode == 0 else ""


def autor_git() -> str:
    return slug(git("config", "user.name") or os.environ.get("USERNAME", "anon")) or "anon"
