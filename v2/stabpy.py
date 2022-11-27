#!/usr/bin/python
# -*- coding: utf 8 -*
'''
este es stappy
'''
import gc
from Tkinter import *
import ttk
import tkMessageBox
import json
import mysql.connector
#clases propias
#ventana de login
from login import Dialog
#clase para el ingreso de datos
from claseingresodatos import ingreso_datos
#mensajes y ayudas
from funcionesinfo import *
gc.enable()
stabpy = Tk()
#login
print "login inactivo"
#stabpy.update()
#d = Dialog(stabpy)
# d.acceso[0]
#accesorios generales
stabpy.title("STABPY por William David Suarez")
salida = Button(stabpy, text="Salir",command=quit)#.grid(row=0,column=0)
salida.pack(side=BOTTOM)
info_n_e = StringVar()
info_n_e.set(ayuda())
label_info = Label(stabpy,
                       textvariable=info_n_e,
                       justify=LEFT,
                       width=80,
                       ).pack(side=BOTTOM )
#iniciacion del cuaderno
cuaderno = ttk.Notebook(stabpy)
cuaderno.pack(fill='both',expand='yes')
#cuaderno del nuevo estudio
#funciones en el nuevo estudio
#instrucciones nombre de la molecula
def info_nombre_molecula():
  info_n_e.set(ayuda_1())
  return True
#instrucciones id del estudio
def info_id_estudio():
  info_n_e.set(ayuda_2)
  return True
#instrucciones lote
def info_lote():
  info_n_e.set(ayuda_3())
  return True
nuevo_estudio = ttk.Frame(cuaderno)
#nombre de la molecula
label_molecula_n_e = Label(nuevo_estudio,
                             text='Nombre de la molecula'
                          ).place(x=10,y=10)
molecula_n_e = StringVar()
entrada_molecula_n_e = Entry(nuevo_estudio,
                             textvariable=molecula_n_e,
                             validate="focusin",
                             vcmd=info_nombre_molecula,
                             ).place(x=210,y=10)

#id del estudio
label_idstudio_n_e = Label(nuevo_estudio,
                             text='codigo identificador del estudio'
                            ).place(x=10,y=30)
idstudio_n_e = StringVar()
entrada_istudio_n_e = Entry(nuevo_estudio,
                            textvariable=idstudio_n_e,
                            validate="focusin",
                            vcmd=info_id_estudio,
                           ).place(x=210,y=30)
#lote
label_lote_n_e = Label(nuevo_estudio,
                       text='Lote'
                      ).place(x=10,y=50)
lote_n_e = StringVar()
entrada_lote_n_e = Entry(nuevo_estudio,
                         textvariable=lote_n_e,
                         validate="focusin",
                         vcmd=info_lote,
                        ).place(x=210,y=50)
#data
def info_numero_tiempos():
  info_n_e.set(ayuda_4())
  return True
def info_numero_replicas():
  info_n_e.set(ayuda_5())
  return True
#funcion lanzar ingreso de datos
def lanzar_ingreso_datos():
  try:
    largo = numero_tiempos.get()
    alto = numero_replicas.get()
    replicas_iguales = numero_replicas_igual.get()
    if alto>0 and largo>0:  
      if largo == 1 and replicas_iguales==False:
        f = ingreso_datos(stabpy,largo,alto,True)
      else:
        f = ingreso_datos(stabpy,largo,alto,replicas_iguales)
    elif alto<=0 or largo<=0:
      tkMessageBox.showwarning("ATENCIÓN",
                               "error en valores de timpos y replicas")
  except:
    tkMessageBox.showwarning("ATENCIÓN",
                               "error en valores de timpos y replicas")
  global data  
  data = f.data_resultado
  return funcion_datos_en_transporte()   
#
label_data = Label(nuevo_estudio,
                  text='set de datos por lote'
                 ).place(x=10,y=70)
#tiempos
label_numero_totaltiempos = Label(nuevo_estudio,
                                  text='¿cuántos tiempos?'
                                 ).place(x=10,y=90)
