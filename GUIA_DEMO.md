# Demostración en Windows: aproximadamente 5 minutos

## Antes de la exposición

Extrae el ZIP completo. Abre la carpeta `SIS210-Semana02-Complejidad`, la que contiene README.md y CMakeLists.txt. No abras el ZIP como carpeta de trabajo. Esta demo usa siete números didácticos, identificados como tales; el benchmark separado usa UCI real. No requiere descargar el Excel ni ejecutar 2400 búsquedas para mostrar el programa.

En VS Code: Archivo → Abrir carpeta → selecciona esa raíz. Abre Terminal → Nueva terminal. En Visual Studio: instala la carga de trabajo «Desarrollo para el escritorio con C++» y abre la carpeta que contiene CMakeLists.txt. Son programas diferentes; no sabemos a cuál se refería el docente con «VS».

Para Python necesitas Python 3.12. Verifica `py --version`. Para esta demo no necesitas pandas ni otras bibliotecas. Para C++ necesitas un compilador C++20; VS Code por sí mismo no lo instala.

## Secuencia recomendada

| Tiempo | Acción | Explicación breve |
|---|---|---|
| 0:00–0:40 | Mostrar python/busquedas.py y su contador | «n es el número de elementos; contamos cada posición examinada». |
| 0:40–1:35 | Ejecutar demo Python: lineal, clave 40 | «La posición es 3 porque contamos desde cero; visitamos cuatro elementos». |
| 1:35–2:15 | Seleccionar binaria, clave 40 | «El centro ya es 40; basta un sondeo porque los datos están ordenados». |
| 2:15–3:15 | Desordenar, intentar binaria, corregir y repetir | «La condición de orden es necesaria. El mensaje indica la corrección». |
| 3:15–4:10 | Mostrar cpp/busquedas.hpp y ejecutar demo C++ | «La lógica y los sondeos coinciden; los tiempos pueden cambiar». |
| 4:10–5:00 | Abrir resumen CSV y gráficos | «Las mediciones incluidas son de Work; cada grupo tiene 30 ejecuciones». |

## Ejecutar Python

En la terminal de la raíz:

```powershell
py python/demo.py
```

Selecciona `1`, escribe `40`. Debe aparecer posición `3` y comparaciones/sondeos `4`. El tiempo es variable: no memorices un número de nanosegundos.

Selecciona `2`, escribe `40`. Debe aparecer posición `3` y sondeos `1`.

Selecciona `1`, escribe `99`: posición `-1`, sondeos `7`. Selecciona `2`, escribe `99`: posición `-1`, sondeos `3`.

## Mostrar un error y corregirlo

1. Desde la lista inicial, selecciona `3` para intercambiar extremos: `[70, 20, 30, 40, 50, 60, 10]`.
2. Selecciona `2` y clave `10`. Debe mostrar que la búsqueda binaria requiere datos ordenados; no ejecutará una búsqueda inválida.
3. Selecciona `4` para ordenar.
4. Selecciona `2` y clave `10`: posición `0`, sondeos `3`.
5. Escribe una opción inexistente o una clave `abc`: aparece un mensaje y puedes volver a intentar.

Explica que validar el orden cuesta O(n) y se realiza antes del cronómetro. En un sistema real se mantiene la garantía de orden al preparar la colección, en vez de verificar toda la lista antes de cada consulta.

## Compilar y ejecutar C++ con Visual Studio (MSVC)

Abre **Developer PowerShell for VS** o **x64 Native Tools Command Prompt for VS**. Navega a la raíz del proyecto y ejecuta:

```powershell
mkdir build
cl /nologo /std:c++20 /O2 /EHsc /utf-8 cpp/demo.cpp /Fe:build/demo.exe
.\build\demo.exe
```

Si `build` ya existe, no es necesario volver a crearla. Las opciones del menú son las mismas que Python.

Alternativa desde Visual Studio: Archivo → Abrir → Carpeta, selecciona la raíz con CMakeLists.txt, espera la configuración de CMake, elige configuración Release y destino `demo.exe`, ejecuta sin depurar. Los nombres precisos del menú pueden variar según la versión. El modo de consola mediante `cl` anterior es la ruta reproducible. No añadas los dos archivos `demo.cpp` y `benchmark.cpp` al mismo ejecutable: ambos tienen main.

## C++ con VS Code y GCC/MinGW

Si ya tienes g++ en PATH:

```powershell
mkdir build
g++ -std=c++20 -O2 -Wall -Wextra -pedantic cpp/demo.cpp -o build/demo.exe
.\build\demo.exe
```

Para editar y poner puntos de interrupción en VS Code puedes instalar la extensión oficial C/C++ de Microsoft. No es necesaria para compilar con la terminal. Los binarios de Work son Linux y no se incluyen como ejecutables Windows: debes compilar localmente.

## Qué archivo mostrar y qué significan las salidas

