import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Membuat dataframe dari data yang diberikan
data = {
    'Kepolisian Daerah': [
        'ACEH', 'SUMATERA UTARA', 'SUMATERA BARAT', 'RIAU', 'JAMBI', 
        'SUMATERA SELATAN', 'BENGKULU', 'LAMPUNG', 'KEP. BANGKA BELITUNG', 
        'KEP. RIAU', 'METRO JAYA', 'JAWA BARAT', 'JAWA TENGAH', 
        'DI YOGYAKARTA', 'JAWA TIMUR', 'BANTEN', 'BALI', 
        'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR', 'KALIMANTAN BARAT', 
        'KALIMANTAN TENGAH', 'KALIMANTAN SELATAN', 'KALIMANTAN TIMUR', 
        'KALIMANTAN UTARA', 'SULAWESI UTARA', 'SULAWESI TENGAH', 
        'SULAWESI SELATAN', 'SULAWESI TENGGARA', 'GORONTALO', 
        'SULAWESI BARAT', 'MALUKU', 'MALUKU UTARA', 'PAPUA BARAT', 
        'PAPUA', 'INDONESIA'
    ],
    '2021': [
        6651, 36534, 5666, 7512, 3701, 13037, 3493, 9764, 1566, 2481,
        29103, 7502, 8909, 4774, 19257, 3434, 2404, 6296, 4909, 4048,
        2399, 4973, 4564, 971, 6215, 5139, 14636, 2431, 2445, 1500,
        3139, 1008, 2784, 6236, 239481
    ],
    '2022': [
        10137, 43555, 7691, 12389, 5359, 11453, 3613, 11022, 2072, 3358,
        32534, 29485, 30060, 10591, 51905, 5038, 6304, 5296, 5991, 3975,
        3189, 5016, 4221, 1280, 9618, 5453, 28679, 3828, 2488, 2027,
        2383, 1220, 4083, 7584, 372897
    ],
    '2023': [
        12420, 62278, 12722, 15777, 7432, 21335, 5579, 16608, 2211, 5074,
        87426, 45694, 42304, 12061, 66741, 7392, 11916, 7550, 12692, 6028,
        4420, 6375, 6762, 1701, 14265, 8944, 41196, 6276, 3574, 2679,
        4741, 2334, 6410, 14074, 584991
    ]
}

df = pd.DataFrame(data)

# Pengaturan tampilan plot
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Menghapus baris nasional untuk analisis khusus daerah
df_regional = df[df['Kepolisian Daerah'] != 'INDONESIA'].copy()

# Membuat fungsi untuk memformat angka dalam ribu
def format_thousands(x, pos):
    return f'{x/1000:.0f}K' if x >= 1000 else f'{x:.0f}'

# 1. Visualisasi 1: Tren Tingkat Kejahatan Nasional
plt.figure(figsize=(14, 8))
years = ['2021', '2022', '2023']
national_values = df[df['Kepolisian Daerah'] == 'INDONESIA'][years].values[0]

plt.bar(years, national_values, color=['#3498db', '#2980b9', '#1f618d'])
plt.title('Tren Tindak Pidana di Indonesia (2021-2023)', fontsize=16, fontweight='bold')
plt.ylabel('Jumlah Tindak Pidana', fontsize=14)
plt.xlabel('Tahun', fontsize=14)
plt.grid(axis='y', alpha=0.3)

# Menambahkan label nilai di atas bar
for i, v in enumerate(national_values):
    plt.text(i, v + 10000, f'{v:,}', ha='center', fontsize=12, fontweight='bold')