numero_tiempos = IntVar()
entrada_numero_tiempos = Entry(nuevo_estudio,
                               textvariable=numero_tiempos,
                               validate="focusin",
                               vcmd=info_numero_tiempos
                              ).place(x=210,y=90)
#replicas
label_numero_replicas = Label(nuevo_estudio,
                                  text='¿cuántas replicas?'
                                 ).place(x=10,y=110)
numero_replicas = IntVar()
entrada_numero_replicas = Entry(nuevo_estudio,
                               textvariable=numero_replicas,
                               validate="focusin",
                               vcmd=info_numero_replicas
                               ).place(x=210,y=110)
#radio botón de replicas iguales
label_replicas_iguales = Label(nuevo_estudio,
                                  text='¿tienen los tiempos igual numero de '
                                       +'replicas?'
                                 ).place(x=10,y=130)
numero_replicas_igual = BooleanVar()
numero_replicas_igual.set("true")
Radiobutton(nuevo_estudio,
            text="Sí", 
            variable=numero_replicas_igual, value=True).place(x=10,y=150)
Radiobutton(nuevo_estudio,
            text="No", 
            variable=numero_replicas_igual, value=False).place(x=50,y=150)
#boton que lanza el ingreso de datos
boton_ingreso_datos = Button(nuevo_estudio,
                             text="ingreso de datos",
                             command=lanzar_ingreso_datos
                             ).place(x=10,y=180)
#muestra de datos
def funcion_datos_en_transporte():
  tkMessageBox.showwarning("datos",
                       "verifica con mucha anteción los datos antes guardarlos")
  print "el nombre es ",molecula_n_e.get()
  global a  
  a  = molecula_n_e.get()
  print "el id del estudio es: ",idstudio_n_e.get()
  global b
  b = idstudio_n_e.get()
  print "el lote es: ", lote_n_e.get()
  global c
  c = lote_n_e.get()
  print "trasformacion datos"
  print data
  d = "DATOS:\n"
  type(d)
  for item in data.keys():
    if item == "tiempos":
      d += "los tiempos son: " + json.dumps(data[item])+"\n"
      pass
    else:
      d += "en el "+str(item)+"\n"+"los datos son: "+json.dumps(data[item])+"\n"
  datos_en_transporte.set("estos son los datos que se han recibido\n"
                         +"la molecula es: " + a +"\n"
                         +"el estudio es el: " + b +"\n"
                         +"el lote es: " + c +"\n"
                         + d   
                          )
  pass
datos_en_transporte = StringVar()
antes_datos ="Es importante ser atento en el correcto ingreso de datos"
datos_en_transporte.set(antes_datos)
label_datos_en_transporte = Label(nuevo_estudio,
                                  textvariable=datos_en_transporte,
                                  
                                 ).place(x=10,y=230)
#guardar en base de datos

def enviar_a_db():
  cnx = mysql.connector.connect(user='admin',
                                password='adminstabpy',
                                database='stabpy')
  apuntador =cnx.cursor()
  datos_a_db = json.dumps(data) 
  print type(datos_a_db)
  sentencia =( "INSERT INTO stabpy "
             + "VALUES ('"
             + a +"','"
             + b +"','"
             + c +"','"
             + datos_a_db +"');"
            )
  print sentencia    
  apuntador.execute(sentencia)
  cnx.commit()
  apuntador.close()
  cnx.close()
  pass
boton_enviar_a_bd = Button(nuevo_estudio,
                           text="enviar a base de datos",
                           command=enviar_a_db,
                           ).place(x=300,y=450)                                  
                            
