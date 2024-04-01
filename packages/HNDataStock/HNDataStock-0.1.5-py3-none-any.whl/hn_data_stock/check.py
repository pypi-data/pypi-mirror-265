import chardet
with open(r'G:\My Drive\0. Day ben ngoai (___)\Day DataPass\HNDataStock\hn_data_stock\test_finance_data.py', 'rb') as f:
    print(chardet.detect(f.read()))