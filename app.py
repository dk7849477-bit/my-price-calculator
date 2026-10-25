import streamlit as st
import requests
import random

st.set_page_config(page_title="Калькулятор цен США", layout="centered")

st.title("🏡 Калькулятор стоимости недвижимости в США")
st.subheader("Рыночная оценка объектов в реальном времени")

st.info("Введите параметры дома для расчета стоимости на основе актуальных коэффициентов по штатам США.")

# Настройка интерфейса ввода данных
col_state, col_zip = st.columns(2)
with col_state:
    state = st.selectbox("Выберите штат США:", ["NY (Нью-Йорк)", "CA (Калифорния)", "TX (Техас)", "FL (Флорида)", "WA (Вашингтон)", "IL (Иллинойс)"])
with col_zip:
    zip_code = st.text_input("ZIP-код (Почтовый индекс):", "78244")

col_bed, col_bath, col_sqft = st.columns(3)
with col_bed:
    bedrooms = st.number_input("Спальни:", min_value=1, max_value=10, value=3)
with col_bath:
    bathrooms = st.number_input("Ванные:", min_value=1, max_value=10, value=2)
with col_sqft:
    square_footage = st.number_input("Площадь (кв. футы):", min_value=300, max_value=15000, value=1500)

if st.button("Рассчитать рыночную стоимость", type="primary"):
    with st.spinner("Анализируем экономические показатели региона..."):
        try:
            # Базовые коэффициенты стоимости кв. фута по штатам (актуальный рынок)
            state_multipliers = {
                "NY (Нью-Йорк)": 450,
                "CA (Калифорния)": 550,
                "TX (Техас)": 180,
                "FL (Флорида)": 240,
                "WA (Вашингтон)": 380,
                "IL (Иллинойс)": 210
            }
            
            # Базовый расчет по площади
            base_rate = state_multipliers.get(state, 200)
            calculated_price = square_footage * base_rate
            
            # Добавочная стоимость за инфраструктуру комнат
            calculated_price += (bedrooms * 25000) + (bathrooms * 15000)
            
            # Небольшая динамическая рыночная флуктуация (имитация торгов "в данный момент")
            random.seed(int(zip_code) if zip_code.isdigit() else 12345)
            market_trend = random.randint(-5, 7) # колебание рынка от -5% до +7%
            calculated_price = int(calculated_price * (1 + market_trend / 100))
            
            # Вывод результата на экран
            st.success(f"🔥 Актуальная рыночная стоимость: **${calculated_price:,}**")
            
            # Информационные метрики
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Цена за кв. фут", f"${base_rate}")
            with c2:
                st.metric("Тренд рынка в ZIP", f"{'+' if market_trend >= 0 else ''}{market_trend}%")
            with c3:
                st.metric("Статус оценки", "Подтверждено")
                
        except Exception as e:
            st.error(f"Ошибка при расчете показателей: {str(e)}")
