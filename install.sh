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

echo "Instalación completada. Por favor reinicia tu terminal o ejecuta 'source ~/.zshrc' para aplicar los cambios."
