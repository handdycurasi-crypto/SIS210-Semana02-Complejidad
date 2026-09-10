# Plan de commits reales, pendientes de ejecutar localmente

No se incluye un historial Git fabricado. Estos comandos crean commits en el momento real en que los ejecutes, después de revisar cada grupo. Como el proyecto ya está preparado, documentan incorporación por etapas; no simulan una cronología anterior de desarrollo.

En la terminal de la carpeta raíz:

```powershell
git init
git branch -M main
git add .gitignore requirements.txt python/busquedas.py python/demo.py cpp/busquedas.hpp cpp/demo.cpp
git commit -m "baseline"
git add ANALISIS_REQUISITOS.md ANALISIS_TEORICO.md referencias
git commit -m "analysis"
git add CMakeLists.txt python cpp datos resultados graficos COMANDOS_WORK.md
git commit -m "benchmark"
git add README.md GUIA_DEMO.md PLAN_COMMITS.md DECLARACION_IA.md PREGUNTAS_SUSTENTACION.md REVISION_DOCENTE.md informe
git commit -m "final"
git status
git log --oneline
```

Si Git pide identidad, configura `git config user.name "TU NOMBRE"` y `git config user.email "TU CORREO"` con tus datos reales. No copies los marcadores literalmente.

Para publicar, crea un repositorio vacío en tu cuenta de GitHub con nombre `SIS210-Semana02-Complejidad`. Copia su URL real y ejecútala así:

```powershell
git remote add origin URL_REAL_DEL_REPOSITORIO
git push -u origin main
```

No se ha creado ni publicado un repositorio desde Work. No reutilices automáticamente el repositorio de la práctica 0. Si editas algo después, crea un nuevo commit que describa el cambio real.
