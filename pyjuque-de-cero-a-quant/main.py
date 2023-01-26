from pyjuque.Bot import defineBot
from BBStrategy import BBStrategy

import pandas as pd
import time

#keys = pd.read_csv('Usuarios.csv')


bot_config = {
	'name' : 'bot_enero_22',
	
	'exchange' : {
		'name' : 'binance',
		'params' : {
			'api_key': 'HxR9W43sRtR3urbGttAB4ee06WktwqY7RuhJwzZAMnGyXU3U5ECrfbvyIzZCvu4I',
			'secret' : 'pMXP3FecHTcHq4xKtMPmXGqQBE7deCKTgCSNqF7EbXUNkqpYkKNQYkibcoXe3YVp'
		},
	},

	'symbols' : ['SOL/USDT','ADA/USDT','ETH/USDT'],

	'starting_balance' : 400,

	'strategy': {
		'class': BBStrategy,
		'params': {
			'bb_len' : 20,
			'n_std' : 2.0,
			'rsi_len' : 14,
			'rsi_overbought': 60,
			'rsi_oversold' : 40,
		}
	},
	'timeframe' : '5m',

	'entry_settings' : {

		'initial_entry_allocation': 100,

		'signal_distance': 0.001
	},

	'exit_settings' : {

		'take_profit' : 2,

		'stop_loss_value': 1
	},

	'display_status' : True
}



def main():
	bot_controller = defineBot(bot_config)

	while True:
		try:
			bot_controller.executeBot()
		except KeyboardInterrupt:
			return

		time.sleep(15)

if __name__ == '__main__':
	main()