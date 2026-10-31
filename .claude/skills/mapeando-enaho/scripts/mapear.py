"""Dibuja el mapa de la pobreza de la ENAHO por departamento.

Uso, desde la raíz del repositorio: uv run <ruta>/mapear.py --anio 2024
"""

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

SALIDAS = Path("salidas")
MAPAS = Path("mapas")
GEOJSON = Path("datos/peru_departamental_simple.geojson")

LLAVES = ["conglome", "vivienda", "hogar"]
LIMA, CALLAO = "15", "07"
TOTAL_DEPARTAMENTOS = 25


def pobreza_por_departamento(base):
    """Pobreza por departamento: un registro por hogar, ponderado con factor07 × mieperho."""
    hogares = base.drop_duplicates(LLAVES).copy()
    hogares["peso"] = hogares["factor07"].astype(float) * hogares["mieperho"]
    hogares["peso_pobre"] = hogares["peso"].where(hogares["pobre"], 0)
    grupos = hogares.groupby("departamento")
    return (100 * grupos["peso_pobre"].sum() / grupos["peso"].sum()).rename("pobreza_pct").reset_index()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anio", type=int, default=2024)
    anio = parser.parse_args().anio

    ruta = SALIDAS / f"personas_{anio}.parquet"
    if not ruta.exists():
        sys.exit(f"Falta {ruta}. Corre primero la skill limpiando-enaho.")
    if not GEOJSON.exists():
        sys.exit(f"Falta {GEOJSON}. Bájalo del repositorio del curso.")

    tasas = pobreza_por_departamento(pd.read_parquet(ruta))
    limites = gpd.read_file(GEOJSON)
    limites["departamento"] = limites["FIRST_IDDP"].astype(str).str.zfill(2)

    # Se une por código, nunca por nombre: «APURIMAC» no es «Apurímac»
    mapa = limites.merge(tasas, on="departamento", how="left", validate="1:1")
    sin_dato = mapa.loc[mapa["pobreza_pct"].isna(), "NOMBDEP"].tolist()
    if len(mapa) != TOTAL_DEPARTAMENTOS or sin_dato:
        sys.exit(f"Se esperaban {TOTAL_DEPARTAMENTOS} departamentos con dato; hay {len(mapa)}, sin dato: {sin_dato}")
    if not {LIMA, CALLAO} <= set(mapa["departamento"]):
        sys.exit("Lima (15) y Callao (07) deben ir separados.")

    fig, ax = plt.subplots(figsize=(7, 9))
    mapa.plot(
        column="pobreza_pct",
        cmap="Oranges",
        vmin=0,
        edgecolor="white",
        linewidth=0.5,
        legend=True,
        legend_kwds={"label": "Pobreza monetaria (% de personas)", "shrink": 0.6},
        ax=ax,
    )
    ax.set_title(f"Pobreza monetaria por departamento, Perú {anio}")
    ax.set_axis_off()
    fig.text(0.02, 0.02, f"Fuente: INEI, ENAHO {anio}, ponderado con factor07 × mieperho", fontsize=8)

    MAPAS.mkdir(exist_ok=True)
    salida = MAPAS / "pobreza_departamento.png"
    fig.savefig(salida, dpi=200, bbox_inches="tight")

    orden = mapa.sort_values("pobreza_pct", ascending=False)[["NOMBDEP", "pobreza_pct"]].round(1)
    print("Más pobreza:\n" + orden.head(3).to_string(index=False, header=False))
    print("Menos pobreza:\n" + orden.tail(3).iloc[::-1].to_string(index=False, header=False))
    print(f"Guardado: {salida}")


if __name__ == "__main__":
    main()
