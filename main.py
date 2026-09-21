import os
import xml.etree.ElementTree as ET


# ============================================================
# CONFIGURACIÓN
# ============================================================

image_width = 1024
image_height = 1024

annotations_path = "prueba_conversion/annotations"
labels_path = "prueba_conversion/labels"

classes = [
    "corrosion",
    "craze",
    "surface_injure",
    "thunderstrike",
    "crack",
    "hide_craze"
]


# ============================================================
# CREAR CARPETA DE SALIDA
# ============================================================

os.makedirs(labels_path, exist_ok=True)


# ============================================================
# OBTENER TODOS LOS ARCHIVOS XML
# ============================================================

files = [
    f for f in os.listdir(annotations_path)
    if f.lower().endswith(".xml")
]

print("============================================")
print("ARCHIVOS ENCONTRADOS")
print("============================================")
print("Número de archivos XML encontrados:", len(files))
print()


# ============================================================
# CONTADORES
# ============================================================

convertidos = 0
errores = 0


# ============================================================
# RECORRER TODOS LOS XML
# ============================================================

for filename in files:

    print("Procesando:", filename)

    try:

        # ----------------------------------------------------
        # RUTAS
        # ----------------------------------------------------

        xml_path = os.path.join(annotations_path, filename)

        txt_filename = os.path.splitext(filename)[0] + ".txt"
        output_txt_path = os.path.join(labels_path, txt_filename)


        # ----------------------------------------------------
        # LEER XML
        # ----------------------------------------------------

        tree = ET.parse(xml_path)
        root = tree.getroot()


        # ----------------------------------------------------
        # CONVERTIR OBJETOS
        # ----------------------------------------------------

        with open(output_txt_path, "w") as output_file:

            for obj in root.findall("object"):

                class_name = obj.find("name").text.strip()

                print("  Clase encontrada:", class_name)


                # ------------------------------------------------
                # COMPROBAR CLASE
                # ------------------------------------------------

                if class_name not in classes:

                    print(
                        "  ADVERTENCIA: clase desconocida:",
                        class_name
                    )

                    continue


                # ------------------------------------------------
                # ID DE CLASE
                # ------------------------------------------------

                class_id = classes.index(class_name)


                # ------------------------------------------------
                # BOUNDING BOX PASCAL VOC
                # ------------------------------------------------

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


                # ------------------------------------------------
                # CENTRO
                # ------------------------------------------------

                x_center = (xmin + xmax) / 2
                y_center = (ymin + ymax) / 2


                # ------------------------------------------------
                # ANCHURA Y ALTURA
                # ------------------------------------------------

                width = xmax - xmin
                height = ymax - ymin


                # ------------------------------------------------
                # NORMALIZACIÓN YOLO
                # ------------------------------------------------

                x_center /= image_width
                y_center /= image_height

                width /= image_width
                height /= image_height


                # ------------------------------------------------
                # ESCRIBIR LÍNEA YOLO
                # ------------------------------------------------

                output_file.write(
                    f"{class_id} "
                    f"{x_center:.6f} "
                    f"{y_center:.6f} "
                    f"{width:.6f} "
                    f"{height:.6f}\n"
                )


        # ----------------------------------------------------
        # ARCHIVO CONVERTIDO CORRECTAMENTE
        # ----------------------------------------------------

        convertidos += 1

        print("  ✓ Archivo creado:", txt_filename)
        print()


    # ========================================================
    # SI HAY UN ERROR, CONTINUAR CON EL SIGUIENTE
    # ========================================================

    except Exception as e:

        errores += 1

        print()
        print("  ❌ ERROR EN:", filename)
        print("  Motivo:", e)
        print("  Se continúa con el siguiente archivo.")
        print()


# ============================================================
# RESUMEN FINAL
# ============================================================

print()
print("============================================")
print("CONVERSIÓN TERMINADA")
print("============================================")
print("XML encontrados:", len(files))
print("Convertidos correctamente:", convertidos)
print("Archivos con errores:", errores)
print("============================================")