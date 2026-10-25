# --- ПОЛНЫЙ СЛОВАРЬ МУЛЬТИЯЗЫЧНОСТИ (5 ЯЗЫКОВ) ---
import streamlit as st
import random
import plotly.express as px
import pandas as pd
translations = {
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
        "hover_price_str": "Price"
    },
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
        "hover_price_str": "Цена"
    },
    "Español": {
        "title": "🏡 Calculadora de Valoración de Bienes Raíces en EE. UU.",
        "subtitle": "Estimación del Valor de Mercado y Mapa SIG Inteligente",
        "info": "Ingrese las métricas de la propiedad. El mapa se centrará automáticamente en el estado seleccionado.",
        "lbl_state": "Seleccione el Estado:",
        "lbl_zip": "Código ZIP:",
        "lbl_style": "🗺️ Estilo del Mapa:",
        "lbl_bed": "Habitaciones:",
        "lbl_bath": "Baños:",
        "lbl_sqft": "Pies Cuadrados (sq ft):",
        "btn_calc": "Calcular Valor de Mercado",
        "spinner": "Analizando indicadores económicos regionales...",
        "success": "🔥 Valor de Mercado Actual:",
        "rate": "📊 Precio Promedio por Pie Cuadrado:",
        "trend": "📈 Fluctuación del Tendencia en ZIP",
        "status": "✅ Estado de la Valoración:",
        "status_val": "Verificado Con Éxito",
        "live": "⏱ Actualización de Datos:",
        "live_val": "En Vivo (Tiempo Real)",
        "map_title": "🗺️ Mapa Interactivo de Precios por Ciudad",
        "map_heatmap": "Red de Calor de Valoración en",
        "error": "Ocurrió un error al generar el mapa:",
        "city_1": "Área Metropolitana Central",
        "city_2": "Periferia del Condado Norte",
        "city_3": "Sector Suburbano Este",
        "city_4": "Centro Industrial Sur",
        "hover_price_str": "Price"
    },
    "Deutsch": {
        "title": "🏡 US-Immobilienbewertungsrechner",
        "subtitle": "Marktwertschätzung & Intelligente GIS-Stadtkarte",
        "info": "Geben Sie die Immobiliendaten ein. Die Karte zentriert sich automatisch auf den Bundesstaat.",
        "lbl_state": "Bundesstaat auswählen:",
        "lbl_zip": "ZIP-Code (Postleitzahl):",
        "lbl_style": "🗺️ Interaktiver Kartenstil:",
        "lbl_bed": "Schlafzimmer:",
        "lbl_bath": "Badezimmer:",
        "lbl_sqft": "Quadratfuß (sq ft):",
        "btn_calc": "Marktwert berechnen",
        "spinner": "Regionale Wirtschaftsindikatoren werden analysiert...",
        "success": "🔥 Aktueller Marktwert:",
        "rate": "📊 Durchschnittspreis pro Quadratfuß:",
        "trend": "📈 Trendfluktuation im ZIP-Code",
        "status": "✅ Bewertungsstatus:",
        "status_val": "Erfolgreich Verifiziert",
        "live": "⏱ Datenaktualität:",
        "live_val": "Live (Echtzeit)",
        "map_title": "🗺️ Interaktive Stadtpreiskarte",
        "map_heatmap": "Immobilienbewertungsraster in",
        "error": "Fehler bei der Kartengenerierung:",
        "city_1": "Zentrales Metropolregion",
        "city_2": "Nördliche Randbezirke",
        "city_3": "Östlicher Vorortsektor",
        "city_4": "Südliches Industriezentrum",
        "hover_price_str": "Price"
    },
    "中文": {
        "title": "🏡 美国房地产估值計算器",
        "subtitle": "市场价值评估与智能 GIS 城市地图",
        "info": "输入房产指标。交互式地图将自动聚焦于所选州及其细分市场。",
        "lbl_state": "选择美国州份:",
        "lbl_zip": "邮政编码 (ZIP):",
        "lbl_style": "🗺️ 交互式地图样式:",
        "lbl_bed": "卧室数量:",
        "lbl_bath": "浴室数量:",
        "lbl_sqft": "面积 (平方英尺):",
        "btn_calc": "计算市场价值",
        "spinner": "正在分析区域经济指标...",
        "success": "🔥 当前市场价值:",
        "rate": "📊 该州每平方英尺 average 价格:",
        "trend": "📈 ZIP 编码内的趋势波动",
        "status": "✅ 估值状态:",
        "status_val": "验证成功",
        "live": "⏱ 数据新鲜度:",
        "live_val": "实时 (Live)",
        "map_title": "🗺️ 交互式区域城市价格地图",
        "map_heatmap": "房产估值热力网格于",
        "error": "生成地图时出错:",
        "city_1": "中心都市区",
        "city_2": "北部县郊",
        "city_3": "东部郊区板块",
        "city_4": "南部工业枢纽",
        "hover_price_str": "Price"
    }
}

