import pandas as pd
import numpy as np

def Model_Inventori_BCR(Harga_Komponen_Ho, Kerugian_Komponen_Co, Suku_bunga_i, Waktu_sisa_operasi=5, probabilitas="uniform"):
    # Jika input bukan list, ubah menjadi list
    if isinstance(Waktu_sisa_operasi, (int, float)):
        Waktu_sisa_operasi = [Waktu_sisa_operasi]

    hasil_perhitungan = []
    df_hasil_list = []
    final_hasil_list = []

    for waktu in Waktu_sisa_operasi:
        # Skip jika waktu adalah 0
        if waktu == 0:
            continue

        # Looping dari tahun 0 hingga waktu dalam Waktu_sisa_operasi
        for t in range(waktu + 1):
            if t == 0:
                Benefit_t = None
                BCR = None
                Probabilitas_Kerusakan_Pt = 0  # Inisialisasi nilai 0 untuk t == 0
                Kerugian_Komponen_PeriodeT_Ct = Kerugian_Komponen_Co * ((1 + Suku_bunga_i) ** t)
                Ongkos_Pemakaian_periodeT_Ht = Harga_Komponen_Ho * ((1 + Suku_bunga_i) ** t)
            else:
                Kerugian_Komponen_PeriodeT_Ct = Kerugian_Komponen_Co * ((1 + Suku_bunga_i) ** t)
                Ongkos_Pemakaian_periodeT_Ht = Harga_Komponen_Ho * ((1 + Suku_bunga_i) ** t)
                
                # Menghitung probabilitas berdasarkan jenis probabilitas yang dipilih
                if probabilitas == "uniform":
                    Probabilitas_Kerusakan_Pt = 1 / waktu
                elif probabilitas == "linear":
                    sigma_t = sum(range(1, waktu + 1))
                    Probabilitas_Kerusakan_Pt = t / sigma_t
                elif probabilitas == "hiperbolik":
                    sigma_sqrt_t = sum(np.sqrt(t) for t in range(1, waktu + 1))
                    Probabilitas_Kerusakan_Pt = np.sqrt(t) / sigma_sqrt_t
                elif probabilitas == "kuadratis":
                    sigma_t_squared = sum(t**2 for t in range(1, waktu + 1))
                    Probabilitas_Kerusakan_Pt = t**2 / sigma_t_squared
                elif probabilitas == "kubik":
                    sigma_t_kubik = sum(t**3 for t in range(1, waktu + 1))
                    Probabilitas_Kerusakan_Pt = t**3 / sigma_t_kubik
                else:
                    raise ValueError("Jenis probabilitas tidak dikenal. Gunakan 'uniform', 'linear', 'hiperbolik', 'kuadratis', atau 'kubik'.")

                Benefit_t = Probabilitas_Kerusakan_Pt * Kerugian_Komponen_PeriodeT_Ct
                BCR = Benefit_t / Ongkos_Pemakaian_periodeT_Ht

            # Simpan hasil ke dalam list untuk dataframe
            df_hasil_list.append({
                "Tahun": t,
                "Probabilitas Kerusakan (Pt)": Probabilitas_Kerusakan_Pt,
                "Kerugian Komponen Periode T (Ct)": Kerugian_Komponen_PeriodeT_Ct,
                "Ongkos Pemakaian Periode T (Ht)": Ongkos_Pemakaian_periodeT_Ht,
                "Benefit T": Benefit_t,
                "BCR": BCR
            })

        # Setelah loop selesai, cari nilai BCR > 1
        pembelian_ditemukan = False
        for row in df_hasil_list:
            if row["BCR"] and row["BCR"] > 1:
                tahun_optimal = row["Tahun"] - 1  # Dikurangi 1 sesuai permintaan Anda
                print(f"\nDari hasil hitung dengan model BCR ini diperoleh pembelian sparepart pada tahun ke-{tahun_optimal} karena nilai BCR == {row['BCR']:.2f}\n")
                
                # Simpan hasil ke dalam list untuk dataframe final
                final_hasil_list.append({
                    "Tahun": tahun_optimal,  # Menambahkan kolom Tahun
                    "Waktu Sisa Operasi (tahun)": waktu,
                    "Harga Komponen (Ho)": Harga_Komponen_Ho,
                    "Kerugian Komponen (Co)": Kerugian_Komponen_Co,
                    "Suku Bunga (i)": Suku_bunga_i,
                    "Probabilitas Kerusakan (Pt)": row["Probabilitas Kerusakan (Pt)"],
                    "Kerugian Komponen Periode T (Ct)": row["Kerugian Komponen Periode T (Ct)"],
                    "Ongkos Pemakaian Periode T (Ht)": row["Ongkos Pemakaian Periode T (Ht)"],
                    "Benefit-Cost Ratio (BCR)": row["BCR"],
                    "Probabilitas": probabilitas  # Menambahkan informasi jenis probabilitas
                })
                
                pembelian_ditemukan = True
                break

        # Jika tidak ada nilai BCR > 1, tampilkan pesan
        if not pembelian_ditemukan:
            print("\nTidak ada pembelian sparepart yang direkomendasikan karena tidak ada nilai BCR > 1.\n")

    # Simpan hasil dalam dictionary serupa dengan model non-linear yang Anda inginkan
    if pembelian_ditemukan:
        hasil_model_bcr = {
            "Waktu Sisa Operasi (tahun)": waktu,
            "Harga Komponen (Ho)": Harga_Komponen_Ho,
            "Kerugian Komponen (Co)": Kerugian_Komponen_Co,
            "Suku Bunga (i)": Suku_bunga_i,
            "Benefit-Cost Ratio (BCR)": row["BCR"],
            "Strategi Penyediaan Optimal (Tahun)": tahun_optimal,
            "Jenis Probabilitas": probabilitas
        }
    else:
        hasil_model_bcr = {
            "Waktu Sisa Operasi (tahun)": waktu,
            "Harga Komponen (Ho)": Harga_Komponen_Ho,
            "Kerugian Komponen (Co)": Kerugian_Komponen_Co,
            "Suku Bunga (i)": Suku_bunga_i,
            "Pesan": "Tidak ada pembelian sparepart yang direkomendasikan"
        }

    return hasil_model_bcr

# # Contoh penggunaan fungsi
# Harga_Komponen_Ho = 2_501_501_612
# Kerugian_Komponen_Co = 3_720_000_000
# Suku_bunga_i = 0.1  # 10%

# # Panggil fungsi Model_Inventori_BCR dengan probabilitas kuadratis
# hasil_model_bcr = Model_Inventori_BCR(Harga_Komponen_Ho, Kerugian_Komponen_Co, Suku_bunga_i, probabilitas="uniform", Waktu_sisa_operasi=20)
# print(hasil_model_bcr)
