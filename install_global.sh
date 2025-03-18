#!/bin/bash

# Comprobar si se está ejecutando como root
if [ "$(id -u)" != "0" ]; then
   echo "Este script debe ejecutarse como root"
   exit 1
fi

echo "Instalando VisualGit globalmente..."

# Instalar dependencias
pip install simple_term_menu requests

# Crear el directorio de la aplicación
INSTALL_DIR="/usr/local/lib/visualgit"
mkdir -p $INSTALL_DIR

# Copiar los archivos de la aplicación
cp -r vigit $INSTALL_DIR/
cp README.md $INSTALL_DIR/

# Crear el script ejecutable
cat > /usr/local/bin/vg << 'EOF'
#!/bin/bash
# Script global para VisualGit

# Añadir el directorio de la aplicación al PYTHONPATH
export PYTHONPATH="/usr/local/lib/visualgit:$PYTHONPATH"

# Ejecutar la aplicación
python -c "from vigit.main import main; main()"
EOF

# Hacer el script ejecutable
chmod +x /usr/local/bin/vg

echo "¡Instalación completada! Ahora puedes ejecutar 'vg' desde cualquier directorio."
