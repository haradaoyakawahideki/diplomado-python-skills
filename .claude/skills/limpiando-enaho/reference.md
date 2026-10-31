# Referencia: ENAHO 2024

Cada zip trae el diccionario completo en PDF (`Diccionario2024.pdf`).

## Módulos

| Módulo | Archivo | Una fila por | Filas | Llaves | Factor |
|---|---|---|---|---|---|
| 34 · Sumaria | sumaria-2024.dta | hogar | 33,691 | conglome, vivienda, hogar | factor07 |
| 02 · Miembros | enaho01-2024-200.dta | persona | 117,721 | las tres + codperso | facpob07 |

## Variables de la base

| Variable | Significado |
|---|---|
| pobreza | 1 extremo, 2 no extremo, 3 no pobre. Es un código, nunca un promedio |
| pobre | pobreza ≤ 2 |
| mieperho | miembros del hogar |
| ubigeo, departamento | ubigeo de 6 dígitos; departamento son los 2 primeros, como texto |
| estrato, urbano | urbano es estrato ≤ 5 |
| dominio | dominio geográfico |
| p203 | parentesco |
| p204, p205, p206 | residencia; ya filtrada a residentes habituales |
| p207 | sexo |
| p208a | edad |
| facpob07 | factor de expansión de personas |
| factor07 | factor de expansión del hogar |

## Dos formas de ponderar

| Método | Pobreza nacional |
|---|---|
| Sumaria, factor07 × mieperho | 27.58 % |
| Base de personas, facpob07 | 27.53 % |

Ambas pasan la validación. La base usa facpob07 porque permite cortes por sexo y edad.
Las cifras pueden diferir hasta unas décimas: urbano 24.81 % y 24.74 %, rural 39.30 % y 39.44 %.

## Variables que no están en la base

Si hace falta otra columna, búscala en el diccionario y agrégala a `COLUMNAS_SUMARIA` o `COLUMNAS_MIEMBROS` en `scripts/limpiar.py`. No la unas a mano.
