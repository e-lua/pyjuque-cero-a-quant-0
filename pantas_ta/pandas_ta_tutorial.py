import ccxt
import pandas_ta as ta
import pandas as pd

#Importing the data from utils
import sys
sys.path.insert(0, 'D:/Github/python/Bot Trading/UDEMY/de_cero_a_quant/getData/indicators')
from utils import ccxt_ohlcv_to_dataframe 

exchange=ccxt.binance()
symbol='BTC/USDT'
timeframe='1h'
ohlcv=exchange.fetch_ohlcv(symbol,timeframe)
df=ccxt_ohlcv_to_dataframe(ohlcv)

#Conocer todos los indicadores
#print(df.ta.indicators())

#Declarar un indicador
sma=ta.sma(df['close'],length=21)
#print(sma)

#Agregar el indicador  a nuestro objeto dataframe
#df.ta.sma(length=21, append=True)
#print(df)

#=================ANTES DE DEFINIR LA ESTRATEGIA TENEMOS QUE DEFINIR LOS CORES COMPUTACIONALES A UTILIZAR===========

df.ta.cores=2

#================DEFINIMOSLA ESTRATEGIA===========

#La creación de la estrategia es con "S" mayúsucla
emastrat = ta.Strategy(
    name='emacross',
    ta=[
        {"kind":"ema", "length":9},
        {"kind":"ema", "length":35}
    ]
)

#La el cálculo es con "S" minúscula
df.ta.strategy(emastrat)

print(df)
























