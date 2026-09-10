# Revisión crítica con los criterios de la guía

Esta revisión no asigna una nota oficial ni sustituye la evaluación del docente.

| Criterio | Evidencia comprobada | Observación crítica |
|---|---|---|
| Análisis teórico, 25% | Conteo trazable 7n+5, cota ajustada, supuestos de promedio y derivación logarítmica | El estudiante debe explicar el convenio RAM; no memorizar 7n+5 como fórmula universal. |
| Implementación, 20% | Python y C++20 compilados/ejecutados; 2070 consultas contrastadas por lenguaje; demos probadas | MSVC/Windows no se ejecutó en Work. CMake está preparado, pero no se probó porque no estaba instalado; la compilación GCC directa sí pasó. |
| Experimento, 25% | 2400 búsquedas, 80 combinaciones, 30 repeticiones cada una; 300 ordenamientos separados | Las claves se condicionan para posiciones exactas. No representa una distribución natural de consultas. |
| Resultados, 15% | Crudos, estadísticos completos, cinco figuras desde CSV y modelo de amortización | La tabla del informe es una selección; el detalle se debe poder localizar en CSV. |
| Argumentación, 15% | Distinción entre cotas/casos, tiempo/sondeos, preparación/búsqueda y origen remoto/local | No afirmar superioridad universal de binaria ni del lenguaje C++. |

## Comprobaciones terminadas

- Se descargó el Excel real; se contaron 541909 filas, 135080 CustomerID faltantes y 406829 registros válidos.
- Las muestras incluidas conservan procedencia fila por fila y hashes. En 500000 se declara reemplazo.
- Los objetivos únicos preparados producen las posiciones lineales exactas requeridas.
- Python y C++ coinciden en clave, posición y sondeos para todos los casos medidos.
- Los errores de archivo ausente, columna ausente, limpieza vacía y tamaño excesivo sin reemplazo se probaron con Excel temporales.
- Las demos fueron ejecutadas con entrada de prueba: lineal/binaria, desorden, rechazo, ordenamiento, nueva búsqueda y texto inválido.
- El informe fue compilado realmente: portada más cinco páginas de contenido. Se revisaron visualmente las seis páginas; gráficos, tablas y texto permanecen dentro de márgenes.
- Se entregan referencias verificables, declaración de IA y plan de commits sin historial fabricado.

## Decisiones que pueden ser cuestionadas

**Elegir claves únicas.** Permite que final sea una primera coincidencia real aunque se preserven los demás repetidos. Solo se cambia el orden de la muestra. Debe declararse porque selecciona consultas poco frecuentes y no estima el caso promedio real.

**500000 con reemplazo.** Cumple el tamaño solicitado usando filas auténticas, pero no añade información independiente. Si el docente exige exclusivamente observaciones originales sin reemplazo, utiliza como máximo 406829 registros y documenta la excepción; no ocultes la construcción incluida.

**Comparaciones/sondeos.** Se conserva la métrica del código docente, pero binaria puede hacer dos relaciones de claves en una iteración. Es defendible siempre que se explique el convenio y no se confunda con todas las operaciones RAM.

**Reloj en búsquedas muy rápidas.** C++ registra decenas de ns para casos cortos: la medición incluye sobrecarga y cuantización. El contador determinista aporta evidencia más robusta de crecimiento que una razón de velocidad entre lenguajes.

**Costo total modelado.** Las proyecciones de q=1000 son cálculos con medianas, no mil nuevas búsquedas. Si el docente pide medir directamente ese lote, habría que añadir y ejecutar ese experimento; la guía exige modelar y discutir, por lo que esta entrega identifica las proyecciones con claridad.

## Pendientes personales antes de entregar

1. Abrir y ejecutar la demo en la PC que se usará para exponer; comprobar compilador e IDE.
2. Revisar la derivación RAM, el origen de los datos y la diferencia entre posición original y ordenada.
3. Crear los commits reales siguiendo PLAN_COMMITS.md y publicar en el repositorio de la cuenta del estudiante.
4. Si se decide entregar tiempos locales, regenerar los dos lenguajes juntos, guardar el entorno y actualizar de forma coherente el informe. No cambiar solo una tabla.

Estos pendientes requieren actuar en la PC/cuenta del estudiante; no se presentan como completados en Work.
