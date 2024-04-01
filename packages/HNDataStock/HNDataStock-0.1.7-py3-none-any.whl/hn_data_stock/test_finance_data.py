# tests/test_finance_data.py

from hn_data_stock import get_stock_data

def test_get_stock_data():
    data = get_stock_data('AAPL')  # Ví dụ sử dụng mã cổ phiếu của Apple
    assert data is not None
    # Thêm các assertions kiểm tra cấu trúc dữ liệu nhận được
