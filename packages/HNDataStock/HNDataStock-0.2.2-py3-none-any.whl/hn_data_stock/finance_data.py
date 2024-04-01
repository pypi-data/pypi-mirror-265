# hn_data_stock/finance_data.py

import requests
import yfinance as yf

import yfinance as yf

def get_stock_data(ticker, period):
    """
    Lấy dữ liệu lịch sử cổ phiếu.

    :param ticker: Mã cổ phiếu.
    :param period: Khoảng thời gian lịch sử để truy xuất.
                   Ví dụ: '1d' cho một ngày, '1mo' cho một tháng, '1y' cho một năm, v.v.
    :return: DataFrame chứa dữ liệu lịch sử cổ phiếu, với cột 'Date' được đổi tên thành 'Datetime'.
    """
    history = yf.Ticker(ticker)
    history_data = history.history(period=period)
    
    # Chuyển chỉ mục 'Date' thành một cột và đổi tên cột đó thành 'Datetime'
    history_data = history_data.reset_index().rename(columns={'Date': 'Datetime'})
    
    return history_data
