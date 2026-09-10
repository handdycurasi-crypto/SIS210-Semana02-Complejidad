"""Extrae CustomerID real y crea muestras compartidas, trazables y condicionadas."""
import argparse  # Lee opciones de la terminal.
import csv  # Escribe CSV interoperables.
import hashlib  # Calcula huellas de integridad.
import json  # Guarda metadatos legibles.
import random  # Proporciona muestreo con semilla fija.
from collections import Counter  # Identifica claves únicas dentro de una muestra.
from pathlib import Path  # Maneja rutas en Windows y Linux.
import pandas as pd  # Lee el Excel original de UCI.

RAIZ = Path(__file__).resolve().parents[1]  # Sitúa el proyecto independientemente del directorio actual.
TAMANOS = [100, 1000, 10000, 100000, 500000]  # Define los cinco tamaños exigidos.


def huella(ruta):  # Recibe un archivo para verificar su contenido.
    return hashlib.sha256(ruta.read_bytes()).hexdigest()  # Devuelve SHA-256 de los bytes exactos.
# Bloque completo: permite comprobar que se usaron los mismos archivos.


def escribir_csv(ruta, cabecera, filas):  # Centraliza la escritura de las muestras.
    with ruta.open('w', newline='', encoding='utf-8') as archivo:  # Abre sin líneas vacías extra en Windows.
        escritor = csv.writer(archivo)  # Construye un escritor CSV.
        escritor.writerow(cabecera)  # Identifica las columnas.
        escritor.writerows(filas)  # Guarda las filas en su orden definitivo.
# Bloque completo: genera CSV legibles en ambos lenguajes.


def preparar(ruta, tamanos, permitir_reemplazo):  # Recibe el Excel y las decisiones de muestreo.
    if not ruta.is_file():  # Verifica que exista el origen.
        raise ValueError('Dataset no encontrado. Descarga Online Retail.xlsx y pasa su ruta.')  # Indica qué falta.
    tabla = pd.read_excel(ruta, engine='openpyxl')  # Lee el Excel fuera de cualquier benchmark.
    if 'CustomerID' not in tabla.columns:  # Comprueba la variable requerida.
        raise ValueError('Falta la columna CustomerID; utiliza el Excel original de UCI.')  # Explica el error.
    columna = pd.to_numeric(tabla['CustomerID'], errors='coerce')  # Convierte valores numéricos; inválidos quedan NaN.
    validos = columna.notna() & columna.mod(1).eq(0)  # Conserva únicamente identificadores enteros no faltantes.
    limpios = [(int(i) + 2, int(v)) for i, v in columna[validos].items()]  # Conserva la fila de Excel (incluye cabecera).
    if not limpios:  # Detecta limpieza sin registros utilizables.
        raise ValueError('El dataset quedó vacío después de limpiar CustomerID.')  # Evita muestrear una lista vacía.
    destino = RAIZ / 'datos'  # Elige la carpeta compartida.
    destino.mkdir(exist_ok=True)  # Crea la carpeta si todavía no existe.
    claves = []  # Reúne objetivos comunes a Python y C++.
    muestras = []  # Reúne la trazabilidad de cada tamaño.
    for n in tamanos:  # Construye cada tamaño solicitado.
        if n <= 0:  # Impide tamaños sin sentido.
            raise ValueError('El tamaño debe ser un entero positivo.')  # Explica la corrección.
        reemplazo = n > len(limpios)  # Decide si hacen falta filas repetidas por remuestreo.
        if reemplazo and not permitir_reemplazo:  # Respeta la prohibición explícita del usuario del programa.
            raise ValueError(f'Tamaño {n} mayor que {len(limpios)}. Usa --permitir-reemplazo para remuestrear.')  # Explica la opción.
        rng = random.Random(21002 + n)  # Independiza cada muestra mediante su propia semilla.
        muestra = rng.choices(limpios, k=n) if reemplazo else rng.sample(limpios, n)  # Muestrea filas reales.
        conteos = Counter(valor for fila, valor in muestra)  # Cuenta multiplicidades de CustomerID.
        unicos = [valor for fila, valor in muestra if conteos[valor] == 1]  # Busca objetivos sin coincidencias previas.
        if len(unicos) < 3:  # No inventa claves si el dataset no admite los escenarios exactos.
            raise ValueError(f'n={n}: faltan tres CustomerID únicos en la muestra; revisa la semilla o el dataset.')  # Detalla el problema.
        for nombre, posicion, clave in zip(['inicio', 'centro', 'final'], [0, n // 2, n - 1], unicos[:3]):  # Asigna objetivos distintos.
            actual = next(i for i, registro in enumerate(muestra) if registro[1] == clave)  # Localiza la fila del objetivo.
            muestra[posicion], muestra[actual] = muestra[actual], muestra[posicion]  # Cambia solo el orden, no los valores.
            claves.append([n, nombre, clave, posicion])  # Guarda la posición esperada exacta en la muestra desordenada.
        claves.append([n, 'ausente', max(conteos) + 1, -1])  # Construye una consulta que no pertenece a la muestra.
        archivo = destino / f'muestra_{n}.csv'  # Define un nombre idéntico para ambos lenguajes.
        escribir_csv(archivo, ['fila_excel', 'CustomerID'], muestra)  # Guarda valores y procedencia fila por fila.
        muestras.append({'n': n, 'semilla': 21002 + n, 'con_reemplazo': reemplazo, 'customerid_distintos': len(conteos), 'sha256': huella(archivo)})  # Documenta cada muestra.
    escribir_csv(destino / 'claves.csv', ['n', 'escenario', 'clave', 'posicion_origen'], claves)  # Fija las consultas comparables.
    meta = {'fuente': 'https://archive.ics.uci.edu/dataset/352/online+retail', 'doi': '10.24432/C5BW33', 'licencia': 'CC BY 4.0', 'original_sha256': huella(ruta), 'filas_originales': len(tabla), 'faltantes_customerid': int(tabla.CustomerID.isna().sum()), 'descartadas': int((~validos).sum()), 'filas_validas': len(limpios), 'customerid_distintos': len(set(v for _, v in limpios)), 'duplicados_adicionales_customerid': len(limpios) - len(set(v for _, v in limpios)), 'muestras': muestras, 'diseno': 'Muestreo de filas; tres claves de multiplicidad 1 se permutan al inicio, centro y final. El multiconjunto no cambia. No representa consultas promedio aleatorias.'}  # Registra datos observados y decisiones.
    (destino / 'metadatos.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')  # Conserva la auditoría.
    print(json.dumps(meta, indent=2, ensure_ascii=False))  # Muestra el resumen de preparación.
# Bloque completo: limpia, muestrea, fija escenarios exactos y conserva la trazabilidad.

if __name__ == '__main__':  # Ejecuta el preparador solo desde terminal.
    parser = argparse.ArgumentParser(description=__doc__)  # Crea ayuda de uso.
    parser.add_argument('excel', type=Path)  # Solicita la ruta del archivo original.
    parser.add_argument('--tamanos', nargs='+', type=int, default=TAMANOS)  # Permite reducir tamaños en equipos limitados.
    parser.add_argument('--permitir-reemplazo', action='store_true')  # Exige hacer explícita la ampliación por remuestreo.
    args = parser.parse_args()  # Obtiene los argumentos.
    try:  # Traduce errores esperables a mensajes breves.
        preparar(args.excel, args.tamanos, args.permitir_reemplazo)  # Ejecuta la preparación completa.
    except (ValueError, OSError) as error:  # Captura problemas de datos y archivos.
        parser.exit(1, f'Error: {error}\n')  # Finaliza con una explicación y estado de error.
