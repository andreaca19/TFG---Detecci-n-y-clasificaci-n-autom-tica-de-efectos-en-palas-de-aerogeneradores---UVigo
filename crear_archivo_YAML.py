"""
Función de Python que crea automáticamente el archivo de configuración data.yaml. 
Lee el archivo de texto "classes.txt" donde se listan las clases de objetos a identificar, y obtiene los nombres de estas.
Crea un diccionario con las rutas de acceso a los directorios que se vayan a utilizar, número de clases de objetos y sus nombres.
Escribe la información en formato YAML en el archivo data.yaml.
"""

# Importar librerías para la creación del archivo data.yaml
import yaml
import os

def create_data_yaml(path_to_classes_txt, path_to_data_yaml):

  # Leer el archivo de texto "classes.txt" y obtiene los nombres especificados
  if not os.path.exists(path_to_classes_txt):
    print(f'classes.txt file not found! Please create a classes.txt labelmap and move it to {path_to_classes_txt}')
    return
  with open(path_to_classes_txt, 'r') as f:
    classes = []
    for line in f.readlines():
      if len(line.strip()) == 0: continue
      classes.append(line.strip())
  number_of_classes = len(classes)

  # Crear el diccionario con las rutas de acceso a los directorios
  data = {
      'path': '/content/data',
      'train': 'train/images',
      'val': 'validation/images',
      'test': 'test/images',
      'nc': number_of_classes,
      'names': classes
  }

  # Escribir la información en el archivo data.yaml
  with open(path_to_data_yaml, 'w') as f:
    yaml.dump(data, f, sort_keys=False)
  print(f'Created config file at {path_to_data_yaml}')

  return

# 
path_to_classes_txt = '/content/custom_data/data/classes.txt'
path_to_data_yaml = '/content/data.yaml'

create_data_yaml(path_to_classes_txt, path_to_data_yaml)

print('\nFile contents:\n')
!cat /content/data.yaml
