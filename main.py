import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go

# Função para coletar dados históricos da Dogecoin
def coletar_dados_dogecoin():
    url = 'https://api.coingecko.com/api/v3/coins/dogecoin/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '90',
        'interval': 'daily'
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'preco'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

# Cálculo da Média Móvel Simples (SMA) e Exponencial (EMA)
def calcular_medias(df, periodo):
    df['SMA'] = df['preco'].rolling(window=periodo).mean()
    df['EMA'] = df['preco'].ewm(span=periodo, adjust=False).mean()

# Cálculo do Índice de Força Relativa (RSI)
def calcular_rsi(df, periodo=14):
    delta = df['preco'].diff()
    ganho = (delta.where(delta > 0).rolling(window=periodo).mean()).fillna(0)
    perda = (-delta.where(delta < 0).rolling(window=periodo).mean()).fillna(0)
    rs = ganho / perda
    df['RSI'] = 100 - (100 / (1 + rs))

# Cálculo do MACD
def calcular_macd(df):
    ema12 = df['preco'].ewm(span=12, adjust=False).mean()
    ema26 = df['preco'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

# Identificação de padrões de Candlestick
def identifica_padroes_candlestick(df):
    df['martelo'] = ((df['preco'] < df['preco'].shift(1)) & (df['preco'] > df['preco'].shift(1) * 0.9)).astype(int)

# Geração de sinais de compra e venda
def gerar_sinais(df):
    df['sinal_compra'] = ((df['RSI'] < 30) & (df['preco'] > df['SMA'])).astype(int)
    df['sinal_venda'] = ((df['RSI'] > 70) & (df['preco'] < df['SMA'])).astype(int)

# Visualização dos dados
def visualizar_dados(df):
    plt.figure(figsize=(14, 7))

    # Gráfico de preços e médias móveis
    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['preco'], label='Preço da Dogecoin', color='blue')
    plt.plot(df.index, df['SMA'], label='SMA 14', color='red', alpha=0.7)
    plt.plot(df.index, df['EMA'], label='EMA 14', color='orange', alpha=0.7)
    plt.scatter(df[df['sinal_compra'] == 1].index, df[df['sinal_compra'] == 1]['preco'], 
                label='Sinal de Compra', marker='^', color='green', s=100)
    plt.scatter(df[df['sinal_venda'] == 1].index, df[df['sinal_venda'] == 1]['preco'], 
                label='Sinal de Venda', marker='v', color='red', s=100)
    plt.title('Análise Técnica da Dogecoin')
    plt.xlabel('Data')
    plt.ylabel('Preço (USD)')
    plt.legend()

    # Gráfico de RSI e MACD
    plt.subplot(2, 1, 2)
    plt.plot(df.index, df['RSI'], label='RSI', color='purple')
    plt.axhline(70, linewidth=1, linestyle='--', color='red')
    plt.axhline(30, linewidth=1, linestyle='--', color='green')
    plt.title('Índice de Força Relativa (RSI)')
    plt.xlabel('Data')
    plt.ylabel('RSI')

    plt.tight_layout()
    plt.show()

# Execução do script
if __name__ == "__main__":
    df_dogecoin = coletar_dados_dogecoin()
    calcular_medias(df_dogecoin, periodo=14)
    calcular_rsi(df_dogecoin)
    calcular_macd(df_dogecoin)
    identifica_padroes_candlestick(df_dogecoin)
    gerar_sinais(df_dogecoin)
    visualizar_dados(df_dogecoin)
