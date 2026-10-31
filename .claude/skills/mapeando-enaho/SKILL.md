---
name: mapeando-enaho
description: Dibuja un mapa de la pobreza de la ENAHO del INEI por departamento del Perú y lista los departamentos con más y menos pobreza. Úsala cuando pidan un mapa, un coroplético o la distribución geográfica de la pobreza con la ENAHO.
---

# Mapear la ENAHO

Si no existe salidas/personas_2024.parquet, usa primero la skill limpiando-enaho.

1. Si falta datos/peru_departamental_simple.geojson, pide al usuario bajarlo del repositorio del curso.
2. Corre exactamente: `uv run ${CLAUDE_SKILL_DIR}/scripts/mapear.py`
3. Si el script falla porque no hay 25 departamentos con dato, detente y muestra el error. No entregues un mapa incompleto.
4. Responde con la ruta del PNG en mapas/ y los departamentos con más y menos pobreza que imprime el script. No los recalcules.
