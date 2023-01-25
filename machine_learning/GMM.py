import ccxt
import pandas as pd 
import pandas_ta as ta 
from sklearn import mixture as mix 
import seaborn as sns
import matplotlib.pyplot as plt
from utils import ccxt_ohlcv_to_dataframe



exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '5m'
limit = 1000
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit)
df = ccxt_ohlcv_to_dataframe(ohlcv)


model = mix.GaussianMixture(
	#Cantidad de clases o clúster ALCISTA,LATERAL,BAJISTA
	n_components = 3,
	#Dependiendo de la covariance escogida se puede cambiar el resultado 
	covariance_type = 'spherical',
	#Numero de inicializaciones para el entrenamiento del modelo. Se crearan 50 instancias y se tomará la mejor
	n_init = 50,
	#random_state para que no se cambie el resultado
	random_state = 42,
	)

#Indicadores para separar el mercado
df['market_return'] = df['close']/df['close'].shift(1)
df['rsi'] = ta.rsi(close = df['close'], length = 14)
#roc(rate of change)
df['roc'] = ta.roc(close = df['close'], length = 14)
#Eliminamos los datos vacios
df.dropna(inplace = True)

features = df[['rsi', 'roc', 'market_return']]

#Pasamos a entrenar el modelo
model.fit(features)

#Vamos a entrenar nuestro modelo, y lo guardamos en el df
df['regime'] = model.predict(features)

#Vamos a ver los numeros que se tienen para su grafica
order = set(df['regime'])

#Pasamos a graficar
fig = sns.FacetGrid(data = df, hue = 'regime', hue_order = order, aspect = 2, height = 3)
#Creamos una grafica scatter
fig.map(plt.scatter, 'date', 'close', s =4).add_legend()

plt.title('Regimes')
plt.xlabel('Datetime')
plt.ylabel('close')
plt.show()



#-------------GUARDADO DEL MODELO

import pickle

#Guardado del modelo
filename='Gmodel.sav'
pickle.dump(model,open(filename,'wb'))

#Carga del modelo
model=pickle.load(open(filename,'rb'))
labels=model.predict(features)
print(labels)




