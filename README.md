# 🚲 Bike Sharing Database Dashboard ✨

Proyek ini adalah dashboard interaktif untuk menganalisis pola penggunaan sepeda berbagi berdasarkan dataset yang tersedia secara publik. Dashboard ini dibangun menggunakan **Streamlit** dan menampilkan berbagai visualisasi seperti pola penggunaan sepanjang hari, korelasi antar faktor, dan distribusi penggunaan harian.

## Fitur Utama Dashboard:
- **Pola Penggunaan Sepanjang Hari**: Visualisasi grafik penggunaan sepeda di berbagai jam dalam sehari.
- **Korelasi Antar Faktor**: Heatmap yang menunjukkan korelasi antara variabel seperti suhu, kelembaban, dan kecepatan angin dengan penggunaan sepeda.
- **Distribusi Recency**: Menampilkan berapa lama sejak sepeda terakhir kali digunakan dalam bentuk histogram.
- **Frekuensi Penggunaan Harian**: Grafik yang menunjukkan tren penggunaan sepeda setiap harinya.
- **Distribusi Penggunaan (Monetary)**: Analisis nilai penggunaan sepeda berbagi per hari.
- **Level Penggunaan**: Pengelompokan jumlah penggunaan sepeda ke dalam kategori (Very Low, Low, Medium, High, Very High).

## Setup Environment

### 1. Menggunakan Anaconda
Langkah-langkah berikut akan memandu Anda dalam menyiapkan environment menggunakan **Anaconda**:

# Buat environment baru dengan Python versi 3.9
```bash
conda create --name bike-sharing python=3.9
```

# Aktifkan environment
```bash
conda activate bike-sharing
```

# Install dependencies yang diperlukan
```bash
pip install -r requirements.txt
```


### 2: Menggunakan Shell/Terminal (Pipenv)

```bash
# Buat direktori baru untuk proyek
mkdir proyek_analisis_data

# Masuk ke direktori proyek
cd proyek_analisis_data

# Inisialisasi environment baru dengan pipenv
pipenv install

# Aktifkan shell pipenv
pipenv shell

# Install dependencies dari requirements.txt
pip install -r requirements.txt
```

## Menjalankan Aplikasi Streamlit

```bash
streamlit run dashboard.py
```