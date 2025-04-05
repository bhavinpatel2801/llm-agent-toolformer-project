"""
Tool: Finance Earnings
Fetches stock earnings summary using Yahoo Finance unofficial API.
"""

import requests

def get_earnings_summary(ticker):
    try:
        url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=earnings"
        response = requests.get(url)
        data = response.json()

        earnings = data['quoteSummary']['result'][0]['earnings']['financialsChart']['yearly']
        output = f"Earnings summary for {ticker}:
"
        for year in earnings:
            output += f"{year['date']}: Revenue = {year['revenue']['raw']}, Earnings = {year['earnings']['raw']}
"
        return output
    except Exception as e:
        return f"[Finance API] Failed to fetch earnings for {ticker}: {e}"
