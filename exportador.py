from PIL import Image
import os

# Eliminar el límite de tamaño de imagen
# Remove the image size limit
Image.MAX_IMAGE_PIXELS = None

# Definir carpetas
# Define folders
carpeta_origen = 'render'
carpeta_salida = 'salida'

# Crear carpeta de salida si no existe
# Create output folder if it doesn't exist
os.makedirs(carpeta_salida, exist_ok=True)

# Buscar la imagen PNG en la carpeta de origen
# Find the PNG image in the source folder
imagen_png = None
nombre_base = None
for archivo in os.listdir(carpeta_origen):
    if archivo.lower().endswith('.png'):
        imagen_png = os.path.join(carpeta_origen, archivo)
        nombre_base = os.path.splitext(archivo)[0]  # Obtener el nombre base del archivo sin la extensión
        # Get the base name of the file without the extension
        break

# Verificar si se encontró una imagen
# Check if an image was found
if imagen_png is None:
    print("No se encontró ninguna imagen PNG en la carpeta 'render'.")
    # No PNG image found in the 'render' folder.
else:
    # Cargar la imagen original
    # Load the original image
    imagen = Image.open(imagen_png)

    # Obtener DPI original
    # Get the original DPI
    dpi_original = imagen.info.get('dpi', (72, 72))  # Obtiene el DPI original, o usa (72, 72) si no se encuentra
    # Gets the original DPI, or uses (72, 72) if not found

    # Definir las resoluciones de salida
    # Define output resolutions
    resoluciones = [
        (2000, 2000),  # 2000x2000 px
        (400, 400),    # 400x400 px
        (800, 800)     # 800x800 px
    ]

    # Crear versiones PNG redimensionadas con 72 dpi
    # Create resized PNG versions with 72 dpi
    for ancho, alto in resoluciones:
        imagen_redimensionada = imagen.resize((ancho, alto), Image.LANCZOS)
        nombre_archivo = f'{nombre_base}_{ancho}px.png'
        imagen_redimensionada.save(os.path.join(carpeta_salida, nombre_archivo), 'PNG', dpi=(72, 72))

    # Guardar la versión en JPG con la resolución original y DPI original
    # Save the JPG version with the original resolution and original DPI
    imagen_fondo_blanco = Image.new("RGB", imagen.size, (255, 255, 255))
    if imagen.mode == 'RGBA':
        imagen_fondo_blanco.paste(imagen, mask=imagen.split()[3])  # Usar la transparencia del canal alpha
        # Use the transparency of the alpha channel
    else:
        imagen_fondo_blanco.paste(imagen)
    nombre_archivo_original = f'{nombre_base}_original.jpg'
    imagen_fondo_blanco.save(os.path.join(carpeta_salida, nombre_archivo_original), 'JPEG', dpi=dpi_original, quality=95)

    # Crear versiones JPG redimensionadas con fondo blanco y 72 dpi
    # Create resized JPG versions with a white background and 72 dpi
    for ancho, alto in resoluciones:
        imagen_redimensionada = imagen.resize((ancho, alto), Image.LANCZOS)
        imagen_fondo_blanco = Image.new("RGB", imagen_redimensionada.size, (255, 255, 255))
        if imagen_redimensionada.mode == 'RGBA':
            imagen_fondo_blanco.paste(imagen_redimensionada, mask=imagen_redimensionada.split()[3])  # Usar la transparencia del canal alpha
            # Use the transparency of the alpha channel
        else:
            imagen_fondo_blanco.paste(imagen_redimensionada)
        nombre_archivo_jpg = f'{nombre_base}_{ancho}px.jpg'
        imagen_fondo_blanco.save(os.path.join(carpeta_salida, nombre_archivo_jpg), 'JPEG', dpi=(72, 72), quality=95)

    print("Imágenes creadas y guardadas en la carpeta 'salida'.")
    # Images created and saved in the 'salida' folder.