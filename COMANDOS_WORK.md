# Comandos ejecutados en el entorno remoto de Work

Los comandos se muestran relativos a la raíz del proyecto para que sean legibles. En Work el Excel original se descargó y extrajo en una carpeta temporal; el argumento equivalente se indica aquí.

```bash
python3 python/preparar_datos.py '../tmp/original/Online Retail.xlsx' --permitir-reemplazo
g++ -std=c++20 -O2 -Wall -Wextra -pedantic cpp/demo.cpp -o build/demo
g++ -std=c++20 -O2 -Wall -Wextra -pedantic cpp/benchmark.cpp -o build/benchmark
g++ -std=c++20 -O2 -Wall -Wextra -pedantic cpp/pruebas.cpp -o build/pruebas
python3 python/pruebas.py
./build/pruebas
python3 python/registrar_entorno.py --etiqueta 'Entorno remoto de Work'
python3 python/benchmark.py
./build/benchmark . resultados 30
python3 python/analizar.py
python3 python/tablas_informe.py
```

Las ejecuciones de Python y C++ se hicieron consecutivamente, no simultáneamente. Sus salidas se conservan en resultados/ejecucion_python.txt y ejecucion_cpp.txt. Las pruebas se guardan en pruebas_python.txt y pruebas_cpp.txt. Las versiones y límites reales están en entorno.json.

El orden de tareas se mezcla con semilla 902+n en cada lenguaje; los generadores no producen necesariamente el mismo orden, pero sí el mismo conjunto de consultas y repeticiones. Carga, preparación de tareas, validación y escritura no forman parte del intervalo de búsqueda. No se fijó afinidad ni se aisló la CPU de toda carga del sistema.

El informe se compila desde informe/ con `pdflatex -interaction=nonstopmode -halt-on-error informe.tex` dos veces; las páginas se renderizan con `pdftoppm` y se inspeccionan visualmente.
