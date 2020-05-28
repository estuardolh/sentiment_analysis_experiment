import re

archivo_entrada = 'corpus.n3'
archivo_salida = 'corpus.csv'

contenido_a_escribir = ''

ESTADO_LEYENDO = 0
ESTADO_BUSCANDO = 1
ESTADO_ENCONTRADO = 2

class Entrevista:
  texto = ''
  polaridad = ''

def obtener_csv_de_entrevista(entrevista):
  return '"'+entrevista.texto+'","'+entrevista.polaridad+'"'

def obtener_bloques_en_archivo(archivo_entrada):
  print("Leyendo: "+archivo_entrada)
  lista_bloques = []
  texto_bloque = ''
  with open(archivo_entrada, 'r') as contenido_leer:
    for linea in contenido_leer:
      if len(linea) > 1: # 1 = linea vacia
        texto_bloque += linea + '\n'
      else:
        lista_bloques.append(texto_bloque)
        texto_bloque = ''
  return lista_bloques

def obtener_entrevista_valida(bloque):
  una_entrevista = Entrevista()
  polaridad_indice1 = bloque.find('hasPolarity')
  if polaridad_indice1 > -1:
    polaridad_indice2 = bloque.find('marl/',polaridad_indice1)
    if polaridad_indice2 > -1:
      polaridad_posicion = polaridad_indice2+len('marl/')
      una_entrevista.polaridad = bloque[polaridad_posicion:polaridad_posicion+8]# 6 es el tamano de polaridad

  contenido_indice1 = bloque.find('content')
  texto_contenido = bloque[contenido_indice1:]
  if contenido_indice1 > -1:
    indice_comilla1 = texto_contenido.find('"')
    indice_comilla2 = texto_contenido.find('"', indice_comilla1+1)
    if indice_comilla1 > -1 and indice_comilla2 > -1:
      una_entrevista.texto = texto_contenido[indice_comilla1+1 : indice_comilla2].rstrip()
      # quita url
      una_entrevista.texto = re.sub(r'https://\S+', '', una_entrevista.texto)
      # solo una linea.
      una_entrevista.texto = re.split('\n',una_entrevista.texto)[0]
      # sin tags ni mentions
      una_entrevista.texto = re.sub(r'[#@]','', una_entrevista.texto)

  return una_entrevista

bloques_en_archivo = obtener_bloques_en_archivo(archivo_entrada)
for bloque in bloques_en_archivo:
  entrevista = obtener_entrevista_valida(bloque)
  if(entrevista.polaridad != '' and entrevista.texto != ''):
    contenido_a_escribir += obtener_csv_de_entrevista(entrevista) + '\n'

print("Escribiendo: "+archivo_salida)
with open(archivo_salida, 'w+') as archivo_escribir:
    archivo_escribir.write(contenido_a_escribir)

print("OK")