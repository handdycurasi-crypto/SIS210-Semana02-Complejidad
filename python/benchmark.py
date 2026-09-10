"""Ejecuta las 1200 búsquedas de Python y 150 ordenamientos separados."""
import argparse  # Permite elegir la carpeta de salida y repeticiones.
import csv  # Lee muestras y registra ejecuciones individuales.
import random  # Alterna el orden experimental con semilla fija.
from pathlib import Path  # Construye rutas portables.
from time import perf_counter_ns  # Mide intervalos en nanosegundos.
from busquedas import busqueda_lineal, busqueda_binaria, validar_orden  # Reutiliza las búsquedas manuales.

RAIZ = Path(__file__).resolve().parents[1]  # Ubica la raíz del proyecto.
CABECERA = ['lenguaje', 'n', 'algoritmo', 'escenario', 'repeticion', 'clave', 'posicion_origen', 'posicion', 'comparaciones', 'tiempo_ns']  # Define el esquema compartido.


def ejecutar(salida, repeticiones):  # Ejecuta una sesión completa de Python.
    if repeticiones < 30:  # Comprueba el mínimo de la guía.
        raise ValueError('El benchmark exige al menos 30 repeticiones; para algo rápido usa demo.py.')  # Sugiere el modo adecuado.
    salida.mkdir(parents=True, exist_ok=True)  # Prepara el destino de resultados.
    with (RAIZ / 'datos/claves.csv').open(encoding='utf-8') as archivo:  # Carga las consultas fuera del cronómetro.
        consultas = list(csv.DictReader(archivo))  # Mantiene las mismas claves que C++.
    with (salida / 'crudos_python.csv').open('w', newline='', encoding='utf-8') as crudos, (salida / 'ordenamiento_python.csv').open('w', newline='', encoding='utf-8') as ordenes:  # Abre las dos salidas.
        escritor, preparacion = csv.writer(crudos), csv.writer(ordenes)  # Prepara escritores independientes.
        escritor.writerow(CABECERA)  # Identifica los datos de búsqueda.
        preparacion.writerow(['lenguaje', 'n', 'repeticion', 'tiempo_ns'])  # Identifica los datos de ordenamiento.
        for n in sorted(set(int(c['n']) for c in consultas)):  # Recorre los tamaños presentes.
            with (RAIZ / f'datos/muestra_{n}.csv').open(encoding='utf-8') as archivo:  # Carga la muestra compartida.
                datos = [int(f['CustomerID']) for f in csv.DictReader(archivo)]  # Convierte identificadores a enteros.
            if len(datos) != n:  # Rechaza muestras incompletas.
                raise ValueError(f'Muestra {n}: contiene {len(datos)} filas; regenera los datos.')  # Explica cómo corregir.
            for r in range(1, repeticiones + 1):  # Repite la preparación de manera independiente.
                ordenados = datos.copy()  # Excluye el costo de copia del tiempo de ordenamiento.
                inicio = perf_counter_ns()  # Inicia la medición exclusiva de ordenar.
                ordenados.sort()  # Ordena una copia inicialmente desordenada.
                duracion = perf_counter_ns() - inicio  # Termina el intervalo.
                preparacion.writerow(['Python', n, r, duracion])  # Guarda cada ordenamiento real.
            validar_orden(ordenados)  # Verifica la precondición fuera del tiempo de búsqueda.
            casos = [c for c in consultas if int(c['n']) == n]  # Selecciona los cuatro objetivos de este tamaño.
            tareas = [(r, c, a) for r in range(1, repeticiones + 1) for c in casos for a in ['lineal', 'binaria']]  # Construye la matriz experimental.
            random.Random(902 + n).shuffle(tareas)  # Reduce el sesgo por ejecutar siempre el mismo algoritmo primero.
            for c in casos:  # Realiza un calentamiento no registrado por caso.
                busqueda_lineal(datos, int(c['clave']))  # Calienta la ejecución lineal.
                busqueda_binaria(ordenados, int(c['clave']))  # Calienta la ejecución binaria.
            for r, c, algoritmo in tareas:  # Ejecuta una búsqueda por observación.
                x = int(c['clave'])  # Convierte la clave antes de medir.
                a = datos if algoritmo == 'lineal' else ordenados  # Selecciona el arreglo adecuado.
                funcion = busqueda_lineal if algoritmo == 'lineal' else busqueda_binaria  # Selecciona la función antes de medir.
                inicio = perf_counter_ns()  # Inicia la región cronometrada.
                posicion, ops = funcion(a, x)  # Ejecuta la búsqueda y su contador.
                tiempo = perf_counter_ns() - inicio  # Cierra la región cronometrada.
                esperado = int(c['posicion_origen'])  # Recupera la posición original registrada.
                if (posicion == -1) != (esperado == -1) or (posicion >= 0 and a[posicion] != x):  # Verifica existencia y valor encontrado.
                    raise ValueError('Resultado incorrecto: revisar la implementación antes de usar los CSV.')  # Impide publicar datos erróneos.
                if algoritmo == 'lineal' and posicion != esperado:  # Comprueba que los escenarios sean exactos.
                    raise ValueError('La posición lineal no coincide con el escenario preparado.')  # Detecta modificaciones del dataset.
                escritor.writerow(['Python', n, algoritmo, c['escenario'], r, x, esperado, posicion, ops, tiempo])  # Guarda una ejecución real.
            print(f'Python: n={n} completado')  # Informa avance fuera de las mediciones.
# Bloque completo: mide búsquedas aisladas y ordenamientos separados; valida cada resultado.

if __name__ == '__main__':  # Habilita uso desde terminal.
    parser = argparse.ArgumentParser(description=__doc__)  # Prepara ayuda.
    parser.add_argument('--salida', type=Path, default=RAIZ / 'resultados')  # Permite separar sesiones locales.
    parser.add_argument('--repeticiones', type=int, default=30)  # Cumple el mínimo por defecto.
    args = parser.parse_args()  # Lee las opciones.
    try:  # Evita trazas ante problemas esperables.
        ejecutar(args.salida, args.repeticiones)  # Lanza el experimento.
    except (OSError, ValueError, KeyError) as error:  # Captura errores de archivos, muestras y columnas.
        parser.exit(1, f'Error: {error}. Revisa datos/ y ejecuta preparar_datos.py si falta una muestra.\n')  # Explica el paso de recuperación.
