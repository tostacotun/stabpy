#!/usr/bin/python
#librerias
import numpy
import os
import sys
import csv
#objetos
from anova import anova
from DMS import dms
from regresion import regresion
#grafico
import matplotlib.pyplot as plt
#requeridoporpyinstaller en linux
import FileDialog
#iniciamos el garbache colllector 
import gc
gc.enable()
#area para crear el manejo de directorios
#ubicamos el sistema operativo
sistema_operativo = os.name
if sistema_operativo == "posix":
  directorio = os.environ['HOME']
  if os.access(directorio + "/stabpy", os.F_OK) == False:
    os.mkdir(directorio + "/stabpy")
    directorio = directorio + "/stabpy"
    os.mkdir(directorio + "/datos")
    os.mkdir(directorio + "/reportes")
    directorio_datos = directorio + "/datos/"
    directorio_reportes = directorio + "/reportes/"
  if os.access(directorio + "/stabpy", os.F_OK) == True:
    directorio_datos = directorio + "/stabpy" + "/datos/"
    directorio_reportes = directorio + "/stabpy" + "/reportes/"
if sistema_operativo == "nt":
  directorio = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
  if os.access(directorio + "\stabpy", os.F_OK) == False:
    os.mkdir(directorio + "\stabpy")
    directorio = directorio + "\stabpy"
    os.mkdir(directorio + "\datos")
    os.mkdir(directorio + r"\reportes")
    directorio_datos = directorio + r'\datos' + '\\'
    directorio_reportes = directorio + r'\reportes' + '\\'
  if os.access(directorio + "\stabpy", os.F_OK) == True:
    directorio_datos = directorio + "\stabpy" + r'\datos' + '\\'
    directorio_reportes = directorio + "\stabpy" + r'\reportes' + '\\'

#intro
hola_mundo = "Hola, este programa predente ayudar en estabilidad, primero\nharemos una anova usando librerias open source en python de scipy y numpy la \nidea es evaluar su funcionalidad en linux y windows al tiempo\n inicialmente, el codigo esta escrito con ASCII crudo, no contamos con caracteres ee idiomal espanol\n es decir hay muchos errores ortograficos"
print(hola_mundo)
#preguntar si existen los datos
origen_datos = 0
#
while origen_datos != 1 and origen_datos != 2:
  print "Selecciona una de las siguientes opciones"
  print "1 ==> datos ya creados, datos en formato CSV"
  print("2 ==> datos nuevos, se ingresan datos desde cero,"
          " y se crea el archivo CSV")
  try:
    origen_datos = int(input("digita el numero de la opcion: "))
  except:
    print "\n\nERROR:debe digitarse un numero de las opciones listadas\n\n"
if origen_datos == 2:
  print "crearemos la serie de datos"
  #iniciacion de variables para los datos
  pregunta_tiempos = "cuantos tiempos vamos a comparar?\n"
  tiempos = int(input(pregunta_tiempos))
  #muestras por cada tiempo
  muestras = int(input("cuantas replicas se realizaron por cada tiempo?\n"))
  datos = [[j*2 for j in range(muestras)] for i in range(tiempos)]
  titulos = [0 for i in range(tiempos)]
  tiempos_x = [0 for i in range(tiempos)]
  #valores de tiempos
  for i in range(tiempos):
    tiempos_x[i] = float(input("el tiempo {} corresponde al mes? ".format(i+1)))
    titulos[i] = str("mes {}".format(tiempos_x[i]))
  #variables para cada tiempo es decir datos
  for i in range(tiempos):
    for j in range(muestras):
        datos[i][j] = float(input("ingresa el valor de la muestra {} del tiempo {}:\t".format(j+1,i+1)))
  #datos creados  
  print( "lo datos crearon fueron, no es un bug, el desarrollador "
         "de este software es un fanatico de star wars\n"
         "fin de la creacion de datos"
         "los datos se guardaran en un archivo CSV, para usos futuros "
         "Es recomendable que el nombre sea el lote de la molecula "
         "pues este mismo archivo puede ser usado en estudios con "
         "lotes combinados\n")
  
  nombre_archivo_datos = raw_input("el nombre del archivo es?: ")
  archivo_de_datos = open(directorio_datos + nombre_archivo_datos + ".csv","wb")
  escritor = csv.writer(archivo_de_datos,delimiter=',')
  escritor.writerow(tiempos_x)
  escritor.writerows(datos)
  archivo_de_datos.close()
