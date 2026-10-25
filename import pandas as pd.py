import pandas as pd
from sklearn.datasets import fetch_california_housing

print("📥 Загружаю данные о недвижимости...")
# Скачиваем готовый датасет
california = fetch_california_housing(as_frame=True)
df = california.frame

# Показываем первые 5 строчек таблицы в консоли
print("\n✅ Данные успешно загружены! Вот как выглядит таблица:")
print(df.head())

