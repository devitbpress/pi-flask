import pandas as pd
import numpy as np
import math
from scipy.stats import poisson

# Model Wilson
# Karakteristik Model Wilson
    # 1.	Besarnya ukuran lot pemesanan (q0) selalu tetap untuk setiap kali pemesanan dilakukan.
    # 2.	Pemesanan dilakukan apabila jumlah inventori yang dimiliki telah mencapai suatu tingkat tertentu (r) yang disebut titik pemesanan ulang (reorder point).


# Kriteria Kinerja
    # Ongkos Inventori Total per tahun       : OT 

# Variabel Keputusan 
    # Ukuran lot pemesanan ekonomis (EOQ) 	 : qo
    # Saat pemesanan kembali (ROP)	    	 : r

    # Parameter                                         
    # Ongkos pesan tiap kali pemesanan       : A
    # Ongkos simpan per unit pertahun	   	 : h
    # Harga barang per unit	                 : p
    # Permintaan barang per tahun	         : D

# Contoh Numerik dari Laporan Interim
# Kebutuhan barang XYZ PT untuk tahun depan (D) sebanyak 10.000 unit/tahun. 
# Untuk mendapatkan barang tersebut dibeli dari pemasok lokal dengan harga barang (p) sebesar Rp. 8.000,-/unit 
# dan ongkos pesan (A) sebesar Rp. 1.000.000,-/pesan dengan lead time 3 bulan. 
# Jika ongkos simpan barang (h) sebesar Rp. 2.000,-/unit/tahun, 
# bagaimana kebijakan inventori optimalnya agar pengadaan barang XYZ yang paling ekonomis?

# # Inisasi Input parameter
# Permintaan_Barang_ModelWilson_D = 10000 # unit/tahun
# Harga_barang_ModelWilson_p = 8000       # Rp ,-/Unit
# Ongkos_Pesan_ModelWilson_A = 1000000    # Rp ,-/Pesan
# Lead_Time_ModelWilson_L = 3/12          # 3 Bulan -> 1/4 tahun
# Ongkos_Simpan_ModelWilson_h = 2000      # Rp ,-/Unit/Tahun

# # Inisasi Input parameter
# Permintaan_Barang_ModelWilson_D = 10000 # unit/tahun
# Harga_barang_ModelWilson_p = 8000       # Rp ,-/Unit
# Ongkos_Pesan_ModelWilson_A = 1000000    # Rp ,-/Pesan
# Lead_Time_ModelWilson_L = 3/12          # 3 Bulan -> 1/4 tahun
# Ongkos_Simpan_ModelWilson_h = 2000      # Rp ,-/Unit/Tahun

