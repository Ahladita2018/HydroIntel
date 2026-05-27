import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="🌊 HydroIntel",
    layout="wide"
)
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 1rem;
}

h1 {
    color: #00B4D8;
}

h2, h3 {
    color: #0077B6;
}

div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.stAlert {
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)
# =====================================================
# TITLE
# =====================================================

st.markdown("""
# 🌊 HydroIntel
            
### India Water Scarcity Intelligence Platform

**Predict • Analyze • Prevent**
            
""")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🌊 HydroIntel")
st.caption(
    "AI-powered decision support system "
    "for monitoring water scarcity across India"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "District Intelligence",
        "Scenario Simulator",
        "AI Prediction",
        "Risk Map",
        "Model Insights"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info("""
### About

AI-powered platform for:

- Water scarcity prediction
- District intelligence
- Risk monitoring
- Scenario simulation
- Early warning alerts
""")

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "master_water_data.csv"
)

# load trained model
model = joblib.load(
    "water_model.pkl"
)

# load scaler
scaler = joblib.load(
    "scaler.pkl"
)

# =====================================================
# DASHBOARD PAGE
# =====================================================

if page == "Dashboard":

    st.header("National Water Risk Overview")

    high_count = len(
        df[df['risk_level'] == 'High']
    )

    medium_count = len(
        df[df['risk_level'] == 'Medium']
    )

    low_count = len(
        df[df['risk_level'] == 'Low']
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🔴 High Risk Districts",
            high_count
        )

    with col2:
        st.metric(
            "🟡 Medium Risk Districts",
            medium_count
        )

    with col3:
        st.metric(
            "🟢 Low Risk Districts",
            low_count
        )

    st.header("🚨 Highest Risk Districts")

    top_10 = (
        df.sort_values(
            by='scarcity_score',
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_10.sort_values(
            by='scarcity_score'
        ),
        x='scarcity_score',
        y='district',
        orientation='h',
        color='scarcity_score',
        color_continuous_scale='Turbo',
        text='scarcity_score'
    )

    fig.update_traces(
        texttemplate='%{text:.2f}',
        textposition='outside'
    )

    fig.update_layout(
        xaxis_title="Scarcity Score",
        yaxis_title="",
        showlegend=False,
        height=500,
        margin=dict(
            l=10,
            r=10,
            t=30,
            b=10
        ),
         paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=14),
        coloraxis_colorbar=dict(
            title="Risk"
        )
    )


    st.plotly_chart(

    fig,
    use_container_width=True
) 
    

    st.header("Key Insights")

    top_risk = top_10.iloc[0]

    st.write(
        f"⚠ Highest Risk District: "
        f"**{top_risk['district'].title()}**"
    )

    st.write(
        "📌 Groundwater stress emerged "
        "as the strongest predictor "
        "of water scarcity."
    )

    st.write(
        "📌 Population pressure "
        "significantly increases risk."
    )
    st.header("📈 National Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"""
            🔴 High Risk Districts:
            **{high_count}**

            ⚠ Medium Risk Districts:
            **{medium_count}**

            ✅ Low Risk Districts:
            **{low_count}**
            """
        )

    with col2:
        avg_score = round(
            df['scarcity_score'].mean(),
            2
        )

        st.info(
            f"""
            📊 Average Scarcity Score:
            **{avg_score}**

            💧 Strongest Predictor:
            **Groundwater Stress**
            """
        )

# =====================================================
# DISTRICT INTELLIGENCE PAGE
# =====================================================

elif page == "District Intelligence":

    st.header("District Intelligence")

    district = st.selectbox(
        "Select District",
        sorted(df['district'].unique())
    )

    district_data = df[
        df['district'] == district
    ].iloc[0]

    st.subheader(
        f"📍 {district.title()}"
    )

    st.caption(
        f"State: "
        f"{district_data['state'].title()}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Rainfall",
            round(
                district_data['avg_rainfall'],
                2
            )
        )

        st.metric(
            "Population",
            int(
                district_data['population']
            )
        )

    with col2:
        st.metric(
            "Groundwater Resource",
            round(
                district_data[
                    'groundwater_resource'
                ],
                2
            )
        )

        st.metric(
            "Groundwater Stress",
            round(
                district_data[
                    'groundwater_stress'
                ],
                2
            )
        )

    with col3:
        st.metric(
            "Scarcity Score",
            round(
                district_data[
                    'scarcity_score'
                ],
                2
            )
        )

        st.metric(
            "Risk Level",
            district_data['risk_level']
        )

    st.progress(
        min(
            district_data[
                'scarcity_score'
            ] / 3,
            1.0
        )
    )

    if district_data['risk_level'] == 'High':
        st.error(
            "⚠ High Water Scarcity Risk"
        )

    elif district_data['risk_level'] == 'Medium':
        st.warning(
            "⚠ Medium Water Stress"
        )

    else:
        st.success(
            "✅ Low Water Scarcity Risk"
        )

    st.header("Recommendations")

    recommendations = []

    if district_data['groundwater_stress'] > 0.7:
        recommendations.append(
            "Increase groundwater recharge initiatives"
        )

    if district_data['avg_rainfall'] < 0.4:
        recommendations.append(
            "Promote rainwater harvesting"
        )

    if district_data['population'] > 0.6:
        recommendations.append(
            "Implement demand-side water management"
        )

    if not recommendations:
        recommendations.append(
            "Current water conditions appear stable"
        )

    for rec in recommendations:
        st.write("•", rec)

# =====================================================
# SCENARIO SIMULATOR
# =====================================================

elif page == "Scenario Simulator":

    st.header("Scenario Simulator")

    district = st.selectbox(
        "Select District",
        sorted(df['district'].unique()),
        key="scenario_district"
    )

    district_data = df[
        df['district'] == district
    ].iloc[0]

    rainfall_change = st.slider(
        "Rainfall Change (%)",
        -50,
        50,
        0
    )

    groundwater_change = st.slider(
        "Groundwater Change (%)",
        -50,
        50,
        0
    )

    population_change = st.slider(
        "Population Change (%)",
        -50,
        50,
        0
    )

    simulated = district_data.copy()

    simulated['avg_rainfall'] *= (
        1 + rainfall_change / 100
    )

    simulated['groundwater_resource'] *= (
        1 + groundwater_change / 100
    )

    simulated['population'] *= (
        1 + population_change / 100
    )

    availability = (
        0.4 * simulated['avg_rainfall']
        + 0.3 * simulated['groundwater_resource']
        + 0.3 * simulated['future_groundwater']
    )

    demand = (
        0.7 * simulated['population']
        + 0.3 * simulated['groundwater_stress']
    )

    new_score = (
        demand /
        (availability + 0.01)
    )

    if new_score < 0.8:
        simulated_risk = "Low"
    elif new_score < 1.5:
        simulated_risk = "Medium"
    else:
        simulated_risk = "High"

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Current Risk",
            district_data['risk_level']
        )

    with col2:
        st.metric(
            "Predicted Risk",
            simulated_risk
        )

    st.metric(
        "New Scarcity Score",
        round(new_score, 2)
    )

# =====================================================
# AI PREDICTION PAGE
# =====================================================

elif page == "AI Prediction":

    st.header("AI Risk Prediction")

    col1, col2 = st.columns(2)

    with col1:
        rainfall_input = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            value=700.0
        )

        groundwater_input = st.number_input(
            "Groundwater Resource",
            min_value=0.0,
            value=80000.0
        )

        future_groundwater_input = st.number_input(
            "Future Groundwater",
            min_value=0.0,
            value=20000.0
        )

    with col2:
        groundwater_stress_input = st.number_input(
            "Groundwater Stress (%)",
            min_value=0.0,
            max_value=200.0,
            value=70.0
        )

        population_input = st.number_input(
            "Population",
            min_value=0.0,
            value=1000000.0
        )

    if st.button(
        "Predict Risk",
        key="predict_button"
    ):

        input_data = pd.DataFrame([[
            rainfall_input,
            groundwater_input,
            future_groundwater_input,
            groundwater_stress_input,
            population_input
        ]], columns=[
            'avg_rainfall',
            'groundwater_resource',
            'future_groundwater',
            'groundwater_stress',
            'population'
        ])

        input_scaled = scaler.transform(
            input_data
        )

        prediction = model.predict(
            input_scaled
        )[0]

        if prediction == "High":
            st.error(
                "🚨 Predicted Risk: HIGH"
            )

        elif prediction == "Medium":
            st.warning(
                "⚠ Predicted Risk: MEDIUM"
            )

        else:
            st.success(
                "✅ Predicted Risk: LOW"
            )

# =====================================================
# RISK MAP PAGE
# =====================================================

elif page == "Risk Map":

    st.header("🗺 India Water Scarcity Map")

    # average scarcity by state
    state_avg = (
        df.groupby('state')['scarcity_score']
        .mean()
        .reset_index()
    )

    # proper state name mapping
    state_name_fixes = {
        'andhrapradesh': 'Andhra Pradesh',
        'arunachalpradesh': 'Arunachal Pradesh',
        'assam': 'Assam',
        'bihar': 'Bihar',
        'chhattisgarh': 'Chhattisgarh',
        'goa': 'Goa',
        'gujarat': 'Gujarat',
        'haryana': 'Haryana',
        'himachalpradesh': 'Himachal Pradesh',
        'jharkhand': 'Jharkhand',
        'karnataka': 'Karnataka',
        'kerala': 'Kerala',
        'madhyapradesh': 'Madhya Pradesh',
        'maharashtra': 'Maharashtra',
        'manipur': 'Manipur',
        'meghalaya': 'Meghalaya',
        'mizoram': 'Mizoram',
        'nagaland': 'Nagaland',
        'odisha': 'Odisha',
        'orissa': 'Odisha',
        'punjab': 'Punjab',
        'rajasthan': 'Rajasthan',
        'sikkim': 'Sikkim',
        'tamilnadu': 'Tamil Nadu',
        'telangana': 'Telangana',
        'tripura': 'Tripura',
        'uttarakhand': 'Uttarakhand',
        'uttarpradesh': 'Uttar Pradesh',
        'westbengal': 'West Bengal',
        'jammukashmir': 'Jammu and Kashmir',
        'delhi': 'Delhi'
    }

    state_avg['state'] = (
        state_avg['state']
        .str.lower()
        .replace(state_name_fixes)
    )

    # GOOD INDIA GEOJSON
    india_geojson = (
        "https://raw.githubusercontent.com/"
        "geohacker/india/master/state/"
        "india_state.geojson"
    )

    fig = px.choropleth(
        state_avg,
        geojson=india_geojson,
        locations="state",
        featureidkey="properties.NAME_1",
        color="scarcity_score",
        hover_name="state",
        color_continuous_scale="Viridis",
        title="Average Water Scarcity by State"
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            t=40,
            b=0
        ),
        height=650
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# MODEL INSIGHTS PAGE
# =====================================================

elif page == "Model Insights":

    st.header("Model Insights")

    importance = pd.DataFrame({
        'Feature': [
            'Rainfall',
            'Groundwater Resource',
            'Future Groundwater',
            'Groundwater Stress',
            'Population'
        ],
        'Importance': model.feature_importances_
    })

    importance = importance.sort_values(
        by='Importance',
        ascending=True
    )

    fig = px.bar(
        importance,
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale='Turbo',
        title='Feature Importance'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    top_feature = (
        importance.iloc[-1]['Feature']
    )

    st.success(
        f"Most influential factor: "
        f"{top_feature}"
    )

    st.write("""
    The model identified groundwater
    stress and population pressure
    as major contributors to water
    scarcity risk.
    """)
st.markdown("---")

st.caption(
    "Built using Python, "
    "Scikit-learn, "
    "Streamlit, Pandas "
    "and Plotly"
)
