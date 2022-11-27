import numpy
from scipy import stats
import math
class regresion:
  def __init__(self,x,y):
    self.x = x
    self.y = y
  def regresion(self):
    SCxx = numpy.sum([(self.x[i] - numpy.mean(self.x))**2 for i in range(len(self.x))])
    SCxy = numpy.sum([ ((self.y[i] - numpy.mean(self.y))*(self.x[i] - numpy.mean(self.x ))) for i in range(len(self.y))])
    rate = SCxy/SCxx
    intercept = numpy.mean(self.y) -(rate*numpy.mean(self.x))
    return intercept,rate
  def anovar(self,blist):
    b_0 = blist[0]
    b_1 = blist[1]
    dispersion_experimental = [self.y[i] - numpy.mean(self.y) for i in range(len(self.y)) ]
    dispersion_predicha = [((self.x[i]*b_1)+b_0) - numpy.mean(self.y) for i in range(len(self.y))]
    df_total = len(self.y)-1
    df_regresion = 2-1
    df_residuos = df_total - df_regresion
    SCt = numpy.sum([dispersion_experimental[i]**2 for i in range(len(self.y)) ] )
    SCreg = numpy.sum([dispersion_predicha[i]**2 for i in range(len(self.y))])
    SCres = SCt - SCreg
    CMreg = SCreg/df_regresion
    CMres = SCres/df_residuos
    F = CMreg/CMres
    F_crit = stats.f.ppf(1-0.05,df_regresion,df_residuos)
    conlusion = None
    if F>F_crit:
      conclusion = 1
    elif F<=F_crit:
      conclusion = 0
    return conclusion,df_regresion,SCreg,CMreg,F,F_crit,df_residuos,SCres,CMres,df_total,SCt
  def decaimiento(self,vectorx,blist,CMres,df_res,limiteinferior):
    S_e = math.sqrt(CMres)
    vectorypromedio = [((vectorx[i]*blist[1])+blist[0]) for i in range(len(vectorx))]
    t_alfa = stats.t.ppf(0.95,df_res)
    n = float(df_res)+2
    #raiz = math.sqrt(((n+1)/n)+((pow(vectorx[0]-numpy.mean(self.x),2)/(numpy.sum([(self.x[i] - numpy.mean(self.x))**2 for i in range(len(self.x))])))))
    vector_li = [(vectorypromedio[i]-(S_e*t_alfa*(math.sqrt(((n+1)/n)+((pow(vectorx[i]-numpy.mean(self.x),2)/(numpy.sum([(self.x[i] - numpy.mean(self.x))**2 for i in range(len(self.x))]))))))))for i in range(len(vectorx))]
    timepodevida = None
    for i in range(len(vector_li)):
      objeto = vector_li[i]
      if objeto <= limiteinferior:
        tiempodevida = vectorx[i]
        break
      else:
        tiempodevida = 0
        continue
            
    return vectorypromedio,vector_li,tiempodevida