# Perhitungan Model Wilson
# Membuat fungsi Perhitungan Model Wilson
def Model_Wilson(Permintaan_Barang_ModelWilson_D, Harga_barang_ModelWilson_p, Ongkos_Pesan_ModelWilson_A, Lead_Time_ModelWilson_L, Ongkos_Simpan_ModelWilson_h, MaterialCode=None, Material_Description=None, ABC_Indikator=None):
    # 1. Hitung Lot Pengadaaan barang untuk setiap kali pembelian (EOQ) sebesar qo:
    Lot_Pengadaan_barang_ModelWilson_qo = math.sqrt(2*Ongkos_Pesan_ModelWilson_A*Permintaan_Barang_ModelWilson_D/Ongkos_Simpan_ModelWilson_h)

    # 2. Hitung nilai Reorder Point (ROP)
    Reorder_Point_ModelWilson_r = Permintaan_Barang_ModelWilson_D * Lead_Time_ModelWilson_L
    Selang_waktu_pesan_tahun_ModelWilson_T = math.sqrt(2*Ongkos_Pesan_ModelWilson_A/(Permintaan_Barang_ModelWilson_D*Ongkos_Simpan_ModelWilson_h))
    Selang_waktu_pesan_bulan_ModelWilson_T = Selang_waktu_pesan_tahun_ModelWilson_T*12
    Selang_waktu_pesan_hari_ModelWilson_T = Selang_waktu_pesan_tahun_ModelWilson_T*365

    # 3 Hitung besar Ongkos Inventori Optimal total pertahun (OT)
    # Ongkos Inventori (OT) = Ongkos Beli (Ob) + Ongkos Pemesanan (Op) + Ongkos Simpan (Os)
    #
    # Hitung Ongkos Pemesanan (Op)
    frequensi_Pemesanan_ModelWilson_f = Permintaan_Barang_ModelWilson_D/Lot_Pengadaan_barang_ModelWilson_qo
    Ongkos_Pemesanan_ModelWilson_Op = frequensi_Pemesanan_ModelWilson_f*Ongkos_Pesan_ModelWilson_A
    # 
    # Hitung Ongkos Penyimpanan (Os)
    Ongkos_Penyimpanan_ModelWilson_Os = 0.5*Ongkos_Simpan_ModelWilson_h*Lot_Pengadaan_barang_ModelWilson_qo
    # 
    # Hitung Ongkos Inventori Optimal
    Ongkos_Pembelian_ModelWilson_Ob = Permintaan_Barang_ModelWilson_D*Harga_barang_ModelWilson_p
    Ongkos_Inventori_ModelWilson_OT = Ongkos_Pembelian_ModelWilson_Ob + Ongkos_Pemesanan_ModelWilson_Op + Ongkos_Penyimpanan_ModelWilson_Os

    # print(f"----------------------------------------------------------------------------------------------")
    # print(f"Model Determinstik: Model Wilson\n")
    # print(f"material code         : {MaterialCode}") 
    # print(f"material Description  : {Material_Description}")
    # print(f"ABC Indicator         : {ABC_Indikator}")
    # print(f"----------------------------------------------------------------------------------------------\n")

    # if MaterialCode is not None:
    #     print(f"Parameter input:")
    #     print(f" Permintaan Barang  (D) : {Permintaan_Barang_ModelWilson_D:.0f} Unit/Tahun")
    #     print(f" Harga Barang       (p) : Rp {Harga_barang_ModelWilson_p:,.0f} /Unit")
    #     print(f" Ongkos Pesan       (A) : Rp {Ongkos_Pesan_ModelWilson_A:,.0f} /Pesan")
    #     print(f" Lead Time          (L) : {Lead_Time_ModelWilson_L:.03f} Tahun")
    #     print(f" Ongkos_Simpan      (h) : Rp {Ongkos_Simpan_ModelWilson_h:,.0f} /Unit/Tahun")
    # else:
    #     print(f"Perhitungan Contoh Laporan Interim")
    #     print(f"Parameter input:")
    #     print(f" Permintaan Barang  (D) : {Permintaan_Barang_ModelWilson_D:.0f} Unit/Tahun")
    #     print(f" Harga Barang       (p) : Rp {Harga_barang_ModelWilson_p:,.0f} /Unit")
    #     print(f" Ongkos Pesan       (A) : Rp {Ongkos_Pesan_ModelWilson_A:,.0f} /Pesan")
    #     print(f" Lead Time          (L) : {Lead_Time_ModelWilson_L:.03f} Tahun")
    #     print(f" Ongkos_Simpan      (h) : Rp {Ongkos_Simpan_ModelWilson_h:,.0f} /Unit/Tahun\n\n")
    
    # print(f"----------------------------------------------------------------------------------------------")
    # print(f"Hasil Hitung Model Wilson")
    # print(f"----------------------------------------------------------------------------------------------\n")
    # print(f"Lot Pengadaan Optimum Barang Model Wilson   (EOQ) : {Lot_Pengadaan_barang_ModelWilson_qo:.3f} Unit/Pesanan\n")
    # print(f"Saat Pemesanan Kembali                      (ROP) : {Reorder_Point_ModelWilson_r:.0f} Unit\n")
    # print(f"Selang waktu pesan kembali dalam Tahun            : {Selang_waktu_pesan_tahun_ModelWilson_T:.3f} Tahun atau \nSelang waktu pesan kembali dalam Bulan : {Selang_waktu_pesan_bulan_ModelWilson_T:.3f} Bulan \nSelang waktu pesan kembali dalam Hari : {Selang_waktu_pesan_hari_ModelWilson_T:.0f} Hari\n\n")

    # print(f"Frequensi Pemesanan Barang Model Wilson     (f)   : {frequensi_Pemesanan_ModelWilson_f:.0f} Unit")
    # print(f"Ongkos Pembelian                            (Ob)  : Rp {Ongkos_Pembelian_ModelWilson_Ob:,.0f} /Tahun")
    # print(f"Ongkos Pemesanan                            (Op)  : Rp {Ongkos_Pemesanan_ModelWilson_Op:,.0f} /Tahun")
    # print(f"Ongkos Penyimpanan                          (Os)  : Rp {Ongkos_Penyimpanan_ModelWilson_Os:,.0f} /Tahun")
    # print(f"Ongkos Inventori                            (OT)  : Rp {Ongkos_Inventori_ModelWilson_OT:,.0f} /Tahun")
    # print(f"----------------------------------------------------------------------------------------------")

    hasil = {
        "Material Code": MaterialCode,
        "Material Description": Material_Description,
        "ABC Indicator": ABC_Indikator,
        "Permintaan Barang (D) Unit/Tahun": Permintaan_Barang_ModelWilson_D,
        "Harga Barang (p) /Unit": Harga_barang_ModelWilson_p,
        "Ongkos Pesan (A) /Pesan": Ongkos_Pesan_ModelWilson_A,
        "Lead Time (L) Tahun": Lead_Time_ModelWilson_L,
        "Ongkos Simpan (h) /Unit/Tahun": Ongkos_Simpan_ModelWilson_h,
        "Lot Pengadaan (EOQ) Unit/Pesanan": Lot_Pengadaan_barang_ModelWilson_qo,
        "Reorder Point (ROP) Unit": Reorder_Point_ModelWilson_r,
        "Selang Waktu Pesan Kembali (Tahun)": Selang_waktu_pesan_tahun_ModelWilson_T,
        "Selang Waktu Pesan Kembali (Bulan)": Selang_waktu_pesan_bulan_ModelWilson_T,
        "Selang Waktu Pesan Kembali (Hari)": Selang_waktu_pesan_hari_ModelWilson_T,
        "Frequensi Pemesanan (f)": frequensi_Pemesanan_ModelWilson_f,
        "Ongkos Pembelian (Ob) /Tahun": Ongkos_Pembelian_ModelWilson_Ob,
        "Ongkos Pemesanan (Op) /Tahun": Ongkos_Pemesanan_ModelWilson_Op,
        "Ongkos Penyimpanan (Os) /Tahun": Ongkos_Penyimpanan_ModelWilson_Os,
        "Ongkos Inventori (OT) /Tahun": Ongkos_Inventori_ModelWilson_OT
    }

    return hasil
# # Cek Hasil Model Wilson
# Model_Wilson(Permintaan_Barang_ModelWilson_D, Harga_barang_ModelWilson_p, Ongkos_Pesan_ModelWilson_A, Lead_Time_ModelWilson_L, Ongkos_Simpan_ModelWilson_h, MaterialCode=None, Material_Description=None, ABC_Indikator=None)