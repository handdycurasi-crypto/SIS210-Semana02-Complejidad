cmake_minimum_required(VERSION 3.16) # Define la versión mínima de CMake.
project(SIS210_Semana02 LANGUAGES CXX) # Crea un proyecto C++ estándar.
set(CMAKE_CXX_STANDARD 20) # Solicita C++20 como en la parte operativa de la guía.
set(CMAKE_CXX_STANDARD_REQUIRED ON) # Impide bajar silenciosamente de versión.
set(CMAKE_CXX_EXTENSIONS OFF) # Evita extensiones no portables.
add_executable(demo cpp/demo.cpp) # Compila la demostración como ejecutable independiente.
add_executable(benchmark cpp/benchmark.cpp) # Compila el benchmark por separado.
