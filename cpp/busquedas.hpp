#pragma once // Evita incluir dos veces estas definiciones.
#include <vector> // Proporciona el arreglo dinámico estándar.
#include <algorithm> // Se utiliza solo para validar orden, no para buscar.
#include <stdexcept> // Permite comunicar precondiciones inválidas.

struct Resultado { // Agrupa la respuesta de cada búsqueda.
    int posicion; // Índice base cero; -1 significa ausencia.
    long long comparaciones; // Número de elementos examinados, igual que ops en la guía.
}; // Termina el tipo de resultado.

inline Resultado busqueda_lineal(const std::vector<long long>& a, long long x) { // Recibe el arreglo sin copiarlo.
    long long ops = 0; // Inicializa los sondeos.
    for (std::size_t i = 0; i < a.size(); ++i) { // Visita posiciones desde el inicio.
        ++ops; // Cuenta el elemento examinado.
        if (a[i] == x) return {static_cast<int>(i), ops}; // Devuelve la primera coincidencia.
    } // Termina el recorrido si no hubo coincidencias.
    return {-1, ops}; // Informa ausencia y total examinado.
} // Bloque completo: búsqueda secuencial manual, sin precondición de orden.

inline Resultado busqueda_binaria(const std::vector<long long>& a, long long x) { // Requiere orden ascendente previo.
    int izq = 0, der = static_cast<int>(a.size()) - 1; // Delimita el intervalo inclusivo.
    long long ops = 0; // Inicializa los sondeos.
    while (izq <= der) { // Continúa mientras el intervalo no esté vacío.
        int medio = izq + (der - izq) / 2; // Calcula el centro inferior sin sumar los extremos.
        ++ops; // Cuenta un sondeo aunque después haya dos comparaciones relacionales.
        if (a[medio] == x) return {medio, ops}; // Devuelve una coincidencia, no necesariamente la primera.
        if (a[medio] < x) izq = medio + 1; // Descarta los valores inferiores a la clave.
        else der = medio - 1; // Descarta los valores superiores a la clave.
    } // Termina cuando no quedan candidatos.
    return {-1, ops}; // Comunica ausencia.
} // Bloque completo: reduce el intervalo de búsqueda aproximadamente a la mitad.

inline void validar_orden(const std::vector<long long>& a) { // Se llama fuera de la región cronometrada.
    if (!std::is_sorted(a.begin(), a.end())) throw std::runtime_error("Binaria requiere datos ordenados. Usa ordenar primero."); // Rechaza una inversión.
} // Bloque completo: valida la precondición en O(n), sin atribuirla al tiempo logarítmico.
