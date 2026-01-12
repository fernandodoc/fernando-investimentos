import yfinance as yf
import pandas as pd
import numpy as np

def calcular_metricas_risco(ticker):
    # Coletando dados (2 anos)
    # Usamos ['Close'] para pegar apenas os preços de fechamento
    dados = yf.download(ticker, period="2y", progress=False)['Close']
    
    # Se o retorno for um DataFrame (com 1 coluna), transformamos em Series
    if isinstance(dados, pd.DataFrame):
        dados = dados.iloc[:, 0]

    # Calculando retornos diários
    retornos = dados.pct_change().dropna()
    
    # 1. CÁLCULO DO ÍNDICE DE SHARPE
    taxa_livre_risco_diaria = 0.00038
    retorno_excedente = retornos - taxa_livre_risco_diaria
    
    # Calculamos a média e o desvio padrão, garantindo que sejam valores escalares
    media_excedente = retorno_excedente.mean()
    desvio_padrao = retornos.std()
    
    sharpe_ratio = (media_excedente / desvio_padrao) * np.sqrt(252)
    
    # 2. CÁLCULO DO MAXIMUM DRAWDOWN (MDD)
    pico = dados.cummax()
    quedas = (dados - pico) / pico
    max_drawdown = quedas.min()
    
    # --- FORMATAÇÃO DOS RESULTADOS ---
    # Convertendo para float puro para evitar o erro de TypeError
    sharpe_final = float(sharpe_ratio)
    mdd_final = float(max_drawdown)

    print(f"--- Relatório de Risco: {ticker} ---")
    print(f"Índice de Sharpe Anualizado: {sharpe_final:.2f}")
    print(f"Maximum Drawdown (Pior Queda): {mdd_final * 100:.2f}%")
    
    if sharpe_final > 1:
        print("💡 Insight: Este ativo apresenta um excelente retorno ajustado ao risco.")
    elif sharpe_final < 0:
        print("⚠️ Insight: O ativo não está compensando o risco em relação à renda fixa.")

# Executando
calcular_metricas_risco("PETR4.SA")
