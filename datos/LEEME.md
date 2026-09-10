# Datos reales y procedencia

Fuente: Chen, D. (2015). *Online Retail* [Conjunto de datos]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

Licencia de los datos: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Adaptación realizada: extracción de CustomerID, descarte de faltantes/no enteros, muestreo de filas y permutación de tres objetivos. No hay afiliación con UCI ni con el autor.

Los cinco CSV incluidos son suficientes para ejecutar ambos benchmarks sin conexión. Contienen `fila_excel` (número de fila del Excel original, cabecera en fila 1) y `CustomerID`. La columna de procedencia no se cronometra ni se busca. `claves.csv` fija los objetivos de ambos lenguajes. `metadatos.json` contiene conteos observados, semillas y huellas SHA-256.

Para volver al origen:

1. Abrir https://archive.ics.uci.edu/dataset/352/online+retail
2. Pulsar Download y extraer `Online Retail.xlsx` del ZIP.
3. Guardarlo en `datos/Online Retail.xlsx`.
4. Desde la raíz ejecutar:

```powershell
py python/preparar_datos.py "datos/Online Retail.xlsx" --permitir-reemplazo
```

La descarga directa oficial es https://archive.ics.uci.edu/static/public/352/online+retail.zip

El Excel original no se incluye para reducir tamaño. Se puede cotejar su SHA-256 con `original_sha256` de los metadatos. La preparación tarda más que la demostración.

## Decisiones metodológicas

- No se eliminan duplicados de CustomerID: una persona puede tener varias transacciones.
- No se filtran anulaciones, precios o países: el problema es localizar el identificador, no calcular ventas.
- Para tamaños hasta 100 000 se seleccionan filas sin reemplazo; esto NO implica CustomerID distintos.
- Para 500 000 se remuestrean filas válidas con reemplazo. Son valores y filas reales repetidos, no 500 000 transacciones independientes. Si se omite `--permitir-reemplazo`, el programa rechaza tamaños mayores al disponible.
- Una semilla `21002+n` determina cada muestra. La secuencia de Python de la versión registrada y los CSV incluidos fijan la reproducibilidad exacta.
- Tres claves que aparecen una sola vez en la muestra se intercambian con las posiciones 0, n//2 y n−1. Así hay primera coincidencia exacta al inicio, centro y final. Es un diseño condicionado, no una simulación de consultas uniformes.
- La clave ausente es máximo de la muestra +1. Es una consulta construida, no un CustomerID observado que se agregue al dataset.
- Lineal usa la muestra en el orden del CSV y binaria una copia ascendente: mismos registros y claves, posiciones distintas. La binaria retorna índice dentro de la copia ordenada.
- Los lenguajes leen exactamente los mismos CSV. Cambiar datos obliga a regenerar las mediciones de ambos y a actualizar el informe.
