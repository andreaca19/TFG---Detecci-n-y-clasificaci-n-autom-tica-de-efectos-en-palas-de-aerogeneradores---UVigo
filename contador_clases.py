"""
El siguiente código recorre los archivos XML en la carpeta de anotaciones, contando cuántas veces aparece cada clase de objeto. 
El objetivo es conocer el número de veces que se etiquetó cada clase para su posterior relación con los resultados obtenidos
en el entrenamiento.
"""

import os
import xml.etree.ElementTree as ET
from collections import Counter

# Carpeta donde están los archivos XML
xml_folder = "nombre_carpeta_principal/nombre_carpeta_archivos_xml"

# Archivo de salida en formato .txt
output_file = "nombre_carpeta_principal/recuento_clases.txt"

# Contador de objetos por clase
class_counter = Counter()

# Recorrer todos los archivos XML
for filename in os.listdir(xml_folder):

    if filename.endswith(".xml"):

        xml_path = os.path.join(xml_folder, filename)

        # Leer el XML
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Buscar todos los objetos anotados
        for obj in root.findall("object"):

            # Obtener el nombre de la clase
            class_name = obj.find("name").text.strip()

            # Contabilizar esa instancia
            class_counter[class_name] += 1


# Crear el archivo .txt con los resultados
with open(output_file, "w", encoding="utf-8") as file:

    file.write("Número de objetos anotados por clase\n")
    file.write("--------------------------------------\n\n")

    for class_name, count in sorted(class_counter.items()):
        file.write(f"{class_name}: {count}\n")

print(f"Recuento guardado en: {output_file}")
