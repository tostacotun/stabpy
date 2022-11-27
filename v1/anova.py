import numpy
from scipy import stats
class anova:
    def __init__(self,matriz):
        self.x = matriz
        self.columnas = len(matriz)
        self.filas = len(matriz[0])
        pass

    def anova(self):
        F_critico = stats.f.ppf(1-0.05,self.columnas-1,((self.filas*self.columnas)-(self.columnas)))
        df_medias = self.columnas-1
        df_residual = (self.filas*self.columnas)-(self.columnas)
        FC = numpy.sum(self.x)**2 / (self.filas*self.columnas)
        SC_grupos = 0
        for i in range(self.columnas):
            SC_grupos = SC_grupos + numpy.sum(self.x[i])**2 / self.filas
        SCM = SC_grupos - FC
        SC_totales = 0
        for i in range(self.columnas):
            for j in range(self.filas):
                SC_totales += self.x[i][j]**2
        SCT = SC_totales - FC
      
        
        CM_medias = SCM/df_medias
        CM_residual = (SCT-SCM)/df_residual
        F_exp = CM_medias / CM_residual
        output ="no hay resultado"  
        if F_exp <= F_critico:
            output = 1
        else:
            output = 0
        retorno = [output,df_medias,SCM,CM_medias,F_exp,"{0:.2f}".format(F_critico),
                  df_residual,(SCT-SCM),CM_residual,SCT]
        return retorno
        
        
