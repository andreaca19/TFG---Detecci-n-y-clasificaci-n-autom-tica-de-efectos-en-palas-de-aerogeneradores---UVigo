"""
El siguiente código permite el cambio de formato de los archivos de anotaciones en PASCAL VOC XML a YOLO
Se lee cada archivo XML, se realizan las operaciones para obtener los datos necesarios para el formato YOLO
y se crea un archivo .txt con estos datos manteniendo en el nombre del archivo original.
"""

import os
import xml.etree.ElementTree as ET

# Variables de anchura y altura de la imagen 1024 x 1024
image_width = 1024
image_height = 1024

# Carpeta donde están los archivos XML
annotations_path = "nombre_carpeta_principal/nombre_carpeta_archivos_xml"

# Carpeta donde se guardarán los archivos convertidos a formato YOLO
labels_path = "nombre_carpeta_principal/labels"

# Nombres de cada clase de objeto a detectar en la imagen
classes = [
    "corrosion",
    "craze",
    "surface_injure",
    "thunderstrike",
    "crack",
    "hide_craze"
]


# Crear carpeta de salida
os.makedirs(labels_path, exist_ok=True)

# Obtener todos los archivos XML
files = [
    f for f in os.listdir(annotations_path)
    if f.lower().endswith(".xml")
]

# Recorrer todos los archivos XML
for filename in files:
    try:

        xml_path = os.path.join(annotations_path, filename)

        txt_filename = os.path.splitext(filename)[0] + ".txt"
        output_txt_path = os.path.join(labels_path, txt_filename)

        # Leer el XML
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Convertir objetos
        with open(output_txt_path, "w") as output_file:

            for obj in root.findall("object"):

                class_name = obj.find("name").text.strip()

                print("  Clase encontrada:", class_name)

                # Comprobar clase de objeto
                if class_name not in classes:

                    print(
                        "  ADVERTENCIA: clase desconocida:",
                        class_name
                    )

                    continue

                class_id = classes.index(class_name)

                # Bounding Box PASCAL VOC XML
                bndbox = obj.find("bndbox")

                xmin = float(
                    bndbox.find("xmin").text
                )

                ymin = float(
                    bndbox.find("ymin").text
                )

                xmax = float(
                    bndbox.find("xmax").text
                )

                ymax = float(
                    bndbox.find("ymax").text
                )

                # Calcular centro
                x_center = (xmin + xmax) / 2
                y_center = (ymin + ymax) / 2

                # Anchura y Altura
                width = xmax - xmin
                height = ymax - ymin

                # Normalización YOLO
                x_center /= image_width
                y_center /= image_height

                width /= image_width
                height /= image_height

                # Escribir línea YOLO
                output_file.write(
                    f"{class_id} "
                    f"{x_center:.6f} "
                    f"{y_center:.6f} "
                    f"{width:.6f} "
                    f"{height:.6f}\n"
                )

    # Aviso en caso de error
    except Exception as e:

        errores += 1

        print()
        print("  ❌ ERROR EN:", filename)
        print("  Motivo:", e)
        print("  Se continúa con el siguiente archivo.")
        print()
