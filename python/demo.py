"""Demostración interactiva, independiente del dataset y del benchmark."""
from time import perf_counter_ns  # Importa el reloj de alta resolución.
from busquedas import busqueda_lineal, busqueda_binaria, validar_orden  # Reutiliza los algoritmos.


def main():  # Organiza una demostración repetible.
    datos = [10, 20, 30, 40, 50, 60, 70]  # Lista pequeña editable delante del docente.
    while True:  # Permite repetir búsquedas y corregir entradas sin reiniciar.
        print('\nDatos:', datos)  # Muestra la lista actual y su orden.
        print('1: lineal | 2: binaria | 3: desordenar | 4: ordenar | 0: salir')  # Explica las opciones.
        try:  # Captura errores esperables del usuario.
            opcion = input('Opción: ').strip()  # Lee la selección sin espacios exteriores.
            if opcion == '0':  # Reconoce la salida voluntaria.
                return  # Termina la demostración.
            if opcion == '3':  # Prepara una entrada que viola la precondición.
                datos[0], datos[-1] = datos[-1], datos[0]  # Intercambia los extremos.
                continue  # Vuelve a mostrar el menú.
            if opcion == '4':  # Permite corregir el desorden.
                datos.sort()  # Ordena fuera del cronómetro de búsqueda.
                continue  # Vuelve al menú con la lista corregida.
            if opcion not in ('1', '2'):  # Rechaza opciones desconocidas.
                raise ValueError('Elige 0, 1, 2, 3 o 4.')  # Explica las opciones válidas.
            x = int(input('Clave entera: '))  # Convierte la clave; las letras producen ValueError.
            if opcion == '2':  # Comprueba la precondición solo para binaria.
                validar_orden(datos)  # Rechaza datos desordenados antes de medir.
            funcion = busqueda_lineal if opcion == '1' else busqueda_binaria  # Selecciona el algoritmo.
            inicio = perf_counter_ns()  # Inicia la región de medición.
            posicion, ops = funcion(datos, x)  # Ejecuta únicamente la búsqueda instrumentada.
            tiempo = perf_counter_ns() - inicio  # Finaliza la medición en nanosegundos.
            print(f'Posición (base 0): {posicion}; comparaciones/sondeos: {ops}; tiempo: {tiempo} ns')  # Muestra resultados.
        except ValueError as error:  # Captura conversiones y precondiciones inválidas.
            print('Entrada inválida:', error)  # Muestra un mensaje sin traza técnica.
        except (EOFError, KeyboardInterrupt):  # Permite cerrar la entrada o interrumpir.
            print('\nDemostración terminada.')  # Confirma el cierre.
            return  # Sale de forma limpia.
# Bloque completo: muestra, consulta, valida, mide y permite corregir errores.

if __name__ == '__main__':  # Evita iniciar el menú al importar el archivo.
    main()  # Ejecuta la demostración.
