import pandas as pd
import numpy as np
import math
from scipy.stats import poisson

def Model_Poisson(
        Rata_Rata_Pemesanan_Barang_ModelPoisson_D, 
        Standar_Deviasi_Barang_ModelPoisson_S, 
        Lead_Time_ModelPoisson_L, 
        Ongkos_Pesan_ModelPoisson_A, 
        Harga_Barang_ModelPoisson_p, 
        Ongkos_Simpan_ModelPoisson_h, 
        Ongkos_Kekurangan_Barang_ModelPoisson_Cu,
        MaterialCode=None, 
        Material_Description=None, 
        ABC_Indikator=None
    ):

    if MaterialCode is np.nan:
        if pd.isna(MaterialCode):
            MaterialCode = ""

    if Material_Description is np.nan:
        if pd.isna(Material_Description):
            Material_Description = ""

    if ABC_Indikator is np.nan:
        if pd.isna(ABC_Indikator):
            ABC_Indikator = ""

    Standar_Deviasi_Waktu_Ancang_Ancang_SL = Standar_Deviasi_Barang_ModelPoisson_S * math.sqrt(Lead_Time_ModelPoisson_L)
    qo_1_Awal_Poisson = math.sqrt((2 * Ongkos_Pesan_ModelPoisson_A * Rata_Rata_Pemesanan_Barang_ModelPoisson_D) / Ongkos_Simpan_ModelPoisson_h)

    # Hitung nilai alpha
    alpha_Awal_poisson = (Ongkos_Simpan_ModelPoisson_h * qo_1_Awal_Poisson) / (Ongkos_Kekurangan_Barang_ModelPoisson_Cu * Rata_Rata_Pemesanan_Barang_ModelPoisson_D)

    # Hitung rata-rata jumlah permintaan selama waktu ancang-ancang
    x_Poisson  = Rata_Rata_Pemesanan_Barang_ModelPoisson_D * Lead_Time_ModelPoisson_L
    
    # Mulai dengan nilai reorder point awal
    reorder_point_awal_Poisson = 0
    
    # Hitung nilai probabilitas P(X)
    while True:
        probabilitas_kumulatif_poisson_reorder_point = poisson.cdf(reorder_point_awal_Poisson, x_Poisson)
        
        # Tetap lakukan looping hingga 1-probabilitas_kumulatifnya <= alpha_poisson
        if 1 - probabilitas_kumulatif_poisson_reorder_point <= alpha_Awal_poisson:
            # print(f"Nilai reorder point r1* Awal Iterasi adalah {reorder_point_awal_Poisson:.0f} Unit")
            break
        reorder_point_awal_Poisson += 1
    
    # Hitung nilai Safety Stock (SS) Iterasi 1
    SS_Awal_Poisson = reorder_point_awal_Poisson - (Rata_Rata_Pemesanan_Barang_ModelPoisson_D * Lead_Time_ModelPoisson_L)
    
    # Hitung nilai awal dari Ongkos Inventori (OT)
    Ongkos_Inventori_Awal_Poisson = (
        (Rata_Rata_Pemesanan_Barang_ModelPoisson_D * Harga_Barang_ModelPoisson_p) +
        ((Ongkos_Pesan_ModelPoisson_A * Rata_Rata_Pemesanan_Barang_ModelPoisson_D) / qo_1_Awal_Poisson) +
        Ongkos_Simpan_ModelPoisson_h * (0.5 * qo_1_Awal_Poisson + SS_Awal_Poisson) +
        (Ongkos_Kekurangan_Barang_ModelPoisson_Cu * alpha_Awal_poisson * Rata_Rata_Pemesanan_Barang_ModelPoisson_D)
    )

    # Looping Perhitungan Ongkos Inventori
    alpha_poisson = alpha_Awal_poisson
    qo_1_Poisson = qo_1_Awal_Poisson
    reorder_point_Poisson = reorder_point_awal_Poisson
    iterasi = 0
    
    while True:
        iterasi += 1

        # Hitung nilai lot optimal
        qo_1_Poisson = math.sqrt(
            2 * Rata_Rata_Pemesanan_Barang_ModelPoisson_D *
            (Ongkos_Pesan_ModelPoisson_A + (Ongkos_Kekurangan_Barang_ModelPoisson_Cu * alpha_poisson * qo_1_Poisson)) /
            Ongkos_Simpan_ModelPoisson_h
        )
        
        # Hitung nilai alpha
        alpha_poisson = (Ongkos_Simpan_ModelPoisson_h * qo_1_Poisson) / (Ongkos_Kekurangan_Barang_ModelPoisson_Cu * Rata_Rata_Pemesanan_Barang_ModelPoisson_D)
        
        while True:
            # Hitung probabilitas kumulatif iterasi
            probabilitas_kumulatif_poisson_reorder_point = poisson.cdf(reorder_point_Poisson, x_Poisson)
            
            # Tetap lakukan looping hingga 1-probabilitas_kumulatifnya <= alpha_poisson
            if 1 - probabilitas_kumulatif_poisson_reorder_point <= alpha_poisson:
                break
            
            # Iterasi
            reorder_point_Poisson += 1

        # Cek kondisi untuk menghentikan loop utama
        if abs(reorder_point_Poisson - reorder_point_awal_Poisson) <= 10:
            # print(f"Nilai reorder point r1* pada Iterasi ke-{iterasi:.0f} adalah {reorder_point_Poisson:.0f} Unit")
            break

    # Hitung nilai Safety Stock (SS)
    SS_Poisson = reorder_point_Poisson - (Rata_Rata_Pemesanan_Barang_ModelPoisson_D * Lead_Time_ModelPoisson_L)
    
    # Hitung nilai dari Ongkos Inventori (OT)
    Ongkos_Inventori_Poisson = (
        (Rata_Rata_Pemesanan_Barang_ModelPoisson_D * Harga_Barang_ModelPoisson_p) +
        ((Ongkos_Pesan_ModelPoisson_A * Rata_Rata_Pemesanan_Barang_ModelPoisson_D) / qo_1_Poisson) +
        Ongkos_Simpan_ModelPoisson_h * (0.5 * qo_1_Poisson + SS_Poisson) +
        (Ongkos_Kekurangan_Barang_ModelPoisson_Cu * alpha_poisson * Rata_Rata_Pemesanan_Barang_ModelPoisson_D)
    )
    
    Service_Level_Poisson = (1 - alpha_poisson) * 100

    # Simpan hasil dalam dictionary
    hasil_Model_Poisson = {
        "Material Code": MaterialCode,
        "Material Description": Material_Description,
        "ABC Indicator": ABC_Indikator,
        "Rata - Rata Permintaan Barang (D) Unit/Tahun": Rata_Rata_Pemesanan_Barang_ModelPoisson_D,
        "Standar Deviasi Permintaan Barang (s) Unit/Tahun": Standar_Deviasi_Barang_ModelPoisson_S,
        "Lead Time (L) Tahun": Lead_Time_ModelPoisson_L,
        "Ongkos Pesan (A) /Pesan": Ongkos_Pesan_ModelPoisson_A,
        "Harga Barang (p) /Unit": Harga_Barang_ModelPoisson_p,
        "Ongkos Simpan (h) /Unit/Tahun": Ongkos_Simpan_ModelPoisson_h,
        "Ongkos Kekurangan Inventori (Cu) /Unit/Tahun": Ongkos_Kekurangan_Barang_ModelPoisson_Cu,
        "Nilai Alpha": alpha_poisson,
        "Standar Deviasi Waktu Ancang - Ancang (SL) Unit/Tahun": Standar_Deviasi_Waktu_Ancang_Ancang_SL,
        "Economic Order Quantity (EOQ) Lot Optimum (qo1)": qo_1_Poisson,
        "Reorder Point (ROP) Unit": reorder_point_Poisson,
        "Safety Stock (SS) Unit": SS_Poisson,
        "Service Level (%)": Service_Level_Poisson,
        "Ongkos Inventori (OT) /Tahun": Ongkos_Inventori_Poisson
    }

    return hasil_Model_Poisson