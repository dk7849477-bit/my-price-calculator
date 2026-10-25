import streamlit as st
import requests
import os

# Безопасное чтение API-ключа из настроек окружения
api_key = os.environ.get("RAPIDAPI_KEY")

st.set_page_config(page_title="Калькулятор цен США", layout="centered")

st.title("🏡 Калькулятор стоимости недвижимости в США")
st.subheader("Оценка объектов в реальном времени")

# Пример корректного ввода адреса для пользователя
st.info("Пример формата: 5500 Grand Lake Dr, San Antonio, TX 78244")
address = st.text_input("Введите точный адрес объекта:", "5500 Grand Lake Dr, San Antonio, TX")

if st.button("Узнать актуальную цену объектов", type="primary"):
    if not api_key:
        st.error("Критическая ошибка: API_KEY не настроен в конфигурации сервера.")
    else:
        url = "https://rapidapi.com"
        querystring = {"address": address}
        headers = {
            "X-RapidAPI-Host": "://rapidapi.com",
            "X-RapidAPI-Key": api_key
        }
        
        with st.spinner("Связываемся с американскими базами данных Zillow/RealtyMole..."):
            try:
                response = requests.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data and isinstance(data, dict):
                        price = data.get("price")
                        
                        if price:
                            st.success(f"🔥 Актуальная рыночная стоимость: **${price:,}**")
                            
                            # Вывод дополнительных характеристик
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Спальни", data.get("bedrooms", "—"))
                            with col2:
                                st.metric("Ванные", data.get("bathrooms", "—"))
                            with col3:
                                st.metric("Площадь (sqft)", f"{data.get('squareFootage', '—'):,}")
                        else:
                            st.warning("Объект найден, но точная цена для него сейчас не определена.")
                    else:
                        st.error("Данные по этому адресу не найдены. Проверьте правильность написания города и штата.")
                elif response.status_code == 403:
                    st.error("Ошибка авторизации API: Проверьте правильность токена в Secrets.")
                else:
                    st.error(f"Сервер баз данных вернул ошибку кода: {response.status_code}")
            except Exception as e:
                st.error("Не удалось подключиться к серверу проверки цен. Попробуйте позже.")


