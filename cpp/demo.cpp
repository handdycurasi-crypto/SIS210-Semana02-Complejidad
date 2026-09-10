#include "busquedas.hpp" // Importa las dos búsquedas manuales y la validación.
#include <chrono> // Proporciona el reloj monotónico.
#include <iostream> // Permite mostrar resultados y leer entradas.
#include <string> // Conserva entradas para validarlas completamente.

long long leer_entero(const std::string& mensaje) { // Lee un entero sin aceptar texto sobrante.
    std::cout << mensaje; // Muestra la pregunta.
    std::string texto; // Reserva la línea de entrada.
    if (!std::getline(std::cin, texto)) throw std::runtime_error("Entrada cerrada."); // Detecta fin de entrada.
    std::size_t usados = 0; // Registra cuántos caracteres fueron numéricos.
    long long valor = std::stoll(texto, &usados); // Convierte o lanza error si no es un entero válido.
    if (texto.find_first_not_of(" \t\r", usados) != std::string::npos) throw std::invalid_argument("Escribe solamente un entero."); // Rechaza sufijos.
    return valor; // Devuelve la entrada válida.
} // Bloque completo: lectura estricta y reutilizable para menú y clave.

int main() { // Inicia el modo demostración.
    std::vector<long long> datos = {10, 20, 30, 40, 50, 60, 70}; // Lista pequeña que puede editarse en clase.
    while (true) { // Permite repetir la demostración sin recompilar.
        std::cout << "\nDatos: "; // Presenta los datos actuales.
        for (long long valor : datos) std::cout << valor << ' '; // Imprime cada elemento.
        std::cout << "\n1: lineal | 2: binaria | 3: desordenar | 4: ordenar | 0: salir\n"; // Describe las opciones.
        try { // Controla errores esperables.
            long long opcion = leer_entero("Opcion: "); // Lee la opción.
            if (opcion == 0) return 0; // Finaliza voluntariamente.
            if (opcion == 3) { std::swap(datos.front(), datos.back()); continue; } // Desordena y vuelve al menú.
            if (opcion == 4) { std::sort(datos.begin(), datos.end()); continue; } // Corrige el orden sin cronometrarlo.
            if (opcion != 1 && opcion != 2) throw std::invalid_argument("Elige 0, 1, 2, 3 o 4."); // Rechaza opciones inválidas.
            long long clave = leer_entero("Clave entera: "); // Obtiene el objetivo.
            if (opcion == 2) validar_orden(datos); // Verifica el orden antes de medir.
            auto funcion = opcion == 1 ? busqueda_lineal : busqueda_binaria; // Selecciona la búsqueda.
            auto inicio = std::chrono::steady_clock::now(); // Inicia el cronómetro monotónico.
            Resultado resultado = funcion(datos, clave); // Ejecuta solo la búsqueda instrumentada.
            auto fin = std::chrono::steady_clock::now(); // Finaliza el intervalo.
            auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(fin - inicio).count(); // Convierte a ns.
            std::cout << "Posicion (base 0): " << resultado.posicion << "; comparaciones/sondeos: " << resultado.comparaciones << "; tiempo: " << ns << " ns\n"; // Muestra el resultado observable.
        } catch (const std::exception& error) { // Intercepta conversiones y precondiciones.
            std::cout << "Entrada invalida: " << error.what() << '\n'; // Explica el problema.
            if (std::cin.eof()) return 0; // Sale limpiamente si se cerró la entrada.
        } // Continúa después de un error corregible.
    } // Termina el bucle únicamente por salida explícita.
} // Bloque completo: muestra, consulta, mide y permite demostrar una corrección.
