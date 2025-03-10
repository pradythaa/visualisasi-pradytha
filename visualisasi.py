import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from IPython.display import HTML
import seaborn as sns

# Baca data
df = pd.read_csv('data_kriminal.csv')

# Siapkan data regional (tanpa Indonesia)
df_without_indonesia = df[df['Kepolisian Daerah'] != 'INDONESIA'].copy()

# Hitung pertumbuhan
df_without_indonesia['Pertumbuhan 2021-2022 (%)'] = ((df_without_indonesia['2022'] - df_without_indonesia['2021']) / df_without_indonesia['2021'] * 100).round(1)
df_without_indonesia['Pertumbuhan 2022-2023 (%)'] = ((df_without_indonesia['2023'] - df_without_indonesia['2022']) / df_without_indonesia['2022'] * 100).round(1)

# Fungsi untuk menyimpan grafik sebagai gambar base64
def get_image_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    return img_str

# Buat HTML untuk menampilkan semua visualisasi
html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Visualisasi Data Kriminal Indonesia (2021-2023)</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #333;
        }
        .chart-container {
            margin: 30px 0;
            text-align: center;
        }
        .chart-img {
            max-width: 100%;
            height: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Visualisasi Data Statistik Kriminal Indonesia (2021-2023)</h1>
        <p>Analisis data statistik kriminal di Indonesia berdasarkan data Kepolisian Daerah tahun 2021-2023.</p>
'''

# ---- Visualisasi 1: Top 10 daerah dengan kriminalitas tertinggi 2023 ----
plt.figure(figsize=(12, 8))
top10_2023 = df_without_indonesia.sort_values('2023', ascending=False).head(10)
sns.barplot(x='2023', y='Kepolisian Daerah', data=top10_2023)
plt.title('10 Daerah dengan Tingkat Kriminalitas Tertinggi (2023)', fontsize=14)
plt.xlabel('Jumlah Kasus', fontsize=12)
plt.ylabel('Daerah', fontsize=12)
for i, v in enumerate(top10_2023['2023']):
    plt.text(v + 1000, i, f"{v:,}", va='center')
plt.tight_layout()

html_content += f'''
        <div class="chart-container">
            <h2>10 Daerah dengan Tingkat Kriminalitas Tertinggi (2023)</h2>
            <img class="chart-img" src="data:image/png;base64,{get_image_base64(plt.gcf())}" alt="Top 10 Daerah">
        </div>
'''
plt.close()

# ---- Visualisasi 2: Tren kriminalitas Indonesia ----
plt.figure(figsize=(10, 6))
indonesia_data = df[df['Kepolisian Daerah'] == 'INDONESIA']
years = ['2021', '2022', '2023']
crime_values = indonesia_data[years].values.flatten()
plt.plot(years, crime_values, marker='o', linewidth=3, markersize=10, color='darkred')
plt.title('Tren Total Kriminalitas di Indonesia (2021-2023)', fontsize=14)
plt.xlabel('Tahun', fontsize=12)
plt.ylabel('Jumlah Kasus', fontsize=12)
for i, v in enumerate(crime_values):
    plt.text(i, v + 10000, f"{v:,}", ha='center')
plt.grid(True, alpha=0.3)
plt.tight_layout()

html_content += f'''
        <div class="chart-container">
            <h2>Tren Total Kriminalitas di Indonesia (2021-2023)</h2>
            <img class="chart-img" src="data:image/png;base64,{get_image_base64(plt.gcf())}" alt="Tren Kriminalitas">
        </div>
'''
plt.close()

# ---- Visualisasi 3: Pertumbuhan kriminalitas tertinggi ----
plt.figure(figsize=(12, 8))
top_growth = df_without_indonesia.sort_values('Pertumbuhan 2022-2023 (%)', ascending=False).head(10)
sns.barplot(x='Pertumbuhan 2022-2023 (%)', y='Kepolisian Daerah', data=top_growth, palette='Reds')
plt.title('10 Daerah dengan Pertumbuhan Kriminalitas Tertinggi (2022-2023)', fontsize=14)
plt.xlabel('Pertumbuhan (%)', fontsize=12)
plt.ylabel('Daerah', fontsize=12)
for i, v in enumerate(top_growth['Pertumbuhan 2022-2023 (%)']):
    plt.text(v + 1, i, f"{v}%", va='center')
plt.tight_layout()

html_content += f'''
        <div class="chart-container">
            <h2>10 Daerah dengan Pertumbuhan Kriminalitas Tertinggi (2022-2023)</h2>
            <img class="chart-img" src="data:image/png;base64,{get_image_base64(plt.gcf())}" alt="Pertumbuhan Tertinggi">
        </div>
'''
plt.close()

# ---- Visualisasi 4: Heatmap ----
plt.figure(figsize=(12, 10))
top15_regions = df_without_indonesia.sort_values('2023', ascending=False).head(15)
heatmap_data = top15_regions.set_index('Kepolisian Daerah')[['2021', '2022', '2023']]
sns.heatmap(heatmap_data, annot=True, fmt=",", cmap='YlOrRd')
plt.title('Tren Kriminalitas di 15 Daerah Tertinggi (2021-2023)', fontsize=14)
plt.ylabel('Daerah', fontsize=12)
plt.xlabel('Tahun', fontsize=12)
plt.tight_layout()

html_content += f'''
        <div class="chart-container">
            <h2>Tren Kriminalitas di 15 Daerah Tertinggi (2021-2023)</h2>
            <img class="chart-img" src="data:image/png;base64,{get_image_base64(plt.gcf())}" alt="Heatmap">
        </div>
'''
plt.close()

# ---- Tabel Statistik ----
summary_stats = df_without_indonesia[['2021', '2022', '2023', 'Pertumbuhan 2021-2022 (%)', 'Pertumbuhan 2022-2023 (%)']].describe().round(1)
stats_html = summary_stats.to_html(classes='stats-table')

html_content += f'''
        <div class="chart-container">
            <h2>Statistik Ringkasan Data Kriminal</h2>
            {stats_html}
        </div>
'''

# ---- Analisis Pulau ----
# Definisikan kelompok pulau
island_groups = {
    'Jawa': ['METRO JAYA', 'JAWA BARAT', 'JAWA TENGAH', 'DI YOGYAKARTA', 'JAWA TIMUR', 'BANTEN'],
    'Sumatera': ['ACEH', 'SUMATERA UTARA', 'SUMATERA BARAT', 'RIAU', 'JAMBI', 'SUMATERA SELATAN', 
                'BENGKULU', 'LAMPUNG', 'KEP. BANGKA BELITUNG', 'KEP. RIAU'],
    'Kalimantan': ['KALIMANTAN BARAT', 'KALIMANTAN TENGAH', 'KALIMANTAN SELATAN', 
                   'KALIMANTAN TIMUR', 'KALIMANTAN UTARA'],
    'Sulawesi': ['SULAWESI UTARA', 'SULAWESI TENGAH', 'SULAWESI SELATAN', 
                'SULAWESI TENGGARA', 'GORONTALO', 'SULAWESI BARAT'],
    'Indonesia Timur': ['BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR', 
                         'MALUKU', 'MALUKU UTARA', 'PAPUA BARAT', 'PAPUA']
}

# Buat data pulau
island_data = []
for group, regions in island_groups.items():
    group_data = df_without_indonesia[df_without_indonesia['Kepolisian Daerah'].isin(regions)]
    for year in ['2021', '2022', '2023']:
        island_data.append({
            'Kelompok Pulau': group,
            'Tahun': year,
            'Total Kasus': group_data[year].sum()
        })

island_df = pd.DataFrame(island_data)

# Visualisasi pulau
plt.figure(figsize=(12, 8))
sns.barplot(x='Kelompok Pulau', y='Total Kasus', hue='Tahun', data=island_df, palette='Blues')
plt.title('Perbandingan Kriminalitas berdasarkan Kelompok Pulau (2021-2023)', fontsize=14)
plt.xlabel('Kelompok Pulau', fontsize=12)
plt.ylabel('Total Kasus', fontsize=12)
plt.legend(title='Tahun')
plt.tight_layout()

html_content += f'''
        <div class="chart-container">
            <h2>Perbandingan Kriminalitas berdasarkan Kelompok Pulau (2021-2023)</h2>
            <img class="chart-img" src="data:image/png;base64,{get_image_base64(plt.gcf())}" alt="Perbandingan Pulau">
        </div>
'''
plt.close()

# Tutup HTML
html_content += '''
    </div>
</body>
</html>
'''

# Simpan HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Visualisasi berhasil dibuat. Silakan buka file index.html")
