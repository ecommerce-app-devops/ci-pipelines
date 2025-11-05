#!/bin/bash

# Script helper para ejecutar Locust con el entorno virtual activado

# Activar el entorno virtual
source venv/bin/activate

# Ejecutar locust con los argumentos proporcionados
locust "$@"

