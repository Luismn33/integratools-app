from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import pandas as pd
import os

# Configuraciones
archivo_excel = 'data/INVENTARIO_MORATO_VALORIZADO.xlsx'
hoja = 'CORRECTIVA'
ruta_logo = 'static/img/Integratools.jpg'
ruta_pdf_salida = 'static/pdf/correctiva_no1.pdf'

# Leer Excel
try:
    df = pd.read_excel(archivo_excel, sheet_name=hoja)
    productos = df['DESCRIPCION'].dropna().tolist()
except Exception as e:
    print(f"Error leyendo Excel: {e}")
    exit()

# Crear PDF
c = canvas.Canvas(ruta_pdf_salida, pagesize=letter)
width, height = letter

def dibujar_encabezado(c, pagina):
    if os.path.exists(ruta_logo):
        c.drawImage(ruta_logo, 40, height - 100, width=120, height=60, preserveAspectRatio=True)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, height - 70, f"CORRECTIVA No. 1 - Página {pagina}")

# Variables
producto_index = 0
pagina = 1
margen_inferior = 80  # Espacio para no pisar el borde
alto_fila = 18  # Altura aproximada de cada fila
espacio_encabezado = 150  # Espacio ocupado por el encabezado
area_disponible = height - espacio_encabezado - margen_inferior
filas_por_pagina = int(area_disponible / alto_fila)

# Comienza generación
while producto_index < len(productos):
    c.setFont("Helvetica", 10)
    dibujar_encabezado(c, pagina)

    data = [["#", "Producto"]]
    filas_esta_pagina = 0

    # Agregar filas respetando espacio
    while filas_esta_pagina < filas_por_pagina and producto_index < len(productos):
        data.append([producto_index + 1, productos[producto_index]])
        producto_index += 1
        filas_esta_pagina += 1

    table = Table(data, colWidths=[50, 450])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))

    table_width, table_height = table.wrap(0, 0)
    y_position = height - espacio_encabezado

    # Dibuja la tabla
    table.drawOn(c, 40, y_position - table_height)

    if producto_index < len(productos):
        c.showPage()
        pagina += 1

c.save()

print(f"✅ PDF generado correctamente en: {ruta_pdf_salida}")
