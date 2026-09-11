# Distribución sugerida para sustentación - 3 integrantes

## YANA MENDOZA CARLOS BENEDICTO

**Núcleos 1-4**

- Tamaño de entrada `n`.
- Modelo RAM.
- Función de costo `T(n)`.
- Operación dominante y tasas de crecimiento.

Debe poder explicar por qué el modelo RAM no pretende imitar exactamente una CPU y cómo se pasa del código a una función de costo.

## BELIZARIO YANA DAVID VICTOR

**Núcleos 5-8**

- Notación `O`.
- Notación `Ω`.
- Notación `Θ`.
- Mejor, promedio y peor caso.

Debe poder corregir la afirmación incorrecta `O = peor caso`, `Ω = mejor caso`, `Θ = promedio` y dar un ejemplo con búsqueda lineal.

## CURASI ZEVALLOS HANDDY RONALD

**Núcleos 9-12 + evidencia experimental**

- Búsqueda lineal.
- Búsqueda binaria.
- Costo de preparación y amortización.
- Complejidad teórica frente a rendimiento empírico y reproducibilidad.

Debe poder ejecutar la demo, explicar por qué la binaria exige orden, mostrar el error cuando los datos están desordenados, corregirlo, comentar los gráficos y distinguir resultados del entorno remoto de la validación local.

## Pregunta común para los tres

**¿Por qué no basta con medir tiempo para afirmar la complejidad de un algoritmo?**

Respuesta esperada: porque la complejidad describe el crecimiento de una función de costo respecto a `n`, mientras el tiempo real también depende de constantes, hardware, compilador/intérprete, caché y sistema operativo. El benchmark aporta evidencia empírica, pero no sustituye la derivación teórica.
