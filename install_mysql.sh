#!/bin/bash

# Actualizar el sistema
sudo apt update
sudo apt upgrade -y

# Instalar MySQL
sudo apt install mysql-server -y

# Iniciar el servicio de MySQL
sudo systemctl start mysql

# Habilitar MySQL para que se inicie al arrancar el sistema
sudo systemctl enable mysql

# Configurar la seguridad de MySQL
sudo mysql_secure_installation

# Mostrar el estado del servicio de MySQL
sudo systemctl status mysql