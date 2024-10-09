import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')
pd.options.display.max_columns = 999

url = 'https://raw.githubusercontent.com/Hairul008/Project-Analisis-Data/main/hour.csv'
data = pd.read_csv(url)

# Title of the dashboard
st.title("🚲 Dashboard Penggunaan Sepeda Berbagi")

# Convert 'dteday' column to datetime objects
data['dteday'] = pd.to_datetime(data['dteday'])

# Sidebar for user inputs
st.sidebar.header("Pengaturan Dashboard")
st.sidebar.text("Silakan pilih opsi berikut untuk menampilkan informasi.")

# Select the date range from the available dates
min_date = data['dteday'].min().date()
max_date = data['dteday'].max().date()

# Use date_input with min and max date
date_range = st.sidebar.date_input("Pilih rentang tanggal:", 
                                     [min_date, max_date], 
                                     min_value=min_date, 
                                     max_value=max_date)

# Filter data based on selected date range
filtered_data = data[(data['dteday'] >= pd.to_datetime(date_range[0])) & 
                     (data['dteday'] <= pd.to_datetime(date_range[1]))]

# Display data information
st.subheader("Informasi Dataset")
st.write(filtered_data.head())
st.write("Dimensi dataset:", filtered_data.shape)
st.write(filtered_data.dtypes)
st.write("Missing values per column:")
st.write(filtered_data.isnull().sum())

# Data preprocessing
filtered_data.fillna(method='ffill', inplace=True)

# Ensure 'hr' is an integer or numeric value representing the hour
filtered_data['hr'] = filtered_data['hr'].astype(int)

# Calculate hourly usage
hourly_usage = filtered_data.groupby('hr')['cnt'].sum()

# Plot hourly usage
st.subheader("📈 Pola Penggunaan Sepeda Berbagi Sepanjang Hari")
fig1, ax1 = plt.subplots()
sns.lineplot(x=hourly_usage.index, y=hourly_usage.values, ax=ax1, color='blue', marker='o')
ax1.set_title('Pola Penggunaan Sepeda Berbagi Sepanjang Hari')
ax1.set_xlabel('Jam')
ax1.set_ylabel('Jumlah Penggunaan Sepeda')
plt.grid(True)
st.pyplot(fig1)

# Correlation heatmap
st.subheader("🔍 Korelasi antara Faktor-faktor dengan Jumlah Penggunaan Sepeda")
numerical_features = filtered_data.select_dtypes(include=['number'])
fig2, ax2 = plt.subplots(figsize=(12, 8))
sns.heatmap(numerical_features.corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax2)
plt.title('Korelasi antara Faktor-faktor dengan Jumlah Penggunaan Sepeda')
st.pyplot(fig2)

# Menghitung jumlah hari sejak sepeda terakhir digunakan
filtered_data['date'] = pd.to_datetime(filtered_data['dteday'])  # Kolom tanggal
current_date = filtered_data['date'].max()  # Mendapatkan tanggal terakhir dalam dataset
filtered_data['days_since_last_ride'] = (current_date - filtered_data['date']).dt.days  # Recency

# Visualisasi Recency
st.subheader("📊 Distribusi Recency (Hari Sejak Penggunaan Terakhir)")
fig3, ax3 = plt.subplots(figsize=(10, 6))  # Mengatur ukuran gambar
sns.histplot(filtered_data['days_since_last_ride'], bins=20, kde=False, ax=ax3, color='green')  # Menghapus kde
ax3.set_title('Distribusi Recency (Hari Sejak Penggunaan Terakhir)')
ax3.set_xlabel('Hari Sejak Penggunaan Terakhir')
ax3.set_ylabel('Frekuensi')
plt.grid(True)
st.pyplot(fig3)  # Menggunakan Streamlit untuk menampilkan grafik

# Menghitung frekuensi penggunaan sepeda per hari
daily_frequency = filtered_data.groupby('date')['cnt'].sum()  # Pastikan menggunakan kolom 'date' untuk konsistensi

# Visualisasi Frekuensi Harian
st.subheader("📅 Frekuensi Penggunaan Sepeda Harian")
fig4, ax4 = plt.subplots(figsize=(10, 6))  # Menyesuaikan ukuran gambar
sns.lineplot(x=daily_frequency.index, y=daily_frequency.values, ax=ax4, color='gold', marker='o')  # Sesuai dengan hasil kode visualisasi
ax4.set_title('Frekuensi Penggunaan Sepeda Harian')
ax4.set_xlabel('Tanggal')
ax4.set_ylabel('Total Penggunaan Sepeda')
ax4.grid(True)
st.pyplot(fig4)  # Menampilkan gambar dalam Streamlit


# Monetary visualization (assumes 'cnt' is a proxy for value)
monetary = filtered_data.groupby('dteday')['cnt'].sum()

# Visualize monetary
st.subheader("💰 Distribusi Penggunaan Sepeda Harian (Monetary)")
fig5, ax5 = plt.subplots()
sns.histplot(monetary, bins=20, kde=True, ax=ax5, color='purple')
ax5.set_title('Distribusi Penggunaan Sepeda Harian (Monetary)')
ax5.set_xlabel('Total Penggunaan Sepeda')
ax5.set_ylabel('Frekuensi')
plt.grid(True)
st.pyplot(fig5)

# RFM score calculation
filtered_data['R_Score'] = pd.qcut(filtered_data['days_since_last_ride'], 5, labels=range(5, 0, -1))
filtered_data['F_Score'] = pd.qcut(daily_frequency.rank(method='first'), 5, labels=range(1, 6))
filtered_data['M_Score'] = pd.qcut(monetary.rank(method='first'), 5, labels=range(1, 6))
filtered_data['RFM_Score'] = filtered_data['R_Score'].astype(str) + filtered_data['F_Score'].astype(str) + filtered_data['M_Score'].astype(str)

# Visualizing usage levels
filtered_data['usage_level'] = pd.cut(filtered_data['cnt'], 
                             bins=[0, 100, 200, 300, 400, filtered_data['cnt'].max()], 
                             labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
usage_level_counts = filtered_data['usage_level'].value_counts()

# Visualize usage levels
st.subheader("📊 Distribusi Penggunaan Sepeda Berdasarkan Level Penggunaan")
fig6, ax6 = plt.subplots(figsize=(10, 6))
sns.barplot(x=usage_level_counts.index, y=usage_level_counts.values, palette='coolwarm', ax=ax6)
ax6.set_title('Distribusi Penggunaan Sepeda Berdasarkan Level Penggunaan')
ax6.set_xlabel('Level Penggunaan Sepeda')
ax6.set_ylabel('Jumlah Penggunaan')
plt.grid(True)
st.pyplot(fig6)

# Add footer
st.markdown("---")
st.markdown("Data diperoleh dari dataset bike sharing.")
