##### Inisiasi Upload Data

import pandas as pd
import numpy as np # type: ignore
from scipy.stats import shapiro, kstest
from scipy.stats import poisson, chisquare, f
from tkinter import Tk, filedialog
import time
import os

# Upload data
def upload_data():
    root = Tk()
    root.withdraw()  # Menyembunyikan jendela utama Tkinter
    file_paths = filedialog.askopenfilenames(title="Pilih File CSV atau Excel", filetypes=(("Excel files", "*.xlsx"), ("CSV files", "*.csv")))

    dataframes = []
    for file in file_paths:
        print(f"Sedang mengupload data: {file}")
        if file.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            raise ValueError(f"Tipe file tidak didukung: {file}")
        dataframes.append((df, file))  # Simpan DataFrame bersama dengan nama file untuk referensi selanjutnya
    
    return dataframes

def normalize_and_combine_dataframes(*df_tuples):
    dfs = []
    for df, filename in df_tuples:
        print(f"Sedang menggabungkan data: {filename}")

        # Normalize kolom yang ada pada setiap DataFrame
        if 'Movement Type' in df.columns and 'Order' not in df.columns:
            df.insert(df.columns.get_loc('Movement Type'), 'Order', '')

        if 'Material.1' in df.columns:
            df.drop('Material.1', axis=1, inplace=True)

        if 'Unnamed: 8' in df.columns:
            df.rename(columns={'Unnamed: 8': 'Unnamed: 7'}, inplace=True)

        dfs.append(df)  # Tambahkan DataFrame yang telah diubah ke dalam daftar dfs

    # Gabungkan semua DataFrame berdasarkan baris (axis=0)
    df_com_hist = pd.concat(dfs, ignore_index=True)

    # Pastikan 'Posting Date' dalam format datetime
    df_com_hist['Posting Date'] = pd.to_datetime(df_com_hist['Posting Date'], errors='coerce')

    # Buat data kolom periode month untuk aggregate dalam satu bulan
    df_com_hist['Month'] = df_com_hist['Posting Date'].dt.to_period('M')

    # Menambahkan kolom Week dengan nomor minggu yang berulang dari 1 hingga 4
    def week_in_month(date):
        first_day = date.replace(day=1)
        day_of_month = date.day
        adjusted_dom = day_of_month + first_day.weekday()
        return (adjusted_dom - 1) // 7 % 4 + 1

    df_com_hist['Week'] = df_com_hist['Posting Date'].apply(lambda x: f"{x.strftime('%Y-%m')} Week {week_in_month(x)}" if pd.notnull(x) else None)

    df_com_hist['Day'] = df_com_hist['Posting Date'].dt.strftime('%Y-%m-%d')

    condition = df_com_hist['Movement Type'].isin(['105', '201', '261', '351', 'Z61'])
    df_com_hist['Mvt_type'] = np.where(condition, 'Order', 'cancel')

    return df_com_hist

