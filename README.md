# diplomado-python-skills

Tres skills de Claude Code que limpian, grafican y mapean la ENAHO 2024. Clona el repositorio, pide «un mapa de la pobreza por departamento» y Claude usa las skills, con la pobreza oficial replicada.

| Skill | Entra | Sale |
|---|---|---|
| `limpiando-enaho` | Zips de los módulos 34 y 02 | `salidas/personas_2024.parquet`, `salidas/validacion.txt` |
| `graficando-enaho` | Base limpia y un corte: área, sexo o edad | `figuras/pobreza_<corte>_2024.png` |
| `mapeando-enaho` | Base limpia y límites de los 25 departamentos | `mapas/pobreza_departamento.png` |

Si falta la base limpia, las otras dos skills usan primero `limpiando-enaho`.

## Cómo usarlo

Requiere [uv](https://docs.astral.sh/uv/) y [Claude Code](https://claude.com/claude-code). Los datos no se versionan; se descargan así:

```bash
git clone https://github.com/haradaoyakawahideki/diplomado-python-skills.git
cd diplomado-python-skills
uv sync

mkdir -p datos && cd datos
curl -fLO https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/966-Modulo34.zip
curl -fLO https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/966-Modulo02.zip
curl -fLO https://raw.githubusercontent.com/d2cml-ai/Data-Science-Python/main/sessions/06-geoespacial/lab/Data/peru_departamental_simple.geojson
cd ..
```

Luego abre `claude` en la raíz del repositorio y pide, por ejemplo:

- ¿Cuál fue la pobreza en Cusco en 2024?
- Grafica la pobreza urbana y rural con la ENAHO 2024
- Haz un mapa de la pobreza por departamento con la ENAHO 2024

## Validación

| Prueba | Oficial o esperado | Resultado |
|---|---|---|
| Pobreza nacional | 27.6 % | 27.58 % |
| Pobreza extrema | 5.5 % | 5.50 % |
| Residentes habituales | 108,664 | 108,664 |

`limpiar.py` no guarda la base si alguna prueba falla. El detalle está en `salidas/validacion.txt`.

## Ponderación

Las skills de limpieza y gráficos ponderan con `facpob07`, que permite cortes por sexo y edad. El mapa pondera con `factor07 × mieperho` para replicar las cifras de referencia de la clase. Por eso una misma cifra puede variar unas décimas: Ica da 6.0 % con el segundo método y 5.91 % con el primero.

## Límites

Solo cubre la ENAHO 2024 y los módulos 34 y 02. Son estimaciones de una muestra y las skills no calculan márgenes de error.

## Archivos

- `.claude/skills/`: las tres skills.
- `evaluacion.md`: tres pedidos, con y sin skills.
- `sesion.ipynb`: bitácora de la sesión, paso a paso.
