#!/bin/bash
PROJECT_DIR="/Users/alexadler/Documents/Documents - MacBook Air (6)/VisualGit/Local"
source "$PROJECT_DIR/venv/bin/activate"
# Ejecutar el comando vg con Python 3 y pasar todos los argumentos
python3 -m vigit.main "$@"
