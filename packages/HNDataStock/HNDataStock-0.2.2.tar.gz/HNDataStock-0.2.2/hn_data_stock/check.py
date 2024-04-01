import chardet
with open(r'G:\My Drive\0. Day ben ngoai (___)\Day DataPass\HNDataStock\hn_data_stock\__init__.py', 'rb') as f:
    print(chardet.detect(f.read()))


# This Python code uses the `chardet` library to guess the encoding of a file
# and then opens the file in binary mode to check for null bytes.

import chardet

# Function to check for null bytes in a file
def check_for_null_bytes(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        # Detect file encoding
        result = chardet.detect(content)
        print(f"Detected encoding is {result['encoding']} with {result['confidence']*100}% confidence")
        # Check for null bytes
        if b'\x00' in content:
            print(f"Null bytes found in {file_path}")
        else:
            print(f"No null bytes found in {file_path}")

# Replace 'path_to_your_file.py' with the actual file paths.
# Example:
# check_for_null_bytes('path_to_your_init_file.py')
# check_for_null_bytes('path_to_your_finance_data_file.py')
# Add additional files as needed

# Since we don't have the actual file paths, we'll use placeholders
check_for_null_bytes(r'G:\My Drive\0. Day ben ngoai (___)\Day DataPass\HNDataStock\hn_data_stock\__init__.py')