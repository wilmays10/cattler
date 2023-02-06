#!/bin/bash

# entorno virtual
sudo apt update
sudo apt install python3-pip
python3 -m venv env
source env/bin/activate

# instalar dependencias
pip3 install -r requirements.txt

# Creacion base de datos
python manage.py makemigrations
python manage.py migrate

# Inicializar server local
python manage.py runserver
