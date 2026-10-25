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
        st.error("Критическая ошибка: RAPIDAPI_KEY не настроен в конфигурации сервера.")
    else:
        # Используем самый точный эндпоинт для оценки стоимости недвижимости
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
                        # Realty Mole возвращает оценку в поле 'price' или 'value'
                        price = data.get("price") or data.get("value")
                        
                        if price:
                            st.success(f"🔥 Актуальная рыночная стоимость: **${int(price):,}**")
                            
                            # Вывод характеристик объекта, если они пришли в ответе
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Спальни", data.get("bedrooms", "—"))
                            with col2:
                                st.metric("Ванные", data.get("bathrooms", "—"))
                            with col3:
                                st.metric("Площадь (sqft)", f"{data.get('squareFootage', '—'):,}" if data.get('squareFootage') else "—")
                        else:
                            st.warning("Объект найден, но точная рыночная цена для него сейчас не определена.")
                    else:
                        st.error("Данные по этому адресу не найдены. Проверьте правильность написания города и штата.")
                elif response.status_code == 403:
                    st.error("Ошибка авторизации API: Ваш ключ RapidAPI не активен или введен неверно в Secrets.")
                elif response.status_code == 429:
                    st.error("Превышен лимит запросов на бесплатном тарифе API.")
                else:
                    st.error(f"Сервер баз данных вернул ошибку. Код ответа: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"Техническая ошибка подключения: {str(e)}")



