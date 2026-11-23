"""Roda valores/gerar_valores.py do repositório com os microdados locais do Tales (nomes de arquivo diferentes)."""
import sys, importlib.util
from pathlib import Path
import pandas as pd
REPO, DADOS = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("gv", REPO / "valores" / "gerar_valores.py")
sys.argv = [sys.argv[0], str(DADOS)]
gv = importlib.util.module_from_spec(spec); spec.loader.exec_module(gv)
gv.DESPESAS = {a: DADOS / f"POF{a}__GZ__Despesas_POF_{a}.gz" for a in gv.ANOS}
_read = pd.read_csv
def read_csv(p, *a, **k):
    p = Path(p)
    if p.name in ("MORADORES_H.RDS", "DOMICILIOS.RDS"):
        p = DADOS / f"{p.parent.parent.name}__RDS__{p.name}"
    return _read(p, *a, **k)
gv.pd.read_csv = read_csv
gv.main()