def export_data_with_progress(df, output_folder, filename):
    # Gabungkan path folder dan nama file
    full_path = os.path.join(output_folder, filename)

    print(f"Sedang mengekspor data ke {full_path}...")
    total_rows = len(df)
    chunk_size = max(total_rows // 3, 1)  # Pastikan chunk_size minimal 1

    try:
        with pd.ExcelWriter(full_path) as writer:
            for i in range(0, total_rows, chunk_size):
                end_row = min(i + chunk_size, total_rows)
                df.iloc[i:end_row].to_excel(writer, index=True, header=(i == 0), startrow=i)

                # Menghitung persentase dan menampilkannya
                progress = (end_row / total_rows) * 100
                print(f"Progres ekspor: {progress:.2f}%")

                # Simulasi delay untuk memperjelas progres (opsional)
                time.sleep(0.5)

        print(f"Data berhasil diekspor ke {full_path}")
        print(f"----------------------------------------------------------------------------------------------")

    except Exception as e:
        print(f"Terjadi kesalahan saat mengekspor data: {e}")


# Mengunggah data
df_tuples = upload_data()

# Menggabungkan dan menormalkan data
df_com_hist = normalize_and_combine_dataframes(*df_tuples)

print(f"----------------------------------------------------------------------------------------------")
print(f"Hasil Gabungan")
print(f"----------------------------------------------------------------------------------------------")
# Menampilkan hasil
print(df_com_hist.head())
print(f"----------------------------------------------------------------------------------------------")

df_Histori_2016_2022_GI = df_com_hist


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Proses filtering awal data
# Fungsi untuk memproses pengelompokan dan filtering sesuai kondisi yang diberikan
def process_data(df):
    # Mengelompokkan data berdasarkan kolom "Material"
    grouped = df.groupby('Material')
    
    # DataFrame untuk menyimpan hasil akhir, unmatched cancels, dan matched rows
    result = pd.DataFrame()
    unmatched_cancels = pd.DataFrame()
    matched_df = pd.DataFrame()
    
    # Iterasi melalui setiap grup
    for material, group in grouped:
        matched_rows = []
        # Memeriksa apakah ada nilai 'cancel' pada kolom 'Mvt_type'
        if 'cancel' in group['Mvt_type'].values:
            # Iterasi melalui baris yang memiliki nilai 'cancel'
            for _, cancel_row in group[group['Mvt_type'] == 'cancel'].iterrows():
                # Mencari baris dengan nilai sama pada kolom 'Unnamed: 7' dan 'Order' pada kolom 'Mvt_type'
                condition = (
                    (group['Unnamed: 7'] == cancel_row['Unnamed: 7']) &
                    (group['Mvt_type'] == 'Order') &
                    (
                        ((group['Movement Type'] == "105") & (cancel_row['Movement Type'] == "106")) |
                        ((group['Movement Type'] == "201") & (cancel_row['Movement Type'] == "202")) |
                        ((group['Movement Type'] == "261") & (cancel_row['Movement Type'] == "262")) |
                        ((group['Movement Type'] == "351") & (cancel_row['Movement Type'] == "352")) |
                        ((group['Movement Type'] == "Z61") & (cancel_row['Movement Type'] == "Z62"))
                    )
                )
                potential_matches = group[condition]
                if not potential_matches.empty:
                    # Menghitung selisih tanggal terdekat
                    potential_matches = potential_matches.copy()  # Avoid SettingWithCopyWarning
                    potential_matches['date_diff'] = (potential_matches['Posting Date'] - cancel_row['Posting Date']).abs()
                    closest_match = potential_matches.loc[potential_matches['date_diff'].idxmin()]
                    # Jika ditemukan, tambahkan baris yang cocok ke list matched_rows
                    matched_rows.append(cancel_row.name)
                    matched_rows.append(closest_match.name)
                    matched_df = pd.concat([matched_df, cancel_row.to_frame().T, closest_match.to_frame().T])
                    
                else:
                    # Jika tidak ditemukan pasangan 'order', tambahkan ke unmatched_cancels
                    unmatched_cancels = pd.concat([unmatched_cancels, cancel_row.to_frame().T])
                    
    
        # Menyimpan hanya baris yang tidak ada di matched_rows
        unmatched_group = group.drop(index=matched_rows)
        result = pd.concat([result, unmatched_group])
    print(f"Sedang memproses data Histori GI")
    # Reset index untuk hasil akhir
    result.reset_index(drop=True, inplace=True)
    unmatched_cancels.reset_index(drop=True, inplace=True)
    matched_df.reset_index(drop=True, inplace=True)
    
    # Drop semua baris dengan Mvt_type 'cancel' dari result
    result = result[result['Mvt_type'] != 'cancel']
    
    print(f"Sedang memproses data Histori GI")
    return result, unmatched_cancels, matched_df

# Memproses data
filtered_df, unmatched_cancels_df, matched_df = process_data(df_Histori_2016_2022_GI)

# Rename kolom dalam DataFrame
filtered_df = filtered_df.rename(columns={
    'Material': 'Material_Code',
    'Unnamed: 7': 'Quantity(EA)'
})

# data input sebelum klasifikasi
data_input_sebelum_klasifikasi = filtered_df[['Posting Date', 'Material_Code', 'Material Description', 'Quantity(EA)', 'Movement Type']]

# Tentukan folder output untuk menyimpan file
output_folder = "s:/Project & Research/01. Pupuk Indonesia/pi/Data Pa Bambang/Data History/Model_Kalkulator_Fixed/testfolder/output"  # Ganti dengan path folder yang diinginkan
filename = 'Data_input_sebelum_klasifikasi.xlsx'

# Mengekspor data gabungan dengan progres
export_data_with_progress(data_input_sebelum_klasifikasi, output_folder, filename)

print(f"----------------------------------------------------------------------------------------------")
print(f'Sebelum filter Data Histori Order GI 2016 - 2022 Order                                               : {df_Histori_2016_2022_GI.shape[0]}')
print(f'Setelah filter Data Histori Order GI 2016 - 2022                                                     : {filtered_df.shape[0]}')

print(f'Matched Rows DataFrame (baris cancel yang memiliki pasangan) Data Histori Order GI 2016 - 2022       : {matched_df.shape[0]}')
print(f'Matched Rows DataFrame (baris cancel yang Tidak memiliki pasangan) Data Histori Order GI 2016 - 2022 : {unmatched_cancels_df.shape[0]}')
print(f"----------------------------------------------------------------------------------------------")


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

##### Klasifikasi dan Indentifikasi Pola Distribusi Barang
# Menambahkan kolom sementara untuk menandai apakah ada 'Z61' di kolom 'Movement Type'
filtered_df['Has_Z61'] = filtered_df['Movement Type'] == 'Z61'

# Fungsi untuk menghitung jumlah data per grup berdasarkan kolom 'Material' dan menghitung statistik lainnya
def count_and_stats_by_material(df):
    # Mengelompokkan data berdasarkan kolom 'Material' dan menghitung ukuran grup, rata-rata, variansi, dan standar deviasi
    grouped = df.groupby('Material_Code').agg(
        Jumlah_Data=('Quantity(EA)', 'size'),
        Rata_Rata=('Quantity(EA)', 'mean'),
        Variansi=('Quantity(EA)', 'var'),
        Standar_Deviasi=('Quantity(EA)', 'std'),
        Has_Z61=('Has_Z61', 'any')
    ).reset_index()
    
    # Mengisi nilai None untuk grup dengan Jumlah Data 0 atau 1
    grouped.loc[grouped['Jumlah_Data'] <= 1, ['Rata_Rata', 'Variansi', 'Standar_Deviasi']] = None
    
    # Menambahkan kolom 'Proses1' dan mengisi sesuai kondisi
    grouped['Kategori'] = None
    grouped['Proses1'] = None
    grouped['Proses2'] = None
    grouped['P_Value'] = 0.0
    grouped['Deskripsi_Pengujian_Statistik'] = None
    grouped['Hasil_uji'] = None

    grouped.loc[grouped['Jumlah_Data'] == 0, 'Proses1'] = 'PT'
    grouped.loc[grouped['Jumlah_Data'] >= 30, 'Proses1'] = 'PN'
    grouped.loc[(grouped['Jumlah_Data'] > 0) & (grouped['Jumlah_Data'] < 30), 'Proses1'] = 'PP'
    
    # Mengisi nilai None untuk kolom 'Proses2' berdasarkan kondisi awal
    mask = (grouped['Standar_Deviasi'] == 0) & (grouped['Variansi'] == 0) & (grouped['Proses1'].isin(['PN', 'PP']))
    grouped.loc[mask, 'Proses2'] = 'MD'
    mask2 = (grouped['Jumlah_Data'] == 1) & (grouped['Proses1'].isin(['PN', 'PP']))
    grouped.loc[mask2, 'Proses2'] = 'MT'
    mask3 = (grouped['Has_Z61'] == True)
    grouped.loc[mask3, 'Proses2'] = 'MD'

    for idx, row in grouped.iterrows():
        material_data = df[df['Material_Code'] == row['Material_Code']]['Quantity(EA)']

        if row['Proses1'] in ['PN', 'PP'] and row['Standar_Deviasi'] is not None and row['Proses2'] is None:
            # Pengujian F-test pada alpha 5%
            f_value = row['Variansi'] / 1e-10  # Variansi 0 diasumsikan sangat kecil
            dfn = row['Jumlah_Data'] - 1
            dfd = 1e10  # Degrees of freedom for the assumed zero variance group
            p_value_ftest = 1 - f.cdf(f_value, dfn, dfd)
            grouped.at[idx, 'P_Value'] = p_value_ftest
            grouped.at[idx, 'Hasil_uji'] = 'Ya' if p_value_ftest < 0.05 else 'Tidak'
            grouped.at[idx, 'Deskripsi_Pengujian_Statistik'] = f"Material dengan kode {row['Material_Code']} telah dilakukan pengujian statistik dengan metode Uji F dengan Tingkat Signifikansi 5%. {'Berhasil' if p_value_ftest < 0.05 else 'Tidak Berhasil'} menolak Hypotesis Null."

            if grouped.at[idx, 'Hasil_uji'] == 'Tidak':
                grouped.at[idx, 'Proses2'] = 'MD'
                continue

            # Jika F-test signifikan, lanjutkan dengan pengujian normalitas atau Poisson
            if row['Proses1'] == 'PN' and row['Proses2'] is None:
                # Uji Shapiro-Wilk pada alpha 5%
                stat, p_value_shapiro = shapiro(material_data)
                grouped.at[idx, 'P_Value'] = p_value_shapiro
                grouped.at[idx, 'Hasil_uji'] = 'Ya' if p_value_shapiro < 0.05 else 'Tidak'
                grouped.at[idx, 'Deskripsi_Pengujian_Statistik'] = f"Material dengan kode {row['Material_Code']} telah dilakukan pengujian statistik dengan metode Uji Normal Shapiro Wilk Test dengan Tingkat Signifikansi 5%. {'Berhasil' if p_value_shapiro < 0.05 else 'Tidak Berhasil'} menolak Hypotesis Null."

                if grouped.at[idx, 'Hasil_uji'] == 'Tidak':
                    grouped.at[idx, 'Proses2'] = 'MN'
                    continue

                # Uji Kolmogorov-Smirnov pada alpha 5%
                stat, p_value_ks = kstest(material_data, 'norm', args=(material_data.mean(), material_data.std()))
                grouped.at[idx, 'P_Value'] = p_value_ks
                grouped.at[idx, 'Hasil_uji'] = 'Ya' if p_value_ks < 0.05 else 'Tidak'
                grouped.at[idx, 'Deskripsi_Pengujian_Statistik'] = f"Material dengan kode {row['Material_Code']} telah dilakukan pengujian statistik dengan metode Uji Normal Kolmogorov-Smirnov Test dengan Tingkat Signifikansi 5%. {'Berhasil' if p_value_ks < 0.05 else 'Tidak Berhasil'} menolak Hypotesis Null."

                if grouped.at[idx, 'Hasil_uji'] == 'Tidak':
                    grouped.at[idx, 'Proses2'] = 'MN'
                else:
                    grouped.at[idx, 'Proses2'] = 'MT'

            elif row['Proses1'] == 'PP' and row['Proses2'] is None:
                if row['Jumlah_Data'] == 1:
                    grouped.at[idx, 'Proses2'] = 'MT'
                    continue  # Langsung skip untuk uji distribusi poisson

                # Uji Distribusi Poisson
                nilai, hitung = np.unique(material_data, return_counts=True)
                rata_rata_data = material_data.mean()
                frekuensi_diharapkan = [poisson.pmf(k, rata_rata_data) * len(material_data) for k in nilai]

                # Uji Distribusi Poisson
                nilai, hitung = np.unique(material_data, return_counts=True)
                rata_rata_data = material_data.mean()
                frekuensi_diharapkan = [poisson.pmf(k, rata_rata_data) * len(material_data) for k in nilai]

                scaling_factor = 1 if np.sum(frekuensi_diharapkan) == 0 or np.sum(hitung) == 0 else np.sum(hitung) / np.sum(frekuensi_diharapkan)
                frekuensi_diharapkan = [f * scaling_factor for f in frekuensi_diharapkan]

                # if np.sum(frekuensi_diharapkan) == 0 or np.sum(hitung) == 0:
                #     grouped.at[idx, 'Hasil_uji'] = 'Tidak dapat diuji dengan Poisson'
                #     grouped.at[idx, 'Proses2'] = 'MT'
                #     continue

                # scaling_factor = np.sum(hitung) / np.sum(frekuensi_diharapkan)
                # frekuensi_diharapkan = [f * scaling_factor for f in frekuensi_diharapkan]

                try:
                    stat, p_value_poiss = chisquare(hitung, frekuensi_diharapkan)
                    grouped.at[idx, 'P_Value'] = p_value_poiss
                    grouped.at[idx, 'Hasil_uji'] = 'Ya' if p_value_poiss < 0.1 else 'Tidak'
                    grouped.at[idx, 'Deskripsi_Pengujian_Statistik'] = f"Material dengan kode {row['Material_Code']} telah dilakukan pengujian statistik dengan metode Uji Poisson Test dengan Tingkat Signifikansi 5%. {'Berhasil' if p_value_poiss < 0.1 else 'Tidak Berhasil'} menolak Hypotesis Null."
                except ValueError as e:
                    grouped.at[idx, 'Hasil_uji'] = 'Hasil pengujian menunjukan pola distribusi tak tentu'
                    grouped.at[idx, 'Proses2'] = 'MT'
                    continue

                if grouped.at[idx, 'Hasil_uji'] == 'Tidak':
                    grouped.at[idx, 'Proses2'] = 'MP'
                else:
                    grouped.at[idx, 'Proses2'] = 'MT'

    grouped['Kategori'] = grouped.apply(lambda row: 
                                        'Pola Deterministik' if row['Proses2'] == 'MD' else 
                                        'Pola Normal' if row['Proses2'] == 'MN' else 
                                        'Pola Poisson' if row['Proses2'] == 'MP' else 
                                        'Pola Tak - Tentu' if row['Proses2'] == 'MT' else None, 
                                        axis=1)

    # Mengatur ulang urutan kolom
    ordered_columns = ['Material_Code', 'Kategori', 'Proses1', 'Proses2', 'Jumlah_Data', 'Rata_Rata', 
                       'Variansi', 'Standar_Deviasi', 'P_Value', 'Deskripsi_Pengujian_Statistik', 'Hasil_uji']
    grouped = grouped[ordered_columns]

    return grouped

# Menghitung jumlah data dan statistik lainnya per grup
Hasil_Klasifikasi = count_and_stats_by_material(filtered_df)

# Menampilkan hasil
# Pastikan data unik sebelum melakukan join
filtered_df_unique = filtered_df[['Material_Code', 'Material Description']].drop_duplicates(subset='Material_Code')

# Lakukan left join berdasarkan 'Material Code' untuk menambahkan kolom 'Material Description'
Hasil_Klasifikasi = Hasil_Klasifikasi.merge(
    filtered_df_unique,  # Ambil kolom 'Material' dan 'Material Description' yang unik
    how='left',
    left_on='Material_Code',
    right_on='Material_Code'
)

# Pindahkan kolom 'Material Description' setelah 'Material Code'
cols = list(Hasil_Klasifikasi.columns)
material_code_index = cols.index('Material_Code')
cols.insert(material_code_index + 1, cols.pop(cols.index('Material Description')))

# Reorder the columns
Hasil_Klasifikasi = Hasil_Klasifikasi[cols]

# # Tampilkan hasil setelah pengaturan ulang kolom
# print(Hasil_Klasifikasi.shape)
# print(Hasil_Klasifikasi.to_string(index=False))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Mang ALI DISINI yang harus diperbaiki
#### Perhitungan Statistik kembali untuk Pola distribusi tak - tentu
def hitung_statistik_tahunan(filtered_df, hasil_klasifikasi):
    # Filter data berdasarkan kategori "Pola Tak - Tentu"
    pola_tak_tentu_codes = hasil_klasifikasi[hasil_klasifikasi['Kategori'] == "Pola Tak - Tentu"]['Material_Code'].unique()
    
    # Filter aggregate_df berdasarkan kode yang telah teridentifikasi
    aggregate_filtered = filtered_df[filtered_df['Material_Code'].isin(pola_tak_tentu_codes)]
    
    # Tambahkan kolom tahun untuk analisis level tahunan
    aggregate_filtered['Tahun'] = pd.to_datetime(aggregate_filtered['Posting Date']).dt.year
    
    # Buat crosstab berdasarkan Material_Code dan Tahun dengan Quantity sebagai nilai
    crosstab_df = pd.crosstab(aggregate_filtered['Material_Code'], aggregate_filtered['Tahun'], 
                              values=aggregate_filtered['Quantity(EA)'], aggfunc='sum', dropna=False).fillna(0)
    
    # Hitung Rata-Rata, Variansi, dan Standar Deviasi
    hasil_statistik = pd.DataFrame()
    hasil_statistik['Rata_Rata'] = crosstab_df.mean(axis=1)
    hasil_statistik['Variansi'] = crosstab_df.var(axis=1)
    hasil_statistik['Standar_Deviasi'] = crosstab_df.std(axis=1)
    
    return crosstab_df, hasil_statistik

# panggil fungsi statistik pola tak tentu
crosstab_df, hasil_statistik = hitung_statistik_tahunan(filtered_df, Hasil_Klasifikasi)


def update_hasil_klasifikasi(hasil_klasifikasi, hasil_statistik):
    # Lakukan merge antara Hasil_Klasifikasi dan hasil_statistik berdasarkan Material_Code
    hasil_klasifikasi_updated = hasil_klasifikasi.copy()

    # Update kolom 'Rata_Rata', 'Variansi', dan 'Standar_Deviasi' hanya untuk Material_Code yang sama
    for material_code in hasil_statistik.index:
        hasil_klasifikasi_updated.loc[hasil_klasifikasi_updated['Material_Code'] == material_code, 'Rata_Rata'] = hasil_statistik.loc[material_code, 'Rata_Rata']
        hasil_klasifikasi_updated.loc[hasil_klasifikasi_updated['Material_Code'] == material_code, 'Variansi'] = hasil_statistik.loc[material_code, 'Variansi']
        hasil_klasifikasi_updated.loc[hasil_klasifikasi_updated['Material_Code'] == material_code, 'Standar_Deviasi'] = hasil_statistik.loc[material_code, 'Standar_Deviasi']

    return hasil_klasifikasi_updated

# panggil funsi update hasil klasifikasi
Hasil_Klasifikasi_updated = update_hasil_klasifikasi(Hasil_Klasifikasi, hasil_statistik)

# Tentukan folder output untuk menyimpan file
output_folder2 = "s:/Project & Research/01. Pupuk Indonesia/pi/Data Pa Bambang/Data History/Model_Kalkulator_Fixed/testfolder/output"  # Ganti dengan path folder yang diinginkan
filename2 = 'Data_output_setelah_klasifikasi.xlsx'

print(f"----------------------------------------------------------------------------------------------")
# Menampilkan rekap hasilnya
print(Hasil_Klasifikasi['Proses1'].value_counts())
print(f"----------------------------------------------------------------------------------------------")
print(Hasil_Klasifikasi['Kategori'].value_counts(dropna=False))
print(f"----------------------------------------------------------------------------------------------")

# Mengekspor data gabungan dengan progres
export_data_with_progress(Hasil_Klasifikasi, output_folder2, filename2)

# Sampai sini mang ALI

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Import Master Data Material Target SHP
# import Master Data Material Target SHP
def upload_data_material_target():
    """
    Fungsi untuk mengunggah file Excel yang berisi data material target.
    File yang diunggah kemudian dibaca dan dikembalikan sebagai DataFrame.
    Proses ini juga menampilkan persentase progres pengunggahan.
    """
    # Membuka dialog untuk memilih file
    root = Tk()
    root.withdraw()  # Menyembunyikan jendela utama Tkinter
    file_path = filedialog.askopenfilename(
        title="Pilih File Excel Material Target SHP",
        filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
    )

    # Memastikan pengguna memilih file
    if not file_path:
        raise ValueError("Tidak ada file yang dipilih. Harap pilih file Excel yang benar.")

    print(f"Sedang mengupload data: {file_path}")

    # Membaca file Excel ke dalam DataFrame
    try:
        # Simulasi proses pembacaan data untuk menampilkan progres (misalnya jika file besar)
        df_material_target = pd.read_excel(file_path, sheet_name="Rencana Evaluasi SHP")

        # Menghitung total baris untuk menampilkan progres
        total_rows = len(df_material_target)
        chunk_size = total_rows // 4  # Membagi progres menjadi 10 bagian (setiap 25%)

        for i in range(0, total_rows, chunk_size):
            time.sleep(0.2)  # Simulasi delay pembacaan data
            progress = (i / total_rows) * 100
            print(f"Progres pengunggahan: {progress:.0f}%")

        print("Progres pengunggahan: 100% - Data berhasil diunggah.")

    except Exception as e:
        raise ValueError(f"Terjadi kesalahan saat membaca file: {e}")

    # Mengembalikan DataFrame yang sudah dibaca
    return df_material_target

# panggil fungsi upload data material target
df_masterData = upload_data_material_target()

# Membuat filter untuk data input pada model kalkulator
Data_Input = Hasil_Klasifikasi[['Material_Code', 'Material Description', 'Kategori', 'Rata_Rata', 'Standar_Deviasi']]

# Mendapatkan kode material
unique_code_material_data_input = Data_Input['Material_Code']

# Mengambil informasi harga dan estimasi waktu berdasarkan kode material yang terfilter
join_harga_barang_DataInput = df_masterData[df_masterData['Material Code'].isin(unique_code_material_data_input)][['Material Code', 'Unit Price', 'ABC Indicator', 'Estimasi Lead Time (Mon)', 'Estimasi Lead Time (Day)']]

# Mengecek dan menampilkan baris yang duplikat dalam Result Harga Barang berdasarkan 'Material Code'
Pengecekan_data_duplicate_count = join_harga_barang_DataInput['Material Code'].duplicated(keep=False).sum()
if Pengecekan_data_duplicate_count > 0:
    print(f"\nAda {Pengecekan_data_duplicate_count} data duplikat berdasarkan 'Material Code':")
    print(join_harga_barang_DataInput[join_harga_barang_DataInput['Material Code'].duplicated(keep=False)].sort_values(by='Material Code').to_string(index=False))
else:
    print("")

# Menambahkan kolom yang menghitung jumlah nilai non-NaN di kolom-kolom yang relevan
join_harga_barang_DataInput['non_nan_count'] = join_harga_barang_DataInput[['Unit Price', 'Estimasi Lead Time (Mon)', 'Estimasi Lead Time (Day)']].notna().sum(axis=1)

# Mengurutkan DataFrame berdasarkan 'Material Code' dan 'non_nan_count' (prioritas untuk nilai non-NaN paling banyak)
join_harga_barang_DataInput = join_harga_barang_DataInput.sort_values(by=['Material Code', 'non_nan_count'], ascending=[True, False])

# Menghapus duplikat berdasarkan 'Material Code', menjaga baris dengan nilai non-NaN paling banyak
join_harga_barang_DataInput = join_harga_barang_DataInput.drop_duplicates(subset=['Material Code'], keep='first')

# Menghapus kolom 'non_nan_count' setelah tidak diperlukan lagi
join_harga_barang_DataInput.drop(columns=['non_nan_count'], inplace=True)

# Menggabungkan Data_Input dengan join_harga_barang_DataInput berdasarkan 'Material_Code'
Data_Input = pd.merge(Data_Input, join_harga_barang_DataInput, left_on='Material_Code', right_on='Material Code', how='left')

# Menghapus kolom yang redundant setelah merge
Data_Input.drop(columns=['Material Code'], inplace=True)

print(f"\nJumlah Data Unique Material Code Sebelum Input Calculator: {Data_Input.shape[0]} baris")
print(f"----------------------------------------------------------------------------------------------")
print(f"Proses Join kolom 'Harga Barang/Unit Price' dari file 'Master Data Material Target SHP 22-11-2022'")

# Mencetak baris dengan nilai NaN pada kolom "Unit Price"
nan_rows = Data_Input[Data_Input['Unit Price'].isna()]
nan_count = nan_rows.shape[0]
if nan_count > 0:
    print(f"\n----------------------------------------------------------------------------------------------")
    print(f"Jumlah Data Unique Material Code dengan NaN pada kolom 'Harga Barang/Unit Price': {nan_count}\n\n")
else:
    print("\nTidak ada nilai NaN pada kolom 'Unit Price'.")

print(f"\n----------------------------------------------------------------------------------------------")
print(f"Jumlah Data Unique Material Code dengan NaN pada kolom 'Harga Barang/Unit Price' berdasarkan Jenis Kategori: {nan_rows['Kategori'].value_counts(dropna=False)}\n\n")
print(f"----------------------------------------------------------------------------------------------")

# Identifikasi data input final
Data_Input_Final = Data_Input[(Data_Input['Unit Price'].notna()) & 
                              (Data_Input['Unit Price'] != 0) & 
                              (Data_Input['Unit Price'] != 1)]

# Filter tambahan untuk "Estimasi Lead Time (Mon)" atau "Estimasi Lead Time (Day)" minimal salah satu terisi
Data_Input_Final = Data_Input_Final[(Data_Input_Final['Estimasi Lead Time (Mon)'].notna()) | 
                                    (Data_Input_Final['Estimasi Lead Time (Day)'].notna())]

Data_Input_Final = Data_Input_Final[(Data_Input_Final['Rata_Rata'].notna()) &
                              (Data_Input_Final['Standar_Deviasi'].notna())]

# Transformasi dari bulan ke hari jika "Estimasi Lead Time (Mon)" terisi
Data_Input_Final.loc[Data_Input_Final['Estimasi Lead Time (Mon)'].notna(), 'Estimasi Lead Time (Day)'] = \
    Data_Input_Final.loc[Data_Input_Final['Estimasi Lead Time (Mon)'].notna(), 'Estimasi Lead Time (Mon)'] * 30

# Mengurutkan data dari nilai terkecil ke terbesar berdasarkan kolom "Unit Price"
Data_Input_Final = Data_Input_Final.sort_values(by='Unit Price', ascending=True)

# Rename kolom 'Unit Price' menjadi 'Harga Barang (p) /Unit'
Data_Input_Final.rename(columns={'Unit Price': 'Harga Barang (p) /Unit'}, inplace=True)

# #### Perhitungan Model
import sys
import os

# Tambahkan direktori Model_Kalkulator_Fixed ke path pencarian modul
sys.path.append(os.path.join(os.getcwd(), 'Model_Kalkulator_Fixed'))

# Import fungsi Model_Wilson dari file Model_Wilson_PolaDeterministik.py
try:
    from Model_Wilson_PolaDeterministik import Model_Wilson
    print("Import fungsi Model_Wilson berhasil.")
except ImportError as e:
    print(f"Error: {e}")

# Import fungsi Model_Q dari file Model_Q_PolaDistribusiNormal.py
try:
    from Model_Q_PolaDistribusiNormal import Model_Q
    print("Import fungsi Model_Q berhasil.")
except ImportError as e:
    print(f"Error: {e}")

# Import fungsi Model_Poisson dari file Model_Poisson_PolaPoisson.py
try:
    from Model_Poisson_PolaPoisson import Model_Poisson
    print("Import fungsi Model_Poisson berhasil.")
except ImportError as e:
    print(f"Error: {e}")

# Import fungsi Model_Tchebycheff dari file Model_Tchebycheff_PolaTakTentu.py
try:
    from Model_Tchebycheff_PolaTakTentu import Model_Tchebycheff_TakTentu
    print("Import fungsi Model_Tchebycheff berhasil.")
except ImportError as e:
    print(f"Error: {e}")

# Import fungsi Model_MinMaxRegret dari file Model_MinMaxRegret_PolaNonMoving.py
try:
    from Model_MinMaxRegret_PolaNonMoving import Model_MinMaxRegret
    print("Import fungsi Model_MinMaxRegret berhasil.")
except ImportError as e:
    print(f"Error: {e}")

# Import fungsi Model_KerusakanNonLinear dari file Model_KerusakanNonLinear_PolaNonMoving.py
try:
    from Model_KerusakanNonLinear_PolaNonMoving import model_kerusakan_non_linear
    print("Import fungsi Model_KerusakanNonLinear berhasil.")
except ImportError as e:
    print(f"Error: {e}")
 
# Import fungsi Model_KerusakanLinear dari file Model_KerusakanLinear_PolaNonMoving.py
try:
    from Model_KerusakanLinear_PolaNonMoving import model_kerusakan_linear
    print("Import fungsi Model_KerusakanLinear berhasil.")
except ImportError as e:
    print(f"Error: {e}")

# import fungsi Model_BCR dari file Model_BCR.py
try:
    from Model_BCR_new import Model_Inventori_BCR
    print("Import fungsi Model Inventori BCR berhasil")
except ImportError as e:
    print(f"Error: {e}")


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Inisiasi Data input
# data input untuk setiap pola
df_input_PolaNormal = Data_Input_Final[(Data_Input_Final['Kategori'] == "Pola Normal")]
df_input_PolaDeterminstik = Data_Input_Final[(Data_Input_Final['Kategori'] == "Pola Deterministik")]
df_input_PolaPoisson = Data_Input_Final[(Data_Input_Final['Kategori'] == "Pola Poisson")]
df_input_PolaTakTentu = Data_Input_Final[(Data_Input_Final['Kategori'] == "Pola Tak - Tentu")]

# POLA DETERMINISTIK
# Mengganti nama kolom menggunakan .loc untuk menghindari SettingWithCopyWarning
df_input_PolaDeterminstik = df_input_PolaDeterminstik.rename(columns={
    'Estimasi Lead Time (Mon)': 'Lead Time (L) Tahun',
    'Rata_Rata': 'Permintaan Barang (D) Unit/Tahun'
})

# Menambahkan kolom baru "Ongkos_Pesan_ModelWilson_A" menggunakan .loc
df_input_PolaDeterminstik.loc[:, 'Ongkos Pesan (A) /Pesan'] = df_input_PolaDeterminstik['Harga Barang (p) /Unit'].apply(
    lambda x: 5000000 if x > 100000000 else 1000000
)

# Menambahkan kolom baru "Ongkos Simpan (h) /Unit/Tahun" sebesar 15% dari "Harga Barang (p) /Unit" menggunakan .loc
df_input_PolaDeterminstik.loc[:, 'Ongkos Simpan (h) /Unit/Tahun'] = df_input_PolaDeterminstik['Harga Barang (p) /Unit'] * 0.15

# Menampilkan DataFrame
df_input_PolaDeterminstik

hasil_list_hasil_Model_Wilson_PolaDeterministik = []

total_rows = df_input_PolaDeterminstik.shape[0]  # Total baris untuk penghitungan progres

# Iterasi melalui DataFrame input Pola deterministik
for index, row in df_input_PolaDeterminstik.iterrows():
    try:
        hasil = Model_Wilson(
            Permintaan_Barang_ModelWilson_D=row['Permintaan Barang (D) Unit/Tahun'],
            Harga_barang_ModelWilson_p=row['Harga Barang (p) /Unit'],
            Ongkos_Pesan_ModelWilson_A=row['Ongkos Pesan (A) /Pesan'],
            Lead_Time_ModelWilson_L=row['Lead Time (L) Tahun'],
            Ongkos_Simpan_ModelWilson_h=row['Ongkos Simpan (h) /Unit/Tahun'],
            MaterialCode=row['Material_Code'],
            Material_Description=row['Material Description'],
            ABC_Indikator=row['ABC Indicator']
        )
        hasil_list_hasil_Model_Wilson_PolaDeterministik.append(hasil)

        # Menghitung dan menampilkan progres
        if (index + 1) % (total_rows // 10) == 0 or index == total_rows - 1:  # Menampilkan progres setiap 10%
            progress = (index + 1) / total_rows * 100
            print(f"Sedang menghitung Pola Deterministik: {progress:.2f}% selesai...")

    except ZeroDivisionError:
        # Menampilkan pesan atau log untuk baris yang dilewati (opsional)
        # print(f"Skipping row {index} due to division by zero")
        continue  # Melanjutkan iterasi berikutnya


# Membuat DataFrame dari list hasil
hasil_list_hasil_Model_Wilson_PolaDeterministik_df = pd.DataFrame(hasil_list_hasil_Model_Wilson_PolaDeterministik)

# Menyisipkan kolom "Kategori" di antara "Material Description" dan "Permintaan Barang (D) Unit/Tahun"
hasil_list_hasil_Model_Wilson_PolaDeterministik_df.insert(
    hasil_list_hasil_Model_Wilson_PolaDeterministik_df.columns.get_loc('Permintaan Barang (D) Unit/Tahun'),  # Menentukan posisi kolom "Kategori"
    'Kategori',  # Nama kolom yang akan ditambahkan
    'Pola Deterministik'  # Nilai default untuk kolom "Kategori"
)



print(f"\n----------------------------------------------------------------------------------------------")
print(f'Jumlah Data Sebelum Hitung Model Wilson - Pola Determinstik                                              : {df_input_PolaDeterminstik.shape[0]}')
print(f'Jumlah Data Setelah Hasil Hitung Model Wilson - Pola Determinstik                                        : {hasil_list_hasil_Model_Wilson_PolaDeterministik_df.shape[0]}')
print(f"----------------------------------------------------------------------------------------------\n")
# Tentukan folder output untuk menyimpan file Determinstik
output_folder2 = "s:/Project & Research/01. Pupuk Indonesia/pi/Data Pa Bambang/Data History/Model_Kalkulator_Fixed/testfolder/output"  # Ganti dengan path folder yang diinginkan
filename3 = 'Data_input_Pola_Determinstik.xlsx'
filename4 = 'Data_output_Pola_Determinstik.xlsx'

# Mengekspor data gabungan dengan progres
export_data_with_progress(df_input_PolaDeterminstik[['Material_Code','Material Description','Kategori','Permintaan Barang (D) Unit/Tahun','Harga Barang (p) /Unit','ABC Indicator','ABC Indicator','Ongkos Pesan (A) /Pesan','Ongkos Simpan (h) /Unit/Tahun']], output_folder2, filename3)
export_data_with_progress(hasil_list_hasil_Model_Wilson_PolaDeterministik_df, output_folder2, filename4)

##### Pola Normal
# Mengganti nama kolom menggunakan .loc untuk menghindari SettingWithCopyWarning
df_input_PolaNormal = df_input_PolaNormal.rename(columns={
    'Rata_Rata': 'Rata - Rata Permintaan Barang (D) Unit/Tahun',
    'Standar_Deviasi':'Standar Deviasi Permintaan Barang (s) Unit/Tahun'
})

# Menambahkan kolom baru "Ongkos Simpan (h) /Unit/Tahun" sebesar 15% dari "Harga Barang (p) /Unit" menggunakan .loc
df_input_PolaNormal.loc[:, 'Lead Time (L) Tahun'] = df_input_PolaNormal['Estimasi Lead Time (Mon)'] / 12

# Menambahkan kolom baru "Ongkos_Pesan_ModelWilson_A" menggunakan .loc
df_input_PolaNormal.loc[:, 'Ongkos Pesan (A) /Pesan'] = df_input_PolaNormal['Harga Barang (p) /Unit'].apply(
    lambda x: 5000000 if x > 100000000 else 1000000
)

# Menambahkan kolom baru "Ongkos Simpan (h) /Unit/Tahun" sebesar 15% dari "Harga Barang (p) /Unit" menggunakan .loc
df_input_PolaNormal.loc[:, 'Ongkos Simpan (h) /Unit/Tahun'] = df_input_PolaNormal['Harga Barang (p) /Unit'] * 0.15

# menambahkan kolom baru 
df_input_PolaNormal.loc[:, 'Ongkos Kekurangan Inventori (Cu) /Unit/Tahun'] = 3_720_000_000

# Menampilkan DataFrame
df_input_PolaNormal


# Inisiasi Hasil model Q Pola Normal
hasil_list_hasil_Model_Q_PolaNormal = []

total_rows_normal = df_input_PolaNormal.shape[0]

# Iterasi melalui DataFrame input Pola Normal
for index, row in df_input_PolaNormal.iterrows():
    hasil = Model_Q(
        Rata_Rata_Permintaan_Barang_ModelQ_D=row['Rata - Rata Permintaan Barang (D) Unit/Tahun'],
        Standar_Deviasi_Permintaan_Barang_ModelQ_S=row['Standar Deviasi Permintaan Barang (s) Unit/Tahun'],
        Harga_barang_ModelQ_p=row['Harga Barang (p) /Unit'],
        Ongkos_Pesan_ModelQ_A=row['Ongkos Pesan (A) /Pesan'],
        Lead_Time_ModelQ_L=row['Lead Time (L) Tahun'],
        Ongkos_Simpan_ModelQ_h=row['Ongkos Simpan (h) /Unit/Tahun'],
        Ongkos_kekurangan_inventori_setiap_unit_barang_ModelQ_Cu=row['Ongkos Kekurangan Inventori (Cu) /Unit/Tahun'],
        MaterialCode=row['Material_Code'],
        Material_Description=row['Material Description'],
        ABC_Indikator=row['ABC Indicator']
    )
    hasil_list_hasil_Model_Q_PolaNormal.append(hasil)

    # Menghitung dan menampilkan progres
    if (index + 1) % (total_rows // 10) == 0 or index == total_rows_normal - 1:  # Menampilkan progres setiap 10%
        progress = (index + 1) / total_rows_normal * 100
        print(f"Sedang menghitung Pola Normal: {progress:.2f}% selesai...")

# Membuat DataFrame dari list hasil
hasil_list_hasil_Model_Q_PolaNormal_df = pd.DataFrame(hasil_list_hasil_Model_Q_PolaNormal)

# Menyisipkan kolom "Kategori" di antara "Material Description" dan "Permintaan Barang (D) Unit/Tahun"
hasil_list_hasil_Model_Q_PolaNormal_df.insert(
    hasil_list_hasil_Model_Q_PolaNormal_df.columns.get_loc('Rata - Rata Permintaan Barang (D) Unit/Tahun'),  # Menentukan posisi kolom "Kategori"
    'Kategori',  # Nama kolom yang akan ditambahkan
    'Pola Normal'  # Nilai default untuk kolom "Kategori"
)

# # print dataframe hasil output model Normal
# hasil_list_hasil_Model_Q_PolaNormal_df

print(f"\n----------------------------------------------------------------------------------------------")
print(f'Jumlah Data Sebelum Hitung Model Wilson - Pola Normal                                              : {df_input_PolaNormal.shape[0]}')
print(f'Jumlah Data Setelah Hasil Hitung Model Wilson - Pola Normal                                        : {hasil_list_hasil_Model_Q_PolaNormal_df.shape[0]}')
print(f"----------------------------------------------------------------------------------------------\n")

# Tentukan folder output untuk menyimpan file Determinstik
output_folder2 = "s:/Project & Research/01. Pupuk Indonesia/pi/Data Pa Bambang/Data History/Model_Kalkulator_Fixed/testfolder/output"  # Ganti dengan path folder yang diinginkan
filename5 = 'Data_input_Pola_Normal.xlsx'
filename6 = 'Data_output_Pola_Normal.xlsx'

# Mengekspor data gabungan dengan progres
export_data_with_progress(df_input_PolaNormal[['Material_Code', 'Material Description', 'Kategori',
                                               'Rata - Rata Permintaan Barang (D) Unit/Tahun',
                                               'Standar Deviasi Permintaan Barang (s) Unit/Tahun', 
                                               'Harga Barang (p) /Unit', 'ABC Indicator', 'Lead Time (L) Tahun',
                                               'Ongkos Pesan (A) /Pesan', 'Ongkos Simpan (h) /Unit/Tahun', 
                                               'Ongkos Kekurangan Inventori (Cu) /Unit/Tahun']], output_folder2, filename5)

export_data_with_progress(hasil_list_hasil_Model_Q_PolaNormal_df, output_folder2, filename6)

#### Model Poisson

# Mengganti nama kolom menggunakan .loc untuk menghindari SettingWithCopyWarning
df_input_PolaPoisson = df_input_PolaPoisson.rename(columns={
    'Rata_Rata': 'Rata - Rata Permintaan Barang (D) Unit/Tahun',
    'Standar_Deviasi':'Standar Deviasi Permintaan Barang (s) Unit/Tahun'
})

# Menambahkan kolom baru "Ongkos Simpan (h) /Unit/Tahun" sebesar 15% dari "Harga Barang (p) /Unit" menggunakan .loc
df_input_PolaPoisson.loc[:, 'Lead Time (L) Tahun'] = df_input_PolaPoisson['Estimasi Lead Time (Mon)'] / 12

# Menambahkan kolom baru "Ongkos_Pesan_ModelWilson_A" menggunakan .loc
df_input_PolaPoisson.loc[:, 'Ongkos Pesan (A) /Pesan'] = df_input_PolaPoisson['Harga Barang (p) /Unit'].apply(
    lambda x: 5000000 if x > 100000000 else 1000000
)

# Menambahkan kolom baru "Ongkos Simpan (h) /Unit/Tahun" sebesar 15% dari "Harga Barang (p) /Unit" menggunakan .loc
df_input_PolaPoisson.loc[:, 'Ongkos Simpan (h) /Unit/Tahun'] = df_input_PolaPoisson['Harga Barang (p) /Unit'] * 0.15

# menambahkan kolom baru 
df_input_PolaPoisson.loc[:, 'Ongkos Kekurangan Inventori (Cu) /Unit/Tahun'] = 3720000000

# Menampilkan DataFrame
df_input_PolaPoisson


# Inisiasi Hasil model Poisson 
hasil_list_hasil_Model_Poisson = []

total_rows_poisson = df_input_PolaPoisson.shape[0]

# Iterasi melalui DataFrame input Pola Poisson
for index, row in df_input_PolaPoisson.iterrows():
    hasil = Model_Poisson(
        Rata_Rata_Pemesanan_Barang_ModelPoisson_D=row['Rata - Rata Permintaan Barang (D) Unit/Tahun'],
        Standar_Deviasi_Barang_ModelPoisson_S=row['Standar Deviasi Permintaan Barang (s) Unit/Tahun'],
        Lead_Time_ModelPoisson_L=row['Lead Time (L) Tahun'],
        Ongkos_Pesan_ModelPoisson_A=row['Ongkos Pesan (A) /Pesan'],
        Harga_Barang_ModelPoisson_p=row['Harga Barang (p) /Unit'],
        Ongkos_Simpan_ModelPoisson_h=row['Ongkos Simpan (h) /Unit/Tahun'],
        Ongkos_Kekurangan_Barang_ModelPoisson_Cu=row['Ongkos Kekurangan Inventori (Cu) /Unit/Tahun'],
        MaterialCode=row['Material_Code'],
        Material_Description=row['Material Description'],
        ABC_Indikator=row['ABC Indicator']
    )
    hasil_list_hasil_Model_Poisson.append(hasil)

    # Menghitung dan menampilkan progres
    if (index + 1) % (total_rows // 10) == 0 or index == total_rows_poisson - 1:  # Menampilkan progres setiap 10%
        progress = (index + 1) / total_rows_poisson * 100
        print(f"Sedang menghitung Pola Poisson: {progress:.2f}% selesai...")

# Membuat DataFrame dari list hasil
hasil_list_hasil_Model_Poisson_df = pd.DataFrame(hasil_list_hasil_Model_Poisson)

# Menyisipkan kolom "Kategori" di antara "Material Description" dan "Permintaan Barang (D) Unit/Tahun"
hasil_list_hasil_Model_Poisson_df.insert(
    hasil_list_hasil_Model_Poisson_df.columns.get_loc('Rata - Rata Permintaan Barang (D) Unit/Tahun'),  # Menentukan posisi kolom "Kategori"
    'Kategori',  # Nama kolom yang akan ditambahkan
    'Pola Poisson'  # Nilai default untuk kolom "Kategori"
)


print(f"\n----------------------------------------------------------------------------------------------")
print(f'Jumlah Data Sebelum Hitung Model Wilson - Pola Poisson                                              : {df_input_PolaPoisson.shape[0]}')
print(f'Jumlah Data Setelah Hasil Hitung Model Wilson - Pola Poisson                                        : {hasil_list_hasil_Model_Poisson_df.shape[0]}')
print(f"----------------------------------------------------------------------------------------------\n")

# Tentukan folder output untuk menyimpan file Determinstik
output_folder2 = "s:/Project & Research/01. Pupuk Indonesia/pi/Data Pa Bambang/Data History/Model_Kalkulator_Fixed/testfolder/output"  # Ganti dengan path folder yang diinginkan
filename7 = 'Data_input_Pola_Poisson.xlsx'
filename8 = 'Data_output_Pola_Poisson.xlsx'

# Mengekspor data gabungan dengan progres
export_data_with_progress(df_input_PolaPoisson[['Material_Code', 'Material Description', 'Kategori', 
                                                'Rata - Rata Permintaan Barang (D) Unit/Tahun',
                                                'Standar Deviasi Permintaan Barang (s) Unit/Tahun', 
                                                'Harga Barang (p) /Unit', 'ABC Indicator', 'Lead Time (L) Tahun',
                                                'Ongkos Pesan (A) /Pesan', 'Ongkos Simpan (h) /Unit/Tahun', 
                                                'Ongkos Kekurangan Inventori (Cu) /Unit/Tahun']], output_folder2, filename7)
export_data_with_progress(hasil_list_hasil_Model_Poisson_df, output_folder2, filename8)

###Pola Tak Tentu
# Mengganti nama kolom menggunakan .loc untuk menghindari SettingWithCopyWarning
df_input_PolaTakTentu = df_input_PolaTakTentu.rename(columns={
    'Rata_Rata': 'Rata - Rata Permintaan Barang (alpha)',
    'Standar_Deviasi':'Standar Deviasi Permintaan Barang (s)'
})

# menambahkan kolom baru 
df_input_PolaTakTentu.loc[:, 'Kerugian Ketidakadaan Barang (Cu) /Unit'] = 3720000000

# Inisiasi Hasil model Tchebycheff
hasil_list_hasil_Model_Tchebycheff = []

total_rows_TakTentu = df_input_PolaTakTentu.shape[0]

# Iterasi melalui DataFrame input Pola Tchebycheff
for index, row in df_input_PolaTakTentu.iterrows():
    hasil = Model_Tchebycheff_TakTentu(
        Harga_Barang_model_Tchebycheff_p=row['Harga Barang (p) /Unit'],
        Kerugian_Ketidakadaan_barang_model_Tchebycheff_Cu=row['Kerugian Ketidakadaan Barang (Cu) /Unit'],
        Standar_Deviasi_model_Tchebycheff_s=row['Standar Deviasi Permintaan Barang (s)'],
        Rata_Rata_Permintaan_barang_model_Tchebycheff_alpha=row['Rata - Rata Permintaan Barang (alpha)'],
        MaterialCode=row['Material_Code'],
        Material_Description=row['Material Description'],
        ABC_Indikator=row['ABC Indicator']
    )
    
    hasil_list_hasil_Model_Tchebycheff.append(hasil)
    # Menghitung dan menampilkan progres
    if (index + 1) % (total_rows // 10) == 0 or index == total_rows_TakTentu - 1:  # Menampilkan progres setiap 10%
        progress = (index + 1) / total_rows_TakTentu * 100
        print(f"Sedang menghitung Pola Poisson: {progress:.2f}% selesai...")

hasil_list_hasil_Model_Tchebycheff_PolaTakTentu_df = pd.DataFrame(hasil_list_hasil_Model_Tchebycheff)
hasil_list_hasil_Model_Tchebycheff_PolaTakTentu_df

# Menyisipkan kolom "Kategori" di antara "Material Description" dan "Permintaan Barang (D) Unit/Tahun"
hasil_list_hasil_Model_Tchebycheff_PolaTakTentu_df.insert(
    hasil_list_hasil_Model_Tchebycheff_PolaTakTentu_df.columns.get_loc('Rata - Rata Permintaan Barang (alpha)'),  # Menentukan posisi kolom "Kategori"
    'Kategori',  # Nama kolom yang akan ditambahkan
    'Pola Tak Tentu'  # Nilai default untuk kolom "Kategori"
)

# Tentukan folder output untuk menyimpan file Determinstik
output_folder2 = "s:/Project & Research/01. Pupuk Indonesia/pi/Data Pa Bambang/Data History/Model_Kalkulator_Fixed/testfolder/output"  # Ganti dengan path folder yang diinginkan
filename9 = 'Data_input_Pola_TakTentu.xlsx'
filename10 = 'Data_output_Pola_TakTentu.xlsx'

# Mengekspor data gabungan dengan progres
export_data_with_progress(df_input_PolaTakTentu[['Material_Code', 'Material Description', 'Kategori',
                                                 'Rata - Rata Permintaan Barang (alpha)',
                                                 'Standar Deviasi Permintaan Barang (s)', 'Harga Barang (p) /Unit',
                                                 'ABC Indicator','Kerugian Ketidakadaan Barang (Cu) /Unit']], output_folder2, filename9)
export_data_with_progress(hasil_list_hasil_Model_Tchebycheff_PolaTakTentu_df, output_folder2, filename10)

# # print dataframe hasil output model Normal
# hasil_list_hasil_Model_Q_PolaNormal_df

print(f"\n----------------------------------------------------------------------------------------------")
print(f'Jumlah Data Sebelum Hitung Model Tchebycheff - Pola Tak Tentu                                                 : {df_input_PolaTakTentu.shape[0]}')
print(f'Jumlah Data Setelah Hasil Hitung Model Tchebycheff - Pola Tak Tentu                                           : {hasil_list_hasil_Model_Tchebycheff_PolaTakTentu_df.shape[0]}')
print(f"----------------------------------------------------------------------------------------------\n")

# Membaca file Excel dan mendefinisikan kolom berdasarkan baris kedua (indeks 1)
df_verifikasi_No_Moving = pd.read_excel(
    "20Agustus_Hasil_Hitung_Kalkulator_Stock_Holding_update_Data.xlsx", 
    sheet_name= "No_Moving (Belum)", 
    header=1  # Memulai pembacaan header dari baris kedua
)
df_verifikasi_No_Moving
# Ganti titik sebagai pemisah ribuan dengan string kosong, lalu konversi menjadi float
df_verifikasi_No_Moving['Stock Out Effect'] = 3_720_000_000.00
df_verifikasi_No_Moving

# Inisiasi hasil model MinMaxRegret
hasil_list_hasil_Model_No_Moving_MinMaxRegret = []

# Iterasi melalui DataFrame input Pola No Moving
for index, row in df_verifikasi_No_Moving.iterrows():
    hasil_MinMaxRegret = Model_MinMaxRegret(
        Ongkos_pemakaian_komponen_H= row['Unit Price'],
        Ongkos_Kerugian_akibat_kerusakan_L= row['Stock Out Effect'],
        Jumlah_komponen_terpasang_m= row['Jumlah Komponen Terpasang']  
    )
    
    hasil_list_hasil_Model_No_Moving_MinMaxRegret.append(hasil_MinMaxRegret)

# Konversi hasil ke dalam DataFrame untuk tampilan yang lebih baik
df_hasil_Model_No_Moving_MinMaxRegret = pd.DataFrame(hasil_list_hasil_Model_No_Moving_MinMaxRegret)

pd.options.display.float_format = '{:,.0f}'.format
# Tampilkan hasil
df_hasil_Model_No_Moving_MinMaxRegret


# Inisiasi hasil model LinearKerusakan
hasil_list_hasil_Model_No_Moving_LinearKerusakan = []

# Iterasi melalui DataFrame input Pola No Moving
for index, row in df_verifikasi_No_Moving.iterrows():
    hasil_LinearKerusakan = model_kerusakan_linear(
        Ongkos_pemakaian_komponen_H= row['Unit Price'],
        Ongkos_Kerugian_akibat_kerusakan_L= row['Stock Out Effect'],
        Jumlah_komponen_terpasang_m= row['Jumlah Komponen Terpasang']  
    )
    
    hasil_list_hasil_Model_No_Moving_LinearKerusakan.append(hasil_LinearKerusakan)

# Konversi hasil ke dalam DataFrame untuk tampilan yang lebih baik
df_hasil_Model_No_Moving_LinearKerusakan = pd.DataFrame(hasil_list_hasil_Model_No_Moving_LinearKerusakan)

pd.options.display.float_format = '{:,.0f}'.format
# Tampilkan hasil
df_hasil_Model_No_Moving_LinearKerusakan

# Inisiasi hasil model MinMaxRegret
hasil_list_hasil_Model_No_Moving_Non_LinearKerusakan_beta4 = []

# Iterasi melalui DataFrame input Pola No Moving
for index, row in df_verifikasi_No_Moving.iterrows():
    hasil_Non_LinearKerusakan_beta4 = model_kerusakan_non_linear(
        Ongkos_pemakaian_komponen_H= row['Unit Price'],
        Ongkos_Kerugian_akibat_kerusakan_L= row['Stock Out Effect'],
        Jumlah_komponen_terpasang_m= row['Jumlah Komponen Terpasang'],
        beta=4  
    )
    
    hasil_list_hasil_Model_No_Moving_Non_LinearKerusakan_beta4.append(hasil_Non_LinearKerusakan_beta4)

# Konversi hasil ke dalam DataFrame untuk tampilan yang lebih baik
df_hasil_Model_No_Moving_Non_LinearKerusakan_beta4 = pd.DataFrame(hasil_list_hasil_Model_No_Moving_Non_LinearKerusakan_beta4)

pd.options.display.float_format = '{:,.0f}'.format
# Tampilkan hasil
df_hasil_Model_No_Moving_Non_LinearKerusakan_beta4


# Inisiasi hasil model MinMaxRegret
hasil_list_hasil_Model_No_Moving_Non_LinearKerusakan_beta5 = []

# Iterasi melalui DataFrame input Pola No Moving
for index, row in df_verifikasi_No_Moving.iterrows():
    hasil_Non_LinearKerusakan_beta5 = model_kerusakan_non_linear(
        Ongkos_pemakaian_komponen_H= row['Unit Price'],
        Ongkos_Kerugian_akibat_kerusakan_L= row['Stock Out Effect'],
        Jumlah_komponen_terpasang_m= row['Jumlah Komponen Terpasang'],
        beta=5  
    )
    
    hasil_list_hasil_Model_No_Moving_Non_LinearKerusakan_beta5.append(hasil_Non_LinearKerusakan_beta5)

# Konversi hasil ke dalam DataFrame untuk tampilan yang lebih baik
df_hasil_Model_No_Moving_Non_LinearKerusakan_beta5 = pd.DataFrame(hasil_list_hasil_Model_No_Moving_Non_LinearKerusakan_beta5)

pd.options.display.float_format = '{:,.0f}'.format
# Tampilkan hasil
df_hasil_Model_No_Moving_Non_LinearKerusakan_beta5

# Tentukan folder output untuk menyimpan file
output_folder = "s:/Project & Research/01. Pupuk Indonesia/pi/Data Pa Bambang/Data History/Model_Kalkulator_Fixed/testfolder/output"  # Ganti dengan path folder yang diinginkan
filename11 = 'Data_Output_MinMaxRegret.xlsx'
filename12 = 'Data_Output_LinearKerusakan.xlsx'
filename13 = 'Data_Output_Non_LinearKerusakan_beta4.xlsx'
filename14 = 'Data_Output_Non_LinearKerusakan_beta4.xlsx'


# Mengekspor data gabungan dengan progres
export_data_with_progress(df_hasil_Model_No_Moving_MinMaxRegret, output_folder, filename11)
export_data_with_progress(df_hasil_Model_No_Moving_LinearKerusakan, output_folder, filename12)
export_data_with_progress(df_hasil_Model_No_Moving_Non_LinearKerusakan_beta4, output_folder, filename13)
export_data_with_progress(df_hasil_Model_No_Moving_Non_LinearKerusakan_beta5, output_folder, filename14)


# Membaca file Excel dan mendefinisikan kolom berdasarkan baris kedua (indeks 1)
df_verifikasi_Model_BCR = pd.read_excel(
    "20Agustus_Hasil_Hitung_Kalkulator_Stock_Holding_update_Data.xlsx", 
    sheet_name="BCR (belum)", 
    header=1  # Memulai pembacaan header dari baris kedua
)

# Ganti titik sebagai pemisah ribuan dengan string kosong, lalu konversi menjadi float
df_verifikasi_Model_BCR['Stock Out Effect'] = 3_720_000_000
df_verifikasi_Model_BCR

# Inisiasi hasil model BCR
hasil_list_hasil_Model_BCR = []

# Iterasi melalui DataFrame input Pola No Moving
for index, row in df_verifikasi_Model_BCR.iterrows():
    hasil_Model_BCR = Model_Inventori_BCR(
    Harga_Komponen_Ho=row['Unit Price'],
    Kerugian_Komponen_Co=row['Stock Out Effect'],
    Suku_bunga_i= 0.1,
    Waktu_sisa_operasi=row['Sisa Tahun Pemakaian'],
    probabilitas= "uniform"
    )
    # Tambahkan hasil ke dalam list
    hasil_list_hasil_Model_BCR.append(hasil_Model_BCR)

# Konversi hasil ke dalam DataFrame untuk tampilan yang lebih baik
df_hasil_Model_BCR_Uniform = pd.DataFrame(hasil_list_hasil_Model_BCR)

pd.options.display.float_format = '{:,.0f}'.format

# Export dataaset
filename15 = 'Data_Output_Non_Linear_ModelBCR_Uniform.xlsx'


# Mengekspor data gabungan dengan progres
export_data_with_progress(df_hasil_Model_BCR_Uniform, output_folder, filename15)