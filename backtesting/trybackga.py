from GA import Population
from stratcode import BBStrategy
from utils import ccxt_ohlcv_to_dataframe

import ccxt

exchange = ccxt.binance()
symbol = 'RARE/USDT'
timeframe = '15m'
limit = 1000
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit)
df = ccxt_ohlcv_to_dataframe(ohlcv)

#Generamos la población de individuos para aplicar el backtesting
P = Population(
	#Cantidad de individuos por generación
	generation_size = 50,
	#Cantidad de genes, es decir, los parámetros: 1.Longitud de las BB | 2. Desviación estándar de las BB | 3. Periodos del RSI |
		# 4.Nivel de sobrecompra | 5. Nivel de sobreventa 
	n_genes = 5,
	#Lista de tuplas [(bb_len(inicio),bb_len(fin)), (n_std*10(parte desde 1.0),n_std*10(hasta 3.0)), 
		# (rsi_len(inicio),rsi_len(fin)), (rsi_overbought(niveldesobrecompra inicial),rsi_overbought(niveldesobrecompra final)),
			# (rsi_overbought(niveldesobreventa inicial),rsi_overbought(niveldesobreventa final))]
	gene_ranges = [(20, 100),(10, 30),(8, 100),(50, 100),(0, 50)],
	#Seleccionamos los mejores de cada generación
	n_best = 5,
	#Si podemos un Mutation_rate muy elevado como 100%, puede no llegar a converger, por eso es recomendable 0.1(10%)
	mutation_rate = 0.1
	)

#Asignamos todos los individuos
population = P.population

#Cuantas generaciones tienen que pasar para que nuestros algoritmos genéticos entren
number_of_generations = 20

print('GENETIC ALGORITHM TO OPTIMIZE QUANT STRATEGY')
print('BOLLINGER BANDS - RSI')
print('SYMBOL: ', symbol, 'TIMEFRAME: ', timeframe)

print()
print()


for x in range(number_of_generations):
	
	#Para cada individuo de la población
	for individual in population:
		
		#Vamos a reiniciar los valores del backtester
		individual.backtester.reset_results()
		
		#Guardamos los genes del individuo
		genes = individual.genes

		#n_std lo dividos entre 10 porque lo habiamos multiplicado x10
		strategy = BBStrategy(
			bb_len = genes[0],
			n_std = genes[1]/10,
			rsi_len = genes[2],
			rsi_overbought = genes[3],
			rsi_oversold = genes[4]
			)
		#Esto es para enviarle los parametros para calcular los indicadores
		strategy.setUp(df)
		#El resultado del backtester se va a almacenar en el objeto backtester del individuo
		individual.backtester.__backtesting__(df, strategy)
	
	#Por cada generación hacemos el crossover
	P.crossover()
	#Por cada generación hacemos la mutación
	P.mutation()


	population = sorted(
					population,
					key = lambda individual: individual.backtester.return_results(
					symbol = '-',
					start_date = '-',
					end_date = '-',
					)['fitness_function'],
					reverse = True
					)

	print()
	print('GENERATION: ', x)
	print('_________________')
	print('\n\n')

	print('BEST INDIVIDUAL:')
	print(population[0].backtester.return_results(
		symbol = symbol,
		start_date = '',
		end_date = ''
		))
	print(population[0].genes)
	print('\n')

	print('WORST INDIVIDUAL:')
	print(population[-1].backtester.return_results(
		symbol = symbol,
		start_date = '',
		end_date = ''
		))
	print(population[-1].genes)

	#Incluso podriamos usar K-MEANS  para ver el mejor grupo de resultados

	print('\n\n')