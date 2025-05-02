from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import qrcode
import os
from openpyxl import Workbook
from datetime import datetime

app = Flask(__name__)

# Link del PDF para el QR
pdf_url = ""
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
    archivo_guardado = os.path.join(BASE_DIR, "data", f"validacion_correctiva_{fecha_archivo}.xlsx")

    # Crear la carpeta 'data' si no existe
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

    # Guardar el archivo
    wb.save(archivo_guardado)

    # Redirigir a una página de éxito con el enlace de descarga
    return render_template("registro_exitoso.html", archivo=os.path.basename(archivo_guardado))

@app.route('/descargas/<archivo>')
def descargar_archivo(archivo):
    # Ruta a la carpeta 'data'
    ruta_descargas = os.path.join(BASE_DIR, "data")
    return send_from_directory(ruta_descargas, archivo, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)