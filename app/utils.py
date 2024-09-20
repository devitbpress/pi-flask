import pandas as pd
import numpy as np
from scipy.stats import f, shapiro, kstest, poisson, chisquare

from app.calc import Model_Wilson_PolaDeterministik
from app.calc import Model_Tchebycheff_PolaTakTentu
from app.calc import Model_Q_PolaDistribusiNormal
from app.calc import Model_Poisson_PolaPoisson
from app.calc import Model_MinMaxRegret_PolaNonMoving
from app.calc import Model_KerusakanNonLinear_PolaNonMoving
from app.calc import Model_KerusakanLinear_PolaNonMoving
from app.calc import Model_BCR_new

datafile_session = {}
dataframe_session = {}

def convert_string_to_number(s):
    if '.' in s:
        return convert_string_to_number(s)
    else:
        return int(s)

def calc_model(data, model):
    data_calc = []
    
    if model == "wilson":
        required_keys = ["Permintaan Barang (D) Unit/Tahun","Harga Barang (p) /Unit","Ongkos Pesan (A) /Pesan","Lead Time (L) Tahun","Ongkos Simpan (h) /Unit/Tahun","Material Code","Material Description","ABC Indicator"]
        
        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}

            permintaan_barang = item["Permintaan Barang (D) Unit/Tahun"]
            harga_barang = item["Harga Barang (p) /Unit"]
            ongkos_pesan = item["Ongkos Pesan (A) /Pesan"]
            lead_time = item["Lead Time (L) Tahun"]
            ongkos_simpan = item["Ongkos Simpan (h) /Unit/Tahun"]
            material_code = item["Material Code"]
            material_description = item["Material Description"]
            abc_indikator = item["ABC Indicator"]
            
            data_calc.append(Model_Wilson_PolaDeterministik.Model_Wilson(
                permintaan_barang,
                harga_barang, 
                ongkos_pesan, 
                lead_time, 
                ongkos_simpan, 
                material_code,
                material_description,
                abc_indikator
            ))
    
    if model == "tchebycheff":
        required_keys = ["Harga Barang (p) /Unit","Kerugian Ketidakadaan Barang (Cu) /Unit","Standar Deviasi Permintaan Barang (s)","Rata - Rata Permintaan Barang (alpha)"]

        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            harga_barang = item["Harga Barang (p) /Unit"]
            kerugian_ketidakadaan_barang = item["Kerugian Ketidakadaan Barang (Cu) /Unit"]
            standar_deviasi = item["Standar Deviasi Permintaan Barang (s)"]
            rata_rata_permintaan_barang = item["Rata - Rata Permintaan Barang (alpha)"]
            material_code = item["Material Code"]
            material_description = item["Material Description"]
            abc_indikator = item["ABC Indicator"]
            
            data_calc.append(Model_Tchebycheff_PolaTakTentu.Model_Tchebycheff_TakTentu(
                harga_barang, 
                kerugian_ketidakadaan_barang, 
                standar_deviasi, 
                rata_rata_permintaan_barang, 
                material_code,
                material_description,
                abc_indikator))
    
    if model == "q":
        required_keys = ["Rata - Rata Permintaan Barang (D) Unit/Tahun","Lead Time (L) Tahun","Standar Deviasi Permintaan Barang (s) Unit/Tahun","Ongkos Pesan (A) /Pesan","Harga Barang (p) /Unit","Ongkos Simpan (h) /Unit/Tahun","Ongkos Kekurangan Inventori (Cu) /Unit/Tahun","Material Code","Material Description","ABC Indicator"]

        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            rata_rata_permintaan_barang =  item['Rata - Rata Permintaan Barang (D) Unit/Tahun']
            lead_time = item['Lead Time (L) Tahun']
            standar_deviasi = item['Standar Deviasi Permintaan Barang (s) Unit/Tahun']
            ongkos_pesan = item['Ongkos Pesan (A) /Pesan']
            harga_barang = item['Harga Barang (p) /Unit']
            ongkos_simpan = item['Ongkos Simpan (h) /Unit/Tahun']
            ongkos_kekurangan_inventori_setiap_unit_barang = item['Ongkos Kekurangan Inventori (Cu) /Unit/Tahun']
            material_code = item['Material Code']
            material_description = item['Material Description']
            abc_indikator = item['ABC Indicator']
            
            data_calc.append(Model_Q_PolaDistribusiNormal.Model_Q(rata_rata_permintaan_barang , 
                lead_time, 
                standar_deviasi, 
                ongkos_pesan ,
                harga_barang,
                ongkos_simpan, 
                ongkos_kekurangan_inventori_setiap_unit_barang,
                material_code, 
                material_description, 
                abc_indikator))
    
    if model == "poisson":
        required_keys = ["Rata - Rata Permintaan Barang (D) Unit/Tahun","Standar Deviasi Permintaan Barang (s) Unit/Tahun","Lead Time (L) Tahun","Ongkos Pesan (A) /Pesan","Harga Barang (p) /Unit","Ongkos Simpan (h) /Unit/Tahun","Ongkos Kekurangan Inventori (Cu) /Unit/Tahun",]
        
        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            rata_rata_pemesanan_barang = item["Rata - Rata Permintaan Barang (D) Unit/Tahun"]
            standar_deviasi_barang = item["Standar Deviasi Permintaan Barang (s) Unit/Tahun"]
            lead_time = item["Lead Time (L) Tahun"]
            ongkos_pesan = item["Ongkos Pesan (A) /Pesan"]
            harga_barang = item["Harga Barang (p) /Unit"]
            ongkos_simpan = item["Ongkos Simpan (h) /Unit/Tahun"]
            ongkos_kekurangan_barang = item["Ongkos Kekurangan Inventori (Cu) /Unit/Tahun"]
            material_code = item["Material Code"]
            material_description = item["Material Description"]
            abc_indikator = item["ABC Indicator"]
            
            data_calc.append(Model_Poisson_PolaPoisson.Model_Poisson(
                rata_rata_pemesanan_barang, 
                standar_deviasi_barang, 
                lead_time,
                ongkos_pesan, 
                harga_barang, 
                ongkos_simpan, 
                ongkos_kekurangan_barang,
                material_code,
                material_description,
                abc_indikator
            ))

    if model == "nonmoving":
        required_keys = ["Ongkos Pemakaian Komponen (H)", "Ongkos Kerugian Akibat Kerusakan (L)", "Jumlah Komponen Terpasang (m)"]
        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            material_code = item["Material Code"]
            material_description = item["Material Description"]
            abc_indikator = item["ABC Indicator"]
            ongkos_pemakaian_komponen = item["Ongkos Pemakaian Komponen (H)"]
            ongkos_kerugian_akibat_kerusakan = item["Ongkos Kerugian Akibat Kerusakan (L)"]
            jumlah_komponen_terpasang = item["Jumlah Komponen Terpasang (m)"]
            
            data_calc.append({
                "regret": Model_MinMaxRegret_PolaNonMoving.Model_MinMaxRegret(
                    ongkos_pemakaian_komponen,
                    ongkos_kerugian_akibat_kerusakan,
                    jumlah_komponen_terpasang,
                    material_code,
                    material_description,
                    abc_indikator
                ),
                "linear": Model_KerusakanLinear_PolaNonMoving.model_kerusakan_linear(
                    ongkos_pemakaian_komponen,
                    ongkos_kerugian_akibat_kerusakan,
                    jumlah_komponen_terpasang,
                    material_code,
                    material_description,
                    abc_indikator
                ),
                "non_linear": Model_KerusakanNonLinear_PolaNonMoving.model_kerusakan_non_linear(
                    ongkos_pemakaian_komponen,
                    ongkos_kerugian_akibat_kerusakan,
                    jumlah_komponen_terpasang,
                    material_code,
                    material_description,
                    abc_indikator,
                )
            })

    if model == "bcr":
        required_keys = ["Harga Komponen (Ho)", "Kerugian Komponen (Co)", "Suku Bunga (I)", "Waktu Sisa Operasi (tahun)"]
        
        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            material_code = item["Material Code"]
            material_description = item["Material Description"]
            abc_indikator = item["ABC Indicator"]
            harga_komponen = item["Harga Komponen (Ho)"]
            kerugian_komponen = item["Kerugian Komponen (Co)"]
            suku_bunga = item["Suku Bunga (I)"]
            waktu_sisa_operasi = item["Waktu Sisa Operasi (tahun)"]
            
            data_calc.append(Model_BCR_new.Model_Inventori_BCR(
                harga_komponen,
                kerugian_komponen, 
                suku_bunga, 
                waktu_sisa_operasi,
                material_code,
                material_description,
                abc_indikator,
            ))

    return data_calc

