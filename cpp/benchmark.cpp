#include "busquedas.hpp" // Reutiliza los algoritmos manuales.
#include <chrono> // Mide intervalos con steady_clock.
#include <filesystem> // Maneja rutas y crea carpetas con C++20.
#include <fstream> // Lee muestras y escribe CSV.
#include <iostream> // Informa el avance y los errores.
#include <sstream> // Divide filas CSV sencillas.
#include <string> // Maneja nombres de escenarios.
#include <random> // Mezcla el orden experimental.
#include <set> // Reúne los tamaños distintos.

struct Consulta { // Conserva una fila del archivo de claves.
    int n, origen; // Guarda tamaño y posición en la muestra original.
    std::string escenario; // Identifica inicio, centro, final o ausente.
    long long clave; // Guarda el CustomerID buscado.
}; // Termina la definición de consulta.
struct Tarea { // Representa una observación cronometrada.
    int repeticion, algoritmo; // Identifica repetición y algoritmo (0 lineal, 1 binaria).
    Consulta consulta; // Conserva el objetivo compartido.
}; // Termina la definición de tarea.

std::vector<std::string> dividir(const std::string& linea) { // Procesa únicamente los CSV numéricos generados por el proyecto.
    std::stringstream flujo(linea); // Convierte la línea en un flujo de texto.
    std::vector<std::string> partes; // Acumula las columnas.
    std::string parte; // Guarda una columna cada vez.
    while (std::getline(flujo, parte, ',')) partes.push_back(parte); // Separa por comas sin campos entrecomillados.
    return partes; // Devuelve las columnas.
} // Bloque completo: lector mínimo para nuestros CSV; no intenta interpretar el Excel original.

std::vector<Consulta> leer_claves(const std::filesystem::path& ruta) { // Carga los objetivos experimentales.
    std::ifstream archivo(ruta); // Abre el archivo de claves.
    if (!archivo) throw std::runtime_error("No se encuentra datos/claves.csv; ejecuta desde la raiz o pasa su ruta."); // Rechaza archivo ausente.
    std::string linea; // Reserva la línea de lectura.
    std::getline(archivo, linea); // Omite la cabecera.
    std::vector<Consulta> consultas; // Acumula consultas.
    while (std::getline(archivo, linea)) { // Lee cada escenario.
        auto p = dividir(linea); // Separa las cuatro columnas.
        if (p.size() != 4) throw std::runtime_error("claves.csv debe tener cuatro columnas."); // Detecta estructura inválida.
        consultas.push_back({std::stoi(p[0]), std::stoi(p[3]), p[1], std::stoll(p[2])}); // Convierte y conserva la consulta.
    } // Termina la lectura.
    if (consultas.empty()) throw std::runtime_error("El archivo de claves esta vacio."); // Rechaza experimento vacío.
    return consultas; // Entrega todos los objetivos.
} // Bloque completo: carga las mismas consultas que usa Python, fuera del cronómetro.

std::vector<long long> leer_muestra(const std::filesystem::path& ruta, int n) { // Carga un tamaño del dataset preparado.
    std::ifstream archivo(ruta); // Abre el CSV correspondiente.
    if (!archivo) throw std::runtime_error("Muestra no encontrada. Regenera datos con preparar_datos.py."); // Comunica la falta de datos.
    std::string linea; // Reserva una línea.
    std::getline(archivo, linea); // Lee la cabecera.
    if (linea.find("CustomerID") == std::string::npos) throw std::runtime_error("Falta la columna CustomerID."); // Comprueba la variable.
    std::vector<long long> datos; // Conserva los identificadores en orden original.
    while (std::getline(archivo, linea)) { // Recorre las observaciones.
        auto p = dividir(linea); // Divide procedencia e identificador.
        if (p.size() != 2) throw std::runtime_error("Muestra invalida: se esperan fila_excel y CustomerID."); // Rechaza filas mal formadas.
        datos.push_back(std::stoll(p[1])); // Agrega el identificador entero.
    } // Termina de cargar.
    if (static_cast<int>(datos.size()) != n) throw std::runtime_error("Tamano solicitado distinto del disponible; regenera la muestra."); // Controla n.
    return datos; // Entrega el arreglo sin ordenar.
} // Bloque completo: lectura y validación de la muestra compartida.

