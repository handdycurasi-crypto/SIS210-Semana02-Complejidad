# SIS210 · Semana 2 · Complejidad y búsquedas

Proyecto reproducible con búsqueda lineal y binaria manuales en Python y C++20, demos interactivas, datos reales UCI, 2400 búsquedas registradas y un informe LaTeX compilado.

**Universidad:** Universidad Nacional del Altiplano – Puno  
**Escuela:** Ingeniería de Sistemas  
**Curso:** Algoritmos y Estructuras de Datos – SIS210  
**Docente:** ZANABRIA GALVEZ ALDO HERNAN  
**Integrantes:** YANA MENDOZA CARLOS BENEDICTO; BELIZARIO YANA DAVID VICTOR; CURASI ZEVALLOS HANDDY RONALD.

Objetivo: relacionar n, T(n), RAM, O/Ω/Θ y escenarios de entrada con sondeos y tiempos reales; distinguir costo de búsqueda y preparación.

## Empieza aquí

Para exponer, abre **GUIA_DEMO.md**: contiene una secuencia de 5 minutos. Para entregar, revisa **informe/informe.pdf**. Para comprender cada paso, lee **ANALISIS_TEORICO.md** y **PREGUNTAS_SUSTENTACION.md**.

Los resultados de `resultados/` pertenecen al **entorno remoto de Work**, no a la PC del estudiante. Las demos y el benchmark C++ fueron probados en Linux con GCC; la ejecución en Windows/MSVC debe comprobarse localmente. No se incluye ni se afirma un repositorio ya publicado en GitHub.

## Estructura

| Ruta | Contenido |
|---|---|
| python/ | Búsquedas comentadas; demo, preparación, benchmark, análisis, entorno y pruebas |
| cpp/ | Búsquedas comentadas y ejecutables separados para demo, benchmark y pruebas |
| datos/ | Cinco muestras reales con fila de origen, claves, metadatos y guía de descarga |
| resultados/ | Crudos, estadísticos, preparación, amortización y evidencias de ejecución |
| graficos/ | Sondeos y tiempos separados por lenguaje |
| informe/ | informe.tex, informe.pdf y tablas generadas desde CSV |
| referencias/ | Referencias APA 7 y enlaces verificados |
| CMakeLists.txt | Dos ejecutables independientes; compatible con Visual Studio/CMake |
| ANALISIS_REQUISITOS.md | Extracción de guía, decisiones, rúbrica y lista de cotejo |
| GUIA_DEMO.md | Demostración Windows, errores y correcciones |
| PLAN_COMMITS.md | Comandos para crear historial real localmente |
| DECLARACION_IA.md | Asistencia de IA y alcance de validación |
| REVISION_DOCENTE.md | Revisión crítica y pendientes del estudiante |

## Entorno utilizado y requisitos

Se ejecutó con Python **3.12.14**, GCC **13.3.0**, C++20, pandas **2.2.3**, matplotlib **3.10.8** y openpyxl **3.1.5**. SO Linux 6.18.35 x86_64; CPU visible AMD EPYC 9V74; 9 CPU lógicas visibles y cuota de CPU equivalente a 8 núcleos; memoria visible 16399700 kB, límite de contenedor 14 GiB. El entorno completo y reloj están en `resultados/entorno.json`.

Compilación medida: `-std=c++20 -O2 -Wall -Wextra -pedantic`. No se usó `-march=native` ni LTO. En Windows se recomienda Python 3.12 de 64 bits y MSVC o GCC con C++20. CMake 3.16+ es opcional; su configuración está preparada, pero no se ejecutó en Work porque CMake no estaba instalado. La compilación directa con GCC sí fue probada. Las demos usan únicamente bibliotecas estándar.

Instala dependencias para preparación/análisis desde la raíz:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell impide activar el entorno, no necesitas cambiar políticas: usa directamente `.\.venv\Scripts\python.exe` en lugar de `python` en todos los comandos Python. Fuera del entorno virtual puedes usar `py` en Windows; en Linux usa `python3`.

## Demo Python

```powershell
python python/demo.py
```

Con la lista inicial, lineal buscando 40 devuelve `(posición=3, sondeos=4)` y binaria devuelve `(3,1)`. El tiempo varía. Menú 3 desordena; menú 4 ordena; menú 0 termina.