plt.savefig('tren_nasional.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Visualisasi 2: 10 Daerah dengan Tingkat Kejahatan Tertinggi pada 2023
top_10_2023 = df_regional.sort_values('2023', ascending=False).head(10)

plt.figure(figsize=(14, 8))
bars = plt.bar(top_10_2023['Kepolisian Daerah'], top_10_2023['2023'], color='#c0392b')
plt.title('10 Daerah dengan Tindak Pidana Tertinggi (2023)', fontsize=16, fontweight='bold')
plt.ylabel('Jumlah Tindak Pidana', fontsize=14)
plt.xlabel('Kepolisian Daerah', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

# Menambahkan label nilai di atas bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1000,
            f'{height:,}', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('top_10_daerah_2023.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Visualisasi 3: Persentase Kenaikan 2021-2023
df_regional['Kenaikan_2021_2023_%'] = ((df_regional['2023'] - df_regional['2021']) / df_regional['2021'] * 100).round(1)
top_growth = df_regional.sort_values('Kenaikan_2021_2023_%', ascending=False).head(10)

plt.figure(figsize=(14, 8))
bars = plt.bar(top_growth['Kepolisian Daerah'], top_growth['Kenaikan_2021_2023_%'], color='#27ae60')
plt.title('10 Daerah dengan Persentase Kenaikan Tertinggi (2021-2023)', fontsize=16, fontweight='bold')
plt.ylabel('Persentase Kenaikan (%)', fontsize=14)
plt.xlabel('Kepolisian Daerah', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

# Menambahkan label nilai di atas bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 10,
            f'{height}%', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('top_kenaikan_persentase.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Visualisasi 4: Heatmap Regional berdasarkan Tahun
# Ubah format dataframe untuk heatmap
df_heatmap = df_regional.set_index('Kepolisian Daerah')[['2021', '2022', '2023']]
df_heatmap = df_heatmap.sort_values('2023', ascending=False)

plt.figure(figsize=(12, 16))
ax = sns.heatmap(df_heatmap, cmap='YlOrRd', annot=True, fmt=',', linewidths=.5)
plt.title('Heatmap Tindak Pidana per Daerah (2021-2023)', fontsize=16, fontweight='bold')
plt.ylabel('Kepolisian Daerah', fontsize=14)
plt.xlabel('Tahun', fontsize=14)
plt.tight_layout()
plt.savefig('heatmap_regional.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Visualisasi 5: Perbandingan 5 Daerah Tertinggi
top5_daerah = df_regional.sort_values('2023', ascending=False).head(5)

plt.figure(figsize=(14, 8))
x = np.arange(len(top5_daerah))
width = 0.25

plt.bar(x - width, top5_daerah['2021'], width, label='2021', color='#3498db')
plt.bar(x, top5_daerah['2022'], width, label='2022', color='#e74c3c')
plt.bar(x + width, top5_daerah['2023'], width, label='2023', color='#2ecc71')

plt.title('Perbandingan 5 Daerah dengan Tindak Pidana Tertinggi (2021-2023)', fontsize=16, fontweight='bold')
plt.ylabel('Jumlah Tindak Pidana', fontsize=14)
plt.xlabel('Kepolisian Daerah', fontsize=14)
plt.xticks(x, top5_daerah['Kepolisian Daerah'], rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('perbandingan_top5.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Visualisasi 6: Proporsi Kejahatan per Wilayah 2023 (Pie Chart)
# Pengelompokan wilayah berdasarkan pulau utama
def get_region(area):
    if area in ['ACEH', 'SUMATERA UTARA', 'SUMATERA BARAT', 'RIAU', 'JAMBI', 
                'SUMATERA SELATAN', 'BENGKULU', 'LAMPUNG', 'KEP. BANGKA BELITUNG', 'KEP. RIAU']:
        return 'Sumatera'
    elif area in ['METRO JAYA', 'JAWA BARAT', 'JAWA TENGAH', 'DI YOGYAKARTA', 'JAWA TIMUR', 'BANTEN']:
        return 'Jawa'
    elif area in ['BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR']:
        return 'Bali & Nusa Tenggara'
    elif area in ['KALIMANTAN BARAT', 'KALIMANTAN TENGAH', 'KALIMANTAN SELATAN', 
                 'KALIMANTAN TIMUR', 'KALIMANTAN UTARA']:
        return 'Kalimantan'
    elif area in ['SULAWESI UTARA', 'SULAWESI TENGAH', 'SULAWESI SELATAN', 
                 'SULAWESI TENGGARA', 'GORONTALO', 'SULAWESI BARAT']:
        return 'Sulawesi'
    elif area in ['MALUKU', 'MALUKU UTARA', 'PAPUA BARAT', 'PAPUA']:
        return 'Maluku & Papua'
    else:
        return 'Lainnya'

df_regional['Wilayah'] = df_regional['Kepolisian Daerah'].apply(get_region)
wilayah_2023 = df_regional.groupby('Wilayah')['2023'].sum().sort_values(ascending=False)

plt.figure(figsize=(12, 10))
colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
explode = [0.1 if i == 0 else 0 for i in range(len(wilayah_2023))]

patches, texts, autotexts = plt.pie(wilayah_2023, 
                                   labels=wilayah_2023.index, 
                                   autopct='%1.1f%%',
                                   explode=explode,
                                   colors=colors, 
                                   shadow=True, 
                                   startangle=90)

for text in texts:
    text.set_fontsize(12)
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_color('white')

plt.axis('equal')
plt.title('Proporsi Tindak Pidana Berdasarkan Wilayah (2023)', fontsize=16, fontweight='bold')
plt.savefig('proporsi_wilayah_2023.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Visualisasi 7: Scatter plot hubungan antara tindak pidana tahun 2021 vs 2023
plt.figure(figsize=(12, 10))
plt.scatter(df_regional['2021'], df_regional['2023'], alpha=0.7, s=100, c='#3498db')

# Menambahkan garis tren
z = np.polyfit(df_regional['2021'], df_regional['2023'], 1)
p = np.poly1d(z)
plt.plot(df_regional['2021'], p(df_regional['2021']), "r--", alpha=0.8)

# Anotasi untuk daerah yang menonjol
for i, row in df_regional.iterrows():
    if row['2023'] > 40000 or row['2021'] > 25000:
        plt.annotate(row['Kepolisian Daerah'], 
                    xy=(row['2021'], row['2023']),
                    xytext=(5, 5),
                    textcoords='offset points',
                    fontsize=10,
                    fontweight='bold')

plt.title('Hubungan Tindak Pidana 2021 vs 2023', fontsize=16, fontweight='bold')
plt.xlabel('Jumlah Tindak Pidana 2021', fontsize=14)
plt.ylabel('Jumlah Tindak Pidana 2023', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('scatter_2021_2023.png', dpi=300, bbox_inches='tight')
plt.close()

# Menyimpan analisis statistik ke file teks
with open('analisis_statistik.txt', 'w') as f:
    # 1. Statistik Nasional
    nasional = df[df['Kepolisian Daerah'] == 'INDONESIA']
    f.write("ANALISIS STATISTIK TINDAK PIDANA DI INDONESIA (2021-2023)\n")
    f.write("="*60 + "\n\n")
    
    f.write("1. STATISTIK NASIONAL\n")
    f.write("-"*30 + "\n")
    f.write(f"Total tindak pidana 2021: {nasional['2021'].values[0]:,}\n")
    f.write(f"Total tindak pidana 2022: {nasional['2022'].values[0]:,}\n")
    f.write(f"Total tindak pidana 2023: {nasional['2023'].values[0]:,}\n\n")
    
    kenaikan_2021_2022 = (nasional['2022'].values[0] - nasional['2021'].values[0]) / nasional['2021'].values[0] * 100
    kenaikan_2022_2023 = (nasional['2023'].values[0] - nasional['2022'].values[0]) / nasional['2022'].values[0] * 100
    kenaikan_2021_2023 = (nasional['2023'].values[0] - nasional['2021'].values[0]) / nasional['2021'].values[0] * 100
    
    f.write(f"Kenaikan 2021-2022: {kenaikan_2021_2022:.1f}%\n")
    f.write(f"Kenaikan 2022-2023: {kenaikan_2022_2023:.1f}%\n")
    f.write(f"Kenaikan total 2021-2023: {kenaikan_2021_2023:.1f}%\n\n")
    
    # 2. Lima daerah tertinggi 2023
    f.write("2. LIMA DAERAH DENGAN TINGKAT TINDAK PIDANA TERTINGGI (2023)\n")
    f.write("-"*60 + "\n")
    top5 = df_regional.sort_values('2023', ascending=False).head(5)
    for i, row in top5.iterrows():
        f.write(f"{row['Kepolisian Daerah']}: {row['2023']:,} kasus\n")
    f.write("\n")
    
    # 3. Lima daerah dengan kenaikan tertinggi
    f.write("3. LIMA DAERAH DENGAN PERSENTASE KENAIKAN TERTINGGI (2021-2023)\n")
    f.write("-"*60 + "\n")
    top_growth_5 = df_regional.sort_values('Kenaikan_2021_2023_%', ascending=False).head(5)
    for i, row in top_growth_5.iterrows():
        f.write(f"{row['Kepolisian Daerah']}: {row['Kenaikan_2021_2023_%']:.1f}%\n")
    f.write("\n")
    
    # 4. Statistik per wilayah
    f.write("4. STATISTIK PER WILAYAH (2023)\n")
    f.write("-"*30 + "\n")
    for region, value in wilayah_2023.items():
        f.write(f"{region}: {value:,} kasus ({value/wilayah_2023.sum()*100:.1f}%)\n")
    f.write("\n")
    
    # 5. Rata-rata dan median
    f.write("5. STATISTIK DESKRIPTIF\n")
    f.write("-"*30 + "\n")
    f.write(f"Rata-rata tindak pidana per daerah 2021: {df_regional['2021'].mean():.1f}\n")
    f.write(f"Rata-rata tindak pidana per daerah 2022: {df_regional['2022'].mean():.1f}\n")
    f.write(f"Rata-rata tindak pidana per daerah 2023: {df_regional['2023'].mean():.1f}\n\n")
    
    f.write(f"Median tindak pidana per daerah 2021: {df_regional['2021'].median():.1f}\n")
    f.write(f"Median tindak pidana per daerah 2022: {df_regional['2022'].median():.1f}\n")
    f.write(f"Median tindak pidana per daerah 2023: {df_regional['2023'].median():.1f}\n\n")

    # 6. Korelasi
    correlation = df_regional[['2021', '2022', '2023']].corr()
    f.write("6. KORELASI ANTAR TAHUN\n")
    f.write("-"*30 + "\n")
    f.write(f"Korelasi 2021-2022: {correlation.loc['2021', '2022']:.4f}\n")
    f.write(f"Korelasi 2022-2023: {correlation.loc['2022', '2023']:.4f}\n")
    f.write(f"Korelasi 2021-2023: {correlation.loc['2021', '2023']:.4f}\n")

print("Visualisasi selesai! Semua file telah disimpan.")