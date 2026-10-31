---
name: graficando-enaho
description: Grafica la pobreza de la ENAHO del INEI por área (urbano y rural), sexo o grupo de edad, en barras listas para presentar. Úsala cuando pidan un gráfico, una figura o barras de la pobreza con la ENAHO, o comparar la pobreza entre esos grupos.
argument-hint: [area|sexo|edad]
---

# Graficar la ENAHO

Si no existe salidas/personas_2024.parquet, usa primero la skill limpiando-enaho.

1. Elige el corte según el pedido: area, sexo o edad.
2. Corre exactamente: `uv run ${CLAUDE_SKILL_DIR}/scripts/graficar.py --por <corte>`
3. Responde con la ruta del PNG en figuras/ y las cifras que imprime el script. No las recalcules.
4. Si piden otro corte u otra variable, dilo y ofrece los tres disponibles. No improvises un gráfico fuera del script.
