import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Load Data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(base_dir, "main_data.csv"))
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")

date_range = st.sidebar.date_input(
    "Rentang Tanggal",
    value=(df['dteday'].min().date(), df['dteday'].max().date()),
    min_value=df['dteday'].min().date(),
    max_value=df['dteday'].max().date()
)

weather_filter = st.sidebar.multiselect(
    "Kondisi Cuaca", df['weathersit'].unique(), default=df['weathersit'].unique()
)

season_filter = st.sidebar.multiselect(
    "Musim", df['season'].unique(), default=df['season'].unique()
)

day_type_filter = st.sidebar.multiselect(
    "Tipe Hari", df['day_type'].unique(), default=df['day_type'].unique()
)

# Apply Filters
start_date, end_date = (date_range if len(date_range) == 2
                        else (df['dteday'].min().date(), df['dteday'].max().date()))

df_filtered = df[
    (df['dteday'].dt.date >= start_date) &
    (df['dteday'].dt.date <= end_date) &
    (df['weathersit'].isin(weather_filter)) &
    (df['season'].isin(season_filter)) &
    (df['day_type'].isin(day_type_filter))
]

# Validation
st.title("🚲 Bike Sharing Dashboard")

if df_filtered.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter. Silakan ubah kriteria di sidebar.")
    st.stop()

# KPI
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rental",      f"{int(df_filtered['cnt'].sum()):,}")
col2.metric("Rata-rata Harian",  f"{int(df_filtered['cnt'].mean()):,}")
col3.metric("Max Rental / Hari", f"{int(df_filtered['cnt'].max()):,}")
col4.metric("Jumlah Hari",       f"{len(df_filtered):,}")

st.divider()

# Bar Chart
def bar_chart(data, x, y, title):
    colors = ["#3284bf" if v == data[y].max() else "#72add7" for v in data[y]]
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(data[x], data[y], color=colors)
    ax.bar_label(bars, fmt='%.0f', padding=3)
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.tick_params(axis='x', rotation=30)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Chart row1
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🌤️ Cuaca vs Penyewaan")
    weather_avg = df_filtered.groupby('weathersit')['cnt'].mean().sort_values(ascending=False).reset_index()
    bar_chart(weather_avg, "weathersit", "cnt", "Rata-rata per Kondisi Cuaca")

with col_b:
    st.subheader("🍂 Musim vs Penyewaan")
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_avg = df_filtered.groupby('season')['cnt'].mean().reindex(season_order).dropna().reset_index()
    bar_chart(season_avg, "season", "cnt", "Rata-rata per Musim")

st.divider()

# Chart row2
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("📅 Hari vs Penyewaan")
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_avg = df_filtered.groupby('weekday')['cnt'].mean().reindex(weekday_order).dropna().reset_index()
    bar_chart(weekday_avg, "weekday", "cnt", "Rata-rata per Hari")

with col_d:
    st.subheader("💼 Tipe Hari vs Penyewaan")
    day_type_avg = df_filtered.groupby('day_type')['cnt'].mean().sort_values(ascending=False).reset_index()
    bar_chart(day_type_avg, "day_type", "cnt", "Working Day vs Weekend")

st.divider()

# Monthly Trend
st.subheader("📈 Monthly Trend")

month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
monthly_avg = df_filtered.groupby('month')['cnt'].mean().reindex(month_order).dropna()

fig, ax = plt.subplots(figsize=(12, 4))
sns.lineplot(x=monthly_avg.index, y=monthly_avg.values, marker='o', linewidth=2.5, ax=ax)
ax.grid(True, linestyle='--', alpha=0.5)
for x, y in zip(monthly_avg.index, monthly_avg.values):
    ax.annotate(f'{y:,.0f}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan")
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)