#cuaderno de continuar con el estudio
continuar_estudio = ttk.Frame(cuaderno)
#generar reporte
#funciones en reporte
#consultar para el menu del id del estudio
def consultar():
  cnx = mysql.connector.connect(user='admin',
                                password='adminstabpy',
                                database='stabpy')
  apuntador =cnx.cursor()
  
  
  sentencia = "SELECT idsteudio FROM stabpy;"
  apuntador.execute(sentencia)
  lista = []
  for idsteudio in apuntador:
    l = idsteudio
    lista.append(l[0])
  #en este loop eliminamos repeticiones
  a = True
  while a == True:
    try:
      for i in range(len(lista)):
        if lista.count(lista[i]) >= 2:
          lista.remove(lista[i]) 
        elif lista.count(lista[i]) == 1:
          continue
        else:
          continue
      a = False
    except:
      continue
  apuntador.close()
  cnx.close()
  return lista
#filtrar estudio
def filtrarestudio():
  estudio_a_buscar = listado_estudios.get()
  cnx = mysql.connector.connect(user='admin',
                                password='adminstabpy',
                                database='stabpy')
  apuntador =cnx.cursor()
  
  
  sentencia = ("SELECT lote FROM stabpy where idsteudio='"
              + estudio_a_buscar
              +"';"
              )
  apuntador.execute(sentencia)
  listalotes = []
  for lote in apuntador:
    l = lote
    listalotes.append(l[0])
  apuntador.close()
  cnx.close()
  lista_lotes.delete(0,END)
  for item in listalotes:
    lista_lotes.insert(END,item)
  return listalotes
#vida util individual
#clase para calculo de cada lote
import numpy
from scipy import stats
import math
class regresion:
  def __init__(self,x,y):
    self.x = x
    self.y = y
  def ejecutarregresion(self):
    VARx = (
          numpy.sum([self.x[i]**2 for i in range(len(self.x))])
          /
          len(self.x)
           ) - (numpy.mean(self.x)**2)
    COV = (
          numpy.sum([self.x[i]*self.y[i] for i in range(len(self.x))])
          /
          len(self.x)
          ) - (numpy.mean(self.x)*numpy.mean(self.y))
    pendiente = COV / VARx
    intercepto = numpy.mean(self.y) - (numpy.mean(self.x)*pendiente)
       
    varianza_reg = (numpy.sum([(
                                  (self.y[i]-(intercepto + (pendiente*self.x[i])
                            ))**2)for i in range(len(self.x))]))/(len(self.x)-2)
    #
    self.pendiente = pendiente
    self.intercepto = intercepto
    self.varianza_reg = varianza_reg 
    pass
  def tiempodevida(self):
    Newton_Rhapson = False
    x_0 = 0
    while Newton_Rhapson == False:
      CL = 90
      x_om = self.pendiente*x_0
      alfa = 0.95
      df = (len(self.x)-2)
      t = stats.t.ppf(alfa,df)
      error = math.sqrt(self.varianza_reg)
      sumatoria = numpy.sum([(self.x[i] - numpy.mean(self.x))**2
                             for i in range(len(self.x))] )
      valor = (x_0 - numpy.mean(self.x))**2
      cociente = valor / sumatoria
      termino_n = (float(len(self.x)) +1)/float(len(self.x))
      raiz = math.sqrt( termino_n + cociente )
      f_x = -CL + x_om + self.intercepto - (t*error*raiz)
      f_x_prima = self.pendiente - ( 
                   t*error*1/2*(1/raiz)*2*((x_0 - numpy.mean(self.x))/sumatoria)
                                    )
      x_1 = x_0 - (f_x/f_x_prima)
      if abs(x_1 - x_0) <= 0.001:
        Newton_Rhapson = True
      x_0 = x_1
    #fin de la regresion
    pass
