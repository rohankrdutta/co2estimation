import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="India CO₂ Emission Estimator", layout="centered")

st.title("🇮🇳 Exhaustive CO₂ Emission Calculator (India)")
st.markdown("Estimate your **annual carbon footprint** based on Indian lifestyle patterns.")

st.sidebar.title("Customize Your Inputs")

# -----------------------------
# Input Widgets
# -----------------------------

# Electricity
grid_kwh = st.sidebar.number_input("Grid Electricity (kWh/month)", value=150.0)
solar_kwh = st.sidebar.number_input("Solar Offset (kWh/month)", value=0.0)

# Transport
st.sidebar.subheader("Transport (km/week)")
car_km = st.sidebar.number_input("Car", value=20.0)
bike_km = st.sidebar.number_input("2-wheeler", value=10.0)
cab_km = st.sidebar.number_input("Cab/Taxi", value=5.0)
bus_km = st.sidebar.number_input("Bus", value=10.0)
train_km = st.sidebar.number_input("Train", value=5.0)
metro_km = st.sidebar.number_input("Metro", value=5.0)

# Cooking
lpg_cyl = st.sidebar.slider("LPG Cylinders (per year)", 0, 24, 12)
induction_kwh = st.sidebar.number_input("Induction Cooking (kWh/month)", value=20.0)

# Flights
st.sidebar.subheader("Flights (per year)")
dom_flights = st.sidebar.slider("Domestic Flights", 0, 20, 2)
intl_short = st.sidebar.slider("Short-haul Intl Flights", 0, 10, 1)
intl_long = st.sidebar.slider("Long-haul Intl Flights", 0, 5, 1)

# Diet
diet_type = st.sidebar.selectbox("Diet Type", ["Vegetarian", "Eggetarian", "Occasional Meat", "Regular Meat"])
diet_map = {"Vegetarian": 1000, "Eggetarian": 1200, "Occasional Meat": 1500, "Regular Meat": 2000}
diet_emission = diet_map[diet_type]
dairy_ltr = st.sidebar.number_input("Milk & Dairy (litres/week)", value=2.0)

# Digital usage
screen_hr = st.sidebar.number_input("Screen Time (hours/day)", value=3.0)

# Waste
plastic_kg = st.sidebar.number_input("Plastic Waste (kg/month)", value=1.0)
ewaste_kg = st.sidebar.number_input("E-Waste (kg/year)", value=0.5)

# Appliance usage
geyser_hr = st.sidebar.number_input("Geyser Use (hours/day)", value=0.5)
ac_hr = st.sidebar.number_input("A/C Use (hours/day)", value=2.0)

# -----------------------------
# Emission Factors (kg CO2e)
# -----------------------------

factors = {
    "grid_elec": 0.82,
    "car": 0.192,
    "bike": 0.045,
    "cab": 0.2,
    "bus": 0.027,
    "train": 0.015,
    "metro": 0.03,
    "lpg_cylinder": 32,
    "induction": 0.82,
    "flight_dom": 150,
    "flight_intl_short": 400,
    "flight_intl_long": 600,
    "dairy": 1.5,
    "screen": 0.05,
    "plastic": 6,
    "ewaste": 20,
    "geyser_hour": 1.5,
    "ac_hour": 1.6
}

# -----------------------------
# Emissions Calculation
# -----------------------------

elec = max(0, (grid_kwh - solar_kwh)) * 12 * factors["grid_elec"]
trans = 52 * (
    car_km * factors["car"] +
    bike_km * factors["bike"] +
    cab_km * factors["cab"] +
    bus_km * factors["bus"] +
    train_km * factors["train"] +
    metro_km * factors["metro"]
)
cooking = lpg_cyl * factors["lpg_cylinder"] + induction_kwh * 12 * factors["induction"]
flights = dom_flights * factors["flight_dom"] + intl_short * factors["flight_intl_short"] + intl_long * factors["flight_intl_long"]
diet = diet_emission + dairy_ltr * 52 * factors["dairy"]
digital = 365 * screen_hr * factors["screen"]
waste = plastic_kg * 12 * factors["plastic"] + ewaste_kg * factors["ewaste"]
appliances = 365 * (geyser_hr * factors["geyser_hour"] + ac_hr * factors["ac_hour"])

total = elec + trans + cooking + flights + diet + digital + waste + appliances

# -----------------------------
# Results Display
# -----------------------------

st.header("📊 Annual CO₂ Emissions Breakdown (in kg)")
data = {
    "Electricity": elec,
    "Transport": trans,
    "Cooking": cooking,
    "Flights": flights,
    "Diet": diet,
    "Digital": digital,
    "Waste": waste,
    "Appliances": appliances,
    "Total": total,
    "Total (tons)": total / 1000
}
df = pd.DataFrame.from_dict(data, orient="index", columns=["CO₂ (kg)"])
st.dataframe(df)

# Pie Chart
st.subheader("🧩 Emission Distribution")
fig, ax = plt.subplots()
keys = list(data.keys())[:-2]
values = [data[k] for k in keys]
ax.pie(values, labels=keys, autopct="%1.1f%%", startangle=140, colors=plt.cm.tab20.colors)
ax.axis("equal")
st.pyplot(fig)

# Tips
st.markdown("### 🌱 Tips to Reduce Your Footprint")
st.markdown("""
- Switch to energy-efficient appliances (5-star rated).
- Use public transport or EVs.
- Reduce meat and dairy consumption.
- Switch to induction cooking with solar offset.
- Minimize air travel and offset emissions.
- Properly recycle plastic and e-waste.
""")
