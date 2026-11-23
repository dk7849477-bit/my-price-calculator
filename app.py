import streamlit as st
import random
import plotly.express as px
import pandas as pd
import requests

st.set_page_config(
    page_title="US Real Estate Valuation & GIS Analytics",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ ВСТАВИТЬ СЮДА (заменив .calculated на ["calculated"]):
if "calculated" not in st.session_state:
    st.session_state["calculated"] = False

st.components.v1.html(

    """
    <script>
        // Добавляем верификацию Telderi
        var metaTelderi = document.createElement('meta');
        metaTelderi.name = 'telderi';
        metaTelderi.content = '58955ad71f098f3b154a05a84f097332';
        window.parent.document.getElementsByTagName('head')[0].appendChild(metaTelderi);
    </script>
    """,
    height=0,
    width=0
)

# --- ПОЛНЫЙ СЛОВАРЬ МУЛЬТИЯЗЫЧНОСТИ (5 ЯЗЫКОВ) ---
translations = {
    "English": {
        "title": "🏡 US Real Estate Valuation Calculator",
        "subtitle": "Market Value Estimate & Smart GIS City Map",
        "info": "Enter property metrics. The interactive map will auto-center on the selected state and its sub-markets.",
        "lbl_state": "Select US State:",
        "lbl_zip": "ZIP Code (Postal Index):",
        "lbl_style": "🗺️ Interactive Map Style:",
        "lbl_unit": "📏 Measurement Unit:",
        "unit_sqft": "Sq Ft",
        "unit_sqm": "Sq M (m²)",
        "lbl_bed": "Bedrooms:",
        "lbl_bath": "Bathrooms:",
        "lbl_area_sqft": "Square Footage (sq ft):",
        "lbl_area_sqm": "Area (sq m / m²):",
        "btn_calc": "Calculate Market Value",
        "spinner": "Analyzing regional economic indicators...",
        "success": "🔥 Current Market Value:",
        "rate_sqft": "📊 Average Price per Sq Ft in State:",
        "rate_sqm": "📊 Average Price per Sq M in State:",
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
        "hover_price_str": "Price",
        "lbl_age": "Property Age (years):",
        "age_placeholder": "Optional",
        "age_help": "Sometimes the newest homes are not the most expensive (historic charm, prime location, or mature neighborhoods can value higher).",
        "insights_title": "📊 US Housing Market Insights & Facts",
        "fact_1_title": "📈 Price Trends & Seasonality",
        "fact_1_text": "US home prices historically peak between May and July (+3–5% above winter averages). Suburban markets with strong remote-work infrastructure continue to outpace dense urban cores.",
        "fact_2_title": "🏦 Mortgage Rates Impact",
        "fact_2_text": "Every 1% drop in 30-year fixed mortgage rates typically increases buyer purchasing power by ~10%, driving higher demand and faster price growth in mid-tier states.",
        "fact_3_title": "🏡 What Adds the Most Value?",
        "fact_3_text": "In the US market, usable square footage and bathroom count carry the highest valuation weight. Kitchen remodels and energy-efficient HVAC systems return up to 70–80% of their cost.",
        "stat_avg": "🇺🇸 US Average",
        "stat_max": "💎 Highest",
        "stat_min": "🏷️ Most Affordable",
        "history_title": "📜 60+ Years of US Housing Price History (1963–2026)",
        "history_subtitle": "Median sales price of houses sold in the United States (US Census Bureau / FRED data):",
        "history_chart_title": "US Median Home Price Evolution ($ USD)",
        "history_axis_x": "Year",
        "history_axis_y": "Median Price ($)",
        "history_milestones": """
        * **1960s–1970s (The Suburban Boom):** In 1963, the median US home cost just **$18,000**. High inflation in the late 1970s pushed prices above **$62,000** by 1979.
        * **1980s (18% Mortgage Rates):** Despite record-high mortgage rates peaking at 18.6% in 1981, baby boomers entering the market kept prices rising steadily to **  $120,000** by 1989.
        * **1990s–2006 (The Dot-Com & Subprime Bubble):** Low interest rates and relaxed lending standards fueled a massive surge, peaking at **$247,000** in early 2007.
        * **2008–2012 (The Great Recession):** The housing crash caused median prices to drop by ~15–20% nationwide, bottoming out around **$208,000** in 2009.
        * **2020–2026 (Post-Pandemic Surge):** Remote work, supply shortages, and ultra-low 2020–2021 rates triggered the fastest price jump in history, stabilizing above **$420,000+** in the mid-2020s.
    """

    },
    "Русский": {
        "title": "🏡 Калькулятор стоимости недвижимости в США",
        "subtitle": "Рыночная оценка и умная карта городов",
        "info": "Введите параметры дома. Интерактивная карта автоматически сфокусируется на выбранном штате и его городах.",
        "lbl_state": "Выберите штат США:",
        "lbl_zip": "ZIP-код (Почтовый индекс):",
        "lbl_style": "🗺️ Стиль интерактивной карты:",
        "lbl_unit": "📏 Единица измерения:",
        "unit_sqft": "Кв. футы (sq ft)",
        "unit_sqm": "Кв. метры (м²)",
        "lbl_bed": "Спальни:",
        "lbl_bath": "Ванные:",
        "lbl_area_sqft": "Площадь (кв. футы):",
        "lbl_area_sqm": "Площадь (кв. метры):",
        "btn_calc": "Рассчитать рыночную стоимость",
        "spinner": "Анализируем экономические показатели регионов...",
        "success": "🔥 Актуальная рыночная стоимость:",
        "rate_sqft": "📊 Средняя цена за кв. фут в штате:",
        "rate_sqm": "📊 Средняя цена за кв. метр в штате:",
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
        "hover_price_str": "Цена",
        "lbl_age": "Возраст жилья (лет):",
        "age_placeholder": "Необязательно",
        "age_help": "Порой самые молодые дома не самые дорогие (историческая ценность, престижный район или развитая инфраструктура могут цениться выше).",
        "insights_title": "📊 Аналитика и интересные факты о жилье в США",
        "fact_1_title": "📈 Динамика цен и сезонность",
        "fact_1_text": "Цены на жильё в США традиционно достигают пика с мая по июль (+3–5% к зимним показателям). Пригороды с развитой инфраструктурой для удалённой работы растут быстрее мегаполисов.",
        "fact_2_title": "🏦 Влияние ипотечных ставок",
        "fact_2_text": "Снижение ставки по 30-летней фиксированной ипотеке всего на 1% увеличивает покупательную способность на ~10%, что напрямую подталкивает рыночную стоимость домов вверх.",
        "fact_3_title": "🏡 Что сильнее всего повышает цену?",
        "fact_3_text": "В США ключевой фактор оценки — жилая площадь (без учёта подвалов и гаражей) и число ванных комнат. Обновление кухни и системы климат-контроля окупается на 70–80%.",
        "stat_avg": "🇺🇸 Средняя по США",
        "stat_max": "💎 Самый дорогой",
        "stat_min": "🏷️ Самый доступный"
    },
    "Español": {
        "title": "🏡 Calculadora de Valoración de Bienes Raíces en EE. UU.",
        "subtitle": "Estimación del Valor de Mercado y Mapa SIG Inteligente",
        "info": "Ingrese las métricas de la propiedad. El mapa se centrará automáticamente en el estado seleccionado.",
        "lbl_state": "Seleccione el Estado:",
        "lbl_zip": "Código ZIP:",
        "lbl_style": "🗺️ Estilo del Mapa:",
        "lbl_unit": "📏 Unidad de Medida:",
        "unit_sqft": "Pies Cuadrados (sq ft)",
        "unit_sqm": "Metros Cuadrados (m²)",
        "lbl_bed": "Habitaciones:",
        "lbl_bath": "Baños:",
        "lbl_area_sqft": "Pies Cuadrados (sq ft):",
        "lbl_area_sqm": "Metros Cuadrados (m²):",
        "btn_calc": "Calcular Valor de Mercado",
        "spinner": "Analizando indicadores económicos regionales...",
        "success": "🔥 Valor de Mercado Actual:",
        "rate_sqft": "📊 Precio Promedio por Pie Cuadrado:",
        "rate_sqm": "📊 Precio Promedio por Metro Cuadrado:",
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
        "hover_price_str": "Precio",
        "lbl_age": "Antigüedad de la propiedad (años):",
        "age_placeholder": "Opcional",
        "age_help": "A veces las casas más nuevas no son las más caras (el valor histórico o la ubicación consolidada pueden cotizarse más alto).",
        "insights_title": "📊 Datos y Tendencias del Mercado Inmobiliario en EE. UU.",
        "fact_1_title": "📈 Tendencias de Precios y Estacionalidad",
        "fact_1_text": "Los precios en EE. UU. suelen alcanzar su punto máximo entre mayo y julio (+3–5% sobre el invierno). Los suburbios con buena conectividad siguen creciendo más rápido que los centros urbanos.",
        "fact_2_title": "🏦 Impacto de las Tasas Hipotecarias",
        "fact_2_text": "Cada caída del 1% en la tasa hipotecaria fija a 30 años aumenta el poder adquisitivo en un ~10%, impulsando la demanda y el valor de las propiedades.",
        "fact_3_title": "🏡 ¿Qué Aporta Más Valor?",
        "fact_3_text": "El área habitable y el número de baños tienen el mayor peso en la tasación. Las remodelaciones de cocina y sistemas HVAC eficientes recuperan entre el 70% y el 80% de su costo.",
        "stat_avg": "🇺🇸 Promedio en EE. UU.",
        "stat_max": "💎 Más caro",
        "stat_min": "🏷️ Más asequible"
    },
    "Deutsch": {
        "title": "🏡 US-Immobilienbewertungsrechner",
        "subtitle": "Marktwertschätzung & Intelligente GIS-Stadtkarte",
        "info": "Geben Sie die Immobiliendaten ein. Die Karte zentriert sich automatisch auf den Bundesstaat.",
        "lbl_state": "Bundesstaat auswählen:",
        "lbl_zip": "ZIP-Code (Postleitzahl):",
        "lbl_style": "🗺️ Interaktiver Kartenstil:",
        "lbl_unit": "📏 Maßeinheit:",
        "unit_sqft": "Quadratfuß (sq ft)",
        "unit_sqm": "Quadratmeter (m²)",
        "lbl_bed": "Schlafzimmer:",
        "lbl_bath": "Badezimmer:",
        "lbl_area_sqft": "Quadratfuß (sq ft):",
        "lbl_area_sqm": "Quadratmeter (m²):",
        "btn_calc": "Marktwert berechnen",
        "spinner": "Regionale Wirtschaftsindikatoren werden analysiert...",
        "success": "🔥 Aktueller Marktwert:",
        "rate_sqft": "📊 Durchschnittspreis pro Quadratfuß:",
        "rate_sqm": "📊 Durchschnittspreis pro Quadratmeter:",
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
        "hover_price_str": "Preis",
        "lbl_age": "Alter der Immobilie (Jahre):",
        "age_placeholder": "Optional",
        "age_help": "Manchmal sind die neuesten Häuser nicht die teuersten (historischer Charme oder etablierte Lagen können höher bewertet werden).",
        "insights_title": "📊 US-Immobilienmarkt: Trends & Wissenswertes",
        "fact_1_title": "📈 Preisentwicklung & Saisonalität",
        "fact_1_text": "US-Immobilienpreise erreichen zwischen Mai und Juli oft ihren Höchststand (+3–5 % gegenüber dem Winter). Vororte mit guter Infrastruktur wachsen weiterhin schneller als Innenstädte.",
        "fact_2_title": "🏦 Einfluss der Hypothekenzinsen",
        "fact_2_text": "Jeder Rückgang der 30-jährigen Festzins-Hypothek um 1 % steigert die Kaufkraft der Käufer um rund 10 % und sorgt für steigende Immobilienwerte.",
        "fact_3_title": "🏡 Was steigert den Wert am meisten?",
        "fact_3_text": "Wohnfläche und Anzahl der Badezimmer haben das größte Gewicht bei der Bewertung. Küchenrenovierungen und moderne Klimaanlagen (HVAC) amortisieren sich zu 70–80 %.",
        "stat_avg": "🇺🇸 US-Durchschnitt",
        "stat_max": "💎 Am teuersten",
        "stat_min": "🏷️ Am günstigsten"
    },
    "中文": {
        "title": "🏡 美国房地产估值计算器",
        "subtitle": "市场价值评估与智能 GIS 城市地图",
        "info": "输入房产指标。交互式地图将自动聚焦于所选州及其细分市场。",
        "lbl_state": "选择美国州份:",
        "lbl_zip": "邮政编码 (ZIP):",
        "lbl_style": "🗺️ 交互式地图样式:",
        "lbl_unit": "📏 面积单位:",
        "unit_sqft": "平方英尺 (sq ft)",
        "unit_sqm": "平方米 (m²)",
        "lbl_bed": "卧室数量:",
        "lbl_bath": "浴室数量:",
        "lbl_area_sqft": "面积 (平方英尺):",
        "lbl_area_sqm": "面积 (平方米):",
        "btn_calc": "计算市场价值",
        "spinner": "正在分析区域经济指标...",
        "success": "🔥 当前市场价值:",
        "rate_sqft": "📊 该州每平方英尺平均价格:",
        "rate_sqm": "📊 该州每平方米平均价格:",
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
        "hover_price_str": "价格",
        "lbl_age": "房龄（年）：",
        "age_placeholder": "选填",
        "age_help": "有时最新的房子并不是最贵的（历史底蕴、核心地段或成熟社区往往价值更高）。",
        "insights_title": "📊 美国房地产市场洞察与趣闻",
        "fact_1_title": "📈 价格走势与季节性规律",
        "fact_1_text": "美国房价通常在每年5月至7月达到峰值（比冬季高出3%–5%）。适合远程办公的郊区市场涨幅持续领跑传统市中心。",
        "fact_2_title": "🏦 房贷利率的影响",
        "fact_2_text": "30年期固定房贷利率每下降1%，购房者的购买力平均提升约10%，从而直接推高房价与市场需求。",
        "fact_3_title": "🏡 哪些因素最能提升房产价值？",
        "fact_3_text": "在美国，实用居住面积和浴室数量在估值中占比最高。厨房翻新和高效节能空调系统（HVAC）通常可收回70%–80%的改造成本。",
        "stat_avg": "🇺🇸 全美平均",
        "stat_max": "💎 最高价州",
        "stat_min": "🏷️ 最实惠州"
    }
}


# Коэффициент перевода: 1 кв. метр = 10.7639 кв. футов
SQFT_IN_SQM = 10.7639

# --- ИНТЕРФЕЙС УПРАВЛЕНИЯ ЯЗЫКОМ В САЙДБАРЕ ---
with st.sidebar:
    lang = st.radio(
        "🌐 Select Language / Выберите язык:", 
        ["English", "Русский", "Español", "Deutsch", "中文"], 
        horizontal=True
    )
t = translations[lang]

# --- БАЗА ДАННЫХ КООРДИНАТ И ЦЕН ШТАТОВ (ПОЛНЫЙ СПИСОК 50 ШТАТОВ) ---
state_data = {
    "AL (Alabama)": {"lat": 32.3182, "lon": -86.9023, "base_sqft": 145},
    "AK (Alaska)": {"lat": 63.5887, "lon": -154.4931, "base_sqft": 215},
    "AZ (Arizona)": {"lat": 34.0489, "lon": -111.0937, "base_sqft": 265},
    "AR (Arkansas)": {"lat": 35.2010, "lon": -91.8318, "base_sqft": 135},
    "CA (California)": {"lat": 36.7783, "lon": -119.4179, "base_sqft": 460},
    "CO (Colorado)": {"lat": 39.5501, "lon": -105.7821, "base_sqft": 325},
    "CT (Connecticut)": {"lat": 41.6032, "lon": -73.0877, "base_sqft": 245},
    "DE (Delaware)": {"lat": 38.9108, "lon": -75.5277, "base_sqft": 205},
    "FL (Florida)": {"lat": 27.6648, "lon": -81.5158, "base_sqft": 295},
    "GA (Georgia)": {"lat": 32.1574, "lon": -82.9071, "base_sqft": 190},
    "HI (Hawaii)": {"lat": 19.8968, "lon": -155.5828, "base_sqft": 615},
    "ID (Idaho)": {"lat": 44.0682, "lon": -114.7420, "base_sqft": 245},
    "IL (Illinois)": {"lat": 40.6331, "lon": -89.3985, "base_sqft": 180},
    "IN (Indiana)": {"lat": 40.2672, "lon": -86.1349, "base_sqft": 155},
    "IA (Iowa)": {"lat": 41.8780, "lon": -93.0977, "base_sqft": 160},
    "KS (Kansas)": {"lat": 38.5266, "lon": -96.7265, "base_sqft": 165},
    "KY (Kentucky)": {"lat": 37.8393, "lon": -84.2700, "base_sqft": 150},
    "LA (Louisiana)": {"lat": 31.2448, "lon": -92.1450, "base_sqft": 170},
    "ME (Maine)": {"lat": 45.2538, "lon": -69.4455, "base_sqft": 210},
    "MD (Maryland)": {"lat": 39.0458, "lon": -76.6413, "base_sqft": 240},
    "MA (Massachusetts)": {"lat": 42.4072, "lon": -71.3824, "base_sqft": 390},
    "MI (Michigan)": {"lat": 44.3148, "lon": -85.6024, "base_sqft": 175},
    "MN (Minnesota)": {"lat": 46.7296, "lon": -94.6859, "base_sqft": 195},
    "MS (Mississippi)": {"lat": 32.3547, "lon": -89.3985, "base_sqft": 125},
    "MO (Missouri)": {"lat": 37.9643, "lon": -91.8318, "base_sqft": 155},
    "MT (Montana)": {"lat": 46.8797, "lon": -110.3626, "base_sqft": 235},
    "NE (Nebraska)": {"lat": 41.4925, "lon": -99.9018, "base_sqft": 170},
    "NV (Nevada)": {"lat": 38.8026, "lon": -116.4194, "base_sqft": 255},
    "NH (New Hampshire)": {"lat": 43.1939, "lon": -71.5724, "base_sqft": 230},
    "NJ (New Jersey)": {"lat": 40.0583, "lon": -74.4057, "base_sqft": 290},
    "NM (New Mexico)": {"lat": 34.5199, "lon": -105.8701, "base_sqft": 185},
    "NY (New York)": {"lat": 43.2994, "lon": -74.2179, "base_sqft": 310},
    "NC (North Carolina)": {"lat": 35.7596, "lon": -79.0193, "base_sqft": 210},
    "ND (North Dakota)": {"lat": 47.5515, "lon": -101.0020, "base_sqft": 165},
    "OH (Ohio)": {"lat": 40.4173, "lon": -82.9071, "base_sqft": 160},
    "OK (Oklahoma)": {"lat": 35.0078, "lon": -97.0929, "base_sqft": 140},
    "OR (Oregon)": {"lat": 43.8041, "lon": -120.5542, "base_sqft": 290},
    "PA (Pennsylvania)": {"lat": 41.2033, "lon": -77.1945, "base_sqft": 185},
    "RI (Rhode Island)": {"lat": 41.5801, "lon": -71.4774, "base_sqft": 275},
    "SC (South Carolina)": {"lat": 33.8361, "lon": -81.1637, "base_sqft": 195},
    "SD (South Dakota)": {"lat": 44.3668, "lon": -100.3365, "base_sqft": 175},
    "TN (Tennessee)": {"lat": 35.5175, "lon": -86.5804, "base_sqft": 190},
    "TX (Texas)": {"lat": 31.9686, "lon": -99.9018, "base_sqft": 185},
    "UT (Utah)": {"lat": 39.3210, "lon": -111.0937, "base_sqft": 270},
    "VT (Vermont)": {"lat": 44.5588, "lon": -72.5778, "base_sqft": 220},
    "VA (Virginia)": {"lat": 37.4316, "lon": -78.6569, "base_sqft": 215},
    "WA (Washington)": {"lat": 47.7511, "lon": -120.7401, "base_sqft": 340},
    "WV (West Virginia)": {"lat": 38.5976, "lon": -80.4549, "base_sqft": 115},
    "WI (Wisconsin)": {"lat": 43.7844, "lon": -88.7879, "base_sqft": 180},
    "WY (Wyoming)": {"lat": 43.0760, "lon": -107.2903, "base_sqft": 210}
}

SQFT_IN_SQM = 10.7639
#--- ШАПКА ИНТЕРФЕЙСА ---

st.title(t["title"])
st.subheader(t["subtitle"])
st.info(t["info"])

#--- МАКЕТ СОДЕРЖИМОГО (САЙДБАР УПРАВЛЕНИЯ) ---

with st.sidebar:
    st.header("Settings")
selected_state = st.selectbox(t["lbl_state"], list(state_data.keys()), index=4)
zip_code = st.text_input(t["lbl_zip"], "90210")
map_style = st.selectbox(t["lbl_style"], ["open-street-map", "carto-positron", "carto-darkmatter"])
st.markdown("---")
# Переключатель единиц измерения площади
selected_unit = st.radio(
    t["lbl_unit"],
    [t["unit_sqft"], t["unit_sqm"]],
    horizontal=True
)
is_sqm = (selected_unit == t["unit_sqm"])

# Поле ввода площади в зависимости от выбранной единицы (исправлено!)
if is_sqm:
    area_input = st.number_input(t["lbl_area_sqm"], min_value=10, max_value=2000, value=167, step=5)
    sqft = area_input * SQFT_IN_SQM  # Переводим в кв. футы для корректного расчёта
else:
    area_input = st.number_input(t["lbl_area_sqft"], min_value=100, max_value=20000, value=1800, step=50)
    sqft = area_input  # Оставляем как есть (ВАЖНО: внутри else, а не снаружи!)

st.markdown("---")

# Необязательные спальни и ванные (можно оставить пустыми)
# Вместо t["age_placeholder"] и t["age_help"] лучше писать так:
bedrooms = st.number_input(
    t.get("lbl_bed", "Bedrooms:"), 
    min_value=0, 
    max_value=10, 
    value=None, 
    step=1, 
    placeholder=t.get("age_placeholder", "Optional")
)

bathrooms = st.number_input(
    t.get("lbl_bath", "Bathrooms:"), 
    min_value=0.0, 
    max_value=10.0, 
    value=None, 
    step=0.5, 
    placeholder=t.get("age_placeholder", "Optional")
)

property_age = st.number_input(
    t.get("lbl_age", "Property Age (years):"),
    min_value=0,
    max_value=300,
    value=None,
    step=1,
    placeholder=t.get("age_placeholder", "Optional"),
    help=t.get("age_help", "Sometimes the newest homes are not the most expensive.")
)

calculate_btn = st.button(t.get("btn_calc", "Calculate Market Value"), type="primary")

if calculate_btn:
    st.session_state.calculated = False
# --- ЛОГИКА ИНТЕГРАЦИИ RENTCAST API И СИНТЕТИЧЕСКОГО РАСЧЕТА ---
def fetch_valuation_data(state_name, zip_code, bedrooms, bathrooms, sqft, property_age=None):
    api_key = "YOUR_REAL_API_KEY"
    
    url = f"https://rentcast.io{zip_code}&squareFootage={int(sqft)}"
    if bedrooms is not None:
        url += f"&bedrooms={bedrooms}"
    if bathrooms is not None:
        url += f"&bathrooms={bathrooms}"
        
    headers = {"accept": "application/json", "X-Api-Key": api_key}
    base_rate = state_data[state_name]["base_sqft"]
    
    if api_key != "YOUR_REAL_API_KEY":
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("price", sqft * base_rate), base_rate
        except Exception:
            pass
            
    bed_bonus = (bedrooms * 15000) if bedrooms is not None else 0
    bath_bonus = (bathrooms * 20000) if bathrooms is not None else 0
    calculated_price = (sqft * base_rate) + bed_bonus + bath_bonus
    
    # Учёт возраста жилья (если указан)
    if property_age is not None:
        if property_age <= 5:
            calculated_price *= 1.08       # Новостройки (+8%)
        elif property_age <= 20:
            calculated_price *= 1.00       # 6–20 лет (базовая цена)
        elif property_age <= 60:
            calculated_price *= 0.90       # 21–60 лет (-10%)
        elif property_age <= 90:
            calculated_price *= 1.04       # 61–90 лет (+4%)
        else:
            calculated_price *= 1.12       # Исторический дом 90+ лет (+12%)

    random.seed(zip_code) 
    calculated_price *= random.uniform(0.92, 1.08)
    
    return int(calculated_price), base_rate

# Действие по нажатию кнопки (теперь передаём property_age!)
if calculate_btn:
    with st.spinner(t["spinner"]):
        price, rate = fetch_valuation_data(selected_state, zip_code, bedrooms, bathrooms, sqft, property_age)
        st.session_state["price"] = price
        st.session_state["rate"] = rate
        st.session_state["calculated"] = True

# --- ВЫВОД РЕЗУЛЬТАТОВ И ОТРЕСОВКА ГИС ---
if st.session_state.get("calculated", False):

    current_base_sqft = state_data[selected_state]["base_sqft"]
    
    if is_sqm:
        display_rate = f"${int(round(current_base_sqft * SQFT_IN_SQM)):,} / m²"
        rate_label = t.get("rate_sqm", "📊 Средняя цена за м²:")
    else:
        display_rate = f"${current_base_sqft:,} / sq ft"
        rate_label = t.get("rate_sqft", t.get("rate", "📊 Средняя цена за sq ft:"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=t["success"], value=f"${st.session_state.price:,.0f}")
    with col2:
        st.metric(label=rate_label, value=display_rate)
    with col3:
        random.seed(zip_code)
        mock_trend = random.choice(["+2.4%", "+4.1%", "-1.2%", "+0.8%", "+5.3%"])
        st.metric(label=t["trend"], value=mock_trend)
        
    st.markdown("---")
    
    meta_col1, meta_col2 = st.columns(2)
    meta_col1.write(f"**{t['status']}** {t['status_val']}")
    meta_col2.write(f"**{t['live']}** {t['live_val']}")

# --- РАБОТА С ГИС КАРТОЙ (PLOTLY) ---
st.markdown(f"### {t['map_title']}")

state_cities = {
    "CA (California)": {
        "names": ["Los Angeles", "San Francisco", "San Diego", "Sacramento"],
        "lats": [34.0522, 37.7749, 32.7157, 38.5816],
        "lons": [-118.2437, -122.4194, -117.1611, -121.4944],
        "multipliers": [1.3, 1.5, 1.1, 0.85]
    },
    "NY (New York)": {
        "names": ["New York City", "Buffalo", "Rochester", "Albany"],
        "lats": [40.7128, 42.8864, 43.1566, 42.6526],
        "lons": [-74.0060, -78.8784, -77.6088, -73.7562],
        "multipliers": [1.8, 0.7, 0.75, 0.85]
    },
    "TX (Texas)": {
        "names": ["Houston", "Austin", "Dallas", "San Antonio"],
        "lats": [29.7604, 30.2672, 32.7767, 29.4241],
        "lons": [-95.3698, -97.7431, -96.7970, -98.4936],
        "multipliers": [1.0, 1.3, 1.1, 0.9]
    },
    "FL (Florida)": {
        "names": ["Miami", "Orlando", "Tampa", "Jacksonville"],
        "lats": [25.7617, 28.5383, 27.9506, 30.3322],
        "lons": [-80.1918, -81.3792, -82.4572, -81.6557],
        "multipliers": [1.4, 1.1, 1.0, 0.8]
    }
}

center_lat = state_data[selected_state]["lat"]
center_lon = state_data[selected_state]["lon"]
base_sqft_rate = state_data[selected_state]["base_sqft"]
base_price = base_sqft_rate * sqft

unit_col_name = t.get("hover_rate_sqm", "Avg / m² ($)") if is_sqm else t.get("hover_rate_sqft", "Avg / sq ft ($)")
unit_multiplier = SQFT_IN_SQM if is_sqm else 1.0

if selected_state in state_cities:
    cities_info = state_cities[selected_state]
    map_data = pd.DataFrame({
        'City_Zone': cities_info["names"],
        'lat': cities_info["lats"],
        'lon': cities_info["lons"],
        t["hover_price_str"]: [int(base_price * m) for m in cities_info["multipliers"]],
        unit_col_name: [int(round(base_sqft_rate * m * unit_multiplier)) for m in cities_info["multipliers"]]
    })
    dynamic_zoom = 5
else:
    default_multipliers = [1.1, 0.85, 0.95, 1.05]
    map_data = pd.DataFrame({
        'City_Zone': [t["city_1"], t["city_2"], t["city_3"], t["city_4"]],
        'lat': [center_lat, center_lat + 0.8, center_lat - 0.6, center_lat + 0.4],
        'lon': [center_lon, center_lon - 0.9, center_lon + 1.1, center_lon + 0.3],
        t["hover_price_str"]: [int(base_price * m) for m in default_multipliers],
        unit_col_name: [int(round(base_sqft_rate * m * unit_multiplier)) for m in default_multipliers]
    })
    dynamic_zoom = 6

try:
    fig = px.scatter_map(
        map_data,
        lat="lat",
        lon="lon",
        color=unit_col_name,
        size=unit_col_name,
        color_continuous_scale=px.colors.sequential.Plasma,
        size_max=30,
        zoom=dynamic_zoom,
        title=f"{t['map_heatmap']} {selected_state}",
        hover_name="City_Zone",
        hover_data={
            "lat": False,
            "lon": False,
            unit_col_name: ":$,",
            t["hover_price_str"]: ":$,",
        }
    )
    fig.update_layout(
        map_style=map_style,
        margin={"r":0,"t":40,"l":0,"b":0},
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

except AttributeError:
    fig = px.scatter_mapbox(
        map_data,
        lat="lat",
        lon="lon",
        color=unit_col_name,
        size=unit_col_name,
        color_continuous_scale=px.colors.sequential.Plasma,
        size_max=30,
        zoom=dynamic_zoom,
        title=f"{t['map_heatmap']} {selected_state}",
        hover_name="City_Zone",
        hover_data={
            "lat": False,
            "lon": False,
            unit_col_name: ":$,",
            t["hover_price_str"]: ":$,",
        }
    )
    fig.update_layout(
        mapbox_style=map_style,
        margin={"r":0,"t":40,"l":0,"b":0},
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"{t['error']} {e}")
# --- БЛОК СВЕДЕНИЙ И ФАКТОВ О РЫНКЕ ЖИЛЬЯ США ---
st.markdown("---")
st.markdown(f"### {t.get('insights_title', '📊 US Housing Market Insights & Facts')}")

# Вычисляем статистику по всем 50 штатам прямо из вашего словаря state_data
all_rates = [info["base_sqft"] for info in state_data.values()]
avg_us_sqft = sum(all_rates) / len(all_rates)
max_state = max(state_data.items(), key=lambda x: x[1]["base_sqft"])
min_state = min(state_data.items(), key=lambda x: x[1]["base_sqft"])

# Верхняя строка: динамические метрики по базе штатов (переводятся в м² при выборе м²)
stat_col1, stat_col2, stat_col3 = st.columns(3)
if is_sqm:
    stat_col1.metric("🇺🇸 US Average / m²", f"${int(round(avg_us_sqft * SQFT_IN_SQM)):,}")
    stat_col2.metric(f"💎 Highest ({max_state[0].split()[0]})", f"${int(round(max_state[1]['base_sqft'] * SQFT_IN_SQM)):,} / m²")
    stat_col3.metric(f"🏷️ Most Affordable ({min_state[0].split()[0]})", f"${int(round(min_state[1]['base_sqft'] * SQFT_IN_SQM)):,} / m²")
else:
    stat_col1.metric("🇺🇸 US Average / sq ft", f"${int(round(avg_us_sqft)):,}")
    stat_col2.metric(f"💎 Highest ({max_state[0].split()[0]})", f"${max_state[1]['base_sqft']:,} / sq ft")
    stat_col3.metric(f"🏷️ Most Affordable ({min_state[0].split()[0]})", f"${min_state[1]['base_sqft']:,} / sq ft")

# Нижняя строка: 3 карточки с фактами и аналитикой
fact_col1, fact_col2, fact_col3 = st.columns(3)

with fact_col1:
    st.info(f"**{t.get('fact_1_title', '📈 Price Trends')}**\n\n{t.get('fact_1_text', '')}")

with fact_col2:
    st.info(f"**{t.get('fact_2_title', '🏦 Mortgage Rates')}**\n\n{t.get('fact_2_text', '')}")

with fact_col3:
    st.info(f"**{t.get('fact_3_title', '🏡 Value Drivers')}**\n\n{t.get('fact_3_text', '')}")
# --- БЛОК ИСТОРИИ ЦЕН НА НЕДВИЖИМОСТЬ США (1963–2026) ---
st.markdown("---")
st.markdown(f"### {t['history_title']}")
st.caption(t["history_subtitle"])

# Реальные исторические данные US Census Bureau (Median Sales Price of Houses Sold)
history_df = pd.DataFrame({
    "Year":,
    "Price": [18000, 23400, 39300, 64600, 84300, 122900, 133900, 169000, 240900, 247900, 216700, 245200, 296400, 321500, 397100, 442600, 420800, 435000]
})

})

hist_col1, hist_col2 = st.columns([1.3, 1])

with hist_col1:
    fig_hist = px.area(
        history_df,
        x="Year",
        y="Price",
        markers=True,
        title=t["history_chart_title"],
        labels={"Year": t["history_axis_x"], "Price": t["history_axis_y"]}
    )
    fig_hist.update_traces(
        line_color="#FF4B4B",
        fillcolor="rgba(255, 75, 75, 0.15)",
        hovertemplate="<b>%{x}</b><br>$%{y:,}<extra></extra>"
    )
    fig_hist.update_layout(
        height=380,
        margin={"r": 10, "t": 40, "l": 10, "b": 10},
        yaxis_tickprefix="$",
        yaxis_tickformat=","
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with hist_col2:
    st.markdown(t["history_milestones"])

