#!/bin/bash

# Instalar todo rápido
apt-get update
apt-get install -y python3-pip python3-serial gammu python3-gammu

# Detectar módems
ls /dev/ttyUSB*

# Instalar dependencias Python
pip3 install pyserial requests flask

# Dar permisos
chmod 666 /dev/ttyUSB*

echo "Listo. Conecta los módems y ejecuta: python3 sms_sender.py"