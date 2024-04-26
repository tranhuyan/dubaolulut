import numpy as np
from datetime import datetime, timedelta
from tensorflow.keras.models import load_model

# Load mô hình đã huấn luyện từ tệp 'trained_model.h5'
model = load_model('trained_model.h5')

# dự đoán kết quả cho ngày mai 
next_day_data = np.array([[25, 60, , 1, 24]])
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