import pandas as pd
import numpy as np
import math
from scipy.stats import norm

def Model_Q(
        Rata_Rata_Permintaan_Barang_ModelQ_D , 
        Lead_Time_ModelQ_L, 
        Standar_Deviasi_Permintaan_Barang_ModelQ_S, 
        Ongkos_Pesan_ModelQ_A ,
        Harga_barang_ModelQ_p,
        Ongkos_Simpan_ModelQ_h, 
        Ongkos_kekurangan_inventori_setiap_unit_barang_ModelQ_Cu,
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

    # Hitung Nilai Standar Deviasi Permintaan Barang waktu LeadTime
    Standar_Deviasi_Permintaan_Barang_Waktu_LeadTime_ModelQ_SL = Standar_Deviasi_Permintaan_Barang_ModelQ_S * math.sqrt(Lead_Time_ModelQ_L) #Unit/Tahun

    # 1. Hitung Lot Pengadaaan barang sebesar qo1* inisiasi dengan Metode Hadley-Within:
    Lot_Pengadaan_barang_ModelQ_qo1 = math.sqrt(2*Ongkos_Pesan_ModelQ_A*Rata_Rata_Permintaan_Barang_ModelQ_D/Ongkos_Simpan_ModelQ_h)

    # Hitung nilai Alpha Inisiasi
    alpha_ModelQ_inisiasi = Ongkos_Simpan_ModelQ_h*Lot_Pengadaan_barang_ModelQ_qo1/(Ongkos_kekurangan_inventori_setiap_unit_barang_ModelQ_Cu*Rata_Rata_Permintaan_Barang_ModelQ_D)
    za_one_tailed_ModelQ_Inisiasi = norm.ppf(1 - alpha_ModelQ_inisiasi)

    # DL = D * L
    Rata_Rata_Permintaan_Barang_ModelQ_WaktuLeadTime_DL = Rata_Rata_Permintaan_Barang_ModelQ_D*Lead_Time_ModelQ_L
    
    # Hitung Nilai Reorder Point (r1*)
    # Za = (r1* - DL)/SL
    # r1* = (Za*SL) + DL
    Reorder_Point_ModelQ_r1 = (za_one_tailed_ModelQ_Inisiasi*Standar_Deviasi_Permintaan_Barang_Waktu_LeadTime_ModelQ_SL) + Rata_Rata_Permintaan_Barang_ModelQ_WaktuLeadTime_DL

    # Hitung distribusi Normal Standar ϕ(z)
    Fungsi_Distribusi_Normal_ModelQ_F_Za = norm.pdf(za_one_tailed_ModelQ_Inisiasi)
        
    #Hitung Standar Normal Loss L(z)=ϕ(z)−z(1−Φ(z))

    #Hitung kumulatif Normal Distribusi φ(z)
    Fungsi_Kumulatif_Distribusi_Normal_ModelQ_phi_Za = norm.cdf(za_one_tailed_ModelQ_Inisiasi)
    

    # Hitung Standar Normal Loss L(z)
    Fungsi_Standar_Loss_Distribusi_Normal_ModelQ_phi_Za = Fungsi_Distribusi_Normal_ModelQ_F_Za - za_one_tailed_ModelQ_Inisiasi * (1- Fungsi_Kumulatif_Distribusi_Normal_ModelQ_phi_Za)
    Jumlah_Kekurangan_Barang_N = Standar_Deviasi_Permintaan_Barang_Waktu_LeadTime_ModelQ_SL * (Fungsi_Distribusi_Normal_ModelQ_F_Za - (za_one_tailed_ModelQ_Inisiasi * Fungsi_Standar_Loss_Distribusi_Normal_ModelQ_phi_Za))
    
    # Hitung Nilai Lot Pengadaan barang (qo2*)
    iterasi_ModelQ_i = 0
    Jumlah_Kekurangan_Barang_NT = Jumlah_Kekurangan_Barang_N
    Fungsi_Distribusi_Normal_ModelQ_F_Za2 = Fungsi_Distribusi_Normal_ModelQ_F_Za
    Fungsi_Standar_Loss_Distribusi_Normal_ModelQ_phi_Za2 = Fungsi_Standar_Loss_Distribusi_Normal_ModelQ_phi_Za
    Reorder_Point_ModelQ_r2 = Reorder_Point_ModelQ_r1

    while True:
        # Hitung EOQ (Economic Order Quantity)
        Lot_Pengadaan_barang_ModelQ_qo2 = math.sqrt(2 * Rata_Rata_Permintaan_Barang_ModelQ_D *(Ongkos_Pesan_ModelQ_A + (Ongkos_kekurangan_inventori_setiap_unit_barang_ModelQ_Cu * Jumlah_Kekurangan_Barang_NT)) / Ongkos_Simpan_ModelQ_h)
        # Hitung alpha untuk menentukan za
        alpha_ModelQ_alpha2 = (Ongkos_Simpan_ModelQ_h * Lot_Pengadaan_barang_ModelQ_qo2) / (Ongkos_kekurangan_inventori_setiap_unit_barang_ModelQ_Cu * Rata_Rata_Permintaan_Barang_ModelQ_D)
        # Hitung nilai Za
        za_one_tailed_ModelQ_Za2 = norm.ppf(1 - alpha_ModelQ_alpha2)

        # Hitung Reorder Point (ROP)
        Reorder_Point_ModelQ_r2 = Rata_Rata_Permintaan_Barang_ModelQ_WaktuLeadTime_DL + (za_one_tailed_ModelQ_Za2 * Standar_Deviasi_Permintaan_Barang_Waktu_LeadTime_ModelQ_SL)

        # Hitung distribusi Normal Standar ϕ(z)
        Fungsi_Distribusi_Normal_ModelQ_F_Za2 = norm.pdf(za_one_tailed_ModelQ_Za2)
        
        #Hitung kumulatif Normal Distribusi φ(z)
        Fungsi_Kumulatif_Distribusi_Normal_ModelQ_phi_Za2 = norm.cdf(za_one_tailed_ModelQ_Za2)
        # 
        # Hitung Standar Normal Loss φ(z_alpha)
        Fungsi_Standar_Loss_Distribusi_Normal_ModelQ_phi_Za2 = Fungsi_Distribusi_Normal_ModelQ_F_Za2 - za_one_tailed_ModelQ_Za2 * (1- Fungsi_Kumulatif_Distribusi_Normal_ModelQ_phi_Za2)
        Jumlah_Kekurangan_Barang_NT = Standar_Deviasi_Permintaan_Barang_Waktu_LeadTime_ModelQ_SL * (Fungsi_Distribusi_Normal_ModelQ_F_Za2 - (za_one_tailed_ModelQ_Za2 * Fungsi_Standar_Loss_Distribusi_Normal_ModelQ_phi_Za2))

        # Cek konvergensi
        if (Reorder_Point_ModelQ_r2 - Reorder_Point_ModelQ_r1) < 1:
            Reorder_Point_ModelQ_r1 = Reorder_Point_ModelQ_r2
            # print(f"Selisih Nilai reorder point r1* (Reorder Point Inisiasi) dengan Nilai reorder point r2 pada Iterasi ke-{iterasi_ModelQ_i} adalah {Reorder_Point_ModelQ_r2 - Reorder_Point_ModelQ_r1:.0f} Unit")
            break

        # Update nilai r1 dan iterasi
        iterasi_ModelQ_i += 1

    # Hitung Nilai Safety Stock (SS)
    Safety_Stocks_ModelQ_SS = za_one_tailed_ModelQ_Za2 * Standar_Deviasi_Permintaan_Barang_Waktu_LeadTime_ModelQ_SL

    # Hitung Nilai Pelayanan
    Nilai_Pelayanan_ModelQ_ServiceLevel = (1 - Jumlah_Kekurangan_Barang_N/(Rata_Rata_Permintaan_Barang_ModelQ_WaktuLeadTime_DL))*100

    # Hitung Nilai Ekspetasi Ongkos Inventori Total per Tahun

    # Hitung Ongkos Pembelian (Ob)
    Ongkos_Pembelian_ModelQ_Ob = Rata_Rata_Permintaan_Barang_ModelQ_D*Harga_barang_ModelQ_p
    
    # Hitung Ongkos Pengadaan (Op)
    frequensi_Pemesanan_ModelQ_f = Rata_Rata_Permintaan_Barang_ModelQ_D/Lot_Pengadaan_barang_ModelQ_qo2
    Ongkos_Pengadaan_ModelQ_Op = frequensi_Pemesanan_ModelQ_f*Ongkos_Pesan_ModelQ_A

    # Hitung Ongkos Simpan (Os)
    Ongkos_Penyimpanan_ModelQ_Os = Ongkos_Simpan_ModelQ_h*(0.5*Lot_Pengadaan_barang_ModelQ_qo2 + Reorder_Point_ModelQ_r2 - Rata_Rata_Permintaan_Barang_ModelQ_WaktuLeadTime_DL)

    # Hitung Ongkos Kekurangan Inventori (Ok)
    Ongkos_Kekurangan_Inventori_ModelQ_Ok = Ongkos_kekurangan_inventori_setiap_unit_barang_ModelQ_Cu*Jumlah_Kekurangan_Barang_NT

    Ongkos_Inventori_ModelQ_OT = Ongkos_Pembelian_ModelQ_Ob + Ongkos_Pengadaan_ModelQ_Op + Ongkos_Penyimpanan_ModelQ_Os + Ongkos_Kekurangan_Inventori_ModelQ_Ok

    hasil_Model_Q = {
        "Material Code": MaterialCode,
        "Material Description": Material_Description,
        "ABC Indicator": ABC_Indikator,
        "Rata - Rata Permintaan Barang (D) Unit/Tahun": Rata_Rata_Permintaan_Barang_ModelQ_D,
        "Standar Deviasi Permintaan Barang (s) Unit/Tahun": Standar_Deviasi_Permintaan_Barang_ModelQ_S,
        "Lead Time (L) Tahun": Lead_Time_ModelQ_L,
        "Ongkos Pesan (A) /Pesan": Ongkos_Pesan_ModelQ_A,
        "Harga Barang (p) /Unit": Harga_barang_ModelQ_p,
        "Ongkos Simpan (h) /Unit/Tahun": Ongkos_Simpan_ModelQ_h,
        "Ongkos Kekurangan Inventori (Cu) /Unit/Tahun": Ongkos_kekurangan_inventori_setiap_unit_barang_ModelQ_Cu,
        "Standar Deviasi Permintaan Barang Waktu Lead Time (SL) Unit/Tahun": Standar_Deviasi_Permintaan_Barang_Waktu_LeadTime_ModelQ_SL,
        "Rata - Rata Permintaan Barang Waktu Lead Time (DL) Unit/Tahun": Rata_Rata_Permintaan_Barang_ModelQ_WaktuLeadTime_DL,
        "Lot Pengadaan Optimum Barang (EOQ) Unit/Pesanan": Lot_Pengadaan_barang_ModelQ_qo2,
        "Reorder Point (ROP) Unit": Reorder_Point_ModelQ_r2,
        "Safety Stock (SS) Unit": Safety_Stocks_ModelQ_SS,
        "Frequensi Pemesanan (f)": frequensi_Pemesanan_ModelQ_f,
        "Ongkos Pembelian (Ob) /Tahun": Ongkos_Pembelian_ModelQ_Ob,
        "Ongkos Pemesanan (Op) /Tahun": Ongkos_Pengadaan_ModelQ_Op,
        "Ongkos Penyimpanan (Os) /Tahun": Ongkos_Penyimpanan_ModelQ_Os,
        "Ongkos Kekurangan Inventori (Ok) /Tahun": Ongkos_Kekurangan_Inventori_ModelQ_Ok,
        "Ongkos Inventori (OT) /Tahun": Ongkos_Inventori_ModelQ_OT
    }

    return hasil_Model_Q