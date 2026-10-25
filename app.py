import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.datasets import fetch_california_housing
import joblib
import os

st.set_page_config(page_title="Аналитика недвижимости", layout="wide")
st.title("📊 Умный дашборд недвижимости крупных городов Калифорнии")

@st.cache_data
def load_data():
    california = fetch_california_housing(as_frame=True)
    df = california.frame
    
    # Переводим названия колонок на русский язык для таблицы
    translations = {
        'MedInc': 'Средний доход (в $10к)',
        'HouseAge': 'Возраст дома (лет)',
        'AveRooms': 'Среднее число комнат',
        'AveBedrms': 'Среднее число спален',
        'Population': 'Население района',
        'AveOccup': 'Средняя заселенность',
        'Latitude': 'Широта (Latitude)',
        'Longitude': 'Долгота (Longitude)',
        'MedHouseVal': 'Цена дома (в $100к)'
    }
    return df.rename(columns=translations)

df = load_data()

tab1, tab2 = st.tabs(["📈 Аналитика и Графики", "🤖 Калькулятор стоимости (ИИ)"])

with tab1:
    st.subheader("Реальные данные с рынка")
    # Отображаем таблицу с красивыми русскими заголовками
    st.dataframe(df.head(10))
    
    st.subheader("Карта стоимости жилья в Калифорнии")
    df_sample = df.sample(n=2000, random_state=42)
    
    # В графике используем уже русские названия колонок
    fig_map = px.scatter_map(df_sample, lat="Широта (Latitude)", lon="Долгота (Longitude)", color="Цена дома (в $100к)", 
                             size="Среднее число комнат", color_continuous_scale=px.colors.cyclical.IceFire, 
                             size_max=15, zoom=5, map_style="open-street-map",
                             title="Цены на жилье (красный — дорого, синий — дешево)")
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    st.subheader("Умный калькулятор стоимости на базе географии мегаполисов и ML")
    
    location = st.selectbox(
        "Выберите город/локацию объекта:", 
        [
            "Сан-Франциско (San Francisco)", 
            "Лос-Анджелес (Los Angeles)", 
            "Сан-Диего (San Diego)",
            "Сан-Хосе / Кремниевая долина (San Jose)",
            "Сакраменто / Столица (Sacramento)",
            "Сельская местность (Фермерские долины)"
        ],
        help="💡 Учтите, что в мегаполисах самые новые дома зачастую НЕ самые дорогие! "
             "Новостройки возводят на дешевых окраинах, где еще осталась земля. "
             "В то же время земля в историческом центре или у океана стоит космических денег, "
             "поэтому локация определяет до 80% стоимости объекта."
    )
    
    if "Сан-Франциско" in location:
        lat, lon = 37.7749, -122.4194
    elif "Лос-Анджелес" in location:
        lat, lon = 34.0522, -118.2437
    elif "Сан-Диего" in location:
        lat, lon = 32.7157, -117.1611
    elif "Сан-Хосе" in location:
        lat, lon = 37.3382, -121.8863
    elif "Сакраменто" in location:
        lat, lon = 38.5816, -121.4944
    else:
        lat, lon = 36.5000, -119.5000 
        
    med_inc = st.number_input(
        "Средний доход жителей района (в десятках тысяч $, например 6.5 = $65,000 в год):", 
        min_value=0.5, max_value=15.0, value=5.5, step=0.1,
        help="💵 Это главный фактор для ИИ. Престижность района напрямую зависит от доходов "
             "его резидентов. Чем богаче соседи — тем дороже и ликвиднее недвижимость вокруг."
    )
    
    house_age = st.slider(
        "Возраст дома (лет):", 
        min_value=1, max_value=52, value=15,
        help="🏠 Парадокс: старые дома в Калифорнии часто стоят ДОРОЖЕ новых. "
             "Учтите, что первые исторические дома строились в самых лакомых местах (у океана или в даунтауне). "
             "Из-за жестких законов о сохранении облика городов их нельзя снести, что создает дефицит "
             "и разгоняет ценность старинных зданий."
    )
    
    ave_rooms = st.slider(
        "Количество комнат в доме:", 
        min_value=1, max_value=10, value=4,
        help="🚪 Среднее число комнат на одно домохозяйство. Чтобы ИИ не путал элитные "
             "городские квартиры (где комнат мало, но они дорогие) с огромными фермерскими "
             "щитовыми домами в глубинке, мы применили математический баланс признаков (Room Value)."
    )
    
    if st.button("Рассчитать честную стоимость"):
        if os.path.exists('price_model.pkl'):
            model = joblib.load('price_model.pkl')
            
            room_value = ave_rooms * med_inc
            
            user_data = pd.DataFrame([[med_inc, house_age, ave_rooms, room_value, lat, lon]], 
                                     columns=['MedInc', 'HouseAge', 'AveRooms', 'Room_Value', 'Latitude', 'Longitude'])
            
            prediction = model.predict(user_data)
            real_price = prediction * 100000
            clean_price = float(real_price)
            
            st.success(f"🏠 Прогноз ИИ для локации '{location}': **${max(clean_price, 15000):,.0f}**")
        else:
            st.error("❌ Сначала обучите модель в файле train_model.py!")



