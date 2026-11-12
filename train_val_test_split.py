"""
El siguiente código generan los directorios destinados a las particiones de datos para el entrenamiento (train), validación (val) y prueba (test). 
Para cada se genera un directorio de imágenes y su correspondiente directorio de anotaciones, 6 en total. Se indica por parámetro train_pct, el 
porcentaje destinado a entrenamiento y por código se calcula la división el porcentaje restante dividido equitativamente entre val y test.
"""

# Importar librerías necesarias para gestionar archivos, procesar archivos XML 
from pathlib import Path
import random
import os
import sys
import shutil
import argparse

# Configuración de los argumentos de entrada del programa
parser = argparse.ArgumentParser(description='División del dataset en train, validation y test.')

parser.add_argument(
    '--datapath',
    help='Ruta del directorio original que contiene las carpetas images y labels',
    required=True
)

parser.add_argument(
    '--train_pct',
    help='Porcentaje de imágenes destinado al entrenamiento',
    type=float,
    default=0.8
)

parser.add_argument(
    '--overwrite',
    help='Permite sustituir las particiones anteriores si ya existen',
    action='store_true'
)

args = parser.parse_args()

# Lectura de los argumentos introducidos
data_path = args.datapath
train_percent = args.train_pct
overwrite = args.overwrite

# Comprobar que el directorio del dataset existe
if not os.path.isdir(data_path):
    print('Error: no se ha encontrado el directorio especificado en --datapath.')
    sys.exit(1)

# Comprobar que el porcentaje de entrenamiento es válido
if train_percent < 0.01 or train_percent > 0.99:
    print('Error: train_pct debe estar comprendido entre 0.01 y 0.99.')
    sys.exit(1)

# Definir las rutas de las imágenes y anotaciones originales
input_image_path = os.path.join(data_path, 'images')
input_label_path = os.path.join(data_path, 'labels')

# Comprobar que existen ambos directorios
if not os.path.isdir(input_image_path) or not os.path.isdir(input_label_path):
    print('Error: el dataset debe contener los directorios images y labels.')
    sys.exit(1)

# El porcentaje restante se distribuye equitativamente entre los subconjuntos de validación y test
remaining_percent = 1 - train_percent

val_percent = remaining_percent / 2
test_percent = remaining_percent / 2

# Directorio principal donde se almacenarán los subconjuntos
output_path = os.path.join(os.getcwd(), 'data')

# Definición de las rutas de imágenes y anotaciones para cada subconjunto de datos
train_img_path = os.path.join(output_path, 'train/images')
train_txt_path = os.path.join(output_path, 'train/labels')

val_img_path = os.path.join(output_path, 'validation/images')
val_txt_path = os.path.join(output_path, 'validation/labels')

test_img_path = os.path.join(output_path, 'test/images')
test_txt_path = os.path.join(output_path, 'test/labels')

# Comprobar si existen particiones de ejecuciones anteriores
previous_splits = [
    os.path.join(output_path, 'train'),
    os.path.join(output_path, 'validation'),
    os.path.join(output_path, 'test')
]

existing_splits = [
    path for path in previous_splits if os.path.exists(path)
]

# Evitar sobrescribir datos anteriores sin autorización
if existing_splits and not overwrite:
    print('Error: ya existen directorios de particiones anteriores.')
    print('Utilice --overwrite si desea sustituirlos.')
    sys.exit(1)

# Eliminar únicamente las particiones anteriores
if overwrite:
    for split_path in existing_splits:
        shutil.rmtree(split_path)

# Crear los seis directorios de salida
for dir_path in [
    train_img_path, train_txt_path,
    val_img_path, val_txt_path,
    test_img_path, test_txt_path
]:
    os.makedirs(dir_path, exist_ok=True)

# Obtener los archivos de imagen del directorio original. (Se consideran únicamente los formatos JPG, JPEG y PNG)
img_file_list = sorted([
    path for path in Path(input_image_path).rglob('*')
    if path.is_file()
    and path.suffix.lower() in ['.jpg', '.jpeg', '.png']
])

# Comprobar que se han encontrado imágenes
if not img_file_list:
    print('Error: no se han encontrado archivos de imagen.')
    sys.exit(1)

print(f'Número de imágenes encontradas: {len(img_file_list)}')

# Semilla aleatoria para garantizar la reproducibilidad de la división
RANDOM_SEED = 42

# Establecer la semilla aleatoria y mezclar la lista de imágenes
random.seed(RANDOM_SEED)
random.shuffle(img_file_list)

# Calcular el número de imágenes de cada subconjunto
file_num = len(img_file_list)

train_num = int(file_num * train_percent)

remaining_num = file_num - train_num

val_num = remaining_num // 2
test_num = remaining_num - val_num

# Mostrar la distribución obtenida
print('\nDistribución del dataset:')

print(f'Train: {train_num} imágenes ({train_num / file_num * 100:.2f}%)')
print(f'Validation: {val_num} imágenes ({val_num / file_num * 100:.2f}%)')
print(f'Test: {test_num} imágenes ({test_num / file_num * 100:.2f}%)')

# Definir los subconjuntos y sus correspondientes directorios
subsets = [
    (train_num, train_img_path, train_txt_path),
    (val_num, val_img_path, val_txt_path),
    (test_num, test_img_path, test_txt_path)
]

# Inicializar el índice de selección
start_index = 0

# Recorrer los tres subconjuntos
for set_num, new_img_path, new_txt_path in subsets:

    # Seleccionar las imágenes correspondientes al subconjunto
    selected_images = img_file_list[start_index:start_index + set_num]

    # Copiar las imágenes y sus anotaciones
    for img_path in selected_images:

        img_fn = img_path.name
        base_fn = img_path.stem

        # Obtener el nombre y la ruta de la anotación correspondiente
        txt_fn = base_fn + '.txt'
        txt_path = os.path.join(input_label_path, txt_fn)

        # Copiar la imagen al directorio de destino
        shutil.copy(img_path, os.path.join(new_img_path, img_fn))

        # Copiar la anotación si existe. Si no existe, la imagen se considera una imagen de fondo
        if os.path.exists(txt_path):
            shutil.copy(txt_path, os.path.join(new_txt_path, txt_fn))

    # Actualizar el índice para el siguiente subconjunto
    start_index += set_num

# Mostrar en el terminal los datos de la división
print('\nDivisión del dataset completada correctamente.')

print(f'\nSemilla aleatoria utilizada: {RANDOM_SEED}')
print(f'Porcentaje de entrenamiento: {train_percent * 100:.1f}%')
print(f'Porcentaje de validación: {val_percent * 100:.1f}%')
print(f'Porcentaje de test: {test_percent * 100:.1f}%')

print(f'\nDirectorio de salida: {output_path}')