elif origen_datos == 1:
  print "los datos deben estar en un archivo de datos separados por comas"
  archivoabierto = 0
  while archivoabierto<1:
    try:
      nombre_archivo_datos = raw_input("el nombre del archivo es?: ")
      archivo_de_datos = open(directorio_datos + nombre_archivo_datos + ".csv","r")
    except :
      print "error en nombre del archivo"
    else:
      archivoabierto = 1
      break  
  lista_archivo_datos = archivo_de_datos.readlines()
  archivo_de_datos.close()
  #definimos numero de tiempos y muestras por tiempo
  tiempos = len(lista_archivo_datos[0].split(","))
  muestras = len(lista_archivo_datos[1].split(","))
  #se crea el vector de los tiempos
  tiempos_x_linea = lista_archivo_datos[0].strip()
  tiempos_x = numpy.asfarray(tiempos_x_linea.split(","))
  titulos = [0 for i in range(tiempos)]
  for i in range(tiempos):
    titulos[i] = str("mes {}".format(tiempos_x[i]))
  #crearemos la matriz de los datos
  datos = [[j*2 for j in range(muestras)] for i in range(tiempos)]
  for i in range(tiempos):
    lista_de_cambio = lista_archivo_datos[i+1].strip()
    datos[i] = numpy.asfarray(lista_de_cambio.split(","))
  #archivo leido y trnasformado
else:
  print "ERROR EN DATOS"
  sys.exit("lo sentimos")
# 
print "evaluando homocedasticidad"
#
diferencia_medianas = [[0 for i in range(muestras)] for i in range(tiempos)]
for i in range(tiempos):
    for j in range(muestras):
        diferencia_medianas[i][j] = abs(datos[i][j] - numpy.median(datos[i]))
levine = anova(diferencia_medianas)
levine_ouput = levine.anova()
conclusion_levine = "error de levine"
if levine_ouput[0] == 1:
    conclusion_levine = "De acuerdo a la prueba de Levine, especificamente la prueba de Brown Forsythe las serie es homocedastica"
        
elif levine_output[0] == 0:
    print "la serie no es homocedastica"
    sys.exit("una serie heterocidastica no permite usar este analisis")
else:
    print levine_output[0]

print "Ejecutando ANOVA sobre los datos"

analisis = anova(datos)
analisis_output = analisis.anova()
conclusion_anova = "error en anova"
conclusion_dms = "no se requiere analisis de diferencia minima significativa"
if analisis_output[0] == 1:
    conclusion_anova = "no hay diferencia estadistica en los tiempos"
elif analisis_output[0] == 0:
    conclusion_anova = "hay diferencia significativa en almenos 1 tiempo"
    E_residual = analisis_output[8]
    #la dms solo se calcula si se rechaza la hipitesis nula
    analisis_dms = dms(datos,E_residual,tiempos_x)
    conclusion_dms = analisis_dms.dms()
else:
    print analisis_output[0]
    sys.exit("lo sentimos error de anova")
#
#en esta parte hacemos la regresion
#
promedios = [0 for i in range(tiempos)]
for i in range(tiempos):
  promedios[i] = numpy.mean(datos[i])
#creacion de eje x para calculode regresion
eje_x = []
contador_1 = 0
contador_2 = 0
while contador_1<tiempos*muestras:
  lista_muestras = [tiempos_x[contador_2] for i in range(muestras)]
  contador_2 += 1
  contador_3 = contador_1 + muestras-1
  eje_x[contador_1:contador_3] = lista_muestras
  contador_1 += muestras
#creacion del eje y
eje_y= []
for i in range(tiempos):
  for j in range(muestras):
    eje_y.append(datos[i][j])
#hacemos los ejes parte de la regresion

recta = regresion(eje_x,eje_y)
coeficientes_regresion = recta.regresion()
analisis_anovar = recta.anovar(coeficientes_regresion)
#generamos la conclusion del anovar
conclusion_anovar = "hay un error en la conclusion de la anovar"
print "Realizando la regresion"
if analisis_anovar[0] == 1:
    conclusion_anovar = "La varianza de la regresion es explicada por el modelo"
