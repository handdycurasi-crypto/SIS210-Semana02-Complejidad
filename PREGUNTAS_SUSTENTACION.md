# Preguntas probables y respuestas breves

1. **¿Qué es n?** Cantidad de registros CustomerID de la muestra, incluidos repetidos. No es el número de clientes distintos.
2. **¿Qué devuelve cada búsqueda?** Posición base cero o −1 y número de elementos examinados. Lineal entrega la primera coincidencia; binaria cualquiera en el arreglo ordenado.
3. **¿Qué es el modelo RAM?** Un modelo abstracto que asigna costo constante a operaciones elementales. Sirve para estudiar crecimiento sin atarnos a un procesador.
4. **¿Cómo derivaste T(n)?** En ausencia: 3 inicializaciones, n+1 controles, n accesos, 2n por incrementar ops, n igualdades, 2n por incrementar índice y 1 retorno. Total 7n+5 con el convenio declarado.
5. **¿7n+5 es el número exacto de instrucciones de Python?** No. Es un conteo RAM explícito de un recorrido equivalente. El intérprete y compilador implementan operaciones de otra manera.
6. **¿El CSV debería tener 7n+5 comparaciones?** No. Registra la operación dominante: n sondeos para lineal ausente. T_RAM incluye más operaciones.
7. **¿Por qué Θ(n)?** Para n≥1, 7n≤7n+5≤12n. Existe cota inferior y superior lineal.
8. **¿O es peor caso y Ω mejor caso?** No. Son cotas de una función. El peor caso lineal también es Ω(n); el mejor caso también es O(1).
9. **¿Qué es Θ?** Cota ajustada: mismo orden de cota superior e inferior. No significa automáticamente promedio.
10. **¿Cuál es el mejor caso lineal?** Clave en la primera posición: un sondeo, Θ(1). Final y ausente necesitan n sondeos.
11. **¿Qué promedio teórico estás usando?** Con éxito y posiciones distintas equiprobables, (n+1)/2 sondeos. Nuestro experimento de cuatro escenarios no estima esa distribución.
12. **¿Treinta repeticiones son el caso promedio?** No. Repiten la misma búsqueda para resumir variación del reloj y del entorno.
13. **¿Por qué binaria necesita orden?** Porque al comparar con el centro solo puede descartar una mitad si todos sus valores respetan ese orden.
14. **¿Por qué es logarítmica?** Después de k divisiones quedan aproximadamente n/2^k elementos; al llegar a uno, k≈log2 n.
15. **¿Cuál es la cota exacta de sondeos?** Para n≥1, floor(log2 n)+1; con n=8 puede necesitar 4. Para n=0 son 0.
16. **¿El centro original es siempre mejor caso de binaria?** No. Ordenar cambia las posiciones. Su mejor caso ocurre en el centro de la copia ordenada.
17. **¿Cada sondeo binario es una sola comparación?** Es una visita al elemento central; puede ejecutar igualdad y menor-que. Se sigue el contador ops de la guía y se declara esa diferencia.
18. **¿Qué hay dentro del cronómetro?** La llamada de búsqueda y el contador. No lectura, ordenamiento, copia, validación, impresión ni escritura CSV.
19. **¿Por qué no validar orden dentro de binaria?** Esa validación cuesta O(n) y ocultaría el costo de una búsqueda logarítmica. Se verifica al preparar.
20. **¿Cómo evitas que C++ elimine la búsqueda?** Se consume la posición y contador en la validación y CSV después de medir; el resultado es observable. Se compila con O2, sin LTO.
21. **¿Por qué hay 500000 si quedaron 406829 registros?** Se remuestrean filas válidas con reemplazo y se registra la procedencia. No se inventan identificadores ni transacciones independientes.
22. **¿Por qué no eliminaste duplicados?** Representan registros distintos del mismo cliente; eliminarlos cambiaría n a clientes únicos y limitaría el universo a 4372.
23. **¿Cómo garantizas el final real?** Selecciono una clave que aparece una vez en la muestra y la intercambio con la última posición; así no existe coincidencia anterior.
24. **¿Eso sesga el experimento?** Sí, condiciona claves y posiciones deliberadamente para comparar casos controlados. Se conserva el multiconjunto, pero no representa consultas aleatorias de clientes.
25. **¿Misma muestra significa mismo orden?** Mismos registros; lineal usa el orden preparado y binaria su copia ordenada, tal como plantea la guía. Ambos lenguajes comparten los mismos CSV y claves.
26. **¿Cómo identificas una clave ausente?** Uso máximo de la muestra +1. Es una consulta construida y no se agrega a los datos.
27. **¿Por qué promedio y mediana pueden diferir?** El promedio es sensible a interrupciones o valores extremos. La mediana resume el centro. También conservamos mínimo y máximo.
28. **¿Puede Θ(n) ser más rápido que Θ(log n)?** Sí: para n pequeño o al inicio, constantes y costos fijos importan. En nuestras mediciones el inicio lineal es más rápido.
29. **¿Qué efecto tiene la caché?** Accesos repetidos pueden abaratar memoria aunque no cambie el número de sondeos. El benchmark incluye calentamiento y no mide arranque en frío.
30. **¿Por qué no declarar C++ siempre mejor?** Estos tiempos dependen del equipo, compilador, representación, instrumentación y consultas. No se comparan todos los programas posibles ni todas las cargas.
31. **¿Cuándo compensa ordenar?** Si L>B, para q>S/(L−B), usando costos comparables. Si L≤B, este modelo no da amortización favorable.
32. **¿Qué dice el experimento de una sola consulta?** Debe sumarse S a B. Para una consulta puede convenir recorrer directamente los datos desordenados.
33. **¿Mil consultas se midieron realmente?** No como lote adicional. amortizacion.csv proyecta S+qB y qL con medianas; los nombres indican que es un modelo.
34. **¿Qué pasa si llegan datos nuevos constantemente?** Hay que considerar mantener o reconstruir el orden. El modelo de colección estable deja de describir todos los costos.
35. **¿Qué estructura podría usarse después?** Tabla hash con búsqueda esperada O(1), a cambio de memoria y colisiones; árbol equilibrado para búsqueda/actualización O(log n).
36. **¿Qué cambia con consultas no uniformes?** El promedio depende de qué claves se repiten y dónde se encuentran. En lineal puede convenir ubicar las frecuentes al principio si el problema lo permite.
37. **¿Qué hipótesis planteas para una búsqueda nativa?** Una implementación nativa podría reducir constantes frente al bucle Python, manteniendo el mismo orden asintótico si ejecuta el mismo algoritmo. Habría que medirlo controlando datos, conversión e instrumentación.
38. **¿Qué memoria adicional necesitas?** Las búsquedas iterativas usan O(1) auxiliar. La copia ordenada del experimento ocupa O(n) extra.
39. **¿Qué pruebas hiciste?** Oráculos de biblioteca, 2070 consultas por lenguaje con casos extremos, validación de orden y errores; además, coincidencia de posiciones y sondeos entre lenguajes para 2400 búsquedas reales.
40. **¿Qué falta antes de entregar?** Probar en la PC del estudiante, crear los commits y publicar el repositorio. Work no afirma haber hecho esos pasos locales.
41. **¿Usaste IA?** Sí, para estructurar, programar, revisar y documentar. Las pruebas y mediciones incluidas son ejecuciones reales en Work; los integrantes deben revisar y comprender el contenido.
42. **¿Cómo detectas un bucle en binaria?** Compruebo que cada iteración reduzca el intervalo; izq=medio+1 y der=medio−1 garantizan progreso cuando no hay igualdad.

## Repaso de 30 segundos

n cuenta elementos. RAM cuenta operaciones abstractas. Lineal visita uno por uno; binaria divide un intervalo ordenado. O es cota superior, Ω inferior y Θ ajustada. Casos y cotas se analizan por separado. Los sondeos explican crecimiento; el reloj mide velocidad en un entorno. Ordenar tiene un costo que solo puede amortizarse con suficientes consultas adecuadas.