def calc_model_manual(data):
    model = data.get("model")
    data_calc = {}
    
    if model == "Q":
        rata_rata_permintaan_barang = convert_string_to_number(data.get('rata_rata_permintaan_barang'))
        lead_time = convert_string_to_number(data.get('lead_time'))
        standar_deviasi = convert_string_to_number(data.get('standar_deviasi'))
        ongkos_pesan = convert_string_to_number(data.get('ongkos_pesan'))
        harga_barang = convert_string_to_number(data.get('harga_barang'))
        ongkos_simpan = convert_string_to_number(data.get('ongkos_simpan'))
        ongkos_kekurangan_inventori_setiap_unit_barang = convert_string_to_number(data.get('ongkos_kekurangan_inventory'))
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
 
        data_calc = Model_Q_PolaDistribusiNormal.Model_Q(
                rata_rata_permintaan_barang , 
                lead_time, 
                standar_deviasi, 
                ongkos_pesan ,
                harga_barang,
                ongkos_simpan, 
                ongkos_kekurangan_inventori_setiap_unit_barang,
                material_code,
                material_description,
                abc_indikator
            )
    
    if model == "Poisson":
        rata_rata_pemesanan_barang = convert_string_to_number(data.get("rata_rata_permintaan_barang"))
        standar_deviasi_barang = convert_string_to_number(data.get("standar_deviasi"))
        lead_time = convert_string_to_number(data.get("lead_time"))
        ongkos_pesan = convert_string_to_number(data.get("ongkos_pesan"))
        harga_barang = convert_string_to_number(data.get("harga_barang"))
        ongkos_simpan = convert_string_to_number(data.get("ongkos_simpan"))
        ongkos_kekurangan_barang = convert_string_to_number(data.get("ongkos_kekurangan_inventory"))
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")

        data_calc = Model_Poisson_PolaPoisson.Model_Poisson(
                rata_rata_pemesanan_barang, 
                standar_deviasi_barang, 
                lead_time,
                ongkos_pesan, 
                harga_barang, 
                ongkos_simpan, 
                ongkos_kekurangan_barang,
                material_code,
                material_description,
                abc_indikator
            )
    
    if model == "Wilson":
        permintaan_barang = convert_string_to_number(data.get("permintaan_barang"))
        harga_barang = convert_string_to_number(data.get("harga_barang"))
        ongkos_pesan = convert_string_to_number(data.get("ongkos_pesan"))
        lead_time = convert_string_to_number(data.get("lead_time"))
        ongkos_simpan = convert_string_to_number(data.get("ongkos_simpan"))
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        
        data_calc = Model_Wilson_PolaDeterministik.Model_Wilson(
                permintaan_barang,
                harga_barang, 
                ongkos_pesan, 
                lead_time, 
                ongkos_simpan, 
                material_code,
                material_description,
                abc_indikator
            )
    
    if model == "Tchebycheff":
        harga_barang = convert_string_to_number(data.get("harga_barang"))
        kerugian_ketidakadaan_barang = convert_string_to_number(data.get("kerugian_ketidakadaan_barang"))
        standar_deviasi = convert_string_to_number(data.get("standar_deviasi"))
        rata_rata_permintaan_barang = convert_string_to_number(data.get("rata_rata_permintaan_barang"))
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        
        data_calc = Model_Tchebycheff_PolaTakTentu.Model_Tchebycheff_TakTentu(
            harga_barang, 
            kerugian_ketidakadaan_barang, 
            standar_deviasi, 
            rata_rata_permintaan_barang, 
            material_code,
            material_description,
            abc_indikator)
    
    if model == "Regret":
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        ongkos_pemakaian_komponen = convert_string_to_number(data.get("ongkos_pemakaian_komponen"))
        ongkos_kerugian_akibat_kerusakan = convert_string_to_number(data.get("ongkos_kerugian_kerusakan"))
        jumlah_komponen_terpasang = convert_string_to_number(data.get("jumlah_komponen_terpasang"))
        
        data_calc = Model_MinMaxRegret_PolaNonMoving.Model_MinMaxRegret(
                        ongkos_pemakaian_komponen,
                        ongkos_kerugian_akibat_kerusakan,
                        jumlah_komponen_terpasang,
                        material_code,
                        material_description,
                        abc_indikator
                    )
    
    if model == "Linear":
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        ongkos_pemakaian_komponen = convert_string_to_number(data.get("ongkos_pemakaian_komponen"))
        ongkos_kerugian_akibat_kerusakan = convert_string_to_number(data.get("ongkos_kerugian_kerusakan"))
        jumlah_komponen_terpasang = convert_string_to_number(data.get("jumlah_komponen_terpasang"))

        data_calc = Model_KerusakanLinear_PolaNonMoving.model_kerusakan_linear(
                        ongkos_pemakaian_komponen,
                        ongkos_kerugian_akibat_kerusakan,
                        jumlah_komponen_terpasang,
                        material_code,
                        material_description,
                        abc_indikator
                    )
    
    if model == "NonLinear":
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        ongkos_pemakaian_komponen = convert_string_to_number(data.get("ongkos_pemakaian_komponen"))
        ongkos_kerugian_akibat_kerusakan = convert_string_to_number(data.get("ongkos_kerugian_kerusakan"))
        jumlah_komponen_terpasang = convert_string_to_number(data.get("jumlah_komponen_terpasang"))

        data_calc = Model_KerusakanNonLinear_PolaNonMoving.model_kerusakan_non_linear(
                        ongkos_pemakaian_komponen,
                        ongkos_kerugian_akibat_kerusakan,
                        jumlah_komponen_terpasang,
                        material_code,
                        material_description,
                        abc_indikator
                    )
    
    if model == "BCR":
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        harga_komponen = convert_string_to_number(data.get("harga_komponen"))
        kerugian_komponen = convert_string_to_number(data.get("kerugian_komponen"))
        suku_bunga = convert_string_to_number(data.get("suku_bunga"))
        waktu_sisa_operasi = convert_string_to_number(data.get("waktu_sisa_operasi"))
        
        data_calc = Model_BCR_new.Model_Inventori_BCR(
                harga_komponen,
                kerugian_komponen, 
                suku_bunga, 
                waktu_sisa_operasi,
                material_code,
                material_description,
                abc_indikator,
            )
    
    return data_calc

