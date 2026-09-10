#include "busquedas.hpp" // Importa las implementaciones bajo prueba.
#include <iostream> // Muestra el resultado de la validación.
#include <random> // Genera arreglos reproducibles.
#include <bit> // Proporciona bit_width en C++20 para la cota exacta.

int main() { // Inicia una validación independiente del benchmark.
    std::mt19937 rng(73); // Fija una semilla de pruebas.
    long long casos = 0; // Cuenta consultas validadas.
    for (int n : {0, 1, 2, 3, 7, 8, 16, 31, 100}) { // Incluye extremos y potencias de dos.
        for (int repeticion = 0; repeticion < 10; ++repeticion) { // Varía el contenido diez veces.
            std::vector<long long> datos(n); // Reserva n elementos.
            for (auto& valor : datos) valor = static_cast<int>(rng() % 21) - 10; // Incluye negativos y duplicados.
            auto ordenados = datos; // Copia la muestra para binaria.
            std::sort(ordenados.begin(), ordenados.end()); // Ordena fuera de las búsquedas.
            for (long long x = -11; x <= 11; ++x) { // Incluye ausentes en ambos extremos.
                auto it = std::find(datos.begin(), datos.end(), x); // Usa biblioteca solo como oráculo.
                int esperado = it == datos.end() ? -1 : static_cast<int>(it - datos.begin()); // Convierte al convenio del proyecto.
                auto l = busqueda_lineal(datos, x); // Ejecuta búsqueda manual lineal.
                auto b = busqueda_binaria(ordenados, x); // Ejecuta búsqueda manual binaria.
                if (l.posicion != esperado || l.comparaciones != (esperado < 0 ? n : esperado + 1)) return 1; // Comprueba posición y contador.
                if ((b.posicion < 0) != (esperado < 0)) return 2; // Comprueba existencia binaria.
                if (b.posicion >= 0 && ordenados[b.posicion] != x) return 3; // Comprueba valor encontrado.
                if (b.comparaciones > std::bit_width(static_cast<unsigned int>(n))) return 4; // Comprueba cota exacta.
                ++casos; // Registra una consulta contrastada.
            } // Termina las claves de prueba.
        } // Termina los arreglos de este tamaño.
    } // Termina los tamaños.
    try { validar_orden({30, 10, 20}); return 5; } // Exige que la validación rechace desorden.
    catch (const std::runtime_error&) {} // La excepción es el resultado correcto de esta prueba.
    std::cout << casos << " consultas C++ validadas contra std::find; orden invalido rechazado.\n"; // Informa evidencia.
    return 0; // Señala aprobación de todos los controles.
} // Bloque completo: contrasta algoritmos y sondeos con un oráculo independiente.
