from crewai.tools import BaseTool
import yfinance as yf
from typing import Optional

class YahooFinanceTool(BaseTool):
    """
    Custom CrewAI tool to fetch real-time financial data from Yahoo Finance.
    Provides price, market cap, P/E ratio, revenue, and stock price change over time.
    """
    name: str = "yahoo_finance_data"
    description: str = "Fetches real-time stock data including price, market cap, and P/E ratio for a given ticker"

    def _run(self, symbol: str, period: Optional[str] = "1y") -> str:
        """
        Fetch financial metrics for a given stock symbol over the specified period.

        Args:
            symbol (str): Stock ticker (e.g. 'AAPL', 'GOOG')
            period (str): Time period for price history (e.g. '1y', '6mo')

        Returns:
            str: Multi-line summary string with financial metrics
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            hist = stock.history(period=period)

            # Extract and format key financial metrics
            current_price = info.get('currentPrice', 'N/A')

            market_cap = info.get('marketCap', 'N/A')
            if market_cap != 'N/A':
                market_cap = f"${market_cap / 1e9:.2f}B"  # Convert to billions

            pe_ratio = info.get('forwardPE', 'N/A')

            revenue = info.get('totalRevenue', 'N/A')
            if revenue != 'N/A':
                revenue = f"${revenue / 1e9:.2f}B"  # Convert to billions

            # Calculate percentage price change over the period
            if not hist.empty:
                price_change = ((hist['Close'][-1] - hist['Close'][0]) / hist['Close'][0]) * 100
                price_change = f"{price_change:.2f}%"
            else:
                price_change = 'N/A'

            return f"""
            Financial Summary for {symbol}:
            Current Price: ${current_price}
            Market Cap: {market_cap}
            P/E Ratio: {pe_ratio}
            Revenue: {revenue}
            Price Change ({period}): {price_change}
            """.strip()

        except Exception as e:
            # Handle any runtime or API error gracefully
            return f"Error fetching data for {symbol}: {str(e)}"
