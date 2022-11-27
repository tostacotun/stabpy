import numpy
import math
from scipy import stats
class dms:
    def __init__(self,matriz,error_residual,tiempos_x):
        self.x = matriz
        self.columnas = len(matriz)
        self.filas = len(matriz[0])
        self.E_r = error_residual
        self.tiempos = tiempos_x
        self.tiempos_rango = len(tiempos_x)
        pass
    def dms(self):
        t_critico = stats.t.ppf(1-(0.05/2),self.columnas*(self.filas-1))
        diferencia_minima = math.sqrt(2*self.E_r/self.filas)*t_critico
        promedios = [0 for i in range(self.columnas)]
        for i in range(self.columnas):
            promedios[i] = numpy.mean(self.x[i])
        diferencias_tiempos = [0 for i in range(self.columnas-1)]
       
        for i in range(self.columnas-1):
            diferencias_tiempos[i] = promedios[i]-promedios[i+1]
        retorno = ["diferencia minima significativa calculada con 95% de confianza"]
        cont = 0            
        while cont<len(diferencias_tiempos):
            if (diferencias_tiempos[cont]>diferencia_minima):
                a = "la concentracion del mes {} es estadisticamente superior al mes {}".format(self.tiempos[cont],self.tiempos[cont+1])
                retorno.append(a)                
            elif (diferencias_tiempos[cont]<=diferencia_minima and diferencias_tiempos[cont] >= (-1*diferencia_minima)):
                a = "la concentracion del mes {} no es estadisticamente diferenciable al mes {}".format(self.tiempos[cont],self.tiempos[cont+1])
                retorno.append(a)
            elif (diferencias_tiempos[cont]< (-1*diferencia_minima)):
                a = ":::ERROR::: ANALSIS NO ACEPTABLE la concentracion aumento del mes {} al mes {}".format(self.tiempos[cont],self.tiempos[cont+1])
                retorno.append(a)
                break
            cont += 1   
        return retorno
