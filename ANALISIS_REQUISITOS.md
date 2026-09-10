# Lectura completa de la guía oficial

Fuente: guía de laboratorio SIS210, Semana 2, siete páginas, facilitada por el docente. El Markdown del estudiante agrega requisitos de demostración, comentarios por línea, ZIP y documentación.

| Elemento | Requisito extraído | Evidencia del proyecto |
|---|---|---|
| Objetivos (secciones 2–3) | Definir n, derivar T(n), distinguir cotas y casos, medir y reproducir | Informe; ANALISIS_TEORICO.md |
| Algoritmos | Lineal y binaria manuales en Python y C++20 | python/busquedas.py; cpp/busquedas.hpp |
| Dataset (secciones 7–8) | Online Retail, UCI, DOI 10.24432/C5BW33; CustomerID o StockCode | datos/metadatos.json; datos/LEEME.md |
| Tamaños | 100, 1 000, 10 000, 100 000, 500 000 si el equipo permite | Cinco muestras CSV incluidas |
| Escenarios | Inicio, centro, final, ausente | datos/claves.csv; posiciones originales exactas |
| Control | Misma muestra y mismas claves; preparación separada | Muestras con SHA-256 y fila de origen; copia ordenada para binaria |
| Repeticiones | Al menos 30 por combinación | 80 combinaciones × 30 = 2400 búsquedas, dos lenguajes |
| Métricas | Comparaciones y tiempo; promedio, mediana, mínimo, máximo | resultados_crudos.csv; resumen_estadistico.csv |
| Relojes | perf_counter_ns y std::chrono | Benchmark de cada lenguaje |
| Preparación | Medir ordenamiento separado de búsqueda | 300 ordenamientos crudos y resumen |
| Visualización | n vs. comparaciones; n vs. tiempo | Cuatro gráficos principales, separados por lenguaje |
| Costo total (sección 14) | Una consulta vs. miles; preparación + q × consulta | amortizacion.csv; discusión del informe |
| Entregables (15–16) | Repositorio, CSV, gráficos, README, informe de 3–5 páginas, IA | ZIP preparado para Git; informe LaTeX compilado |
| Git (12 y 15) | baseline, analysis, benchmark, final | PLAN_COMMITS.md; commits pendientes de ejecución local por solicitud del estudiante |
| Reproducibilidad | Versiones, comandos, fuente y procedimiento | README.md; resultados/entorno.json; COMANDOS_WORK.md |
| Preguntas de análisis (19) | Constantes, Ω, caché, ordenamiento, distribución, lenguajes | PREGUNTAS_SUSTENTACION.md |

## Inconsistencias y decisiones

- La portada dice Semana 1 (diagnóstica), pero título y contenido corresponden a Semana 2: se usa Semana 2.
- La portada dice C++17; resultados de aprendizaje, recursos y código dicen C++20: se usa C++20.
- La portada dice Python 3.12+ y recursos dicen 3.11+: se ejecutó con Python 3.12; se recomienda 3.12 para reproducir.
- La duración global declara dos horas, pero las fases suman 150 minutos: se registra la diferencia; no se utiliza como límite artificial de ejecución.
- La tabla teórica da aproximadamente ceil(log2 n) sondeos para binaria. La cota máxima exacta para este intervalo inclusivo es floor(log2 n)+1 cuando n≥1. Para n=8, buscar una clave mayor que todas exige 4 sondeos, no 3.
- El código base llama `ops` a un incremento por elemento central; no cuenta por separado `==`, `<` ni control del bucle. Se conserva esa métrica para comparabilidad y se la identifica como «comparaciones/sondeos».
- CustomerID contiene repetidos: se conservan. Para que inicio/centro/final sean posiciones de primera coincidencia, tres claves de multiplicidad uno en cada muestra se permutan a esos lugares. La copia de binaria cambia posiciones, no el multiconjunto ni las claves. No se presenta este diseño condicionado como promedio de consultas reales.
- El catálogo UCI declara ausencia de faltantes, pero la limpieza del Excel encuentra celdas CustomerID vacías. Se da prioridad al archivo observado y se registra el conteo real.
- La exposición en «VS» proviene de apuntes del estudiante, no del PDF. Se documentan tanto Visual Studio como VS Code, sin atribuir al docente un IDE específico.

## Rúbrica (20 puntos)

| Criterio | Peso | Requisito para destacado |
|---|---:|---|
| Análisis teórico | 25% | Derivación de T(n), cotas y casos con rigor |
| Implementación | 20% | Ambos lenguajes correctos e instrumentados |
| Experimento | 25% | Controles, ≥30 repeticiones, crudos |
| Resultados | 15% | Tablas, gráficos y estadísticos interpretados |
| Argumentación | 15% | Separar teoría, medición y limitaciones |

## Lista de cotejo

- [x] n representa registros, no clientes únicos.
- [x] Carga, copia, validación y ordenamiento fuera de la búsqueda cronometrada.
- [x] Misma muestra y claves entre algoritmos y lenguajes.
- [x] 30 repeticiones por cada combinación, observaciones individuales conservadas.
- [x] Promedio, mediana, mínimo, máximo y sondeos en los CSV.
- [x] Código y datos crudos incluidos.
- [x] O, Ω y Θ separados de escenarios.
- [x] Conclusiones distinguen crecimiento y velocidad observada.
- [x] Dataset, documentación y bibliografía citados.
- [x] Declaración de IA incluida.
- [ ] El estudiante debe ejecutar los commits localmente y publicar en su cuenta.
- [ ] El estudiante debe probar la demostración en su PC antes de exponer.

La validación empírica automática se conserva en resultados/validacion_matriz.txt. La prueba local y la publicación no se afirman realizadas desde Work.
