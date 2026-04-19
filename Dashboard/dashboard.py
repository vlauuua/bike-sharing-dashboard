import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("dasboard/main_data.csv")

st.title("🚲 Bike Sharing Dashboard")

# SIDEBAR FILTER

st.sidebar.header("Filter Data")

weather_filter = st.sidebar.multiselect(
    "Pilih Cuaca",
    df['weathersit'].unique(),
    default=df['weathersit'].unique()
)

df_filtered = df[df['weathersit'].isin(weather_filter)]

# KPI
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rental", int(df_filtered['cnt'].sum()))
col2.metric("Rata-rata Rental", int(df_filtered['cnt'].mean()))
col3.metric("Max Rental", int(df_filtered['cnt'].max()))

# CUACA VS RENTAL 
st.subheader("🌤️ Cuaca vs Penyewaan")

weather_avg = df_filtered.groupby('weathersit')['cnt'].mean().sort_values(ascending=False)

fig, ax = plt.subplots()
sns.barplot(x=weather_avg.index, y=weather_avg.values, ax=ax)
ax.bar_label(ax.containers[0], fmt='%.0f')

st.pyplot(fig)

# WEEKDAY ANALYSIS
st.subheader("📅 Weekday Analysis")

weekday_avg = df_filtered.groupby('weekday')['cnt'].mean().sort_values(ascending=False)

fig, ax = plt.subplots()
sns.barplot(x=weekday_avg.index, y=weekday_avg.values, ax=ax)

ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
ax.bar_label(ax.containers[0], fmt='%.0f')

st.pyplot(fig)

# MONTHLY TREND 
st.subheader("📈 Monthly Trend")

monthly_avg = df_filtered.groupby('month')['cnt'].mean()
order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
monthly_avg = monthly_avg.reindex(order)

fig, ax = plt.subplots()
sns.lineplot(x=monthly_avg.index, y=monthly_avg.values, marker='o', ax=ax)

ax.plot(monthly_avg.index, monthly_avg.values, marker='o')
ax.grid(True, linestyle='--', alpha=0.5) 
for x, y in zip(monthly_avg.index, monthly_avg.values):
    ax.annotate(
        f'{y:.0f}',
        (x, y),
        textcoords="offset points",
        xytext=(0,8),
        ha='center'
    )

ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig)