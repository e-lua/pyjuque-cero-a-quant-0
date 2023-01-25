import ccxt
from utils import ccxt_ohlcv_to_dataframe

from sklearn.cluster import KMeans

import plotly.graph_objects as go 
from plotly.subplots import make_subplots

exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '15m'
#Limite de 1000 velas
limit = 1000
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit)
df = ccxt_ohlcv_to_dataframe(ohlcv)

#Buscamos clasificar las velas, y trabajaremos a nivel de proporciones
def get_features(df):

	df["H/O"] = df["high"]/df["open"]
	df["L/O"] = df["low"]/df["open"]
	df["C/O"] = df["close"]/df["open"]

	return df[["H/O", "L/O", "C/O"]]

features = get_features(df)

#Definimos K
k = 6

#Definimos nuestro modelo
#random_state es para obtener el mismo resultado
model = KMeans(n_clusters = k, random_state = 42)
#Pasamos a entrenar el modelo con los Centroides para ajustar los datos de Features
model.fit(features)

#Creamos una nueva columna en el dataframe, una vez el modelo esté entrenado accedemos a las etiquetas
df['cluster'] = model.labels_

#Esto permitirá predecir, pero en este caos como tendremos pocas velas no será necesario
# model.predict(new_features)

#Ordenare respecto al cluster
#inplace es para reemplazar
df.sort_values(by = 'cluster', inplace = True)
#Reiniciamos el indice
df.reset_index(inplace = True)
#Creamos una nueva columna para guardar los indices
df['clust_index'] = df.index
#Detectar el cambio ente un clúster y otro
df["clust_change"] = df["cluster"].diff()
#Agrupamos los indices diferentes de 0 (pude clocarse ==1), es decir donde hay una linea vertical
change_indices = df[df["clust_change"] != 0]

#Graficaremos
fig = make_subplots(
	rows = 1, cols = 1,
	)

#Agremos un trazo
fig.add_trace(
	go.Candlestick(
		x = df['clust_index'],
		open = df['open'],
		close = df['close'],
		high = df['high'],
		low = df['low'],
		)
	)

#Iteramos las filas
for row in change_indices.iterrows():
	fig.add_shape(
		type = 'line',
		yref = 'y',
		xref = 'x',
		#Para una linea vertical y darle una dimensión
		x0 = row[1]['clust_index'],
		y0 = df['low'].min(),
		x1 = row[1]['clust_index'],
		y1 = df['high'].max(),
		line = dict(color = 'black', width = 3)
	)


fig.update_layout(xaxis_rangeslider_visible = False, showlegend = False)
fig.show()