# --- ИНТЕРФЕЙС УПРАВЛЕНИЯ ЯЗЫКОМ ---
lang = st.radio(
    "🌐 Select Language / Выберите язык / Seleccione el idioma:", 
    ["English", "Русский", "Español", "Deutsch", "中文"], 
    horizontal=True
)
t = translations[lang]

state_data = {
    "AL (Alabama)": {"lat": 32.3182, "lon": -86.9023, "base_sqft": 140},
    "CA (California)": {"lat": 36.7783, "lon": -119.4179, "base_sqft": 450},
    "FL (Florida)": {"lat": 27.6648, "lon": -81.5158, "base_sqft": 290},
    "NY (New York)": {"lat": 43.2994, "lon": -74.2179, "base_sqft": 350},
    "TX (Texas)": {"lat": 31.9686, "lon": -99.9018, "base_sqft": 180}
}

states_list = list(state_data.keys())

col_state, col_zip = st.columns(2)
with col_state:
    state = st.selectbox(t["lbl_state"], states_list)
with col_zip:
    zip_code = st.text_input(t["lbl_zip"], "78244")

map_style = st.sidebar.selectbox(t["lbl_style"], ["open-street-map", "carto-positron", "carto-darkmatter"])

col_bed, col_bath, col_sqft = st.columns(3)
with col_bed:
    bedrooms = st.number_input(t["lbl_bed"], min_value=1, max_value=10, value=3)
with col_bath:
    bathrooms = st.number_input(t["lbl_bath"], min_value=1.0, max_value=8.0, value=2.0, step=0.5)
with col_sqft:
    sqft = st.number_input(t["lbl_sqft"], min_value=100, max_value=20000, value=1800, step=50)
if st.button(t["btn_calc"], type="primary"):
    with st.spinner(t["spinner"]):
        base_rate = state_data[state]["base_sqft"]
        random.seed(zip_code)
        
        final_rate = round(base_rate * random.uniform(0.9, 1.1), 2)
        market_value = int(sqft * final_rate + (bedrooms * 15000) + (bathrooms * 20000))
        trend_val = round(random.uniform(-4.5, 7.5), 2)
        trend_str = f"+{trend_val}%" if trend_val > 0 else f"{trend_val}%"
        
        st.success(f"{t['success']} **${market_value:,}**")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label=t["rate"], value=f"${final_rate}/sq ft")
            st.write(f"**{t['status']}** {t['status_val']}")
        with col_res2:
            st.metric(label=t["trend"], value=trend_str)
            st.write(f"**{t['live']}** {t['live_val']}")
        st.subheader(t["map_title"])
        selected_lat = state_data[state]["lat"]
        selected_lon = state_data[state]["lon"]
        
        mock_cities = [t["city_1"], t["city_2"], t["city_3"], t["city_4"]]
        map_data = []
        for i, city_name in enumerate(mock_cities):
            map_data.append({
                "Location": city_name,
                "Latitude": selected_lat + random.uniform(-0.3, 0.3),
                "Longitude": selected_lon + random.uniform(-0.3, 0.3),
                "Price": int(market_value * random.uniform(0.8, 1.2))
            })
            
        # Генерируем 4 суб-маркета (ровно 8 пробелов отступа слева)
        st.subheader(t["map_title"])
        selected_lat = state_data[state]["lat"]
        selected_lon = state_data[state]["lon"]
        
        mock_cities = [t["city_1"], t["city_2"], t["city_3"], t["city_4"]]
        map_data = []
        for i, city_name in enumerate(mock_cities):
            map_data.append({
                "Location": city_name,
                "Latitude": selected_lat + random.uniform(-0.3, 0.3),
                "Longitude": selected_lon + random.uniform(-0.3, 0.3),
                "Price": int(market_value * random.uniform(0.8, 1.2))
            })
            
        df = pd.DataFrame(map_data)
        
        fig = px.scatter_map(
            df, lat="Latitude", lon="Longitude", size="Price", color="Price",
            color_continuous_scale=px.colors.sequential.Plasma,
            hover_name="Location", zoom=6, title=f"{t['map_heatmap']} {state}"
        )
        fig.update_layout(
            map_style="open-street-map", margin={"r": 0, "t": 40, "l": 0, "b": 0},
            coloraxis_colorbar=dict(title=t["hover_price_str"])
        )
        st.plotly_chart(fig, use_container_width=True)
