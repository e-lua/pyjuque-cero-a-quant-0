import pandas_ta as ta 
import pandas as pd 
from pyjuque.Strategies import StrategyTemplate

class BBStrategy(StrategyTemplate):
	def __init__(self, bb_len = 20, n_std = 2.0, rsi_len = 14, rsi_overbought = 60, rsi_oversold = 40):
    	#Periodo las BB
		self.bb_len = bb_len
        #Desviacion estandar de las BB
		self.n_std = n_std
        #Periodo del RSI
		self.rsi_len = rsi_len
        #Limite de sobrecomrpa
		self.rsi_overbought = rsi_overbought
        #Limite de sobreventa
		self.rsi_oversold = rsi_oversold


	def setUp(self, df):
		bb = ta.bbands(
			close = df['close'],
			length = self.bb_len,
			std = self.n_std
			)
		#Guardamos la primera linea de la banda bolinger en el dataframe
        #[:,0]->Primera columna
		df['lbb'] = bb.iloc[:,0]
		#Guardamos la segunda linea de la banda bolinger en el dataframe
        #[:,1]->Segunda columna
		df['mbb'] = bb.iloc[:,1]
		#Guardamos la tercera linea de la banda bolinger en el dataframe
        #[:,2]->Tercera columna
		df['ubb'] = bb.iloc[:,2]

		#Agregamos el RSI al dataframe
		df['rsi'] = ta.rsi(close = df['close'], length = self.rsi_len)

		#Para no perder los datos pasaremos el valor del dataframe a una variable de la clase
		self.dataframe = df

	#Verificar si hay a largo -> Compra
	def checkLongSignal(self, i = None):
		df = self.dataframe

		if i == None:
			i = len(df)

		#Pasamos a revisar los niveles del RSI: menor al nivel de sobrecompra y mayor al nivel de sobreventa && 
		#El minimo de la vela anterior sea menor que la banda inferior de la BB
		if (df['rsi'].iloc[i] < self.rsi_overbought) and \
			(df['rsi'].iloc[i] > self.rsi_oversold) and \
			(df['low'].iloc[i-1] < df['lbb'].iloc[i-1]) and \
			(df['low'].iloc[i] > df['lbb'].iloc[i]) :

			return True
		else:
			return False

	#Verificar si hay una entrada en corto -> Venta
	#Si operamos en SPOT y no en FUTUROS, comentamos las lineas de abajo y retornamos Falso, ya que el stop_loss o take_profit 
	# nos sacará del mercado
	def checkShortSignal(self, i = None):
		#df = self.dataframe

		#if i == None:
		#	i = len(df)

		#Pasamos a revisar los niveles del RSI: menor al nivel de sobrecompra y mayor al nivel de sobreventa &&
		#El maximo de la vela anterior sea mayor que la banda superior de la BB
		#if (df['rsi'].iloc[i] < self.rsi_overbought) and \
		#	(df['rsi'].iloc[i] > self.rsi_oversold) and \
		#	(df['high'].iloc[i-1] > df['ubb'].iloc[i-1]) and \
		#	(df['high'].iloc[i] < df['ubb'].iloc[i]):

		#	return True
		return False
















