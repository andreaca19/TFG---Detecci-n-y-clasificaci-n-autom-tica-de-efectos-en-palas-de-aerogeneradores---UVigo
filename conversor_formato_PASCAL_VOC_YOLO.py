"""
El siguiente código permite el cambio de formato de los archivos de anotaciones en PASCAL VOC XML a YOLO
Se lee cada archivo XML, se realizan las operaciones para obtener los datos necesarios para el formato YOLO
y se crea un archivo .txt con estos datos manteniendo en el nombre del archivo original.
"""

# Importar las librerías necesarias para gestionar y procesar archivos XML
import os
import xml.etree.ElementTree as ET

# Variables de anchura y altura de la imagen original 1024 x 1024
image_width = 1024
image_height = 1024

# Carpeta donde están los archivos XML
annotations_path = "nombre_carpeta_principal/nombre_carpeta_archivos_xml"

# Carpeta donde se guardarán los archivos convertidos a formato YOLO
labels_path = "nombre_carpeta_principal/labels"

# Nombres de las clases de objetos a detectar en la imagen
classes = [
    "corrosion",
    "craze",
    "surface_injure",
    "thunderstrike",
    "crack",
    "hide_craze"
]

# Crear la carpeta de salida
os.makedirs(labels_path, exist_ok=True)

# Obtener los nombres de todos los archivos XML en la carpeta de anotaciones
files = [
    f for f in os.listdir(annotations_path)
    if f.lower().endswith(".xml")
]

# Recorrer todos los archivos XML obtenidos
for filename in files:
    try:

        # Crear la ruta completa del archivo XML
        xml_path = os.path.join(annotations_path, filename)

        # Crear el nombre y la ruta del archivo .txt correspondiente
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        output_txt_path = os.path.join(labels_path, txt_filename)

        # Leer y obtener el elemento raíz del archivo XML
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Crear el archivo .txt donde se almacenarán las anotaciones en formato YOLO
        with open(output_txt_path, "w") as output_file:

            # Buscar todos los objetos anotados en el archivo XML
            for obj in root.findall("object"):

                # Obtener el nombre de la clase correspondiente al objeto
                class_name = obj.find("name").text.strip()

                # Comprobar que la clase está incluída en la lista de clases definida
                if class_name not in classes:

                    # Mostrar una advertencia en el terminal si se encuentra una clase desconocida
                    print(
                        "  ADVERTENCIA: clase desconocida:",
                        class_name
                    )

                    continue

                # Obtener el identificador numérico de la clase según su posición en la lista
                class_id = classes.index(class_name)

                # Obtener las coordenadas de la Bounding Box en formato PASCAL VOC XML
                bndbox = obj.find("bndbox")

                # Obtener las coordenadas de los extremos de la Bounding Box
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

                # Calcular las coordenadas del centro de la Bounding Box
                x_center = (xmin + xmax) / 2
                y_center = (ymin + ymax) / 2

                # Calcular la anchura y altura de la Bounding Box
                width = xmax - xmin
                height = ymax - ymin

                # Normalizar las coordenadas y dimensiones respecto al tamaño de la imagen
                x_center /= image_width
                y_center /= image_height

                width /= image_width
                height /= image_height

                # Escribir la anotación en formato YOLO: identificador de clase, centro X, centro Y, anchura y altura
                output_file.write(
                    f"{class_id} "
                    f"{x_center:.6f} "
                    f"{y_center:.6f} "
                    f"{width:.6f} "
                    f"{height:.6f}\n"
                )

    # Aviso en caso de producirse un error durante el procesamiento del archivo
    except Exception as e:

        print()
        print("  ❌ ERROR EN:", filename)
        print("  Motivo:", e)
        print("  Se continúa con el siguiente archivo.")
        print()
