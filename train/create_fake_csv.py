
#  tạo dữ liệu ảo cho cảm biến dht11
import numpy as np
import pandas as pd

# Tạo dữ liệu ảo cho cảm biến DHT11
np.random.seed(0)
n = 10000
temperature = np.random.randint(20, 30, n) + np.random.rand(n)
humidity = np.random.randint(50, 80, n) + np.random.rand(n)
water_level = np.random.randint(5, 10, n) + np.random.rand(n)
date = pd.date_range('2021-01-01', periods=n, freq='H')
# time = pd.date_range('2021-01-01', periods=n, freq='H').time

# Tạo DataFrame từ dữ liệu ảo
df = pd.DataFrame({'temperature': temperature, 'humidity': humidity, 'date': date, 'water_level': water_level})

# Lưu DataFrame vào file CSV
df.to_csv('data.csv', index=False)

print("Dữ liệu đã được lưu vào file data.csv")