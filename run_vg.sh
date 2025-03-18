#!/bin/bash
PROJECT_DIR="/Users/alexadler/Documents/Documents - MacBook Air (6)/VisualGit/Local"
source "$PROJECT_DIR/venv/bin/activate"
# Se ha eliminado el cambio de directorio para permitir que la aplicación use el directorio actual
python -m vigit.main
