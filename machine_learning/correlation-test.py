import ccxt
import pandas as pd
import numpy as np
import ccxt
from utils import ccxt_ohlcv_to_dataframe
import matplotlib.pyplot as plt
import seaborn as sns


exchange = ccxt.binance()
timeframe = '1d'
limit = 1000

symbol1 = 'BTC/USDT'
symbol2 = 'ETH/USDT'

btc = exchange.fetch_ohlcv(symbol1, timeframe, limit)
eth = exchange.fetch_ohlcv(symbol2, timeframe, limit)

btc = ccxt_ohlcv_to_dataframe(btc)
eth = ccxt_ohlcv_to_dataframe(eth)

#====CALCULAREMOS EL MARKET RETURN====

#Dividimos el precio del cierre actual / el del día anterior
y = btc['close']/btc['close'].shift(1)
x = eth['close']/eth['close'].shift(1)

#El primer elemento estará vacio ya que no hay nada al dia anterior del inicio, por lo que eliminaremos el primer dato nulo y vacio
y.dropna(inplace = True)
x.dropna(inplace = True)

#====================================


#Verificaremos la gráfica para ver la distribución

#sns.displot(x = y, color='#F2AB6D', bins=50, kde=True)
#plt.title('BITCOIN')
#sns.displot(x = x, color='#F2AB6D', bins=50, kde=True)
#plt.title('ETHEREUM')
#plt.show()


#====HAREMOS UNA REGRESIÓN LINEAL====
#Revisamores que tan bien se acomoda la gráfica
#deg = 1 es 1° grado, es decir, una recta
constants = np.polyfit(x = x, y = y, deg = 1)

f = np.poly1d(constants)

#Calculamos el Rcudrado, es decir, que tan bien se ajustan las observaciones a la regresión
# Hay una diferencia entre CORRELACIÓN y PENDIENTE DE LA RECTA
# Con la PENDIENTE DE LA RECTA podemos concluir como por cada cierto dinero de BTC se mueve cierta cantidad de ETH 
# Con la CORRELACIÓN verificamos si se mueve excatamente igual, es decir, si se obtiene un Rcuadrado > 0.90
yh = f(x)
yb = sum(y)/len(y)
sst = sum((y - yb)**2)
ssreg = sum((yh - yb) ** 2)
R2 = ssreg/sst

#Generamos la gráfica
#x.values es el retorno de ETH evaluados en f(x) , y "label" es una etiqueta
plt.plot(x.values, f(x), color = 'black', label = f)
#Nos grafica un scatterplot de los puntos
sns.scatterplot(x  = x, y = y)
plt.text(min(x), min(y), 'R2: ' + str(round(R2, 2)))
plt.title('BTC / ETH | Market Returns Correlation')
plt.xlabel('ETH market return')
plt.ylabel('BTC market return')


#Veremos quer tanto correlación tienen si sus datos se acercan al centro de la linea
plt.show()
