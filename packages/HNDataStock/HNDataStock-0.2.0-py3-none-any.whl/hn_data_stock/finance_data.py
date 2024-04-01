# hn_data_stock/finance_data.py

import requests
import yfinance as yf

def get_stock_data(ticker, period='1mo'):
    """
    Lấy dữ liệu lịch sử cổ phiếu.

    :param ticker: Mã cổ phiếu.
    :param period: Khoảng thời gian lịch sử để truy xuất. 
                   Ví dụ: '1d' cho một ngày, '1mo' cho một tháng, '1y' cho một năm, v.v.
    :return: DataFrame chứa dữ liệu lịch sử cổ phiếu.
    """
    history = yf.Ticker(ticker)
    history_data = history.history(period=period)
    
    return history_data