def normalize_and_combine_dataframes(*df_tuples):
    dfs = []
    for df in df_tuples:
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
    # Reset index untuk hasil akhir
    result.reset_index(drop=True, inplace=True)
    unmatched_cancels.reset_index(drop=True, inplace=True)
    matched_df.reset_index(drop=True, inplace=True)
    
    # Drop semua baris dengan Mvt_type 'cancel' dari result
    result = result[result['Mvt_type'] != 'cancel']
    
    return result, unmatched_cancels, matched_df

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
    ordered_columns = ['Material_Code', 'Kategori', 'Proses1', 'Proses2', 'Jumlah_Data', 'Rata_Rata', 'Variansi', 'Standar_Deviasi', 'P_Value', 'Deskripsi_Pengujian_Statistik', 'Hasil_uji']
    grouped = grouped[ordered_columns]

    return grouped

def delete_datafile(numid, session_id):
    if session_id in datafile_session:
        for item in datafile_session[session_id]:
            if numid in item:
                del item[numid]

    return "success"

def processing_save_dataframe(df, num_id, session_id):
    if session_id not in datafile_session:
        datafile_session[session_id] = []
    datafile_session[session_id].append({num_id: df})

    return df

def processing_subset(session_id):
    dataframes = [value for item in datafile_session[session_id] for value in item.values()]
    print("mulai normalize")
    df_com_hist = normalize_and_combine_dataframes(*dataframes)
    print("mulai filterisasi")
    filtered_df, unmatched_cancels_df, matched_df = process_data(df_com_hist)
    filtered_df = filtered_df.rename(columns={'Material': 'Material_Code', 'Unnamed: 7': 'Quantity(EA)'})
    data_input_sebelum_klasifikasi = filtered_df[['Posting Date', 'Material_Code', 'Material Description', 'Quantity(EA)', 'Movement Type']]
    dataframe_session[session_id] = []
    dataframe_session[session_id].append({"subset": filtered_df})

    return data_input_sebelum_klasifikasi

def processing_classification(session_id):
    filtered_df = dataframe_session[session_id][0]['subset']
    filtered_df['Has_Z61'] = filtered_df['Movement Type'] == 'Z61'
    Hasil_Klasifikasi = count_and_stats_by_material(filtered_df)
    filtered_df_unique = filtered_df[['Material_Code', 'Material Description']].drop_duplicates(subset='Material_Code')
    Hasil_Klasifikasi = Hasil_Klasifikasi.merge(filtered_df_unique, how='left', left_on='Material_Code', right_on='Material_Code')
    cols = list(Hasil_Klasifikasi.columns)
    material_code_index = cols.index('Material_Code')
    cols.insert(material_code_index + 1, cols.pop(cols.index('Material Description')))
    Hasil_Klasifikasi = Hasil_Klasifikasi[cols]
    dataframe_session[session_id].append({"class": Hasil_Klasifikasi})

    return Hasil_Klasifikasi
