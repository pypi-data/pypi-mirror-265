# hn_data_stock/finance_data.py

import yfinance as yf
import plotly.graph_objects as go

class StockData:
    @staticmethod
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
        history_data = history_data.reset_index().rename(columns={'Date': 'Datetime'})
        return history_data

    @staticmethod
    def plot_candlestick_chart(ticker, period):
        """
        Vẽ biểu đồ nến cho dữ liệu chứng khoán.

        :param ticker: Mã cổ phiếu.
        :param period: Khoảng thời gian lịch sử để truy xuất.
        """
        history_data = StockData.get_stock_data(ticker, period)

        # Tạo biểu đồ nến
        fig = go.Figure(data=[go.Candlestick(
            x=history_data['Datetime'],
            open=history_data['Open'],
            high=history_data['High'],
            low=history_data['Low'],
            close=history_data['Close']
        )])

        # Cài đặt tiêu đề và nhãn cho trục
        fig.update_layout(
            title=f'Biểu Đồ Nến Cổ Phiếu {ticker} Trong {period}',
            xaxis_title='Thời Gian',
            yaxis_title='Giá Cổ Phiếu',
            xaxis_rangeslider_visible=False
        )

        # Hiển thị biểu đồ
        fig.show()
