# -*- coding: utf 8 -*
from Tkinter import *
import json
from collections import OrderedDict
import tkMessageBox
class ingreso_datos(Toplevel):
  def __init__(self,parent,x,y,z):
    Toplevel.__init__(self,parent)
    self.ancho = x
    self.altura = y + 1
    self.replicas_iguales = z
    self.title('Ingreso de datos para el lote')
    self.parent = parent
    body = Frame(self) 
    self.initial_focus = self.body(body)
    body.pack()
    self.grab_set()
    self.wait_window(self)
  def body(self,master):
    #self.saludo = Label(master,text="Usuario").grid(row=0,column=0)
    tiempo = self.ancho 
    replica = self.altura
    #
    cadena = None
    for i in range(tiempo+1):
      if i==0:
        cadena = '{"tiempos":[]'
      else:
        cadena += ',"tiempo_{}":[]'.format(i)
    cadena2 = cadena + '}' 
    self.data= json.loads(cadena2,object_pairs_hook=OrderedDict)
    contador = 1
    for item in self.data.keys():
      if item == "tiempos":
        self.data[item]=[DoubleVar() for i in range(tiempo)]
        self.l = Label(master,text="valor numerico de los tiempos"
                      ).grid(row=0,column=0)
        for i in range(len(self.data[item])):
          self.b = Entry(master, 
                         textvariable=self.data[item][i],
                         width=6,
                        )
          self.b.grid(row=0, column=i+1)  
      else:
        self.data[item]=[DoubleVar() for i in range(replica)]
        for i in range(replica-1):
          self.l = Label(master,text=("valor de la replica {}".format(i+1))
                      ).grid(row=i+1,column=0)
          #print "aca estamos con el item ", item, " en la columna ", contador
          self.b = Entry(master,
                         text=None,
                         textvariable=self.data[item][i],
                         width=6,
                        ).grid(row=i+1,column=contador)
        contador += 1
    self.guardar = Button(master, 
                          text="Ingresar",
                          command=self.guardar,
                         )
    self.guardar.grid(row=replica+1,columnspan=tiempo,sticky=E)
    #self.nota = Label(master)
  def guardar(self):
    cadena = None
    for i in range(self.ancho+1):
      if i==0:
        cadena = '{"tiempos":[]'
      else:
        cadena += ',"tiempo_{}":[]'.format(i)
    cadena2 = cadena + '}' 
    self.data_resultado = json.loads(cadena2,object_pairs_hook=OrderedDict)
    for item in self.data.keys():
      if item == "tiempos":
        for i in range(len(self.data[item])):
          self.data_resultado['tiempos'].append(self.data['tiempos'][i].get())
      else:
        if self.replicas_iguales == True:
          for i in range(len(self.data[item])-1):
            self.data_resultado[item].append(self.data[item][i].get())
        elif self.replicas_iguales == False:
          lista = range(len(self.data[item])-1)
          for i in lista:
              pregunta = ("¿quieres guardar el valor "
                         + str(self.data[item][i].get())
                         +" indicado en la replica " 
                         +str(i+1)
                         +"?"
                          )
              if tkMessageBox.askokcancel(
                      "En los datos del "+item,
                       pregunta):
                self.data_resultado[item].append(self.data[item][i].get())
              else:
                break
    self.parent.focus_set()
    self.destroy()
    print "fin de la funcion guardar"
