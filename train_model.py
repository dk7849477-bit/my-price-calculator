import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

print("⏳ 1. Загружаю датасет...")
california = fetch_california_housing(as_frame=True)
df = california.frame

# МАТЕРИАЛЬНЫЙ ХАК: Создаем новый признак, который балансирует аномальные комнаты
# Мы привязываем количество комнат к среднему доходу района
df['Room_Value'] = df['AveRooms'] * df['MedInc']

# Выбираем признаки (теперь включая наш новый Room_Value)
X = df[['MedInc', 'HouseAge', 'AveRooms', 'Room_Value', 'Latitude', 'Longitude']] 
y = df['MedHouseVal'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🧠 2. Обучаю скорректированную модель (Random Forest)...")
# Настраиваем модель так, чтобы она не переобучалась на шумах
model = RandomForestRegressor(n_estimators=150, max_depth=12, min_samples_leaf=4, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"🔥 Итоговая точность модели: {accuracy * 100:.2f}%")

print("💾 3. Сохраняю модель...")
joblib.dump(model, 'price_model.pkl')
print("✅ Готово!")

