#!/bin/bash

# Directorio actual del proyecto (con comillas para manejar espacios)
PROJECT_DIR="$(pwd)"

# Crear un entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar el entorno virtual
source "$PROJECT_DIR/venv/bin/activate"

# Instalar el paquete en modo desarrollo
echo "Instalando el paquete en modo desarrollo..."
pip install -e .

# Crear un script wrapper para vg que maneje bien las rutas con espacios
echo "Creando script wrapper para vg..."
cat > "$PROJECT_DIR/venv/bin/vg_wrapper" << EOF
#!/bin/bash
# Activar el entorno virtual
source "$PROJECT_DIR/venv/bin/activate"
# Ejecutar el comando vg desde el directorio actual
python -m vigit.main
EOF

# Hacer el script ejecutable
chmod +x "$PROJECT_DIR/venv/bin/vg_wrapper"

# Crear un alias en el perfil del usuario
echo "Configurando el alias en el perfil..."
echo "alias vg=\"$PROJECT_DIR/venv/bin/vg_wrapper\"" >> ~/.zshrc

# Verificar si diff-so-fancy está instalado
if ! command -v diff-so-fancy &> /dev/null; then
    echo "diff-so-fancy no está instalado. ¿Deseas instalarlo? (y/n)"
    read -r install_diff_so_fancy
    if [[ "$install_diff_so_fancy" =~ ^[Yy]$ ]]; then
        if command -v npm &> /dev/null; then
            echo "Instalando diff-so-fancy usando npm..."
            npm install -g diff-so-fancy
        elif command -v brew &> /dev/null; then
            echo "Instalando diff-so-fancy usando brew..."
            brew install diff-so-fancy
        else
            echo "No se pudo instalar diff-so-fancy. Se requiere npm o brew."
            echo "Puedes instalarlo manualmente siguiendo las instrucciones en: https://github.com/so-fancy/diff-so-fancy"
        fi
    fi
else
    echo "diff-so-fancy ya está instalado."
fi

echo "Instalación completada. Por favor reinicia tu terminal o ejecuta 'source ~/.zshrc' para aplicar los cambios."
