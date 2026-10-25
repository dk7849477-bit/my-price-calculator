import streamlit as st
import requests
import random
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="US Real Estate Calculator", layout="centered")

# --- СЛОВАРЬ МУЛЬТИЯЗЫЧНОСТИ ---
translations = {
    "Русский": {
        "title": "🏡 Калькулятор стоимости недвижимости в США",
        "subtitle": "Рыночная оценка и умная карта городов",
        "info": "Введите параметры дома. Интерактивная карта автоматически сфокусируется на выбранном штате и его городах.",
        "lbl_state": "Выберите штат США:",
        "lbl_zip": "ZIP-код (Почтовый индекс):",
        "lbl_style": "🗺️ Стиль интерактивной карты:",
        "lbl_bed": "Спальни:",
        "lbl_bath": "Ванные:",
        "lbl_sqft": "Площадь (кв. футы):",
        "btn_calc": "Рассчитать рыночную стоимость",
        "spinner": "Анализируем экономические показатели регионов...",
        "success": "🔥 Актуальная рыночная стоимость:",
        "rate": "📊 Средняя цена за кв. фут в штате:",
        "trend": "📈 Динамика тренда в ZIP",
        "status": "✅ Статус текущей оценки:",
        "status_val": "Успешно подтверждено",
        "live": "⏱ Актуальность данных:",
        "live_val": "В данный момент (Live)",
        "map_title": "🗺️ Интерактивная карта цен по городам региона",
        "map_heatmap": "Тепловая сетка стоимости объектов в",
        "error": "Произошла ошибка при генерации карты:",
        "city_1": "Центральная агломерация",
        "city_2": "Северный округ мегаполиса",
        "city_3": "Восточный пригородный сектор",
        "city_4": "Южный индустриальный хаб",
        "hover_price": "Рыночная цена",
        "hover_price_str": "Цена"
    },
    "English": {
        "title": "🏡 US Real Estate Valuation Calculator",
        "subtitle": "Market Value Estimate & Smart GIS City Map",
        "info": "Enter property metrics. The interactive map will auto-center on the selected state and its sub-markets.",
        "lbl_state": "Select US State:",
        "lbl_zip": "ZIP Code (Postal Index):",
        "lbl_style": "🗺️ Interactive Map Style:",
        "lbl_bed": "Bedrooms:",
        "lbl_bath": "Bathrooms:",
        "lbl_sqft": "Square Footage (sq ft):",
        "btn_calc": "Calculate Market Value",
        "spinner": "Analyzing regional economic indicators...",
        "success": "🔥 Current Market Value:",
        "rate": "📊 Average Price per Sq Ft in State:",
        "trend": "📈 Trend Fluctuation in ZIP",
        "status": "✅ Valuation Status:",
        "status_val": "Successfully Verified",
        "live": "⏱ Data Freshness:",
        "live_val": "Live (Real-Time)",
        "map_title": "🗺️ Interactive Regional City Price Map",
        "map_heatmap": "Property Valuation Heat Grid in",
        "error": "An error occurred during map generation:",
        "city_1": "Central Metro Area",
        "city_2": "North County Outskirts",
        "city_3": "East Suburban Sector",
        "city_4": "South Industrial Hub",
        "hover_price": "Market Value",
        "hover_price_str": "Price"
    }
}

# --- ПЕРЕКЛЮЧАТЕЛЬ ЯЗЫКА ТЕПЕРЬ ПО ЦЕНТРУ ЭКРАНА ВВЕРХУ ---
lang = st.radio("🌐 Choose Language / Выберите язык:", ["English", "Русский"], horizontal=True)
t = translations[lang]

# Дальше идут ваши стандартные заголовки, которые теперь зависят от выбранного языка:
st.title(t["title"])
st.subheader(t["subtitle"])
st.info(t["info"])

# ... (весь остальной код калькулятора и карты остается без изменений)

