# -*- coding: utf 8 -*
def ayuda():
  ayuda_t = ("Bienvenido a stabpy, seleciona en cada pestaña lo que deseas"
             +" hacer"
            )
  return ayuda_t

def ayuda_1():
  ayuda_1_t = ('El nombre de la molecula permitirá identificar todos los '
              +'estudios asociados a ella\n'
              +'Recuerda tener organizado la forma en es nombrada la molecula\n'
              +'pues el acceso a los datos tendrá en cuenta mayúsculas\n'
              +'y gedi  minúsculas'
              )
  return ayuda_1_t

def ayuda_2():
  ayuda_2_t = ( 'El id del estudio será el diferenciador del estudio '
               +'realizado\n'
               +'Para estudios de estabilidad acelerada debe contarse con un\n'
               +'codigo que diferencie el set de datos de la estabilidad\n'
               +'acelerada de la natural, pues tendrán el mismo lote\n'
               +'estudios de estabilidad compuestos por varios lotes \n'
               +'deberán tener el mismo codigo de estudio, y se diferenciarán\n'
               +'por el codigo del lote'
              )
  return ayuda_2_t

def ayuda_3():
  ayuda_3_t = ('Un estudio de estabilidad on going se puede desarrollar con\n'
              +'un solo lote, un estudio de estabilidad para determinar\n'
              +'tiempo de vida de un producto terminado debe tener asociados\n'
              +'minimo 3 lotes'
              )
  return ayuda_3_t

def ayuda_4():
  ayuda_4_t = ('El numero de tiempos, en meses o años, en los que se evaluó\n'
              +'la estabilidad'
              )
  return ayuda_4_t 

def ayuda_5():
  ayuda_5_t = ('Si hay distinto numero de replicas, elegir el de numero mayor\n'
              )
  return ayuda_5_t