## Demo y benchmark C++: elige un compilador

MSVC, en Developer PowerShell de Visual Studio, desde la raíz:

```powershell
mkdir build
cl /nologo /std:c++20 /O2 /EHsc /utf-8 cpp/demo.cpp /Fe:build/demo.exe
cl /nologo /std:c++20 /O2 /EHsc /utf-8 cpp/benchmark.cpp /Fe:build/benchmark.exe
.\build\demo.exe
```

GCC/MinGW, en una terminal con g++ disponible:

```powershell
mkdir build
g++ -std=c++20 -O2 -Wall -Wextra -pedantic cpp/demo.cpp -o build/demo.exe
g++ -std=c++20 -O2 -Wall -Wextra -pedantic cpp/benchmark.cpp -o build/benchmark.exe
.\build\demo.exe
```

Si `build` ya existe, omite mkdir. No compiles todos los `.cpp` en un mismo ejecutable: cada programa tiene su main.

También puedes abrir la carpeta con CMakeLists.txt en Visual Studio y seleccionar el destino demo o benchmark. Ruta CMake de terminal:

```powershell
cmake -S . -B build
cmake --build build --config Release
```

Con el generador de Visual Studio, los ejecutables suelen estar en `build/Release/`; ajusta las rutas de ejecución. La guía detallada y fuentes oficiales están en GUIA_DEMO.md y referencias/REFERENCIAS.md.

## Reproducir el experimento en tu PC sin sobrescribir Work

Ejecuta ambos lenguajes consecutivamente sobre los CSV incluidos. Para el ejemplo GCC:

```powershell
python python/registrar_entorno.py --etiqueta "PC del estudiante" --salida resultados_local
python python/benchmark.py --salida resultados_local
.\build\benchmark.exe . resultados_local 30
python python/analizar.py --salida resultados_local --graficos graficos_local
```

Si compilaste con MSVC, sustituye SOLO el comando de registro por:

```powershell
python python/registrar_entorno.py --etiqueta "PC del estudiante" --salida resultados_local --compilador cl --flags "/std:c++20 /O2 /EHsc /utf-8"
```

`registrar_entorno.py` consulta CPU y RAM locales en Windows y almacena el compilador; las banderas son declaradas y deben coincidir con el comando que utilizaste. Si el registro falla, corrige el compilador/terminal antes de atribuir resultados al entorno.

En Linux, usa `python3` y compila con `-o build/demo` y `-o build/benchmark`. Ejecuta `./build/benchmark . resultados_local 30`.

Para regenerar deliberadamente los archivos de `resultados/` y `graficos/`, omite `--salida`/`--graficos` en Python y ejecuta `./build/benchmark . resultados 30` (Windows: `.\build\benchmark.exe . resultados 30`). Hazlo solo cuando quieras reemplazar la sesión. No mezcles crudos de máquinas distintas en una misma carpeta. Los comandos originales están en COMANDOS_WORK.md.

## Datos y reproducibilidad

