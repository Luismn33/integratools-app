import qrcode

# Tu enlace de OneDrive (el que me pasaste)
url = "https://1drv.ms/b/c/38cd35cc36f2a749/EfleQtZJ4_VNlzmBeQH4ymMB2VVHHi4YKdfrJd3etenpTQ?e=0FGNTY"

# Crear el objeto QR
qr = qrcode.make(url)

# Guardarlo en tu equipo
qr.save("static/qr/qr_correctiva_no1.png")

print("¡Código QR generado exitosamente!")