#!/bin/bash

# Comprobar si se está ejecutando como root
if [ "$(id -u)" != "0" ]; then
   echo "Este script debe ejecutarse como root"
   exit 1
fi

echo "Instalando VisualGit globalmente..."

# Eliminar instalación anterior si existe
if [ -d "/usr/local/lib/visualgit" ]; then
   echo "Eliminando instalación anterior..."
   rm -rf /usr/local/lib/visualgit
fi

if [ -f "/usr/local/bin/vg" ]; then
   echo "Eliminando ejecutable anterior..."
   rm -f /usr/local/bin/vg
fi

# Instalar dependencias
pip3 install simple_term_menu requests

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

# Ejecutar la aplicación con Python 3 y pasar todos los argumentos
python3 -m vigit.main "$@"
EOF

# Hacer el script ejecutable
chmod +x /usr/local/bin/vg

echo "¡Instalación completada! Ahora puedes ejecutar 'vg' desde cualquier directorio."
echo "Ejemplos:"
echo "  vg     # Abre la interfaz principal"
echo "  vg a   # Añadir repositorio local"
echo "  vg b   # Crear rama local"
echo "  vg c   # Commit"
echo "  vg p   # Push"
