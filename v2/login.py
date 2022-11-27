# -*- coding: utf 8 -*
from Tkinter import *
import sys
import mysql.connector
from mysql.connector import errorcode
class Dialog(Toplevel):
  def __init__(self, parent, title = "Login"):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)

        self.parent = parent
        self.result = None
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        '''
        #self.buttonbox()
        if not self.initial_focus:
            self.initial_focus = self
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        
        self.geometry("500x500")
        self.initial_focus.focus_set()
        '''
        self.wait_window(self)
  def body(self, master):
        self.saludo = Label(master,text="Usuario").grid(row=0,column=0)
        self.saludo = Label(master,text="contraseña").grid(row=1,column=0)
        self.usr = StringVar()
        self.usr.set('admin')
        self.e1 = Entry(master,textvariable=self.usr).grid(row=0, column=1)
        self.clave = StringVar()
        self.clave.set('adminstabpy')
        print "aca definimos el ususario"
        self.e2 = Entry(master,
                        textvariable=self.clave,
                        show='*').grid(row=1, column=1)

        self.conectar = Button(master, text="Conectar",
                               command=self.apply).grid(row=2,
                                                        column=0
                                                        )   
        self.salir = Button(master, text="Cancelar",command=self.cancel).grid(
                                                                row=2,
                                                                column=1
                                                                )       
        pass
  def apply(self):
        nombre = self.usr.get()
        contra = self.clave.get()
        print nombre , contra  # or something
        try:
            cnx = mysql.connector.connect(user=nombre,
                                          password=contra,
                                          database='stabpy',
                                          host='localhost')
            print "conexción exitosa"
            self.parent.focus_set()
            self.destroy()
        except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("error de ususario o contraseña")
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
          else:
            print(err)
        else:
          cnx.close()
        self.acceso = nombre, contra
  def cancel(self):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
        sys.exit()
