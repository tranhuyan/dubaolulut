import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Giả sử dữ liệu được lưu trong DataFrame df
df = pd.DataFrame({
    'temperature': [25.5, 26.0, 25.8, 27.2],  # Dữ liệu nhiệt độ
    'humidity': [60, 62, 61, 63]  # Dữ liệu độ ẩm
})

# Tạo cột 'next_temperature' dựa trên giá trị hiện tại của nhiệt độ
df['next_temperature'] = df['temperature'].shift(-1)

# Loại bỏ dòng cuối cùng với giá trị NaN trong cột 'next_temperature'
df = df.dropna()

# Chia dữ liệu thành features (X) và target (y)
X = df[['temperature']]
y = df['next_temperature']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Xây dựng mô hình hồi quy tuyến tính
model = LinearRegression()

# Huấn luyện mô hình
model.fit(X_train, y_train)

current_temperature = 26.5

# Dự đoán giá trị nhiệt độ tiếp theo
next_temperature_prediction = model.predict([[current_temperature]])
print("Dự đoán giá trị nhiệt độ tiếp theo:", next_temperature_prediction)
