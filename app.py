from flask import Flask, render_template, request, redirect, url_for
import qrcode
import os
from openpyxl import Workbook
from datetime import datetime

app = Flask(__name__)

# Link del PDF para el QR
pdf_url = "https://1drv.ms/b/c/38cd35cc36f2a749/EfleQtZJ4_VNlzmBeQH4ymMB2VVHHi4YKdfrJd3etenpTQ?e=0FGNTY"
ruta_qr = os.path.join('static', 'qr', 'qr_code.png')

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Crear nombre dinámico con fecha y hora para evitar sobrescribir
fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
archivo_guardado = os.path.join(BASE_DIR, "data", f"validacion_correctiva_{fecha_archivo}.xlsx")

# Lista de productos para el formulario
descripciones = [
    "Multímetro digital",
    "Pinza amperimétrica",
    "Taladro inalámbrico",
    "Destornillador eléctrico"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_qr')
def generar_qr():
    qr = qrcode.make(pdf_url)
    qr.save(ruta_qr)
    return redirect(url_for('ver_qr'))

@app.route('/ver_qr')
def ver_qr():
    return render_template('qr.html')

@app.route('/formulario')
def formulario():
    return render_template("formulario_correctiva.html", descripciones=descripciones)

@app.route('/guardar_formulario', methods=['POST'])
def guardar_formulario():
    total = int(request.form.get("total"))
    wb = Workbook()
    ws = wb.active
    ws.title = "Validación"

    # Encabezados
    encabezados = ["Descripción", "Cantidad", "Cant. Requerida", "Marca", "Referencia", "# de Activo", "Estado", "Fecha"]
    ws.append(encabezados)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    for i in range(total):
        fila = [
            request.form.get(f"descripcion_{i}"),
            request.form.get(f"cantidad_{i}"),
            request.form.get(f"cant_requerida_{i}"),
            request.form.get(f"marca_{i}"),
            request.form.get(f"referencia_{i}"),
            request.form.get(f"activo_{i}"),
            request.form.get(f"estado_{i}"),
            fecha
        ]
        ws.append(fila)

    # Crear nombre dinámico con fecha y hora para evitar sobrescribir
    fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    archivo_guardado = os.path.join(BASE_DIR, "data", f"validacion_correctiva_{fecha_archivo}.xlsx")

    wb.save(archivo_guardado)
    return "✅ Información guardada correctamente."

if __name__ == '__main__':
    app.run(debug=True)