import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Hasil Analisis Data", layout="centered")


# Fungsi untuk menampilkan heatmap korelasi
def correlation(df):
    # Pilih kolom yang relevan
    cols = ['month', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    correlation_matrix = df[cols].corr()
    
    # Buat figure untuk plotting
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title("Korelasi antara polutan dan kondisi meteorologi")
    
    st.subheader("Tabel Korelasi antara Polutan dan Kondisi Meteorologi")
    st.pyplot(fig)

# Fungsi untuk visualisasi rata-rata polutan per bulan
def pollutant_avg(df, selectedYear):
    # Pastikan nilai tahun dalam bentuk integer
    year = int(selectedYear)
    filtered_df = df[df['year'] == year]
    
    # Daftar polutan
    pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
    
    # Hitung rata-rata per bulan untuk tiap polutan
    monthly_avg = filtered_df.groupby('month')[pollutants].mean().reset_index().sort_values('month')
    
    # Standarisasi data (Z-score)
    monthly_avg_scaled = monthly_avg.copy()
    for col in pollutants:
        monthly_avg_scaled[col] = (monthly_avg_scaled[col] - monthly_avg_scaled[col].mean()) / monthly_avg_scaled[col].std()
    
    # Buat figure untuk plotting
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=monthly_avg_scaled, x='month', y='PM2.5', marker='o', label='PM2.5', color='blue', ax=ax)
    sns.lineplot(data=monthly_avg_scaled, x='month', y='PM10', marker='o', label='PM10', color='red', ax=ax)
    sns.lineplot(data=monthly_avg_scaled, x='month', y='O3', marker='o', label='O₃', color='green', ax=ax)
    sns.lineplot(data=monthly_avg_scaled, x='month', y='NO2', marker='o', label='NO2', color='orange', ax=ax)
    sns.lineplot(data=monthly_avg_scaled, x='month', y='SO2', marker='o', label='SO2', color='black', ax=ax)
    sns.lineplot(data=monthly_avg_scaled, x='month', y='CO', marker='o', label='CO', color='brown', ax=ax)
    
    ax.set_title(f'Rata-rata Konsentrasi Polutan (Terstandarisasi) per Bulan\nTahun {year}')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Z-score')
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)
    ax.legend()
    ax.grid(True)
    
    st.subheader("Rata-Rata Konsentrasi Polutan")
    st.pyplot(fig)

# Fungsi untuk visualisasi hubungan antara suhu dan O₃
def temp_o3(df, selectedYear, selectedMonth):
    # Konversi parameter ke integer
    year = int(selectedYear)
    month = int(selectedMonth)
    filtered_df = df[(df['year'] == year) & (df['month'] == month)]
    
    # Buat figure untuk plotting
    fig, ax = plt.subplots(figsize=(5, 2))
    sns.regplot(data=filtered_df, x='TEMP', y='O3', scatter=True, ci=None, line_kws={'color': 'red'}, ax=ax)
    ax.set_title(f"Hubungan antara Suhu (TEMP) dan O₃ di Bulan {month} Tahun {year}")
    ax.set_xlabel("Suhu (TEMP)")
    ax.set_ylabel("Konsentrasi O₃")
    ax.grid(True)
    
    st.subheader("Hubungan Antara Suhu dan O₃")
    st.pyplot(fig)

# Load dataset
df = pd.read_csv("main_data.csv", delimiter=",")

# Konfigurasi tampilan dashboard
st.title("AIR QUALITY INDEX DASHBOARD")
st.header("Changping Station")
st.markdown("Dashboard ini menampilkan hasil analisis data terkait kondisi meteorologi dan polutan di stasiun Changping. "
            "Silakan gunakan panel samping untuk menampilkan data sesuai kebutuhan.")


correlation(df)

# Panel Samping (Sidebar) untuk filter
st.sidebar.header("Filter Data")
# Mengambil pilihan tahun berdasarkan data yang tersedia
selectedYear = st.sidebar.selectbox(
    'Pilih Tahun',
    sorted(df['year'].dropna().unique().astype(int).astype(str))
)
selectedMonth = st.sidebar.selectbox(
    'Pilih Bulan',
    ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
)

# Opsi visualisasi yang ingin ditampilkan
viz_choice = st.sidebar.radio(
    "Pilih Visualisasi",
    ("Pollutant Average", "Temperature vs O₃")
)

# Tampilkan visualisasi sesuai pilihan
if viz_choice == "Pollutant Average":
    pollutant_avg(df, selectedYear=selectedYear)
elif viz_choice == "Temperature vs O₃":
    temp_o3(df, selectedYear=selectedYear, selectedMonth=selectedMonth)