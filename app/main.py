import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(
    page_title="African Climate Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 African Climate Trend Analysis")
st.markdown("### Exploratory Dashboard for COP32 Climate Evidence")
st.markdown("---")

@st.cache_data
def load_data():
    countries = ["Ethiopia", "Kenya", "Sudan", "Tanzania", "Nigeria"]
    dfs = []
    for country in countries:
        filepath = f"data/{country.lower()}_clean.csv"
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df["Country"] = country
            df["Date"] = pd.to_datetime(df["Date"])
            dfs.append(df)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return None

df_all = load_data()

if df_all is None:
    st.error("Data not found. Please ensure clean CSV files are in the data/ folder.")
    st.stop()

st.sidebar.title("Dashboard Controls")
st.sidebar.markdown("---")

all_countries = ["Ethiopia", "Kenya", "Sudan", "Tanzania", "Nigeria"]

select_all = st.sidebar.checkbox("Select All Countries", value=True)

if select_all:
    selected_countries = all_countries
else:
    selected_countries = st.sidebar.radio(
        "Select a Country",
        options=all_countries
    )
    selected_countries = [selected_countries]

min_year = int(df_all["Date"].dt.year.min())
max_year = int(df_all["Date"].dt.year.max())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

variable_options = {
    "Mean Temperature (T2M)": "T2M",
    "Max Temperature (T2M_MAX)": "T2M_MAX",
    "Min Temperature (T2M_MIN)": "T2M_MIN",
    "Precipitation (PRECTOTCORR)": "PRECTOTCORR",
    "Relative Humidity (RH2M)": "RH2M",
    "Wind Speed (WS2M)": "WS2M",
}
selected_variable_label = st.sidebar.selectbox(
    "Select Variable",
    options=list(variable_options.keys())
)
selected_variable = variable_options[selected_variable_label]

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Source:** NASA POWER Database")
st.sidebar.markdown("**Period:** Jan 2015 - Mar 2026")
st.sidebar.markdown("**Program:** 10 Academy KAIM9")

df_filtered = df_all[
    (df_all["Country"].isin(selected_countries)) &
    (df_all["Date"].dt.year >= year_range[0]) &
    (df_all["Date"].dt.year <= year_range[1])
]

if df_filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

st.markdown("## Key Climate Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_temp = df_filtered["T2M"].mean()
    st.metric("Average Temperature", f"{avg_temp:.1f}C")

with col2:
    max_temp = df_filtered["T2M_MAX"].max()
    st.metric("Max Temperature Recorded", f"{max_temp:.1f}C")

with col3:
    avg_precip = df_filtered["PRECTOTCORR"].mean()
    st.metric("Avg Daily Precipitation", f"{avg_precip:.2f} mm")

with col4:
    extreme_days = len(df_filtered[df_filtered["T2M_MAX"] > 35])
    st.metric("Extreme Heat Days (>35C)", f"{extreme_days:,}")

st.markdown("---")

st.markdown("## Temperature Trend Over Time")

colors_map = {
    "Ethiopia": "tomato",
    "Kenya": "steelblue",
    "Sudan": "orange",
    "Tanzania": "green",
    "Nigeria": "purple"
}

fig1, ax1 = plt.subplots(figsize=(14, 5))
for country in selected_countries:
    country_data = df_filtered[df_filtered["Country"] == country]
    monthly = country_data.groupby(
        country_data["Date"].dt.to_period("M"))[selected_variable].mean()
    monthly.index = monthly.index.to_timestamp()
    ax1.plot(monthly.index, monthly.values,
             label=country,
             color=colors_map.get(country, "gray"),
             linewidth=1.5)

ax1.set_title(f"Monthly Average {selected_variable_label} ({year_range[0]}-{year_range[1]})")
ax1.set_xlabel("Date")
ax1.set_ylabel(selected_variable_label)
ax1.legend(loc="upper left")
ax1.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig1)
plt.close()

st.markdown("---")
st.markdown("## Precipitation Distribution by Country")

fig2, ax2 = plt.subplots(figsize=(12, 5))
data_to_plot = []
labels = []
box_colors = []

for country in selected_countries:
    country_data = df_filtered[df_filtered["Country"] == country]
    data_to_plot.append(country_data["PRECTOTCORR"].dropna().values)
    labels.append(country)
    box_colors.append(colors_map.get(country, "gray"))

bp = ax2.boxplot(data_to_plot, labels=labels, patch_artist=True)
for patch, color in zip(bp["boxes"], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax2.set_title("Precipitation Distribution by Country")
ax2.set_xlabel("Country")
ax2.set_ylabel("Precipitation (mm/day)")
ax2.grid(True, alpha=0.3, axis="y")
plt.tight_layout()
st.pyplot(fig2)
plt.close()

st.markdown("---")
st.markdown("## Climate Summary Table")

summary = df_filtered.groupby("Country").agg(
    Mean_Temp=("T2M", "mean"),
    Max_Temp=("T2M_MAX", "max"),
    Avg_Precip=("PRECTOTCORR", "mean"),
    Avg_Humidity=("RH2M", "mean")
).round(2).reset_index()

summary.columns = ["Country", "Mean Temp (C)",
                   "Max Temp (C)", "Avg Precip (mm)", "Avg Humidity (%)"]
st.dataframe(summary, use_container_width=True)

st.markdown("---")
st.markdown("Dashboard built for 10 Academy KAIM9 Week 0 | Data: NASA POWER")

