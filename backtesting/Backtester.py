'''
El Backtester es una simulación del mercado	

-> Open Long/Short position
-> Close Position
-> Set Take Profit
-> Set Stop Loss

'''

import pandas as pd 
import numpy as np 

#Usaremos programación orientada a objetos para guardar el Backtesting por cada individuo
class Backtester():

	#initial_balance son USD
	#leverage es el APALANCAMIENTO
	def __init__(self, initial_balance = 400, leverage = 4, trailing_stop_loss = False):

		#Esta variable no se va a modificar
		self.initial_balance = initial_balance
		#Esta variable va a guardar el resultado de las operaciones
		self.balance = initial_balance
		#Cantidad guardada en la cartera: (1) Al momento de Vender -> amount x (precio de compra - precio actual) ... Entonces si estoy en 
			#Long, y la diferencia es negativa es porque perdí, y si es positiva, gané
		self.amount = 0
		#Cantidad de apalancamiento
		self.leverage = leverage
		#Costo por operación 0.02% por operación
		self.fee_cost = 0.02 / 100
		#Cuanto porcentaje de la cuenta vas a arriesgar por operación, en el ejemplo es 1% por operación
		self.inv = self.balance * 0.01 * self.leverage

		#La ganancia o perdida por oepración se guardará acá
		self.profit = []
		#Cuanto se peridó en total en el sistema de trading
		self.drawdown = []
		#Cantidad de operaciones ganadas
		self.winned = 0
		#Cantidad de operaciones perdidas
		self.lossed = 0
		#Cantidad de operaciones totales
		self.num_operations = 0
		#Cantidad de longs
		self.num_longs = 0
		#Cantidad de shorts
		self.num_shorts = 0

		#Verificamos si esta abierta la operación a largo
		self.is_long_open = False
		#Verificamos si esta abierta la operación a corto
		self.is_short_open = False

		self.trailing_stop_loss = trailing_stop_loss
		self.from_opened = 0

	#Reiniciamos todos los valores, es decir, luego de cada generación de individuos pasamos a reiniciar todo
	def reset_results(self):

		self.balance = self.initial_balance
		self.amount = 0
		self.profit = []
		self.drawdown = []
		self.winned = 0
		self.lossed = 0
		self.num_operations = 0
		self.num_longs = 0
		self.num_shorts = 0
		self.is_long_open = False
		self.is_short_open = False
		self.from_opened = 0
	
	#Abrimos una posición
	def open_position(self, price, side, from_opened = 0):

		#side -> es compra ó venta
		#from_opened-> Si utilizamos un trading StopLoss ocupamos esta variable, y es Falso le colocamos 0 y luego ya lo cambiaremos

		self.num_operations += 1

		if side == 'long':
			self.num_longs += 1

			#Ahora verificamores si tenemos operaciones abiertas
			if self.is_short_open:
				self.close_position(price)

			#Ahora verificamores si tenemos operaciones abiertas
			if self.is_long_open:
				#Buscamos promediar los precios de compra
				self.long_open_price = (self.long_open_price + price)/2
				self.amount += self.inv/price
			else:
				#En caso no se tenga operacion abierta, abriremos una nueva operación
				self.is_long_open = True
				self.long_open_price = price
				self.amount = self.inv/price
			
		#Si no es "long"
		elif side == 'short':
			self.num_shorts += 1

			# comment
			if self.is_long_open:
				self.close_position(price)

			#Ahora verificamores si tenemos operaciones abiertas
			if self.is_short_open:
				#Buscamos promediar los precios de compra
				self.short_open_price = (self.short_open_price + price)/2
				self.amount += self.inv/price
			else:
				#En caso no se tenga operacion abierta, abriremos una nueva operación
				self.is_short_open = True
				self.short_open_price = price
				self.amount = self.inv/price

		#Guardaremos la posición desde la cual se abrió
		if self.trailing_stop_loss:
			self.from_opened = from_opened

	#Cerramos una posición | Tener en cuenta que al cerrar una operación se cobra un fee
	#Indicamos el precio al que vamos a cerrar posición
	def close_position(self, price):
		self.num_operations += 1

		#Compra
		if self.is_long_open:
			#El resultado puede ser positivo o negativo
			result = self.amount * (price - self.long_open_price)
			self.is_long_open = False
			self.long_open_price = 0

		#Venta
		elif self.is_short_open:
			result = self.amount * (self.short_open_price - price)
			self.is_short_open = False
			self.short_open_price = 0


		self.profit.append(result)
		self.balance += result

		if result > 0:
			self.winned += 1
			self.drawdown.append(0)
		else:
			self.lossed += 1
			self.drawdown.append(result)

		#Tenemos que reinciar las variables que nos da el control del flujo del programa
		self.take_profit_price = 0
		self.stop_loss_price = 0

	#Establecer un Take Profit
	def set_take_profit(self, price, tp_long = 1.05, tp_short = 0.95):

		#tp_long 1.05 arriba de nuestro precio de entrada (solo se tendrá 1, ya que el 0.5 es la comisión)
		#tp_short 0.95 debajo de nuestro precio de compra (solo se tendrá 1, ya que el 0.5 es la comisión)

		if self.is_long_open:
			#Calculamos el precio hacia arriba
			self.take_profit_price = price * tp_long

		elif self.is_short_open:
			#Calculamos el precio hacia la baja
			self.take_profit_price = price * tp_short

	#Establecer un Stop Loss
	def set_stop_loss(self, price, sl_long = 0.98, sl_short = 1.02):

		#sl_long es el stoploss para compra
		#sl_short es el stoploss para venta

		if self.is_long_open:
			#Si estamos en una operación long, podemos calcular 1% debajo del precio
			self.stop_loss_price = price * sl_long

		if self.is_short_open:
			#Si estamos en una operación short, podemos calcular 1% por arriba del precio
			self.stop_loss_price = price * sl_short

	#Visualizaremos el resultado
	def return_results(self, symbol, start_date, end_date):
		
		profit = sum(self.profit)
		drawdown = sum(self.drawdown)

		#abs es el valor absoluto
		#Enves de calcularlo por cada operación se calculará en total
		fees = (abs(profit) * self.fee_cost * self.num_operations)

		results = {
		'symbol' : symbol,
		'start_date': start_date,
		'end_date': end_date,
		'balance' : self.balance,
		'profit' :	profit,
		'drawdown': drawdown,
		'profit_after_fees': profit - fees,
		'num_operations' : self.num_operations,
		'num_long' : self.num_longs,
		'num_shorts': self.num_shorts,
		'winned' : self.winned,
		'lossed' : self.lossed

		}

		#Para evitar crasheos validamos que no haya división entre 0
		if self.num_operations > 0 and (self.winned + self.lossed) > 0:
			winrate = self.winned / (self.winned + self.lossed)
			results['winrate'] = winrate
			#Esto servirá para calificar que personaje tuvo mayor ganancia
			results['fitness_function'] = (self.num_longs + self.num_shorts) * (profit - abs(drawdown)) * winrate / self.num_operations

		else:
			results['winrate'] = 0
			results['fitness_function'] = 0


		return results

	#Encargada de hacer el backtesting
	def __backtesting__(self, df, strategy):

		#Nos vasamos en:

		#Alto de  la vela
		high = df['high']
		#Cierre de la vela
		close = df['close']
		#Minimo de la vela
		low = df['low']

		for i in range(len(df)):

			#Con esa condicional descartamos individuos con balance negativo
			if self.balance > 0:

				#Verificamos si tenemos una posición de compra
				if strategy.checkLongSignal(i):
					self.open_position(price = close[i], side = 'long', from_opened = i)

					self.set_take_profit(price = close[i], tp_long = 1.03)
					self.set_stop_loss(price = close[i], sl_long = 0.99)

				elif strategy.checkShortSignal(i):
					self.open_position(price = close[i], side = 'short', from_opened = i)
					self.set_take_profit(price = close[i], tp_short = 0.97)
					self.set_stop_loss(price = close[i], sl_short = 1.01)
				
				#Cuando no tenemos señales, tenemos que darle continuidad a las operaciones abiertas
				else:
					
					#Si hay un short o long abierto y una condicion de stop loss | procedemos a actuaizar el stop loss
					if self.trailing_stop_loss  and (self.is_long_open or self.is_short_open):
						
						#Desde que se abrió la posición hasta el índice actual, regresame el máximo del alto de cada vela
						new_max = high[self.from_opened:i].max()
						#Guardamos el dato del stop loss
						previous_stop_loss = self.stop_loss_price
						#Establecemos un nuevo stop loss
						self.set_stop_loss(price = new_max)

						if previous_stop_loss > self.stop_loss_price:
							#Si el stop loss previo es mayor que el actual, entonces lo dejamos como estaba | Ya si el
								#mercado sube, se tendrá un nuevo stop loss
							self.stop_loss_price = previous_stop_loss

					#Si hay una operación a largo
					if self.is_long_open:
						#Verificamos que si el High price de la vela actual es superior al take profit, cerramos la posición
						if high[i] >= self.take_profit_price:
							self.close_position(price = self.take_profit_price)
						#Verificamos que si el Low price de la vela actual es inferior al stop loss, cerramos la posición
						elif low[i] <= self.stop_loss_price:
							self.close_position(price = self.stop_loss_price)

					#Si hay una operación a corta
					elif self.is_short_open:
						#Verificamos que si el High price de la vela actual es superior al stop loss, cerramos la posición
						if high[i] >= self.stop_loss_price:
							self.close_position(price = self.stop_loss_price)
						#Verificamos que si el Low price de la vela actual es inferio al take profit, cerramos la posición
						elif low[i] <= self.take_profit_price:
							self.close_position(price = self.take_profit_price)


'''
import ccxt
from utils import ccxt_ohlcv_to_dataframe 
from stratcode import BBStrategy


exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1h'
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
df = ccxt_ohlcv_to_dataframe(ohlcv)

#Importamos la estrategia
strategy = BBStrategy()
strategy.setUp(df)

#Inicializamos el backtester
tryback = Backtester()
tryback.__backtesting__(df, strategy)

#Imprimimos el resultado
print(tryback.return_results(symbol = '-', start_date = '-', end_date = '-'))
'''