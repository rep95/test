import yfinance as yf
from datetime import datetime
import os

# Configuration des tickers Yahoo Finance
TICKERS = {
    "BRENT": "BZ=F", # Brent Crude
    "GOLD": "GC=F",  # Gold
    "SILVER": "SI=F" # Silver
}

def fetch_market_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="5d")
        if len(hist) < 2:
            return "N/A", "N/A", "N/A"
        
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        variation = ((current_price - prev_price) / prev_price) * 100
        
        # Détection basique d'anomalie de volume (au lieu du Smart Money complexe)
        current_vol = hist['Volume'].iloc[-1]
        avg_vol = hist['Volume'].mean()
        vol_anom = "YES" if current_vol > (avg_vol * 1.5) else "NO"
        
        return round(current_price, 2), round(variation, 2), vol_anom
    except Exception as e:
        return "N/A", "N/A", "N/A"

def main():
    print("Démarrage de l'extraction des données tactiques...")
    
    brent_pr, brent_var, _ = fetch_market_data(TICKERS["BRENT"])
    gold_pr, gold_var, gold_vol = fetch_market_data(TICKERS["GOLD"])
    silver_pr, silver_var, _ = fetch_market_data(TICKERS["SILVER"])

    # Construction du bloc de contexte (formaté pour être copi�� dans ton LLM)
    context_data = f"""
* COMMODITIES (Date Extraction : {datetime.now().strftime('%Y-%m-%d')}) :
    * Brent Crude ($/baril) : Prix={brent_pr}, Variation_24h={brent_var}%
    * Gold (XAU/oz) : Prix={gold_pr}, Variation_24h={gold_var}%
    * Silver (XAG/oz) : Prix={silver_pr}, Variation_24h={silver_var}%
* SMART MONEY INDICATORS (Proxy) :
    * Anomalie Volume (Or) : {gold_vol}
    * Positioning MM (Or) : [REMPLIR MANUELLEMENT OU VIA API PAYANTE]
    * Options Flow (GLD ETF) : [REMPLIR MANUELLEMENT OU VIA API PAYANTE]
"""
    
    # Sauvegarde dans un fichier texte
    with open("context_du_jour.txt", "w", encoding="utf-8") as f:
        f.write(context_data)
        
    print("Extraction terminée. Fichier context_du_jour.txt généré.")

if __name__ == "__main__":
    main()