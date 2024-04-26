import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Đọc dữ liệu từ file CSV
df = pd.read_csv('data.csv')

df['date'] = pd.to_datetime(df['date'])
df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
df['hours_since_start'] = (df['date'] - df['date'].min()).dt.total_seconds() / 3600

# Chia dữ liệu thành features (nhiệt độ và độ ẩm) và target (nhiệt độ tiếp theo)
X = df[['temperature', 'humidity', 'water_level', 'days_since_start', 'hours_since_start']]
y = df['water_level']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Xây dựng mô hình Sequential của TensorFlow
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Compile mô hình
model.compile(optimizer='adam', loss='mean_squared_error')

# Huấn luyện mô hình
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Lưu mô hình đã huấn luyện thành file 'trained_model.h5'
model.save('trained_model.h5')



print("Mô hình đã được lưu thành công.")

# dự đoán kết quả cho ngày mai 
next_day_data = np.array([[25, 60, 5, 1, 24]])
prediction = model.predict(next_day_data)
print("Dự đoán mức nước cho ngày mai:", prediction[0][0])

# dự đoán kết quả cho ngày kia
next_day_data = np.array([[25, 60, 5, 2, 48]])
prediction = model.predict(next_day_data)
print("Dự đoán mức nước cho ngày kia:", prediction[0][0])


#  dự đoán kết quả cho ngày thứ 3
next_day_data = np.array([[25, 60, 5, 3, 72]])
prediction = model.predict(next_day_data)
print("Dự đoán mức nước cho ngày thứ 3:", prediction[0][0])

#  dự đoán kết quả cho ngày thứ 4
next_day_data = np.array([[25, 60, 5, 4, 96]])
prediction = model.predict(next_day_data)
print("Dự đoán mức nước cho ngày thứ 4:", prediction[0][0])

