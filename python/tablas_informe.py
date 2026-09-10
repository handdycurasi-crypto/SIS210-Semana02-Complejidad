"""Exporta tablas LaTeX desde los CSV reales; no reescribe las conclusiones."""
import argparse  # Permite elegir la sesión de datos.
from pathlib import Path  # Maneja rutas de origen y destino.
import pandas as pd  # Lee los resúmenes reales.

RAIZ = Path(__file__).resolve().parents[1]  # Identifica la raíz del proyecto.


def numero(valor, decimales=0):  # Formatea cifras legibles en LaTeX.
    return f'{valor:,.{decimales}f}'.replace(',', r'\,')  # Separa miles con espacio fino.
# Bloque completo: transforma números observados a texto tipográfico, sin cambiar su valor.


def exportar(salida):  # Genera las tablas del informe desde una sesión explícita.
    resumen = pd.read_csv(salida / 'resumen_estadistico.csv')  # Lee estadísticas de búsqueda.
    amortizacion = pd.read_csv(salida / 'amortizacion.csv')  # Lee el modelo basado en medianas.
    filas = []  # Acumula la comparación de sondeos para n=100000.
    for escenario in ['inicio', 'centro', 'final', 'ausente']:  # Presenta los escenarios en orden pedagógico.
        d = resumen.query('n == 100000 and lenguaje == "Python" and escenario == @escenario').set_index('algoritmo')  # Usa conteos comunes entre lenguajes.
        filas.append(f"{escenario.capitalize()} & {numero(d.loc['lineal','comparaciones_mediana'])} & {numero(d.loc['binaria','comparaciones_mediana'])} " + r'\\')  # Construye una fila de sondeos.
    (RAIZ / 'informe/tabla_sondeos.tex').write_text('\n'.join(filas), encoding='utf-8')  # Guarda la tabla insertable.
    filas = []  # Reinicia para tiempos de n=100000.
    for lenguaje in ['Python', 'C++']:  # Conserva los lenguajes separados.
        for escenario in ['inicio', 'centro', 'final', 'ausente']:  # Recorre los cuatro casos.
            d = resumen.query('n == 100000 and lenguaje == @lenguaje and escenario == @escenario').set_index('algoritmo')  # Recupera medianas reales.
            filas.append(f"{lenguaje} & {escenario.capitalize()} & {numero(d.loc['lineal','mediana_ns']/1000,3)} & {numero(d.loc['binaria','mediana_ns']/1000,3)} " + r'\\')  # Convierte ns a µs para la tabla.
    (RAIZ / 'informe/tabla_tiempos.tex').write_text('\n'.join(filas), encoding='utf-8')  # Guarda la tabla de tiempos.
    filas = []  # Reinicia para costo total.
    for lenguaje in ['Python', 'C++']:  # Compara cada lenguaje consigo mismo.
        for q in [1, 1000]:  # Contrasta una consulta y mil.
            f = amortizacion.query('n == 500000 and escenario == "ausente" and lenguaje == @lenguaje and q == @q').iloc[0]  # Selecciona proyección específica.
            filas.append(f"{lenguaje} & {q} & {numero(f.total_lineal_modelado_ns/1e6,3)} & {numero(f.total_binaria_modelado_ns/1e6,3)} " + r'\\')  # Expresa totales modelados en ms.
    (RAIZ / 'informe/tabla_amortizacion.tex').write_text('\n'.join(filas), encoding='utf-8')  # Conserva la tabla del modelo.
    print('Tablas exportadas; revisa manualmente texto, entorno y conclusiones si cambiaste la sesión.')  # Evita confundir actualización de números con revisión del informe.
# Bloque completo: convierte estadísticas existentes a tablas sin fabricar resultados.

if __name__ == '__main__':  # Permite invocación desde terminal.
    parser = argparse.ArgumentParser(description=__doc__)  # Define ayuda.
    parser.add_argument('--salida', type=Path, default=RAIZ / 'resultados')  # Selecciona la sesión Work por defecto.
    args = parser.parse_args()  # Lee la opción.
    exportar(args.salida)  # Genera los fragmentos LaTeX.