Se usa [Online Retail de UCI](https://doi.org/10.24432/C5BW33), de Chen (2015), bajo CC BY 4.0. Las muestras incluidas permiten repetir todo sin descargar el Excel. Para regenerarlas desde el archivo original consulta datos/LEEME.md.

Conteo observado: 541909 filas originales; 135080 CustomerID faltantes retirados; 406829 filas válidas; 4372 CustomerID distintos. Los duplicados de cliente se conservan. Los primeros cuatro tamaños se muestrean sin reemplazo; 500000 utiliza reemplazo explícito, no transacciones nuevas. Cada muestra registra semilla y SHA-256; cada fila conserva procedencia en Excel.

Tres claves únicas dentro de cada muestra se ubican en 0, n//2 y n−1 mediante intercambios: inicio, centro y final son posiciones exactas para lineal. Binaria usa una copia ordenada de esos mismos registros y los mismos objetivos. Los nombres de escenarios se refieren al orden original, no a posiciones después de ordenar. La consulta ausente usa máximo+1.

## Método de medición

5 tamaños × 2 algoritmos × 4 escenarios × 30 repeticiones × 2 lenguajes = **2400 búsquedas reales**. Se ejecuta un calentamiento por combinación, no registrado; después se mezcla el orden de tareas con semilla. Cada fila cruda corresponde a una llamada de búsqueda instrumentada, medida con perf_counter_ns o steady_clock.

No se incluyen lectura, copia, validación de orden, generación de muestras, selección de función, impresión ni escritura CSV en el intervalo de búsqueda. La llamada y su contador sí forman parte del costo observado; el reloj añade sobrecarga inevitable. El ordenamiento se repite 30 veces por tamaño y lenguaje sobre una nueva copia; se registra por separado (300 filas) y la copia tampoco se cronometra.

## Resultados incluidos

| n=100000, escenario ausente | Sondeos lineal | Sondeos binaria | Mediana lineal | Mediana binaria |
|---|---:|---:|---:|---:|
| Python | 100000 | 17 | 4183.473 µs | 2.7595 µs |
| C++ | 100000 | 17 | 27.140 µs | 0.050 µs |

En n=500000, lineal ausente realiza 500000 sondeos y binaria 19. Con el modelo de medianas y consultas ausentes repetidas, el ordenamiento se amortiza a partir de q=4 en Python y q=142 en C++. Son estimaciones de esta sesión, no umbrales universales. Para el inicio lineal no existe ventaja de amortización en estas mediciones.

- `resultados_crudos.csv`: 2400 filas; lenguaje, n, algoritmo, escenario, repetición, clave, posición de origen, posición encontrada, sondeos y ns.
- `resumen_estadistico.csv`: 80 filas; cantidad de repeticiones y promedio/mediana/mínimo/máximo tanto de tiempo como sondeos.
- `ordenamiento_crudo.csv` y `ordenamiento_resumen.csv`: mediciones separadas de preparación.
- `amortizacion.csv`: costos **modelados**, no nuevos benchmarks, para q=1 y q=1000 por escenario. Un q mínimo vacío significa que L≤B.
- `graficos/`: los cuatro gráficos principales usan ejes logarítmicos; tiempos en µs. Los conteos de ambos lenguajes coinciden.

## Pruebas de corrección

```powershell
python python/pruebas.py
g++ -std=c++20 -O2 -Wall -Wextra -pedantic cpp/pruebas.cpp -o build/pruebas.exe
.\build\pruebas.exe
```

Con MSVC, compila pruebas.cpp igual que demo.cpp cambiando el nombre de entrada/salida. Las pruebas contrastan 2070 consultas por lenguaje con bibliotecas usadas exclusivamente como oráculos, incluyendo vacíos, duplicados, negativos, extremos y potencias de dos. Python además comprueba mensajes para cuatro errores de dataset. El análisis cruza posición y sondeos de todos los resultados de ambos lenguajes.

## Informe LaTeX

El PDF compilado ya está incluido. Para recompilar instala TeX Live o MiKTeX con babel-spanish, geometry, graphicx, booktabs, amsmath, fancyhdr, microtype y hyperref; desde informe/:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error informe.tex
pdflatex -interaction=nonstopmode -halt-on-error informe.tex
```

Las tablas pueden volver a generarse con `python python/tablas_informe.py` desde la raíz, antes de compilar. El informe describe la sesión Work incluida. Repetir benchmarks locales no actualiza automáticamente la interpretación redactada: conserva ambas sesiones y, si deseas entregar tus mediciones, sustituye tablas/gráficos y revisa las conclusiones. No combines un informe de Work con CSV locales presentándolos como una misma sesión.

## Limitaciones y pendientes

Los escenarios son condicionados, las consultas repetidas calientan caché y solo se usa una muestra por n. La muestra de 500000 tiene reemplazo; los cuatro primeros tamaños también conservan duplicados de cliente. No se estima la distribución real de consultas. El tiempo pequeño de C++ está cerca del costo del reloj; no se concluye superioridad universal de un lenguaje. No se midió carga, copia ni actualizaciones en el modelo de amortización.

Antes de entregar: reproducir la demo en tu PC, revisar PREGUNTAS_SUSTENTACION.md, ejecutar PLAN_COMMITS.md y publicar tu repositorio real. No se incluyen historial Git ni marcas de tiempo inventados. La declaración de asistencia de IA está en DECLARACION_IA.md.
