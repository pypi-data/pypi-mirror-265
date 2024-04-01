# hn_data_stock/finance_data.py

import requests
import yfinance as yf
import plotly.graph_objects as go

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

def plot_candlestick_chart(ticker, period='1mo'):
    """
    Vẽ biểu đồ nến cho dữ liệu chứng khoán.

    :param ticker: Mã cổ phiếu.
    :param period: Khoảng thời gian lịch sử để truy xuất.
                   Ví dụ: '1d' cho một ngày, '1mo' cho một tháng, '1y' cho một năm, v.v.
    """
    # Lấy dữ liệu lịch sử cổ phiếu
    history = yf.Ticker(ticker)
    history_data = history.history(period=period)
    
    # Tạo biểu đồ nến
    fig = go.Figure(data=[go.Candlestick(x=history_data.index,
                                         open=history_data['Open'],
                                         high=history_data['High'],
                                         low=history_data['Low'],
                                         close=history_data['Close'])])
    
    # Cài đặt tiêu đề và nhãn cho trục
    fig.update_layout(title=f'Biểu Đồ Nến Cổ Phiếu {ticker} Trong {period}',
                      xaxis_title='Thời Gian',
                      yaxis_title='Giá Cổ Phiếu',
                      xaxis_rangeslider_visible=False)  # Ẩn thanh điều chỉnh khoảng thời gian
    
    # Hiển thị biểu đồ
    fig.show()
    
    return history_data
