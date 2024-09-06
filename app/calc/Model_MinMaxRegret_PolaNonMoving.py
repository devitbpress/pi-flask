import numpy as np
import pandas as pd

# Model Min Max Regret
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

def Model_MinMaxRegret(
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

    # 3. Fungsi untuk menghitung matriks pay-off
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

    # 4. Fungsi untuk menghitung matriks penyesalan
    def matrix_penyesalan(matriks_payoff):
        matriks_penyesalan = np.zeros_like(matriks_payoff)
        for qi in range(matriks_payoff.shape[0]):
            for Dj in range(matriks_payoff.shape[1]):
                if qi == Dj:
                    matriks_penyesalan[qi,Dj] = 0
                elif qi > Dj:
                    matriks_penyesalan[qi,Dj] = ((qi - Dj)*Ongkos_pemakaian_komponen_H) - ((qi - Dj)*Harga_resale_komponen_O)
                elif qi < Dj:
                    matriks_penyesalan[qi,Dj] = (Dj-qi)*Ongkos_pemakaian_komponen_H
        return matriks_penyesalan

    # 5. Menghitung matriks pay-off dan matriks penyesalan
    matriks_hasil_payoff = matrix_payoff(
        Jumlah_komponen_terpasang_m, Ongkos_pemakaian_komponen_H, Ongkos_Kerugian_akibat_kerusakan_L, Harga_resale_komponen_O
    )
    matriks_hasil_penyesalan = matrix_penyesalan(matriks_hasil_payoff)

    # 6. Mengonversi matriks penyesalan menjadi DataFrame
    matriks_hasil_penyesalan_df = pd.DataFrame(
        matriks_hasil_penyesalan, columns=[f'Kerusakan {i}' for i in range(Jumlah_komponen_terpasang_m + 1)]
    )
    matriks_hasil_penyesalan_df['Pay-off Penyesalan'] = matriks_hasil_penyesalan_df.max(axis=1)

    # Menghitung hasil Model Min-Max Regret
    min_regret = min(matriks_hasil_penyesalan_df['Pay-off Penyesalan'])
    strategi_optimal = matriks_hasil_penyesalan_df['Pay-off Penyesalan'].idxmin()

    # # Cetak hasil
    # print(f"----------------------------------------------------------------------------------------------")
    # print(min_regret)
    # print(f"----------------------------------------------------------------------------------------------")
    # print(f"Parameter Input Model Probabilistik Min Max Regret")
    # print(f"Ongkos Pemakaian Sparepart: Rp {Ongkos_pemakaian_komponen_H:,.0f}.-")
    # print(f"Kerugian Ketidakseterdiaan Sparepart: Rp {Ongkos_Kerugian_akibat_kerusakan_L:,.0f}.-")
    # print(f"Harga Resale Sparepart: Rp {Harga_resale_komponen_O:,.0f}.-")
    # print(f"Jumlah komponen terpasang: {Jumlah_komponen_terpasang_m:.0f}")
    # print(f"----------------------------------------------------------------------------------------------")
    # print(f" ")
    # print(f"----------------------------------------------------------------------------------------------")
    # print(f"Model Minimum Regret: Rp {min_regret:,.0f}.-")
    # print(f"Strategi Penyediaan optimal model Min-Max Regret adalah {strategi_optimal:.0f} Unit")
    # print(f"----------------------------------------------------------------------------------------------")

    # Simpan hasil dalam dictionary
    hasil_Model_MinMaxRegret = {
        "Material Code": MaterialCode,
        "Material Description": Material_Description,
        "ABC Indicator": ABC_Indikator,
        "Ongkos Pemakaian Komponen (H)": Ongkos_pemakaian_komponen_H,
        "Ongkos Kerugian Akibat Kerusakan (L)": Ongkos_Kerugian_akibat_kerusakan_L,
        "Jumlah Komponen Terpasang (m)": Jumlah_komponen_terpasang_m,
        "Harga Resale Komponen (O)": Harga_resale_komponen_O,
        "Minimum Regret (Rp )": min_regret,
        "Strategi Penyediaan Optimal (Unit)": strategi_optimal
    }
    return hasil_Model_MinMaxRegret

# Contoh penggunaan fungsi
# Ongkos_pemakaian_komponen_H = 18_000_000.00
# Ongkos_Kerugian_akibat_kerusakan_L = 3_720_000_000.00
# Jumlah_komponen_terpasang_m = 5  # Nilai default untuk jumlah komponen terpasang

# hasil_Model_MinMaxRegret = Model_MinMaxRegret(Ongkos_pemakaian_komponen_H, Ongkos_Kerugian_akibat_kerusakan_L, Jumlah_komponen_terpasang_m)
# print(hasil_Model_MinMaxRegret)