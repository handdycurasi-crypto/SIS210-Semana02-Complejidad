"""Registra el entorno real; no sustituye datos desconocidos por los del estudiante."""
import argparse  # Recibe etiqueta, compilador y banderas.
import json  # Conserva metadatos legibles.
import os  # Consulta límites de CPU cuando están disponibles.
import platform  # Identifica SO, arquitectura y Python.
import subprocess  # Consulta al compilador y a Windows si corresponde.
from datetime import datetime, timezone  # Registra fecha UTC de la ejecución.
from importlib.metadata import version  # Recupera versiones de bibliotecas instaladas.
from pathlib import Path  # Maneja archivos de sistema opcionales.
from time import get_clock_info  # Consulta las características del reloj de Python.


def registrar(args):  # Guarda hechos observados del entorno actual.
    cpu, ram = platform.processor(), 'No detectada automáticamente'  # Mantiene explícita cualquier ausencia.
    if Path('/proc/cpuinfo').exists():  # Reconoce Linux.
        cpu = next((l.split(':', 1)[1].strip() for l in Path('/proc/cpuinfo').read_text().splitlines() if l.startswith('model name')), cpu)  # Lee el modelo informado por el huésped.
        ram = next(l for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemTotal:'))  # Registra memoria visible, no inventa RAM asignada.
    elif platform.system() == 'Windows':  # Consulta la máquina local de Windows.
        cpu = subprocess.check_output(['powershell', '-NoProfile', '-Command', '(Get-CimInstance Win32_Processor).Name'], text=True).strip()  # Lee CPU con CIM.
        ram = subprocess.check_output(['powershell', '-NoProfile', '-Command', '(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory'], text=True).strip() + ' bytes'  # Lee RAM física.
    compilador = subprocess.run([args.compilador, '--version'] if Path(args.compilador).stem.lower() != 'cl' else [args.compilador], capture_output=True, text=True)  # Consulta GCC/Clang o MSVC.
    limites = {str(p): p.read_text().strip() for p in [Path('/sys/fs/cgroup/memory.max'), Path('/sys/fs/cgroup/cpu.max')] if p.exists()}  # Registra límites de contenedor cuando existen.
    reloj = get_clock_info('perf_counter')  # Recupera resolución nominal y monotonicidad.
    info = {'etiqueta': args.etiqueta, 'fecha_utc': datetime.now(timezone.utc).isoformat(), 'so': platform.platform(), 'cpu_visible': cpu, 'ram_visible': ram, 'cpu_logicas_visibles': os.cpu_count(), 'limites_cgroup': limites, 'python': platform.python_version(), 'compilador': (compilador.stdout + compilador.stderr).strip(), 'flags_declarados': args.flags, 'bibliotecas': {n: version(n) for n in ['pandas', 'matplotlib', 'openpyxl']}, 'reloj_python': {'implementacion': reloj.implementation, 'resolucion_s': reloj.resolution, 'monotonico': reloj.monotonic}, 'reloj_cpp': 'std::chrono::steady_clock; duration_cast<nanoseconds>', 'advertencia': 'La memoria visible del huésped no necesariamente es la cuota del contenedor. Los flags deben coincidir con el comando de compilación.'}  # Reúne evidencia y límites.
    args.salida.mkdir(parents=True, exist_ok=True)  # Prepara la carpeta de esta sesión.
    (args.salida / 'entorno.json').write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')  # Guarda el entorno reproducible.
    print(json.dumps(info, ensure_ascii=False, indent=2))  # Muestra la información registrada.
# Bloque completo: captura el entorno real de la sesión y las banderas declaradas.

if __name__ == '__main__':  # Permite invocación directa.
    parser = argparse.ArgumentParser(description=__doc__)  # Define la interfaz de terminal.
    parser.add_argument('--salida', type=Path, default=Path(__file__).resolve().parents[1] / 'resultados')  # Selecciona la carpeta.
    parser.add_argument('--etiqueta', required=True)  # Exige distinguir Work de la PC del estudiante.
    parser.add_argument('--compilador', default='g++')  # Permite MSVC con --compilador cl.
    parser.add_argument('--flags', default='-std=c++20 -O2 -Wall -Wextra -pedantic')  # Documenta las banderas utilizadas.
    args = parser.parse_args()  # Lee los argumentos.
    try:  # Captura fallos de herramientas del sistema.
        registrar(args)  # Escribe el registro.
    except (OSError, subprocess.SubprocessError) as error:  # Detecta compilador o consulta ausente.
        parser.exit(1, f'Error al registrar entorno: {error}\n')  # Explica que el entorno debe completarse.