int main(int argc, char* argv[]) { // Recibe raíz, salida y repeticiones opcionales.
    try { // Intercepta errores antes de mostrar una traza confusa.
        std::filesystem::path raiz = argc > 1 ? argv[1] : "."; // Usa la raíz indicada o el directorio actual.
        std::filesystem::path salida = argc > 2 ? argv[2] : (raiz / "resultados").string(); // Elige el destino.
        int repeticiones = argc > 3 ? std::stoi(argv[3]) : 30; // Usa al menos 30 repeticiones.
        if (repeticiones < 30) throw std::runtime_error("Se requieren al menos 30 repeticiones; usa demo para una prueba rapida."); // Impone la guía.
        auto consultas = leer_claves(raiz / "datos/claves.csv"); // Lee objetivos antes de medir.
        std::filesystem::create_directories(salida); // Crea el destino.
        std::ofstream crudos(salida / "crudos_cpp.csv"), ordenes(salida / "ordenamiento_cpp.csv"); // Abre salidas separadas.
        if (!crudos || !ordenes) throw std::runtime_error("No se pueden escribir los resultados."); // Detecta problemas de permisos.
        crudos << "lenguaje,n,algoritmo,escenario,repeticion,clave,posicion_origen,posicion,comparaciones,tiempo_ns\n"; // Escribe cabecera compartida.
        ordenes << "lenguaje,n,repeticion,tiempo_ns\n"; // Escribe cabecera de preparación.
        std::set<int> tamanos; // Reúne tamaños en orden creciente.
        for (const auto& c : consultas) tamanos.insert(c.n); // Agrega los n definidos en las claves.
        for (int n : tamanos) { // Ejecuta cada tamaño.
            auto datos = leer_muestra(raiz / "datos" / ("muestra_" + std::to_string(n) + ".csv"), n); // Carga fuera del tiempo.
            std::vector<long long> ordenados; // Reserva la copia para binaria.
            for (int r = 1; r <= repeticiones; ++r) { // Mide ordenamientos independientes.
                ordenados = datos; // Copia fuera del cronómetro.
                auto inicio = std::chrono::steady_clock::now(); // Comienza a medir ordenamiento.
                std::sort(ordenados.begin(), ordenados.end()); // Ordena la misma muestra.
                auto fin = std::chrono::steady_clock::now(); // Termina de medir ordenamiento.
                auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(fin - inicio).count(); // Convierte el intervalo.
                ordenes << "C++," << n << ',' << r << ',' << ns << '\n'; // Registra cada preparación.
            } // Termina las repeticiones de ordenamiento.
            validar_orden(ordenados); // Comprueba la precondición fuera del cronómetro.
            std::vector<Tarea> tareas; // Reúne las búsquedas de este n.
            long long calentamiento = 0; // Conserva un resultado observable del calentamiento.
            for (const auto& c : consultas) if (c.n == n) { // Selecciona los escenarios de este tamaño.
                calentamiento += busqueda_lineal(datos, c.clave).posicion + busqueda_binaria(ordenados, c.clave).posicion; // Ejecuta un calentamiento por caso.
                for (int r = 1; r <= repeticiones; ++r) for (int a = 0; a < 2; ++a) tareas.push_back({r, a, c}); // Construye la matriz.
            } // Termina la preparación de tareas.
            std::mt19937 generador(902 + n); // Fija semilla para el orden de ejecución en C++.
            std::shuffle(tareas.begin(), tareas.end(), generador); // Intercala algoritmos y escenarios.
            for (const auto& tarea : tareas) { // Ejecuta una observación por tarea.
                const auto& a = tarea.algoritmo == 0 ? datos : ordenados; // Selecciona arreglo sin copiar.
                auto funcion = tarea.algoritmo == 0 ? busqueda_lineal : busqueda_binaria; // Selecciona función antes de medir.
                auto inicio = std::chrono::steady_clock::now(); // Inicia la región de búsqueda.
                Resultado r = funcion(a, tarea.consulta.clave); // Ejecuta únicamente la búsqueda instrumentada.
                auto fin = std::chrono::steady_clock::now(); // Finaliza la región.
                auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(fin - inicio).count(); // Expresa ns.
                bool ausente = tarea.consulta.origen == -1; // Recupera la existencia esperada.
                if ((r.posicion == -1) != ausente || (r.posicion >= 0 && a[r.posicion] != tarea.consulta.clave)) throw std::runtime_error("Busqueda incorrecta; revisar codigo."); // Valida existencia y valor.
                if (tarea.algoritmo == 0 && r.posicion != tarea.consulta.origen) throw std::runtime_error("Escenario lineal incorrecto."); // Comprueba la posición exacta.
                crudos << "C++," << n << ',' << (tarea.algoritmo == 0 ? "lineal" : "binaria") << ',' << tarea.consulta.escenario << ',' << tarea.repeticion << ',' << tarea.consulta.clave << ',' << tarea.consulta.origen << ',' << r.posicion << ',' << r.comparaciones << ',' << ns << '\n'; // Guarda el resultado para que sea observable.
            } // Termina el conjunto de búsquedas.
            std::cout << "C++: n=" << n << " completado; control=" << calentamiento << '\n'; // Informa avance y usa el calentamiento.
        } // Termina la matriz de tamaños.
        return 0; // Señala ejecución correcta.
    } catch (const std::exception& error) { // Captura archivos, conversiones y resultados inválidos.
        std::cerr << "Error: " << error.what() << '\n'; // Muestra una explicación comprensible.
        return 1; // Devuelve estado de fallo para scripts automatizados.
    } // Termina el control de errores.
} // Bloque completo: mide el experimento C++ con las mismas muestras y claves de Python.
