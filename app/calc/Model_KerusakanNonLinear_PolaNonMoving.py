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

def model_kerusakan_non_linear(
        Ongkos_pemakaian_komponen_H, 
        Ongkos_Kerugian_akibat_kerusakan_L, 
        Jumlah_komponen_terpasang_m=5, 
        MaterialCode=None, 
        Material_Description=None, 
        ABC_Indikator=None,
        Harga_resale_komponen_O=None, 
        beta=4
    ):
    # Set default value for Harga_resale_komponen_O if not provided
    if Harga_resale_komponen_O is None:
        Harga_resale_komponen_O = Ongkos_pemakaian_komponen_H * 0.2

    # Validasi nilai beta hanya boleh 4 atau 5
    if beta not in [4, 5]:
        raise ValueError("Nilai beta hanya boleh 4 atau 5.")

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
    matriks_hasil_payoff_kerusakan_non_linear = matrix_payoff(Jumlah_komponen_terpasang_m, Ongkos_pemakaian_komponen_H, Ongkos_Kerugian_akibat_kerusakan_L, Harga_resale_komponen_O)

    matriks_hasil_payoff_kerusakan_non_linear_df = pd.DataFrame(matriks_hasil_payoff_kerusakan_non_linear, columns=[f'Kerusakan {i}' for i in range(Jumlah_komponen_terpasang_m+1)])

    # Hitung batas maksimum untuk nilai P(Dj) pada beta 4 dan beta 5
    max_Dj_beta_4 = 8
    max_Dj_beta_5 = 10

    # Hitung Nilai P(Dj) dengan logika non-linear
    sum_inverse = sum(1 / (beta * Dj) for Dj in range(1, Jumlah_komponen_terpasang_m+1))  # Sum untuk Dj > 0
    for Dj in range(Jumlah_komponen_terpasang_m+1):
        if Dj == 0:
            value = 1 - sum_inverse
            if beta == 4 and value > max_Dj_beta_4:
                beta = 5
                # print(f"Nilai pada Dj = 0 lebih besar dari batas maksimum untuk beta 4. Beta diubah menjadi {beta}.")
                sum_inverse = sum(1 / (beta * Dj) for Dj in range(1, Jumlah_komponen_terpasang_m+1))
                value = 1 - sum_inverse
                if value > max_Dj_beta_5:
                    # print("range(Jumlah_komponen_terpasang_m+1) harus dibatasi/dikurangi.")
                    break
        else:
            if beta == 4 and 1 / (beta * Dj) > max_Dj_beta_4:
                value = max_Dj_beta_4
            elif beta == 5 and 1 / (beta * Dj) > max_Dj_beta_5:
                value = max_Dj_beta_5
            else:
                value = 1 / (beta * Dj)
        matriks_hasil_payoff_kerusakan_non_linear_df.at['P(Dj)', f'Kerusakan {Dj}'] = value

    # Inisialisasi kolom E(Qi)
    matriks_hasil_payoff_kerusakan_non_linear_df['E(Qi)'] = 0.0  

    # Hitung nilai E(Qi)
    for i in range(len(matriks_hasil_payoff_kerusakan_non_linear_df.index) - 1):  # -1 untuk tidak termasuk baris 'P(Dj)'
        E_qi = 0  # Inisialisasi E_qi untuk baris ini
        for j in range(Jumlah_komponen_terpasang_m+1):  # Menerapkan sum pada definisi E(Qi)
            E_qi += matriks_hasil_payoff_kerusakan_non_linear_df.loc['P(Dj)', f'Kerusakan {j}'] * matriks_hasil_payoff_kerusakan_non_linear_df.iloc[i, j]
        matriks_hasil_payoff_kerusakan_non_linear_df.at[matriks_hasil_payoff_kerusakan_non_linear_df.index[i], 'E(Qi)'] = E_qi

    # Format matriks hasil payoff kerusakan non-linear
    matriks_hasil_payoff_kerusakan_non_linear_df.at['P(Dj)', 'E(Qi)'] = np.nan


    # # Cetak parameter input model
    # print(f"----------------------------------------------------------------------------------------------")
    # print(f"Parameter Input Model Probabilistik Kerusakan Non-Linear")
    # print(f"Ongkos Pemakaian Sparepart: Rp {Ongkos_pemakaian_komponen_H:,.0f}.-")
    # print(f"Kerugian Ketidakseterdiaan Sparepart: Rp {Ongkos_Kerugian_akibat_kerusakan_L:,.0f}.-")
    # print(f"Harga Resale Sparepart: Rp {Harga_resale_komponen_O:,.0f}.-")
    # print(f"Jumlah komponen terpasang: {Jumlah_komponen_terpasang_m:.0f}")
    # print(f"Beta: {beta}")
    # print(f"----------------------------------------------------------------------------------------------")
    # print(f" ")
    # print(f"----------------------------------------------------------------------------------------------")
    # print(f"Ongkos Model Probabilistik Kerusakan (Non-Linier) Rp {min(matriks_hasil_payoff_kerusakan_non_linear_df['E(Qi)']):,.0f}.-")
    # print(f"Strategi Penyediaan optimal model Probabilistik Kerusakan Non-Linear adalah {matriks_hasil_payoff_kerusakan_non_linear_df['E(Qi)'].idxmin()} Unit")
    # print(f"----------------------------------------------------------------------------------------------")

    # Simpan hasil dalam dictionary
    hasil_model_kerusakan_non_linear = {
        "Material Code": MaterialCode,
        "Material Description": Material_Description,
        "ABC Indicator": ABC_Indikator,
        "Ongkos Pemakaian Komponen (H)": Ongkos_pemakaian_komponen_H,
        "Ongkos Kerugian Akibat Kerusakan (L)": Ongkos_Kerugian_akibat_kerusakan_L,
        "Jumlah Komponen Terpasang (m)": Jumlah_komponen_terpasang_m,
        "Harga Resale Komponen (O)": Harga_resale_komponen_O,
        "Ongkos Model Probabilistik Kerusakan": min(matriks_hasil_payoff_kerusakan_non_linear_df['E(Qi)']),
        "Strategi Penyediaan Optimal (Unit)": matriks_hasil_payoff_kerusakan_non_linear_df['E(Qi)'].idxmin()
    }

    return hasil_model_kerusakan_non_linear

# Contoh penggunaan fungsi
# Ongkos_pemakaian_komponen_H = 18_000_000.00
# Ongkos_Kerugian_akibat_kerusakan_L = 3_720_000_000.00
# Jumlah_komponen_terpasang_m = 5  # Nilai default untuk jumlah komponen terpasang

# Panggil fungsi model_kerusakan_non_linear
# hasil_model_kerusakan_non_linear = model_kerusakan_non_linear(Ongkos_pemakaian_komponen_H, Ongkos_Kerugian_akibat_kerusakan_L, Jumlah_komponen_terpasang_m=5, beta=5)
# print(hasil_model_kerusakan_non_linear)