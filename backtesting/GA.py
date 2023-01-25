import numpy as np
from Backtester import Backtester

#Datos del individuo
class Individual:
	def __init__(self, n_genes, gene_ranges):
		#N° de genes que va a tener, esto depende de los parámetros de los indicadores (Por ejemplo, Las BBands tiene (1) El numero de periodos (2) El número de desviaciones | El RSI tiene (1) El numero de periodos (2) Nivel de sobrecompra  (3) Nivel de sobreventa (60 y 40))
		
		#Definimos UN GEN, esto va a iterar en cada tupla buscnado el limite inferior y superior, y guardarlo como una lisa 
		self.genes = [np.random.randint(gene_ranges[x][0], gene_ranges[x][1]) for x in range(n_genes)]

		#Cada individuo va a tene run backtester propio como atributo, podremos acceder al numero de operaciones uqe hizo, al fitness_functions, etc
		self.backtester = Backtester(
			initial_balance = 1000,
			leverage = 10,
			trailing_stop_loss = True
			)


class Population:
	def __init__(self, generation_size, n_genes, gene_ranges, n_best, mutation_rate):

		#Generation_size, es el numero de individuos por población
		#N_best, numero de los mejores 10 individuos por población
		#Mutation_rate, probabilidad de que un gen mute a la hora de aplicar la mutación a algun individuo de la población  
		 
		self.population = [Individual(n_genes, gene_ranges) for _ in range(generation_size)] # El "_" es para no utilizar el valor del iterador,sino solo que queremos que se ejecute un determinado numero de veces
		self.n_genes = n_genes
		self.gene_ranges = gene_ranges
		self.n_best = n_best
		self.generation_size = generation_size
		self.mutation_rate = mutation_rate

	#AHORA VEREMOS LAS ACCIONES QUE TENDRA LA POBLACIÓN
	def selection(self):
		#Retornaremos los mejores individuos
		return sorted(
			#Retornamos a la población
			self.population,
			#Lo ordenamos con el fitness_functions
			
			#	x = lambda a: a + 10
			#	print(x(2))
			#	---> 12

			#	x = lambda a: a + 10
			#	print(x(5))
			#	---> 15
			
			key = lambda individual: individual.backtester.return_results(
				symbol = '-',
				start_date = '-',
				end_date = '-',
				)['fitness_function'],
			reverse = True
			)[0:self.n_best]
			#Con "reverse = True" ordena de mayor a menor
			#Regresamos del 0 al N mejores individuos para que se puedan reproducir

	def crossover(self):
		#Seleccionamos los mejores N individuos
		selected = self.selection()
		#Point será el punto de corto genético, entre padres e hijos, luego indicaremos el numero random
		point = 0
		#Lista de padres de la siguiente generación
		father = []

		for i in range(self.generation_size):
			#Size, la cantidad de muestras que puede seleccionar (Si es 2, singifica que solo puede seleccionar 2 padres)
			#Replace, sin reemplazo, es decir un mismo padre no pueda tener un hijo
			father = np.random.choice(self.n_best, size = 2, replace = False)
			#Guardamos el objeto individuo en la lista de padres
			father = [selected[x] for x in father]

			# Crossover in one point
			#Calculamos el punto del Crossover
			point = np.random.randint(0, self.n_genes)

			#Ahora vamos a acceder al i ésimo individuo de la población, y de esta manera hacemos el corte genetico y reemplazo de genes de los 2 padres, y ya estará reproducida la población
			
			#DEL PUNTO 0 HASTA EL PUNTO A
			#Accedemos al atributo genes[:point], es decir, desde el inicio hasta el point vamos a reemplazar los valores por los valors que tenga
			 	# father[0] hasta genes[:point] 
			self.population[i].genes[:point] = father[0].genes[:point]
			#REEMPLAZAMOS DESDE EL PUNTO A HASTA EL FINAL
			self.population[i].genes[point:] = father[1].genes[point:]


	def mutation(self):
		
		#Vamos a recorrer todos los elementos de la población
		for i in range(self.generation_size):
			point = 0

			for j in range(self.n_genes):
				#Se selecciona un punto aleatorio de los genes
				#Mutaremos una cadena de genes en un mismo individuo
				point = np.random.randint(0, self.n_genes)

				#Probabilidad de que se mute a un nuevo gen
				if np.random.random() <= self.mutation_rate:
					#Generamos un nuevo gen
					new_gen = np.random.randint(self.gene_ranges[point][0], self.gene_ranges[point][1])

					#Debemos validar que el gen nuevo que se genera no sea igual al anterior
					#Si el new_gen es igual al gen_point lo ejecutamos hasta que sean diferentes
					while new_gen == self.population[i].genes[point]:
						new_gen = np.random.randint(self.gene_ranges[point][0], self.gene_ranges[point][1])

					self.population[i].genes[point] = new_gen


