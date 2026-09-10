# Modelo RAM, costo y casos

## Qué representa n

n es la longitud de la muestra: número de registros CustomerID almacenados. Dos registros pueden corresponder al mismo cliente y cuentan como dos elementos. La operación dominante es examinar una posición de la lista.

## Derivación trazable de la lineal

Usamos una traducción conceptual con `n = longitud(a)`, `i = 0`, `ops = 0`, `while i < n`, lectura `a[i]`, incremento de ops, comparación con x, retorno si coincide e incremento de i si no coincide. Es equivalente al recorrido `enumerate`/`for` del código, pero NO pretende contar bytecodes de Python ni instrucciones de CPU.

Convenio RAM de costo unitario: asignación, suma, comparación, acceso y retorno cuestan 1. `v += 1` se descompone en suma + asignación: cuesta 2. Longitud almacenada y asignación de n se consideran una operación abstracta conjunta. Retornar el par posición/ops también se cuenta como una operación abstracta constante. Se incluye la instrumentación.

| Operación | Ausente, n elementos | Hallado en la k-ésima posición visitada |
|---|---:|---:|
| Inicializar n, i y ops | 3 | 3 |
| Evaluar i < n | n+1 | k |
| Acceder a a[i] | n | k |
| Incrementar ops (suma y asignación) | 2n | 2k |
| Comparar valor == x | n | k |
| Incrementar i (suma y asignación) | 2n | 2(k−1) |
| Retornar resultado | 1 | 1 |
| Total | **7n+5** | **7k+2** |

Ausente: T(n)=3+(n+1)+n+2n+n+2n+1=7n+5. En el último elemento: T(n)=7n+2. El mayor de ambos es el ausente. En el primero k=1 y T=9, constante. Cambiar el convenio cambia las constantes, no el orden.

Para n≥1, 7n ≤ 7n+5 ≤ 12n. Por tanto T está en Ω(n) y O(n), luego Θ(n). Podemos elegir c1=7, c2=12 y n0=1. Para n=0 el algoritmo retorna ausencia sin sondeos; el análisis asintótico mira n grande.

El contador entregado NO es T_RAM: `ops=n` para ausencia y `ops=k` para éxito. Resume la operación dominante. Contabilizar ops añade trabajo real al benchmark, incluido por igual en los dos lenguajes.

## Promedio no es «centro»

Si hay n valores distintos, la búsqueda es exitosa y cada posición es igualmente probable, E[ops]=(1+2+…+n)/n=(n+1)/2. Así E[T]=7(n+1)/2+2=Θ(n).

Si la probabilidad de ausencia es p y el éxito sigue siendo uniforme, E[ops]=p·n+(1−p)(n+1)/2. En datos repetidos o consultas sesgadas estas probabilidades cambian; no basta tomar la posición central. Las 30 repeticiones del mismo caso miden variación temporal, no 30 datasets ni el promedio probabilístico del algoritmo.

## Binaria

La lista debe estar ordenada: solo así, si a[medio] < x, se puede descartar todo lo que está a la izquierda. El intervalo inclusivo comienza en [0,n−1] y se vacía cuando izq>der.

Después de k reducciones, quedan como máximo aproximadamente n/2^k candidatos. Resolver n/2^k ≤ 1 da k≥log2(n). Cada iteración hace un número constante de operaciones RAM, de modo que el peor costo es Θ(log n). Para n≥1 esta implementación hace como máximo floor(log2 n)+1 sondeos; para n=0 hace 0.

El mejor caso es que la clave coincida con el primer centro: un sondeo y Θ(1). Con claves distintas y éxito uniforme, la profundidad media de un árbol de búsqueda equilibrado es Θ(log n). Con duplicados y otras distribuciones no se debe trasladar este promedio automáticamente.

Si hay s sondeos y termina encontrando la clave, hay s comparaciones de igualdad y s−1 comparaciones `<` de claves: 2s−1 relaciones entre claves. Si no encuentra, hay 2s. Además existen comparaciones de control `izq <= der`. El CSV cuenta s, conforme al código del docente.

## Cotas y escenarios son dimensiones distintas

- O(g(n)): existen c>0 y n0 tales que T(n)≤c·g(n) para n≥n0: cota superior.
- Ω(g(n)): existen c>0 y n0 tales que T(n)≥c·g(n): cota inferior.
- Θ(g(n)): existen c1,c2>0 y n0 con c1·g(n)≤T(n)≤c2·g(n): cota ajustada.

Se aplican a una función de costo ya definida: mejor, peor o esperada. El peor caso lineal es también Ω(n). Su mejor caso es también O(1). Por eso O no equivale a peor, Ω no equivale a mejor y Θ no equivale a promedio. Un costo lineal también es O(n²), aunque esa cota es menos informativa que O(n).

## Memoria y preparación

Ambas búsquedas iterativas usan Θ(1) memoria auxiliar, sin contar el arreglo de entrada. Mantener original y copia ordenada requiere Θ(n) memoria adicional en el proyecto. El ordenamiento de biblioteca se mide por separado; Python y C++ pueden usar estrategias diferentes. No se atribuye el costo de validar orden (Θ(n)) a la búsqueda binaria.

Para una colección estable: total lineal = q·L; total binaria = S+q·B, con S costo de ordenar, L y B tiempos por consulta. Si L>B, binaria ofrece ventaja estricta cuando q>S/(L−B). El primer entero es floor(S/(L−B))+1. Si L≤B no existe amortización favorable en este modelo.

Se excluye del modelo el costo de copia, carga, red, inserciones y reconstrucción de índices. Es un modelo condicionado a estas mediciones, no una nueva medición de q consultas. Una tabla hash puede ofrecer búsqueda esperada O(1), con memoria extra, colisiones y peor caso potencial O(n); un árbol equilibrado ofrece búsqueda y actualizaciones O(log n).
