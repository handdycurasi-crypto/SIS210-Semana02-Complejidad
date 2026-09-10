"""Consolida CSV reales, comprueba la matriz y genera estadísticos y gráficos."""
import argparse  # Lee carpetas de entrada y salida.
import math  # Calcula el umbral entero de amortización.
from pathlib import Path  # Maneja rutas portables.
import pandas as pd  # Agrupa las observaciones crudas.
import matplotlib  # Configura un backend sin ventanas.
matplotlib.use('Agg')  # Permite generar imágenes en terminal y en Work.
import matplotlib.pyplot as plt  # Construye gráficos desde las mediciones.

RAIZ = Path(__file__).resolve().parents[1]  # Encuentra el proyecto.
GRUPOS = ['lenguaje', 'n', 'algoritmo', 'escenario']  # Identifica cada combinación experimental.


def analizar(salida, graficos):  # Consolida una sola sesión de ambos lenguajes.
    datos = pd.concat([pd.read_csv(salida / 'crudos_python.csv'), pd.read_csv(salida / 'crudos_cpp.csv')], ignore_index=True)  # Lee solo ejecuciones reales.
    if datos.duplicated(GRUPOS + ['repeticion']).any():  # Detecta filas experimentales repetidas.
        raise ValueError('Hay repeticiones duplicadas en los CSV.')  # Evita estadísticas inválidas.
    if (datos.tiempo_ns < 0).any():  # Rechaza intervalos imposibles.
        raise ValueError('Existen tiempos negativos.')  # Indica datos dañados.
    grupos = datos.groupby(GRUPOS)  # Agrupa por tratamiento y escenario.
    if len(grupos) != 80 or grupos.size().min() < 30:  # Exige 2 lenguajes por 5 tamaños por 2 algoritmos por 4 escenarios.
        raise ValueError('Se requieren 80 combinaciones completas con al menos 30 repeticiones.')  # Explica la matriz exigida.
    comparables = datos.pivot(index=['n', 'algoritmo', 'escenario', 'repeticion'], columns='lenguaje', values=['clave', 'posicion', 'comparaciones'])  # Empareja ambos lenguajes.
    for variable in ['clave', 'posicion', 'comparaciones']:  # Revisa concordancia determinista.
        if not comparables[variable]['Python'].equals(comparables[variable]['C++']):  # Compara resultados, no tiempos.
            raise ValueError(f'Python y C++ discrepan en {variable}.')  # Impide presentar discrepancias como válidas.
    datos.sort_values(GRUPOS + ['repeticion']).to_csv(salida / 'resultados_crudos.csv', index=False)  # Conserva todas las observaciones.
    resumen = grupos.agg(repeticiones=('tiempo_ns', 'size'), promedio_ns=('tiempo_ns', 'mean'), mediana_ns=('tiempo_ns', 'median'), minimo_ns=('tiempo_ns', 'min'), maximo_ns=('tiempo_ns', 'max'), comparaciones_promedio=('comparaciones', 'mean'), comparaciones_mediana=('comparaciones', 'median'), comparaciones_minimo=('comparaciones', 'min'), comparaciones_maximo=('comparaciones', 'max')).reset_index()  # Calcula todos los estadísticos solicitados.
    resumen.to_csv(salida / 'resumen_estadistico.csv', index=False)  # Guarda el resumen completo.
    orden = pd.concat([pd.read_csv(salida / 'ordenamiento_python.csv'), pd.read_csv(salida / 'ordenamiento_cpp.csv')], ignore_index=True)  # Reúne las preparaciones.
    orden.to_csv(salida / 'ordenamiento_crudo.csv', index=False)  # Mantiene cada ordenamiento observado.
    orden_resumen = orden.groupby(['lenguaje', 'n']).agg(repeticiones=('tiempo_ns', 'size'), promedio_ns=('tiempo_ns', 'mean'), mediana_ns=('tiempo_ns', 'median'), minimo_ns=('tiempo_ns', 'min'), maximo_ns=('tiempo_ns', 'max')).reset_index()  # Resume preparación por lenguaje y tamaño.
    orden_resumen.to_csv(salida / 'ordenamiento_resumen.csv', index=False)  # Guarda estadísticas de ordenar.
    amortizacion = []  # Acumula estimaciones por escenario.
    for (lenguaje, n, escenario), grupo in resumen.groupby(['lenguaje', 'n', 'escenario']):  # Mantiene separado cada tipo de consulta.
        tiempos = grupo.set_index('algoritmo').mediana_ns  # Recupera medianas de búsquedas.
        s = float(orden_resumen.query('lenguaje == @lenguaje and n == @n').mediana_ns.iloc[0])  # Recupera mediana de ordenar.
        diferencia = tiempos['lineal'] - tiempos['binaria']  # Calcula el ahorro por consulta.
        q = math.floor(s / diferencia) + 1 if diferencia > 0 else None  # Obtiene q para ventaja estricta de binaria.
        for consultas in [1, 1000]:  # Compara una consulta y mil consultas iguales.
            amortizacion.append([lenguaje, n, escenario, consultas, s, tiempos['lineal'], tiempos['binaria'], consultas * tiempos['lineal'], s + consultas * tiempos['binaria'], q])  # Calcula totales modelados, no nuevos tiempos medidos.
    pd.DataFrame(amortizacion, columns=['lenguaje', 'n', 'escenario', 'q', 'ordenar_ns', 'lineal_ns', 'binaria_ns', 'total_lineal_modelado_ns', 'total_binaria_modelado_ns', 'q_minimo_estimado']).to_csv(salida / 'amortizacion.csv', index=False)  # Exporta el modelo con nombres explícitos.
    graficos.mkdir(parents=True, exist_ok=True)  # Crea el destino de figuras.
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})  # Mejora legibilidad.
    for lenguaje, sufijo in [('Python', 'python'), ('C++', 'cpp')]:  # Separa lenguajes para no mezclar escalas de tiempo.
        for variable, ylabel, nombre in [('comparaciones_mediana', 'Sondeos (mediana)', 'comparaciones'), ('mediana_ns', 'Tiempo mediano (µs)', 'tiempo')]:  # Genera las dos métricas exigidas.
            fig, ejes = plt.subplots(2, 2, figsize=(10, 6.2), constrained_layout=True)  # Dedica un panel a cada escenario.
            for eje, escenario in zip(ejes.flat, ['inicio', 'centro', 'final', 'ausente']):  # Mantiene orden pedagógico.
                for algoritmo, color in [('lineal', '#176B87'), ('binaria', '#C06024')]:  # Mantiene colores entre figuras.
                    d = resumen.query('lenguaje == @lenguaje and escenario == @escenario and algoritmo == @algoritmo').sort_values('n')  # Selecciona datos reales.
                    y = d[variable] / 1000 if variable == 'mediana_ns' else d[variable]  # Convierte ns a µs solo para visualizar.
                    eje.plot(d.n, y, 'o-', color=color, label=algoritmo, markersize=4)  # Traza cada algoritmo.
                eje.set(xscale='log', yscale='log', title=escenario.capitalize(), xlabel='n (registros)', ylabel=ylabel)  # Declara las escalas logarítmicas.
                eje.grid(alpha=.2, which='both')  # Facilita comparar órdenes de magnitud.
                eje.legend(fontsize=8)  # Identifica las series.
            fig.suptitle(f'{lenguaje} · {nombre.capitalize()} por tamaño y escenario', fontsize=14)  # Añade título inequívoco.
            fig.savefig(graficos / f'{nombre}_{sufijo}.png', dpi=180)  # Guarda una imagen nítida.
            plt.close(fig)  # Libera memoria.
    fig, ejes = plt.subplots(1, 2, figsize=(8, 2.8), constrained_layout=True)  # Crea una figura compacta para el informe.
    for eje, lenguaje in zip(ejes, ['Python', 'C++']):  # Separa las dos escalas temporales por lenguaje.
        for algoritmo, color in [('lineal', '#176B87'), ('binaria', '#C06024')]:  # Conserva colores de las figuras completas.
            d = resumen.query('lenguaje == @lenguaje and escenario == "ausente" and algoritmo == @algoritmo').sort_values('n')  # Selecciona el caso ausente real.
            eje.plot(d.n, d.mediana_ns / 1000, 'o-', color=color, label=algoritmo, markersize=4)  # Dibuja medianas en microsegundos.
        eje.set(xscale='log', yscale='log', title=lenguaje + ' · ausente', xlabel='n (registros)', ylabel='Mediana (µs)')  # Declara caso, lenguaje y unidades.
        eje.grid(alpha=.2, which='both')  # Facilita la lectura del crecimiento.
        eje.legend(fontsize=8)  # Identifica los dos algoritmos.
    fig.savefig(graficos / 'tiempo_ausente.png', dpi=200)  # Guarda el resumen visual del informe.
    plt.close(fig)  # Libera la figura compacta.
    (salida / 'validacion_matriz.txt').write_text(f'{len(datos)} búsquedas reales; 80 combinaciones; mínimo {grupos.size().min()} repeticiones.\nPython y C++ coinciden en clave, posición y sondeos.\nOrdenamientos separados: {len(orden)}.\n', encoding='utf-8')  # Conserva evidencia de integridad.
    print((salida / 'validacion_matriz.txt').read_text(encoding='utf-8'))  # Presenta el resultado del control.
# Bloque completo: valida, resume, modela amortización y grafica sin fabricar mediciones.

if __name__ == '__main__':  # Ejecuta el análisis desde terminal.
    parser = argparse.ArgumentParser(description=__doc__)  # Prepara opciones.
    parser.add_argument('--salida', type=Path, default=RAIZ / 'resultados')  # Elige la sesión a resumir.
    parser.add_argument('--graficos', type=Path, default=RAIZ / 'graficos')  # Elige el destino de imágenes.
    args = parser.parse_args()  # Lee los argumentos.
    try:  # Controla archivos y datos incompletos.
        analizar(args.salida, args.graficos)  # Regenera todos los derivados.
    except (OSError, ValueError, KeyError) as error:  # Captura problemas previsibles.
        parser.exit(1, f'Error: {error}\n')  # Muestra una explicación breve.
