#!/bin/bash
# Activar el entorno virtual
PROJECT_DIR="/Users/alexadler/Documents/Documents - MacBook Air (6)/VisualGit/Local"
source "$PROJECT_DIR/venv/bin/activate"
# Ejecutar el comando vg desde el directorio actual y pasar todos los argumentos
python -m vigit.main "$@"
