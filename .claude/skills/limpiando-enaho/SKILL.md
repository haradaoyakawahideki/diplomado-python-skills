---
name: limpiando-enaho
description: Limpia datos de la ENAHO del INEI y arma una base de personas con pobreza y factor de expansión. Úsala cuando pidan limpiar, unir o analizar la ENAHO, o calcular pobreza por región, sexo o edad.
---

# Limpiar la ENAHO

1. Si faltan los zip en datos/, pide al usuario bajarlos del INEI (código 966 = 2024).
2. Corre exactamente: `uv run ${CLAUDE_SKILL_DIR}/scripts/limpiar.py --anio 2024`
3. Lee salidas/validacion.txt. Si la pobreza difiere del INEI en más de 0.1 puntos, detente.
4. Responde con salidas/personas_2024.parquet; toda cifra va ponderada con facpob07.
5. Antes de usar una variable que no está en la base, lee reference.md.
