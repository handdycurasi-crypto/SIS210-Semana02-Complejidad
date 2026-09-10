"""Pruebas de corrección con oráculos, extremos y errores de entrada."""
import random  # Genera casos reproducibles.
import tempfile  # Aísla archivos de prueba que no forman parte del dataset.
import unittest  # Ejecuta y reporta pruebas independientes.
from pathlib import Path  # Maneja rutas temporales.
import pandas as pd  # Crea pequeños Excel de prueba para errores de limpieza.
from busquedas import busqueda_lineal, busqueda_binaria, validar_orden  # Importa el código bajo prueba.
from preparar_datos import preparar  # Importa validación de datos originales.

class Pruebas(unittest.TestCase):  # Agrupa controles de corrección.
    def test_oraculo(self):  # Contrasta resultados con la biblioteca, usada solo como oráculo.
        rng = random.Random(73)  # Fija la secuencia de pruebas.
        for n in [0, 1, 2, 3, 7, 8, 16, 31, 100]:  # Incluye vacíos, extremos y potencias de dos.
            for _ in range(10):  # Prueba diez arreglos por tamaño.
                datos = [rng.randrange(-10, 11) for _ in range(n)]  # Incluye negativos y duplicados.
                ordenados = sorted(datos)  # Satisface la precondición de binaria.
                for x in range(-11, 12):  # Incluye claves presentes y ausentes.
                    p, ops = busqueda_lineal(datos, x)  # Ejecuta la implementación manual.
                    esperado = datos.index(x) if x in datos else -1  # Consulta el oráculo independiente.
                    self.assertEqual(p, esperado)  # Verifica primera coincidencia o ausencia.
                    self.assertEqual(ops, p + 1 if p >= 0 else n)  # Verifica el contador exacto.
                    p, ops = busqueda_binaria(ordenados, x)  # Ejecuta la segunda búsqueda manual.
                    self.assertEqual(p >= 0, x in datos)  # Contrasta la existencia.
                    if p >= 0: self.assertEqual(ordenados[p], x)  # Verifica el valor devuelto.
                    self.assertLessEqual(ops, n.bit_length())  # Comprueba la cota floor(log2(n))+1, cero si n=0.
    # Bloque completo: contrasta miles de consultas sin exigir el mismo índice en duplicados.

    def test_orden_y_demo(self):  # Verifica errores y respuestas que se explican en clase.
        with self.assertRaises(ValueError): validar_orden([30, 10, 20])  # Rechaza una lista desordenada.
        self.assertEqual(busqueda_lineal([10, 20, 30, 40, 50, 60, 70], 40), (3, 4))  # Verifica el ejemplo lineal.
        self.assertEqual(busqueda_binaria([10, 20, 30, 40, 50, 60, 70], 40), (3, 1))  # Verifica el ejemplo binario.
        self.assertEqual(busqueda_binaria([0] * 8, 1)[1], 4)  # Detecta la imprecisión ceil(log2 n) en potencias de dos.
    # Bloque completo: protege la demostración y el límite exacto de iteraciones.

    def test_errores_dataset(self):  # Verifica mensajes de preparación sin alterar los datos del proyecto.
        with tempfile.TemporaryDirectory() as carpeta:  # Crea un espacio descartable.
            ruta = Path(carpeta) / 'prueba.xlsx'  # Define el Excel de prueba.
            with self.assertRaisesRegex(ValueError, 'no encontrado'): preparar(ruta, [100], False)  # Comprueba archivo ausente.
            pd.DataFrame({'otra': [1]}).to_excel(ruta, index=False)  # Crea un Excel sin CustomerID.
            with self.assertRaisesRegex(ValueError, 'columna CustomerID'): preparar(ruta, [100], False)  # Comprueba columna ausente.
            pd.DataFrame({'CustomerID': ['invalido']}).to_excel(ruta, index=False)  # Crea un dataset no utilizable.
            with self.assertRaisesRegex(ValueError, 'vacío'): preparar(ruta, [100], False)  # Comprueba limpieza vacía.
            pd.DataFrame({'CustomerID': [1, 2, 3]}).to_excel(ruta, index=False)  # Crea tres registros válidos ficticios solo de prueba.
            with self.assertRaisesRegex(ValueError, 'mayor'): preparar(ruta, [100], False)  # Comprueba rechazo sin reemplazo autorizado.
    # Bloque completo: ejercita cuatro problemas previsibles con archivos temporales.

if __name__ == '__main__':  # Ejecuta pruebas únicamente al invocar este archivo.
    unittest.main(verbosity=2)  # Muestra pruebas aprobadas o fallidas.
