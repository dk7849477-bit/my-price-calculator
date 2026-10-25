import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Загружаем переменные из локального файла .env
load_dotenv()

# Чтение ключа (для ПК и для облака Streamlit)
api_key = os.environ.get("RAPIDAPI_KEY") or st.secrets.get("RAPIDAPI_KEY")

st.set_page_config(page_title="Калькулятор цен США", layout="centered")

st.title("🏡 Калькулятор стоимости недвижимости в США")
st.subheader("Оценка объектов в реальном времени")

st.info("Пример формата: 5500 Grand Lake Dr, San Antonio, TX 78244")
address = st.text_input("Введите точный адрес объекта:", "5500 Grand Lake Dr, San Antonio, TX")

if st.button("Узнать актуальную цену объектов", type="primary"):
    if not api_key:
        st.error("Критическая ошибка: RAPIDAPI_KEY не настроен в конфигурации сервера.")
    else:
        # Исправленный правильный URL эндпоинта базы данных
        url = "https://rapidapi.com"
        querystring = {"address": address, "limit": 1}
        headers = {
            "X-RapidAPI-Host": "realty-mole-property-value.p.rapidapi.com",
            "X-RapidAPI-Key": api_key
        }
        
        with st.spinner("Связываемся с американскими базами данных Zillow/RealtyMole..."):
            try:
                response = requests.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                    except Exception:
                        st.error("Ошибка: Сервер прислал некорректный формат данных вместо JSON.")
                        st.code(response.text[:500])
                        st.stop()
                    
                    # Разбираем список объектов, который возвращает эндпоинт /properties
                    if data and isinstance(data, list) and len(data) > 0:
                        property_info = data[0]
                        price = property_info.get("price") or property_info.get("value")
                        if price:
                            st.success(f"🔥 Актуальная рыночная стоимость: **${int(price):,}**")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Спальни", property_info.get("bedrooms", "—"))
                            with col2:
                                st.metric("Ванные", property_info.get("bathrooms", "—"))
                            with col3:
                                st.metric("Площадь (sqft)", f"{property_info.get('squareFootage', '—'):,}" if property_info.get('squareFootage') else "—")
                        else:
                            st.warning("Объект найден, но точная цена не определена.")
                    else:
                        st.error("Данные по этому адресу не найдены. Убедитесь, что указали город и штат.")
                elif response.status_code == 403:
                    st.error("Ошибка авторизации (403): Ваш аккаунт на RapidAPI не подписан на этот тариф. Проверьте вкладку 'Pricing' у Realty Mole API.")
                elif response.status_code == 404:
                    st.error("Ошибка 404: Данный адрес не найден в базе.")
                else:
                    st.error(f"Сервер вернул код ошибки: {response.status_code}")
                    st.text(response.text[:300])
            except Exception as e:
                st.error(f"Техническая ошибка подключения: {str(e)}")
