"""Grafica la pobreza de la ENAHO por área, sexo o grupo de edad.

Uso, desde la raíz del repositorio: uv run <ruta>/graficar.py --por area --anio 2024
"""

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

SALIDAS = Path("salidas")
FIGURAS = Path("figuras")

COLOR = "#B7451A"
EDADES = [0, 18, 30, 45, 60, 200]
ETIQUETAS_EDAD = ["0 a 17", "18 a 29", "30 a 44", "45 a 59", "60 o más"]


def grupos(base, por):
    """Devuelve la etiqueta de cada persona y si las barras se ordenan por valor."""
    if por == "area":
        return base["urbano"].map({True: "Urbano", False: "Rural"}), True
    if por == "sexo":
        return base["p207"].map({1: "Hombre", 2: "Mujer"}), True
    # La edad tiene su propio orden: de menor a mayor
    return pd.cut(base["p208a"], EDADES, right=False, labels=ETIQUETAS_EDAD), False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--por", choices=["area", "sexo", "edad"], required=True)
    parser.add_argument("--anio", type=int, default=2024)
    args = parser.parse_args()

    ruta = SALIDAS / f"personas_{args.anio}.parquet"
    if not ruta.exists():
        sys.exit(f"Falta {ruta}. Corre primero la skill limpiando-enaho.")
    base = pd.read_parquet(ruta)

    etiqueta, ordenar = grupos(base, args.por)
    if etiqueta.isna().any():
        sys.exit(f"Hay {etiqueta.isna().sum()} personas sin grupo en {args.por}.")

    # Tasa ponderada con facpob07, nunca un promedio de códigos
    pobres = base["facpob07"].where(base["pobre"], 0).groupby(etiqueta, observed=True).sum()
    tasas = 100 * pobres / base["facpob07"].groupby(etiqueta, observed=True).sum()
    if ordenar:
        tasas = tasas.sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    barras = ax.bar(tasas.index.astype(str), tasas.values, color=COLOR)
    ax.bar_label(barras, fmt="%.1f %%", padding=3)
    ax.set_ylim(bottom=0, top=tasas.max() * 1.15)
    ax.set_ylabel("% de personas")
    nombre = {"area": "área", "sexo": "sexo", "edad": "grupo de edad"}[args.por]
    ax.set_title(f"Pobreza monetaria por {nombre}, Perú {args.anio}")
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, f"Fuente: INEI, ENAHO {args.anio}", fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))

    FIGURAS.mkdir(exist_ok=True)
    salida = FIGURAS / f"pobreza_{args.por}_{args.anio}.png"
    fig.savefig(salida, dpi=200)

    print(tasas.astype(float).round(2).to_string())
    print(f"Guardado: {salida}")


if __name__ == "__main__":
    main()
