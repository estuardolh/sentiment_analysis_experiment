import csv

archivo_entrada = 'corpus.csv'
archivo_salida_entrenamiento = 'entrenamiento.txt'
archivo_salida_prueba = 'prueba.txt'

contenido_a_escribir = ''

INDICE_TEXTO = 0
INDICE_POLARIDAD = 1

def obtener_lista_polaridad(direccion_archivo, indice_inicio, cantidad, polaridad):
  lineas = []
  indice = 0
  acumulados = 0
  with open(direccion_archivo, 'r') as archivo_csv:
    csv_lector = csv.reader(archivo_csv, delimiter=',')
    for linea in csv_lector:
        if indice >= indice_inicio and (polaridad == '' or linea[INDICE_POLARIDAD] == polaridad) and acumulados < cantidad:
            lineas.append(linea[INDICE_TEXTO])
            acumulados += 1
        indice += 1

  return lineas

def escribir_archivo(direccion_archivo, contenido):
    with open(direccion_archivo, 'w+') as archivo_escribir:
        archivo_escribir.write(contenido)
#
# Notas:
# - mitad de reviews para entrenamiento: compuesta en orden positivas y negativas
# - mitad para prueba

# primera parte de entrenamiento
lista_textos_positivos = obtener_lista_polaridad(archivo_entrada, 0, 1376, 'positive')
lista_textos_negativos = obtener_lista_polaridad(archivo_entrada, 0, 1376, 'negative')

print("+"+str(len(lista_textos_positivos)))
print("-"+str(len(lista_textos_negativos)))

#
# #+ = 808
# #- = 568
#      -----
#      1376
#
# #+ = 688
# #- = 568
#      -----
#      1256  
#

contenido_entrenamiento = ''
contenido_prueba = ''

mitad1_primera_parte = ''
cantidad_mitad1 = 400
for positivos in lista_textos_positivos:
    contenido_entrenamiento += positivos + '\n'
    cantidad_mitad1 -= 1
    if cantidad_mitad1 < 1:
        break

cantidad_mitad1 = 400
for negativos in lista_textos_negativos:
    contenido_entrenamiento += negativos + '\n'
    cantidad_mitad1 -= 1
    if cantidad_mitad1 < 1:
        break

indice_mitad2 = 400
for positivos in lista_textos_positivos[indice_mitad2:]:
    contenido_prueba += positivos +'\n'

for negativos in lista_textos_negativos[indice_mitad2:]:
    contenido_prueba += negativos + '\n'

escribir_archivo(archivo_salida_entrenamiento, contenido_entrenamiento)
escribir_archivo(archivo_salida_prueba, contenido_prueba)
print("OK")