"""Limpia los módulos 34 y 02 de la ENAHO y arma una base de personas.

Uso, desde la raíz del repositorio: uv run <ruta>/limpiar.py --anio 2024
"""

import argparse
import io
import sys
import zipfile
from pathlib import Path

import pandas as pd

DATOS = Path("datos")
SALIDAS = Path("salidas")

LLAVES = ["conglome", "vivienda", "hogar"]
LLAVES_PERSONA = LLAVES + ["codperso"]

# Por año: código del INEI y cifras oficiales contra las que se valida
ANIOS = {2024: {"codigo": 966, "pobreza": 27.6, "extrema": 5.5, "residentes": 108_664}}
TOLERANCIA = 0.1

COLUMNAS_SUMARIA = LLAVES + ["ubigeo", "dominio", "estrato", "pobreza", "mieperho", "factor07"]
COLUMNAS_MIEMBROS = LLAVES_PERSONA + ["anio", "p203", "p204", "p205", "p206", "p207", "p208a", "facpob07"]


def leer(zip_path, nombre, llaves):
    """Paso 1 y 2: lee el .dta dentro del zip, con llaves como texto y columnas normalizadas."""
    if not zip_path.exists():
        sys.exit(f"Falta {zip_path}. Bájalo del portal de microdatos del INEI.")
    with zipfile.ZipFile(zip_path) as z:
        contenido = io.BytesIO(z.read(f"{zip_path.stem}/{nombre}"))
    df = pd.read_stata(contenido, convert_categoricals=False)
    # La columna del año llega como «aÑo»: pasa a «anio»
    df.columns = [c.lower().replace("ñ", "ni") for c in df.columns]
    for llave in llaves:
        df[llave] = df[llave].astype(str).str.strip()
    return df


def tasa(df, peso):
    """Porcentaje ponderado de pobres y de pobres extremos."""
    pesos = df[peso]
    return (
        100 * pesos[df["pobreza"] <= 2].sum() / pesos.sum(),
        100 * pesos[df["pobreza"] == 1].sum() / pesos.sum(),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anio", type=int, default=2024)
    anio = parser.parse_args().anio
    if anio not in ANIOS:
        sys.exit(f"No hay código ni cifras oficiales para {anio}. Años disponibles: {list(ANIOS)}")
    oficial = ANIOS[anio]
    codigo = oficial["codigo"]

    # 1 y 2. Leer y normalizar
    sumaria = leer(DATOS / f"{codigo}-Modulo34.zip", f"sumaria-{anio}.dta", LLAVES + ["ubigeo"])
    miembros = leer(DATOS / f"{codigo}-Modulo02.zip", f"enaho01-{anio}-200.dta", LLAVES_PERSONA)
    sumaria = sumaria[COLUMNAS_SUMARIA]

    # 3. Filtrar residentes habituales
    residente = ((miembros["p204"] == 1) & (miembros["p205"] == 2)) | (
        (miembros["p204"] == 2) & (miembros["p206"] == 1)
    )
    personas = miembros.loc[residente, COLUMNAS_MIEMBROS]

    # 4. Unir: cada persona con un solo hogar
    base = personas.merge(sumaria, on=LLAVES, how="left", validate="m:1", indicator=True)

    # 5. Construir
    base["departamento"] = base["ubigeo"].str[:2]
    base["urbano"] = base["estrato"] <= 5
    base["pobre"] = base["pobreza"] <= 2

    # 6. Validar
    pobreza, extrema = tasa(sumaria.assign(peso=sumaria["factor07"] * sumaria["mieperho"]), "peso")
    pobreza_personas, _ = tasa(base, "facpob07")
    pruebas = {
        "llaves de hogar únicas": not sumaria.duplicated(LLAVES).any(),
        "llaves de persona únicas": not personas.duplicated(LLAVES_PERSONA).any(),
        "ninguna fila perdida ni duplicada": len(base) == len(personas),
        "toda persona encontró su hogar": (base.pop("_merge") == "both").all(),
        "ubigeo con 6 dígitos": base["ubigeo"].str.fullmatch(r"\d{6}").all(),
        f"residentes = {oficial['residentes']:,}": len(base) == oficial["residentes"],
        f"pobreza a {TOLERANCIA} de {oficial['pobreza']} %": abs(pobreza - oficial["pobreza"]) < TOLERANCIA,
        f"extrema a {TOLERANCIA} de {oficial['extrema']} %": abs(extrema - oficial["extrema"]) < TOLERANCIA,
    }

    # 7. Guardar
    SALIDAS.mkdir(exist_ok=True)
    lineas = [
        f"ENAHO {anio}: validación",
        f"Hogares en la sumaria: {len(sumaria):,}",
        f"Residentes habituales: {len(base):,} de {len(miembros):,} filas en miembros",
        f"Pobreza (sumaria, factor07 × mieperho): {pobreza:.2f} %",
        f"Pobreza extrema (sumaria, factor07 × mieperho): {extrema:.2f} %",
        f"Pobreza (base de personas, facpob07): {pobreza_personas:.2f} %",
        "",
        *[f"{'OK   ' if ok else 'FALLA'} {prueba}" for prueba, ok in pruebas.items()],
    ]
    reporte = "\n".join(lineas) + "\n"
    (SALIDAS / "validacion.txt").write_text(reporte, encoding="utf-8")
    print(reporte)

    if not all(pruebas.values()):
        sys.exit("La validación falló: no se guardó la base.")
    base.to_parquet(SALIDAS / f"personas_{anio}.parquet", index=False)
    print(f"Guardado: {SALIDAS / f'personas_{anio}.parquet'}")


if __name__ == "__main__":
    main()
