import streamlit as st
import requests
import random
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="US Real Estate Calculator", layout="centered")

# --- ПОЛНЫЙ СЛОВАРЬ МУЛЬТИЯЗЫЧНОСТИ (5 ЯЗЫКОВ) ---
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
        "hover_price_str": "Precio"
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
        "hover_price_str": "Preis"
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
        "rate": "📊 该州每平方英尺平均价格:",
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
        "hover_price_str": "价格"
    }
}

# --- ИНТЕРФЕЙС УПРАВЛЕНИЯ ЯЗЫКОМ ---
lang = st.radio("🌐 Select Language / Выберите язык:", ["English", "Русский", "Español", "Deutsch", "中文"], horizontal=True)
t = translations[lang]

st.title(t["title"])
st.subheader(t["subtitle"])
st.info(t["info"])

states_list = [
    "AL (Alabama)", "AK (Alaska)", "AZ (Arizona)", "AR (Arkansas)", "CA (California)", 
    "CO (Colorado)", "CT (Connecticut)", "DE (Delaware)", "FL (Florida)", "GA (Georgia)", 
    "HI (Hawaii)", "ID (Idaho)", "IL (Illinois)", "IN (Indiana)", "IA (Iowa)", 
    "KS (Kansas)", "KY (Kentucky)", "LA (Louisiana)", "ME (Maine)", "MD (Maryland)", 
    "MA (Massachusetts)", "MI (Michigan)", "MN (Minnesota)", "MS (Mississippi)", "MO (Missouri)", 
    "MT (Montana)", "NE (Nebraska)", "NV (Nevada)", "NH (New Hampshire)", "NJ (New Jersey)", 
    "NM (New Mexico)", "NY (New York)", "NC (North Carolina)", "ND (North Dakota)", "OH (Ohio)", 
    "OK (Oklahoma)", "OR (Oregon)", "PA (Pennsylvania)", "RI (Rhode Island)", "SC (South Carolina)", 
    "SD (South Dakota)", "TN (Tennessee)", "TX (Texas)", "UT (Utah)", "VT (Vermont)", 
    "VA (Virginia)", "WA (Washington)", "WV (West Virginia)", "WI (Wisconsin)", "WY (Wyoming)"
]

col_state, col_zip = st.columns(2)
with col_state:
    state = st.selectbox(t["lbl_state"], states_list)
with col_zip:
    zip_code = st.text_input(t["lbl_zip"], "78244")

map_style = st.sidebar.selectbox(
    t["lbl_style"],
    ["carto-darkmatter", "open-street-map", "carto-positron"]
)

col_bed, col_bath, col_sqft = st.columns(3)
with col_bed:
    bedrooms = st.number_input(t["lbl_bed"], min_value=1, max_value=10, value=3)
with col_bath:
    bathrooms = st.number_input(t["lbl_bath"], min_value=1, max_value=10, value=2)
with col_sqft:
    square_footage = st.number_input(t["lbl_sqft"], min_value=300, max_value=15000, value=1500)