- Primero `python/busquedas.py`: contiene la lógica comentada, sin configuración experimental.
- Después `cpp/busquedas.hpp`: muestra la misma lógica en C++.
- `demo.py` y `demo.cpp`: contienen el menú y el cronómetro.
- `posicion` es base cero; `-1` significa ausente. En el benchmark binario corresponde a la copia ordenada, no a la fila original de Excel.
- `comparaciones` cuenta sondeos conforme al código del docente; un sondeo binario puede ejecutar `==` y `<`. No representa todo T(n).
- `tiempo_ns` es tiempo observado con cronómetro e instrumentación; no es una garantía para otra PC.

## Mostrar los CSV y gráficos

Abre `resultados/resumen_estadistico.csv` con Excel, LibreOffice Calc o VS Code. Si Excel coloca todo en una columna, utiliza Datos → Desde texto/CSV y elige coma como delimitador y UTF-8. Filtra n=100000 y escenario=ausente. Cada fila resumida corresponde a 30 búsquedas, no a un único intento.

Abre `resultados/resultados_crudos.csv` para mostrar que cada repetición está guardada. Sus columnas incluyen lenguaje, n, algoritmo, escenario, repetición, clave, posición original, posición devuelta, sondeos y tiempo.

Abre `graficos/comparaciones_python.png`: el final y el ausente lineales crecen con n, mientras binaria necesita pocos sondeos. Inicio lineal es constante. Los mismos sondeos se obtienen en C++; no es necesario superponer líneas idénticas.

Abre `graficos/tiempo_python.png` y `graficos/tiempo_cpp.png`: ambas escalas son logarítmicas, y los tiempos están en microsegundos. No leas una línea ascendente de un gráfico log-log como si fueran ejes lineales. La binaria puede fluctuar; no todas las consultas tienen la misma profundidad.

Abre `resultados/ordenamiento_resumen.csv` para mostrar que ordenar se midió aparte. `amortizacion.csv` contiene proyecciones aritméticas para q=1 y q=1000, no mil nuevas consultas cronometradas.

## Cambio de código que puede pedir el docente

Cambia la lista didáctica agregando `80` al final en demo.py o demo.cpp. Guarda. En Python vuelve a ejecutar `py python/demo.py`; en C++ vuelve a compilar y luego ejecuta. Busca `80`: lineal devuelve posición `7` con `8` sondeos; binaria devuelve posición `7` con `4` sondeos.

Puede pedir cambiar la clave, introducir duplicados o explicar `medio + 1`. Con duplicados, lineal devuelve la primera coincidencia y binaria cualquiera. Si eliminas el `+1` al actualizar izq, el intervalo puede no reducirse y el programa puede quedar en bucle: restaura la línea original y recompila. Para detener una ejecución trabada, Ctrl+C.

Para una modificación inocua durante la demo, también puedes cambiar el texto «Clave entera» por «CustomerID»; luego guardar y volver a ejecutar/compilar. No alteres los CSV publicados sin regenerar los resultados.

## Errores frecuentes y solución

| Problema | Causa probable | Solución |
|---|---|---|
| `py` no reconocido | Python o lanzador no instalado | Instala Python 3.12; prueba `python --version` y usa `python` si está disponible. |
| `cl` no reconocido | Terminal normal o falta carga C++ | Abre Developer PowerShell de Visual Studio y verifica la instalación C++. |
| `g++` no reconocido | Falta GCC/MinGW o PATH | Usa MSVC con Visual Studio o configura un GCC C++20 existente. |
| No se encuentra el archivo | Terminal en otra carpeta | Abre la raíz que contiene python, cpp y datos. |
| `main` duplicado al enlazar | Compilaste todos los .cpp juntos | Compila demo, benchmark y pruebas como ejecutables separados. |
| Letras en la clave | Se esperaba un entero | Escribe un número; el programa permite intentar otra vez. |
| Binaria requiere orden | Lista desordenada | Menú 4 y vuelve a consultar. |
| Dataset no encontrado | Falta Excel al regenerar | Descarga como indica datos/LEEME.md; los benchmarks ya usan los CSV incluidos. |
| Falta CustomerID | Archivo de origen equivocado | Usa Online Retail.xlsx original, no una exportación con columnas renombradas. |
| Dataset vacío al limpiar | Todos los valores son vacíos/no numéricos | Revisa la hoja y la columna de origen. |
| Tamaño mayor al disponible | 500000 > filas válidas | Usa --permitir-reemplazo y explica el remuestreo. |
| `ModuleNotFoundError` en benchmark/análisis | Dependencias sin instalar | `py -m pip install -r requirements.txt`. La demo no las necesita. |
| CSV incompletos | Solo se ejecutó un lenguaje o hubo interrupción | Ejecuta ambos benchmarks en la misma carpeta de salida, luego analizar.py. |
| Programa C++ no cambia | No recompilaste tras guardar | Repite el comando de compilación y ejecuta el nuevo binario. |

## Qué no debes afirmar

No digas que las mediciones de Work son de tu PC. No presentes la muestra de 500000 como transacciones independientes originales. No digas que Ω significa mejor caso ni que binaria siempre gana. No confundas el promedio temporal de 30 repeticiones con el caso promedio probabilístico.
