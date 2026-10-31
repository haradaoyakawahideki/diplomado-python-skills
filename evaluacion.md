# Evaluación: tres pedidos, con y sin skills

Cada corrida usó `claude -p` en una copia limpia: solo `pyproject.toml`, `uv.lock` y `datos/`, sin salidas previas.
Las corridas con skills incluyen `.claude/`. Las corridas sin skills no la incluyen y usan `--disallowedTools Skill`.

| Pedido | Modo | Skills activadas | Cifra | Ponderó | Figura | Tiempo | Costo |
|---|---|---|---|---|---|---|---|
| ¿Cuál fue la pobreza en Cusco en 2024? | Con | limpiando | 18.5 % | facpob07 | No aplica | 57 s | $0.22 |
| | Sin | Ninguna | 18.54 % | factor07 × mieperho | No aplica | 97 s | $0.24 |
| Grafica la pobreza urbana y rural con la ENAHO 2024 | Con | graficando + limpiando | 24.74 % y 39.44 % | facpob07 | Sigue las reglas | 62 s | $0.24 |
| | Sin | Ninguna | 24.8 % y 39.3 % | factor07 × mieperho | Dos colores; línea nacional añadida | 119 s | $0.48 |
| Haz un mapa de la pobreza por departamento con la ENAHO 2024 | Con | mapeando + limpiando | Cajamarca 45.0 %, Ica 6.0 % | factor07 × mieperho | Sigue las reglas | 77 s | $0.29 |
| | Sin | Ninguna | Cajamarca 45.0 %, Ica 6.0 % | factor07 × mieperho | Por rangos, con etiquetas; archivo en otra ruta | 175 s | $0.84 |

## Lectura

- **Las skills fijan el resultado:** producen las mismas rutas y reglas, en menos tiempo y a menor costo en los tres pedidos.
- **Sin skills las cifras también salieron bien:** Claude acertó solo los números de esta prueba, pero eligió por su cuenta formato, ruta y colores. Es una sola corrida por pedido.
- **Con facpob07 hay diferencias de décimas:** urbano 24.74 % frente a 24.8 %, y rural 39.44 % frente a 39.3 %.
- **Error corregido:** `$0` en `limpiando-enaho` tomaba una palabra del pedido (`--anio ENAHO`). Ahora el comando usa `--anio 2024`. La tabla de las corridas con skills es posterior a esa corrección.
