#!/bin/bash

echo "Generando PDF..."
python generar_pdf.py

echo "Agregando archivos al repositorio..."
git add .

echo "Escribe un mensaje para el commit:"
read mensaje

git commit -m "$mensaje"

echo "Haciendo push a GitHub..."
git push origin main

echo "✅ Despliegue enviado a Render automáticamente (si está conectado)."