if st.button(t["btn_calc"], type="primary"):
    with st.spinner(t["spinner"]):
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
        
        st.success(f"{t['success']} **${calculated_price:,}**")
        st.markdown("---")
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.write(f"{t['rate']} `${base_rate}`")
            st.write(f"{t['trend']} {zip_code}:` {'+' if market_trend >= 0 else ''}{market_trend}% `")
        with col_info2:
            st.write(f"{t['status']} `{t['status_val']}`")
            st.write(f"{t['live']} `{t['live_val']}`")
            
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
