import pandas as pd
from fpdf import FPDF
import os
import qrcode

# Ruta de tu archivo Excel
ruta_excel = 'INVENTARIO_MORATO_VALORIZADO.xlsx'  # Ajusta la ruta si es necesario

# Leer los datos de la hoja "CORRECTIVA"
df = pd.read_excel(ruta_excel, sheet_name='CORRECTIVA')

# Tomar solo la columna 'DESCRIPCION' y eliminar filas vacías
descripciones = df['DESCRIPCION'].dropna()

# Crear el PDF
class PDF(FPDF):
    def header(self):
        # Logo
        self.image('static/img/Integratools.jpg', 10, 8, 25)  # Ajusta el tamaño del logo (25 de ancho)

        # Mover el cursor a la derecha del logo
        self.set_xy(30, 12)  # 45 a la derecha, 12 de alto

        # Título
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'CORRECTIVA No. 1', ln=False, align='C')

        # Dejar espacio después del header
        self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

    def table_header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(20, 10, 'No.', border=1, align='C')
        self.cell(160, 10, 'Descripción', border=1, align='C')
        self.ln()

    def table_row(self, num, descripcion):
        self.set_font('Arial', '', 12)
        self.cell(20, 10, str(num), border=1, align='C')
        self.cell(160, 10, descripcion, border=1)
        self.ln()

# Crear instancia del PDF
pdf = PDF()
pdf.add_page()

# Crear tabla
pdf.table_header()
for idx, descripcion in enumerate(descripciones, start=1):
    pdf.table_row(idx, descripcion)

# Definir la ruta de guardado
ruta_pdf = os.path.expanduser('C:/Users/zagat/OneDrive/Integratools/correctiva_no1.pdf')
pdf.output(ruta_pdf)

# Crear QR apuntando al enlace de OneDrive
url_onedrive = "https://1drv.ms/b/c/38cd35cc36f2a749/EfleQtZJ4_VNlzmBeQH4ymMB2VVHHi4YKdfrJd3etenpTQ?e=0FGNTY"

# Crear y guardar el QR
qr = qrcode.make(url_onedrive)
qr.save('static/qr/correctiva_qr.png')

print("PDF actualizado en OneDrive y QR generado exitosamente.")