elif analisis_anovar[0] == 0:
    conclusion_anovar = "la varianza no es explicada por el modelo lineal"
else:
    print conclusion_anovar[0]
    sys.exit("lo sentimos error de anovar")

#tamano de los ejes
limiteinferior = float(input("inserta el valor del limite inferior de la concentracion: "))
maxeje_x = 500
mineje_x = min(eje_x)-0.5
maxeje_y = max(eje_y)+2
mineje_y = limiteinferior-5
#vector de degradacion
print "calculando vida util"
#print "aca cambiamos el vector para hacer preubas mas rapido"
x_decaimiento = numpy.arange(mineje_x,maxeje_x,0.1)
y_decaimiento = recta.decaimiento(x_decaimiento,coeficientes_regresion,analisis_anovar[8],analisis_anovar[6],limiteinferior)
maxeje_x = y_decaimiento[2]+1

#generamos el grafico que va al reporte

plt.plot(eje_x,eje_y,"o",x_decaimiento,y_decaimiento[0],x_decaimiento,y_decaimiento[1],"--",[mineje_x, maxeje_x], [limiteinferior, limiteinferior], 'k-', lw=2)
plt.ylabel('% de cantidad declarada')
plt.xlabel("mes")
plt.axis([mineje_x,maxeje_x,mineje_y,maxeje_y])
plt.savefig(directorio_datos + "logo.png")

#
final =  "la vida util es {} meses y se puede aproximar razonablemente a que el farmaco expira en {} meses".format(y_decaimiento[2],y_decaimiento[2]//1)
#
#vamos a generar el reporte
#
#librerias para el reporte
#from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
import datetime
from reportlab.lib.enums import TA_JUSTIFY
#es el estilo que justificara el texto cuando corresponda
from reportlab.lib.pagesizes import letter
#simpledoctemplate es el tipo de plantilla
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
#colocamos header y footer
#esta seccion es una clase para el creador del reporte traida de
from reportlab.pdfgen import canvas
"""
http://code.activestate.com/recipes/576832/
"""
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        self.drawRightString(8*inch, 10.5*inch,
            "Pag %d de %d" % (self._pageNumber, page_count))
#           
#          
def footer(canvas, reporte):
    canvas.saveState()
    canvas.setFont('Helvetica',9)
    #header
    canvas.line(0.7874015*inch,10.2*inch,7.71259*inch,10.2*inch)
    #footer
    canvas.line(0.7874015*inch,0.77*inch,7.71259*inch,0.77*inch)
    canvas.drawString(inch, 0.54 * inch,
                    "Stabpy fue desarrollado por William David Suarez Arevalo")
    canvas.drawString(inch, 0.40 * inch,
                     "Esta licenciado bajo CC-BY-NC-ND 4.0")    
    canvas.drawInlineImage("cc.png", 6.7*inch,0.35*inch, width=None,height=None)
    
    
    canvas.restoreState()
#se genera el reporte
reporte_pdf = nombre_archivo_datos
print "el reporte sera un pdf llamado:\n",reporte_pdf
print "que estara ubicado en el directorio:\n",directorio_reportes
reporte = SimpleDocTemplate(directorio_reportes + reporte_pdf + ".pdf",
                            pagesize=letter,rightMargin=0.7874015*inch,
                            leftMargin=0.7874015*inch,
                            topMargin=0.7874015*inch,
                            bottomMargin=0.7874015*inch)
#el contenido del reporte es construido de una lista llamada Story
Story=[]
#generamos una variable a la cual le asignamos la instancia de estilos
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
#a una variable le asignamos la lineaque queremos incluir al estilo HTML
#titulo
header = datetime.datetime.now()
fecha = "Reporte de analisis estadistico de datos para estabilidad on-going"
ptext = '<font size=12>%s</font>' % header
#fecha
now = datetime.datetime.now()
fecha = now.strftime("%Y-%m-%d %H:%M")
ptext = '<font size=12>Reporte generado en: %s</font>' % fecha
#agregamos al final de la lista nuestra variable con el formato que se condiciono
Story.append(Paragraph(ptext, styles["Normal"]))
#ya pusimos la fecha ahora el analista
full_name = raw_input("Digita el nombre del analista: ")
ptext = '<font size=12>Analista: %s</font>' % full_name
Story.append(Paragraph(ptext, styles["Normal"])) 
#Molecula
compound_name = raw_input("Digita el nombre de compuesto: ")
ptext = '<font size=12>Molecula: %s</font>' % compound_name
Story.append(Paragraph(ptext, styles["Normal"]))
#lote
batch_code = raw_input("Digita el lote del producto: ")
ptext = '<font size=12>Lote: %s</font>' % batch_code
Story.append(Paragraph(ptext, styles["Normal"]))  
#DATOS
Story.append(Spacer(1, 12))
ptext = '<font size=12>DATOS</font>' 
Story.append(Paragraph(ptext, styles["Normal"]))
#agregar espacio
Story.append(Spacer(1, 12))
#agregaremos datos de una lista
#priemro los titulos de la lista
data = [[str(i) for i in titulos]]
#se genera la lista de datos, se debe trasponer para que queden en colunas
lineas = [[j*2 for j in range(tiempos)] for i in range(muestras)]
for i in range(muestras):
  for j in range(tiempos):
    lineas[i][j] = "{}".format(datos[j][i])
#unimos las dos listas para generar una sola tabla
for i in range(muestras):
  data.append(lineas[i])
t=Table(data)
Story.append(t)
Story.append(Spacer(1, 12))
#Conclusion por levine
ptext = '<font size=12>%s</font>' % conclusion_levine
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
#resultados anova
ptext = '<font size=12>ANOVA</font>' 
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
data= [["Fuente de\nvarianza","df","SC","CM","F cal","F cri"],
       ["Entre tiempos",str(analisis_output[1]),str(analisis_output[2]),
         str(analisis_output[3]),str(analisis_output[4]),
         str(analisis_output[5])],["Intra tiempos",str(analisis_output[6]),
         str(analisis_output[7]),str(analisis_output[8])],["Total",
         str((tiempos*muestras)-1),str(analisis_output[9])]]
t=Table(data)
Story.append(t)
Story.append(Spacer(1, 12))

ptext = '<font size=12>%s</font>' % conclusion_anova
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))

