import numpy as np
import pandas as pd

# Model Kerusakan Linear
# Parameter
# 1. Kriteria Kinerja 
    # ekspetasi ongkos inventori minimum -> E(qi)
# 2. Variable Keputusan
    # Ukuran lot penyediaan stock ekonomis -> qi
# 3. Parameter
    # Jumlah komponen terpasang         -> m, dalam unit diisi dengan nilai integer
    # Ongkos pemakaian komponen         -> H, (Rp/unit/hari)
    # Ongkos kekurangan komponen        -> L (Rp./unit/hari)
    # Harga resale komponen             -> O (Rp./unit/hari)
# sampel data contoh


# 1. Tentukan jumlah komponen m dan jumlah kerusakannya (Dj), dimulai tidak terjadi kerusakan yaitu 0 sampai dengan rusak semua yaitu m
# 2. Tentukan strategi pasokan atau penyediaan (qi) yang dipertimbangkan sesuai dengan informasi kerusakannya (Dj), dimulai tidak penyediaan komponen yaitu 0 sampai dengan semua kerusakan dipenuhi yaitu m

import numpy as np
import pandas as pd

def model_kerusakan_linear(
        Ongkos_pemakaian_komponen_H,
        Ongkos_Kerugian_akibat_kerusakan_L, 
        Jumlah_komponen_terpasang_m=5, 
        MaterialCode=None, 
        Material_Description=None, 
        ABC_Indikator=None,
        Harga_resale_komponen_O=None,
    ):
    # Set default value for Harga_resale_komponen_O if not provided
    if Harga_resale_komponen_O is None:
        Harga_resale_komponen_O = Ongkos_pemakaian_komponen_H * 0.2

    # 1. Fungsi untuk menghitung matriks pay-off
    def matrix_payoff(Jumlah_komponen_terpasang_m, Ongkos_pemakaian_komponen_H, Ongkos_Kerugian_akibat_kerusakan_L, Harga_resale_komponen_O):
        matriks = np.zeros((Jumlah_komponen_terpasang_m + 1, Jumlah_komponen_terpasang_m + 1))
        for strategi_penyediaan_qi in range(Jumlah_komponen_terpasang_m + 1):
            for ekspetasi_kerusakan_Dj in range(Jumlah_komponen_terpasang_m + 1):
                if strategi_penyediaan_qi >= ekspetasi_kerusakan_Dj:
                    matriks[strategi_penyediaan_qi, ekspetasi_kerusakan_Dj] = (
                        Ongkos_pemakaian_komponen_H * strategi_penyediaan_qi
                    ) - (Harga_resale_komponen_O * (strategi_penyediaan_qi - ekspetasi_kerusakan_Dj))
                else:
                    matriks[strategi_penyediaan_qi, ekspetasi_kerusakan_Dj] = (
                        Ongkos_pemakaian_komponen_H * strategi_penyediaan_qi
                    ) + (Ongkos_Kerugian_akibat_kerusakan_L * (ekspetasi_kerusakan_Dj - strategi_penyediaan_qi))
        return matriks
    
    # Membuat matriks ongkos inventori dari fungsi matrix_payoff
    matriks_hasil_payoff_kerusakan_linear = matrix_payoff(Jumlah_komponen_terpasang_m, Ongkos_pemakaian_komponen_H, Ongkos_Kerugian_akibat_kerusakan_L, Harga_resale_komponen_O)

    matriks_hasil_payoff_kerusakan_linear_df = pd.DataFrame(matriks_hasil_payoff_kerusakan_linear, columns=[f'Kerusakan {i}' for i in range(Jumlah_komponen_terpasang_m+1)])


    # Hitung Nilai P(Dj)
    sum_dj = sum(range(Jumlah_komponen_terpasang_m+1))
    for Dj in range(Jumlah_komponen_terpasang_m+1):
        value = (Jumlah_komponen_terpasang_m - Dj) / sum_dj
        matriks_hasil_payoff_kerusakan_linear_df.at['P(Dj)', f'Kerusakan {Dj}'] = value

    # Inisialisasi kolom E(Qi)
    matriks_hasil_payoff_kerusakan_linear_df['E(Qi)'] = 0.0  

    # Hitung nilai E(Qi)
    for i in range(len(matriks_hasil_payoff_kerusakan_linear_df.index) - 1):  # -1 untuk tidak termasuk baris 'P(Dj)'
        E_qi = 0  # Inisialisasi E_qi untuk baris ini
        for j in range(Jumlah_komponen_terpasang_m+1):  # Menerapkan sum pada definisi E(Qi)
            E_qi += matriks_hasil_payoff_kerusakan_linear_df.loc['P(Dj)', f'Kerusakan {j}'] * matriks_hasil_payoff_kerusakan_linear_df.iloc[i, j]
        matriks_hasil_payoff_kerusakan_linear_df.at[matriks_hasil_payoff_kerusakan_linear_df.index[i], 'E(Qi)'] = E_qi

    # Format matriks hasil payoff kerusakan linear
    matriks_hasil_payoff_kerusakan_linear_df.at['P(Dj)', 'E(Qi)'] = np.nan

    # # Cetak parameter input model
    # print(f"----------------------------------------------------------------------------------------------")
    # print(f"Parameter Input Model Probabilistik Kerusakan Linear")
    # print(f"Ongkos Pemakaian Sparepart: Rp {Ongkos_pemakaian_komponen_H:,.0f}.-")
    # print(f"Kerugian Ketidakseterdiaan Sparepart: Rp {Ongkos_Kerugian_akibat_kerusakan_L:,.0f}.-")
    # print(f"Harga Resale Sparepart: Rp {Harga_resale_komponen_O:,.0f}.-")
    # print(f"Jumlah komponen terpasang: {Jumlah_komponen_terpasang_m:.0f}")
    # print(f"----------------------------------------------------------------------------------------------")
    # print(f" ")
    # print(f"----------------------------------------------------------------------------------------------")
    # print(f"Ongkos Model Probabilistik Kerusakan (Linier) Rp {min(matriks_hasil_payoff_kerusakan_linear_df['E(Qi)']):,.0f}.-")
    # print(f"Strategi Penyediaan optimal model Probabilistik Kerusakan Linear adalah {matriks_hasil_payoff_kerusakan_linear_df['E(Qi)'].idxmin()} Unit")
    # print(f"----------------------------------------------------------------------------------------------")

    # Simpan hasil dalam dictionary
    hasil_model_kerusakan_linear = {
        "Material Code": MaterialCode,
        "Material Description": Material_Description,
        "ABC Indicator": ABC_Indikator,
        "Ongkos Pemakaian Komponen (H)": Ongkos_pemakaian_komponen_H,
        "Ongkos Kerugian Akibat Kerusakan (L)": Ongkos_Kerugian_akibat_kerusakan_L,
        "Jumlah Komponen Terpasang (m)": Jumlah_komponen_terpasang_m,
        "Harga Resale Komponen (O)": Harga_resale_komponen_O,
        "Ongkos Model Probabilistik Kerusakan": min(matriks_hasil_payoff_kerusakan_linear_df['E(Qi)']),
        "Strategi Penyediaan Optimal (Unit)": matriks_hasil_payoff_kerusakan_linear_df['E(Qi)'].idxmin()
    }

    return hasil_model_kerusakan_linear

# Contoh penggunaan fungsi
# Ongkos_pemakaian_komponen_H = 820000000
# Ongkos_Kerugian_akibat_kerusakan_L = 1784145909

# Panggil fungsi model_kerusakan_linear
# hasil_model_kerusakan_linear = model_kerusakan_linear(Ongkos_pemakaian_komponen_H, Ongkos_Kerugian_akibat_kerusakan_L, Jumlah_komponen_terpasang_m=5)
# print(hasil_model_kerusakan_linear)