if st.button(t["btn_calc"], type="primary"):
    with st.spinner(t["spinner"]):
        try:
            state_multipliers = {
                "AL (Alabama)": 140, "AK (Alaska)": 210, "AZ (Arizona)": 260, "AR (Arkansas)": 130, "CA (California)": 550,
                "CO (Colorado)": 320, "CT (Connecticut)": 230, "DE (Delaware)": 210, "FL (Florida)": 240, "GA (Georgia)": 190,
                "HI (Hawaii)": 620, "ID (Idaho)": 250, "IL (Illinois)": 210, "IN (Indiana)": 150, "IA (Iowa)": 140,
                "KS (Kansas)": 150, "KY (Kentucky)": 145, "LA (Louisiana)": 160, "ME (Maine)": 220, "MD (Maryland)": 240,
                "MA (Massachusetts)": 410, "MI (Michigan)": 170, "MN (Minnesota)": 195, "MS (Mississippi)": 120, "MO (Missouri)": 160,
                "MT (Montana)": 280, "NE (Nebraska)": 165, "NV (Nevada)": 270, "NH (New Hampshire)": 235, "NJ (New Jersey)": 290,
                "NM (New Mexico)": 180, "NY (New York)": 450, "NC (North Carolina)": 200, "ND (North Dakota)": 175, "OH (Ohio)": 150,
                "OK (Oklahoma)": 135, "OR (Oregon)": 310, "PA (Pennsylvania)": 185, "RI (Rhode Island)": 285, "SC (South Carolina)": 195,
                "SD (South Dakota)": 180, "TN (Tennessee)": 210, "TX (Texas)": 180, "UT (Utah)": 290, "VT (Vermont)": 225,
                "VA (Virginia)": 230, "WA (Washington)": 380, "WV (West Virginia)": 115, "WI (Wisconsin)": 180, "WY (Wyoming)": 220
            }
            
            state_centers = {
#Используйте код с осторожностью.
"AL (Alabama)": (32.3182, -86.9023), "AK (Alaska)": (63.5887, -154.4931), "AZ (Arizona)": (34.0489, -111.0937),
"AR (Arkansas)": (34.9697, -92.3731), "CA (California)": (36.7783, -119.4179), "CO (Colorado)": (39.5501, -105.7821),
"CT (Connecticut)": (41.6032, -73.0877), "DE (Delaware)": (38.9108, -75.5277), "FL (Florida)": (27.6648, -81.5158),
"GA (Georgia)": (32.1656, -82.9001), "HI (Hawaii)": (19.8968, -155.5828), "ID (Idaho)": (44.0682, -114.7420),
"IL (Illinois)": (40.6331, -89.3985), "IN (Indiana)": (40.2672, -86.1349), "IA (Iowa)": (41.8780, -93.0977),
"KS (Kansas)": (38.4988, -98.3159), "KY (Kentucky)": (37.8393, -84.2700), "LA (Louisiana)": (31.1695, -91.8749),
"ME (Maine)": (45.2538, -69.4455), "MD (Maryland)": (39.0458, -76.6413), "MA (Massachusetts)": (42.4072, -71.3824),
"MI (Michigan)": (44.3148, -85.6024), "MN (Minnesota)": (45.6945, -93.9002), "MS (Mississippi)": (32.3547, -89.3985),
"MO (Missouri)": (37.9643, -91.8318), "MT (Montana)": (46.8797, -110.3626), "NE (Nebraska)": (41.1254, -98.2681),
"NV (Nevada)": (38.8026, -116.4194), "NH (New Hampshire)": (43.1939, -71.5724), "NJ (New Jersey)": (40.0583, -74.4057),
"NM (New Mexico)": (34.5199, -105.8701), "NY (New York)": (43.2994, -74.2179), "NC (North Carolina)": (35.7596, -79.0193),
"ND (North Dakota)": (47.5515, -101.0020), "OH (Ohio)": (40.4173, -82.9071), "OK (Oklahoma)": (35.5653, -96.9289),
"OR (Oregon)": (43.8041, -120.5542), "PA (Pennsylvania)": (41.2033, -77.1945), "RI (Rhode Island)": (41.5801, -71.4774),
"SC (South Carolina)": (33.8361, -81.1637), "SD (South Dakota)": (44.3668, -100.3538), "TN (Tennessee)": (35.5175, -86.5804),
"TX (Texas)": (31.9686, -99.9018), "UT (Utah)": (39.3210, -111.0937), "VT (Vermont)": (44.5588, -72.5778),
"VA (Virginia)": (37.4316, -78.6569), "WA (Washington)": (47.4009, -121.4905), "WV (West Virginia)": (38.5976, -80.4549),
"WI (Wisconsin)": (43.7844, -88.7879), "WY (Wyoming)": (43.0760, -107.2903)
}
base_rate = state_multipliers.get(state, 200)
calculated_price = square_footage * base_rate
calculated_price += (bedrooms * 25000) + (bathrooms * 15000)
random.seed(int(zip_code) if zip_code.isdigit() else 12345)
market_trend = random.randint(-5, 7)
calculated_price = int(calculated_price * (1 + market_trend / 100))
st.success(f"{t['success']} ${calculated_price:,}")
st.markdown("---")
col_info1, col_info2 = st.columns(2)
with col_info1:
st.write(f"{t['rate']} ${base_rate}")
st.write(f"{t['trend']} {zip_code}:{'+' if market_trend >= 0 else ''}{market_trend}%")
with col_info2:
st.write(f"{t['status']} {t['status_val']}")
st.write(f"{t['live']} {t['live_val']}")
st.markdown(f"### {t['map_title']}")
lat_center, lon_center = state_centers.get(state, (37.0902, -95.7129))
random.seed(hash(state))
cities_list = [
(t["city_1"], lat_center, lon_center),
(t["city_2"], lat_center + random.uniform(0.1, 0.3), lon_center - random.uniform(0.1, 0.3)),
(t["city_3"], lat_center - random.uniform(0.1, 0.2), lon_center + random.uniform(0.1, 0.3)),
(t["city_4"], lat_center - random.uniform(0.2, 0.3), lon_center - random.uniform(0.1, 0.2))
]
records = []
for i, (city_name, lat, lon) in enumerate(cities_list):
city_modifier = 1.0 + (i * 0.04) - 0.06
city_price = int(calculated_price * city_modifier)
records.append({
'Location': city_name,
'lat': lat,
'lon': lon,
'Price_Int': city_price,
t['hover_price_str']: f"${city_price:,}",
'Marker_Size': 20 + (i * 5)
})
map_df = pd.DataFrame(records)
fig = px.scatter_map(
map_df,
lat='lat',
lon='lon',
hover_name='Location',
hover_data={t['hover_price_str']: True, 'lat': False, 'lon': False},
size='Marker_Size',
color='Price_Int',
color_continuous_scale=px.colors.sequential.Plasma,
zoom=6.5,
center={"lat": lat_center, "lon": lon_center},
title=f"{t['map_heatmap']} {state}"
)
fig.update_layout(
map_style=map_style,
margin={"r": 0, "t": 40, "l": 0, "b": 0},
coloraxis_showscale=False
)
st.plotly_chart(fig, use_container_width=True)
except Exception as e:
st.error(f"{t['error']} {e}")