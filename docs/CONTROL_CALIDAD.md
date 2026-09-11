# Control de calidad - ampliación académica

## Alcance

La ampliación se limitó al contenido académico y documental. No se regeneraron benchmarks ni se sustituyeron resultados, CSV, gráficos, muestras o código de búsqueda.

## Núcleos teóricos

El marco teórico quedó organizado en **12 núcleos**:

1. Tamaño de entrada `n`.
2. Modelo RAM.
3. Función de costo `T(n)`.
4. Operación dominante y tasas de crecimiento.
5. Notación `O`.
6. Notación `Ω`.
7. Notación `Θ` y cota ajustada.
8. Mejor, promedio y peor caso.
9. Búsqueda lineal.
10. Búsqueda binaria.
11. Costo de preparación y amortización.
12. Complejidad teórica, rendimiento empírico y reproducibilidad.

Cada núcleo desarrolla definición, interpretación y relación con el experimento cuando corresponde. Se evitó agregar teoría desconectada del objetivo de la práctica.

## Referencias

La bibliografía se amplió con fuentes académicas y primarias: Cormen et al., Levitin, Skiena, Sedgewick y Wayne, Knuth, McGeoch, NIST/DADS, documentación oficial de Python/C++, UCI y la guía docente.

Se intentó mantener **aproximadamente tres fuentes pertinentes por párrafo teórico sustantivo**. La densidad de citas responde a la indicación académica comunicada por el docente; no se añadieron referencias deliberadamente ajenas al contenido solo para completar una cifra.

## Integridad experimental

Se conservaron sin modificaciones intencionales:

- `resultados/`
- `graficos/`
- `datos/`
- `cpp/`
- `python/`

La ampliación no modifica los 2400 registros de búsqueda, las 300 mediciones de ordenamiento ni las conclusiones empíricas derivadas de la sesión original.

## Estado del proyecto

- Repositorio: https://github.com/handdycurasi-crypto/SIS210-Semana02-Complejidad
- Demo Python validada localmente en Windows 10 con Python 3.14.5.
- Demo C++ validada localmente con MinGW GCC 14.2.0 de Code::Blocks.
- El benchmark conservado corresponde al entorno remoto de Work y se identifica explícitamente como tal.

## Limitación de extensión

La guía original solicita un informe de 3 a 5 páginas. La ampliación académica puede exceder ese rango porque se incorporaron al menos 10 núcleos teóricos y mayor profundidad para un trabajo de tres integrantes. Se priorizó densidad y relación directa con la práctica, evitando relleno y manteniendo la evidencia experimental intacta.
