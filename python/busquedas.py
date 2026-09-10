"""Algoritmos manuales; comparaciones significa sondeos (como ops en la guía)."""

def busqueda_lineal(a, x):  # Recibe una lista y la clave que se desea encontrar.
    ops = 0  # Empieza sin elementos examinados.
    for i, valor in enumerate(a):  # Recorre índices y valores desde el inicio.
        ops += 1  # Cuenta un sondeo: examinar un elemento.
        if valor == x:  # Comprueba si el elemento es la clave.
            return i, ops  # Devuelve la primera posición coincidente y el contador.
    return -1, ops  # Si agotó la lista, informa que la clave está ausente.
# Bloque completo: recorre secuencialmente y se detiene en la primera coincidencia.


def busqueda_binaria(a, x):  # Requiere que a ya esté ordenada de menor a mayor.
    izq, der, ops = 0, len(a) - 1, 0  # Delimita el intervalo inclusivo y el contador.
    while izq <= der:  # Continúa mientras exista al menos una posición candidata.
        medio = izq + (der - izq) // 2  # Calcula el índice central inferior.
        ops += 1  # Cuenta un sondeo, no todas las expresiones booleanas.
        if a[medio] == x:  # Compara la clave con el elemento central.
            return medio, ops  # Devuelve una coincidencia; no garantiza la primera.
        if a[medio] < x:  # Decide si la clave solamente puede estar a la derecha.
            izq = medio + 1  # Descarta la mitad izquierda y el centro.
        else:  # Si el elemento central es mayor, conserva la parte izquierda.
            der = medio - 1  # Descarta la mitad derecha y el centro.
    return -1, ops  # El intervalo vacío demuestra ausencia en una lista ordenada.
# Bloque completo: reduce a la mitad el intervalo; validar el orden se hace fuera.


def validar_orden(a):  # Se usa antes de medir, nunca dentro de la búsqueda.
    if any(a[i] > a[i + 1] for i in range(len(a) - 1)):  # Detecta una inversión.
        raise ValueError('La búsqueda binaria requiere datos ordenados. Ordena primero.')  # Explica la solución.
# Bloque completo: rechaza listas desordenadas; cuesta O(n) y no se cronometra.