#diferencia minima significativa
for i in range(len(conclusion_dms)):  
  if len(conclusion_dms)==58:
    ptext = '<font size=12>%s</font>' % conclusion_dms
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    break
  else:
    ptext = '<font size=12>%s</font>' % conclusion_dms[i]
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    continue
#incluimos en el reporte el resultado del anovar
ptext = '<font size=12>ANOVAR</font>' 
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
#
ptext = '<font size=12>%s</font>' % conclusion_anovar
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
#tabla del anovar
data= [["Fuente de\nvarianza","df","SC","CM","F cal","F cri"],
       ["Regresion",str(analisis_anovar[1]),str(analisis_anovar[2]),
         str(analisis_anovar[3]),str(analisis_anovar[4]),
         str(analisis_anovar[5])],["Residuos",str(analisis_anovar[6]),
         str(analisis_anovar[7]),str(analisis_anovar[8])],["Total",
         str(analisis_anovar[9]),str(analisis_anovar[10])]]
t=Table(data)
Story.append(t)
#se agrega una imagen llamada logo.png
grafico = "En el grafico se observa el resultado de la regresion, en puntos, el resultado experimental, la linea continua es la prediccion y la linea cortada, es el limite de confianza inferior de la regresion, donde pasa por el limite inferior, se dice que el 10 % de la poblacion"
ptext = '<font size=12>%s</font>' % grafico
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
logo = directorio_datos + "logo.png"
im = Image(logo, 6*inch, 4*inch)
Story.append(im)

ptext = '<font size=12>%s</font>' % final
Story.append(Paragraph(ptext, styles["Normal"]))
Story.append(Spacer(1, 12))
#orden de compilancion de reporte
reporte.build(Story,onFirstPage=footer,onLaterPages=footer,canvasmaker=NumberedCanvas)
#linea de terminacion

raw_input("Presiona enter para terminar")
   
    
  

