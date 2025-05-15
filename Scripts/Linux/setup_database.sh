#!/bin/bash

# Colores para la salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Configurar autenticación por contraseña para el usuario root
echo -e "${YELLOW}Configurando autenticación por contraseña para el usuario root...${NC}"
ROOT_PASSWORD="lunarspace"  # Cambia esto por una contraseña segura
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${ROOT_PASSWORD}';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Mostrar información de la nueva configuración
echo -e "${GREEN}La autenticación por contraseña ha sido configurada para el usuario root.${NC}"
echo -e "${GREEN}Contraseña establecida: ${ROOT_PASSWORD}${NC}"
echo -e "${YELLOW}Por favor, anote esta contraseña en un lugar seguro.${NC}"

# Verificar si existe el archivo SQL de base de datos
SQL_FILE="$(dirname "$0")/walli_database.sql"
if [ -f "$SQL_FILE" ]; then
    echo -e "${YELLOW}Importando estructura de base de datos desde $SQL_FILE...${NC}"
    
    # Crear la base de datos si no existe
    sudo mysql -u root -p"${ROOT_PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS walli_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    
    # Importar el esquema de la base de datos
    sudo mysql -u root -p"${ROOT_PASSWORD}" walli_db < "$SQL_FILE"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Base de datos importada correctamente.${NC}"
    else
        echo -e "${RED}Error al importar la base de datos.${NC}"
        exit 1
    fi
else
    echo -e "${RED}No se encontró el archivo SQL de base de datos en $SQL_FILE${NC}"
    echo -e "${YELLOW}Por favor, asegúrese de que el archivo walli_database.sql existe en la carpeta scripts.${NC}"
fi

# Configurar la seguridad de MySQL (opcional)
echo -e "${YELLOW}¿Desea ejecutar mysql_secure_installation para configuración de seguridad adicional? (y/n)${NC}"
read -r response
if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
    echo -e "${YELLOW}Iniciando configuración de seguridad adicional...${NC}"
    echo -e "${YELLOW}NOTA: Cuando se le pida la contraseña de root, use la que acaba de establecerse: ${ROOT_PASSWORD}${NC}"
    sudo mysql_secure_installation
else
    echo -e "${YELLOW}Omitiendo configuración de seguridad adicional.${NC}"
fi

# Mostrar el estado del servicio de MySQL
echo -e "${YELLOW}Estado del servicio MySQL:${NC}"
sudo systemctl status mysql | head -n 10

echo -e "${GREEN}Instalación y configuración de MySQL completada.${NC}"
echo -e "${YELLOW}Puede acceder a MySQL con el siguiente comando:${NC}"
echo -e "mysql -u root -p"
echo -e "${YELLOW}Y luego ingrese la contraseña: ${ROOT_PASSWORD}${NC}"
echo -e "${YELLOW}Para conectarse directamente a la base de datos walli_db:${NC}"
echo -e "mysql -u root -p walli_db"

# Guardar la contraseña en un archivo para referencia
echo "MySQL Root Password: $ROOT_PASSWORD" > mysql_root_password.txt
chmod 600 mysql_root_password.txt
echo -e "${YELLOW}La contraseña también ha sido guardada en el archivo mysql_root_password.txt${NC}"