#la clase ancova se inicia aqui
class ancova:
  def __init__(self,x,y):
    self.x = x
    self.y = y
    pass  
  def ancovacal(self):
    print "acá iniciamos"
    cuadrados_x = [[self.x[i][j]*self.x[i][j] for j in range(len(self.x[i]))]
                                                    for i in range(len(self.x))]
    suma_cuadrados_x = [numpy.sum(cuadrados_x[i] ) 
                                               for i in range(len(cuadrados_x))]    
    suma_al_cuadrado_x = [pow(numpy.sum(self.x[i]),2) 
                                                    for i in range(len(self.x))]
    varianza_x = [(suma_cuadrados_x[i]-(
                          suma_al_cuadrado_x[i]/float(len(self.x[i])))) 
                                          for i in range(len(suma_cuadrados_x))]   
    varianza_total_x = numpy.sum(varianza_x)
    cuadrados_xy = [[self.x[i][j]*self.y[i][j] for j in range(len(self.x[i]))]
                                                    for i in range(len(self.x))]   
    suma_cuadrados_xy = [numpy.sum(cuadrados_xy[i] ) 
                                              for i in range(len(cuadrados_xy))]
    producto_suma_xy = [ numpy.sum(self.x[i])*numpy.sum(self.y[i]) 
                      for i in range(len(self.x))]
    varianza_xy = [(suma_cuadrados_xy[i]-(
                          producto_suma_xy[i]/float(len(self.x[i])))) 
                                         for i in range(len(suma_cuadrados_xy))]
    varianza_total_xy = numpy.sum(varianza_xy)
    cuadrados_y = [[self.y[i][j]*self.y[i][j] for j in range(len(self.y[i]))]
                                                    for i in range(len(self.y))]
    suma_cuadrados_y = [numpy.sum(cuadrados_y[i] ) 
                                               for i in range(len(cuadrados_y))]    
    suma_al_cuadrado_y = [pow(numpy.sum(self.y[i]),2) 
                                                    for i in range(len(self.y))]
    varianza_y = [(suma_cuadrados_y[i]-(
                          suma_al_cuadrado_y[i]/float(len(self.y[i])))) 
                                          for i in range(len(suma_cuadrados_y))]   
    varianza_total_y = numpy.sum(varianza_y)
    suma_intra_grupos = varianza_total_y - (
                                      pow(varianza_total_xy,2)/varianza_total_x)
    concatenado_x =[]
    for i in range(len(self.x)):
      concatenado_x += self.x[i]
    suma_cuadrados_concatenado_x = numpy.sum([pow(concatenado_x[i],2) 
                                            for i in range(len(concatenado_x))])
    cuadrado_suma_x_concatenado = (pow(numpy.sum(concatenado_x),2) 
                                  /float(len(concatenado_x)))
    residuos_de_x = suma_cuadrados_concatenado_x - cuadrado_suma_x_concatenado
    concatenado_y =[]
    for i in range(len(self.y)):
      concatenado_y += self.y[i]
    suma_cuadrados_concatenado_y = numpy.sum([pow(concatenado_y[i],2) 
                                            for i in range(len(concatenado_y))])
    cuadrado_suma_y_concatenado = (pow(numpy.sum(concatenado_y),2) 
                                  /float(len(concatenado_y)))
    residuos_de_y = suma_cuadrados_concatenado_y - cuadrado_suma_y_concatenado
    suma_producto_concatenado_xy = numpy.sum([concatenado_y[i]*concatenado_x[i] 
                                            for i in range(len(concatenado_x))])
    producto_suma_xy_concatenado = (
                               numpy.sum(concatenado_y)*numpy.sum(concatenado_x)
                                  /float(len(concatenado_y)))
    residuos_de_xy = suma_producto_concatenado_xy - producto_suma_xy_concatenado
    sumas_totales = residuos_de_y - ( pow(residuos_de_xy,2) / residuos_de_x)    
    sumas_entre_lotes = sumas_totales - suma_intra_grupos    
    df_entre_lotes = float(len(self.x)-1)
    df_intra_grupos = float(len(concatenado_x)-len(self.x)-1)
    df_totales = df_entre_lotes + df_intra_grupos
    CM_entre_lotes = sumas_entre_lotes / df_entre_lotes
    CM_intra_grupos = suma_intra_grupos / df_intra_grupos    
    F_de_tiempo = CM_entre_lotes / CM_intra_grupos
    if F_de_tiempo <= stats.f.ppf(1-0.05,df_entre_lotes,df_intra_grupos):
      print "error, hay efecto del tiempo"
    else:
      print "Hay efecto del tiempo"
      pass
    residuos_individuales = [ varianza_y[i] - ( 
                                            pow(varianza_xy[i],2)/varianza_x[i]) 
                                                for i in range(len(varianza_y))]    
    suma_residuos_individuales = numpy.sum(residuos_individuales)    
    suma_de_heterogenea = suma_intra_grupos -suma_residuos_individuales 
    df_de_heterogenea = len(self.x)-1
    df_residuos_individuales = len(concatenado_x)-(2*len(self.x))
    CM_de_heterogenea = suma_de_heterogenea / df_de_heterogenea
    CM_residuos_individuales = (suma_residuos_individuales 
                                                     / df_residuos_individuales)
    F_ancova = CM_de_heterogenea / CM_residuos_individuales  
    pcvalue = 1-stats.f.cdf(F_ancova,df_de_heterogenea,df_residuos_individuales)
    print "aca va el p critico"    
    print pcvalue 
    pendiente_ajustada = varianza_total_xy/varianza_total_x
    intercepto_ajustado = (numpy.sum(concatenado_y)/float(len(concatenado_y)))-(
        pendiente_ajustada*(numpy.sum(concatenado_x)/float(len(concatenado_x))))
    print "aca vamos"
    pass
    

def calcularvidautil():
  #inicio de datos para vida util
  index_de_lotes = lista_lotes.curselection()
  lotes = filtrarestudio()
  #llamado del estudi
  print listado_estudios.get()
  estudio_a_evaluar = listado_estudios.get()
  ancova_x = []  
  ancova_y = []
  for i in index_de_lotes:
    #lote
    print lotes[i]
    cnx = mysql.connector.connect(user='admin',
                                password='adminstabpy',
                                database='stabpy')
    apuntador =cnx.cursor()
  
  
    sentencia = ("SELECT data FROM stabpy where idsteudio='"
              + estudio_a_evaluar
              +"' and lote='"
              +lotes[i]
              +"';"
              )
    
    apuntador.execute(sentencia)
    eje_x = []
    eje_y = []
    
    for data in apuntador:
      datos_pre_regresion = eval(data[0])
      llaves = datos_pre_regresion.keys()
      llaves.sort()
      incremento_tiempos = 0
      for item in llaves:
        if item == "tiempos":
          print "\n"
        else:
          eje_y = eje_y + datos_pre_regresion[item]
          for i in range(len(datos_pre_regresion[item])):
            eje_x.append(datos_pre_regresion["tiempos"][incremento_tiempos])
          incremento_tiempos += 1
      reg = regresion(eje_x,eje_y)
      reg.ejecutarregresion()
      reg.tiempodevida()
      ancova_x.append(eje_x)
      ancova_y.append(eje_y)    
    apuntador.close()
    cnx.close()
  print "aca se inicia la ancova"
  ancov = ancova(ancova_x,ancova_y)
  ancov.ancovacal()
  pass
#cuerpo del reporte
reporte = ttk.Frame(cuaderno)
estudio_label = Label(reporte,text="identificador del estudio")
estudio_label.grid(row=0,column=0)
listado_estudios = StringVar()
lista_estudios = ttk.Combobox(reporte,textvariable=listado_estudios)
lista_estudios['values'] = consultar()
lista_estudios.grid(row=0,column=1)
boton_filtrar_estudios = Button(reporte,text="Filtrar",
                                command=filtrarestudio)
boton_filtrar_estudios.grid(row=0,column=3)
label_de_lotes = Label(reporte,text='Lotes')
label_de_lotes.grid(row=1,column=0)
lista_lotes = Listbox(reporte,selectmode=MULTIPLE)
lista_lotes.grid(row=1,column=1)
boton_calcular_vida_util = Button(reporte,text="evaluar",
                                  command=calcularvidautil)
boton_calcular_vida_util.grid(row=1,column=3)



#cierre cuaderno el mainloop

cuaderno.add(nuevo_estudio,text='nuevo estudio')
cuaderno.add(continuar_estudio,text='continuar estudio')
cuaderno.add(reporte,text="reporte")
stabpy.geometry('800x600')
stabpy.mainloop()
