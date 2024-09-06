# harga_komponen = True
# kerugian_komponen = True
# suku_bunga = True
# waktu_sisa_operasi = 5
# material_code = None
# material_description = None
# abc_indikator = None
# probabilitas = "uniform"
# ongkos_pemakaian_komponen = True
# ongkos_kerugian_akibat_kerusakan

# model_inventory_bcr = ()

# model_inventory_bcr(
#         harga_komponen,
#         kerugian_komponen, 
#         suku_bunga, 
#         waktu_sisa_operasi=5, 
#         material_code=None, 
#         material_description=None, 
#         abc_indikator=None,
#         probabilitas="uniform"
#     )
    
# model_kerusakan_linear(
#         Ongkos_pemakaian_komponen_H,
#         Ongkos_Kerugian_akibat_kerusakan_L, 
#         Jumlah_komponen_terpasang_m=5, 
#         MaterialCode=None, 
#         Material_Description=None, 
#         ABC_Indikator=None,
#         Harga_resale_komponen_O=None,
#     )
    
# model_kerusakan_non_linear(
#         Ongkos_pemakaian_komponen_H, 
#         Ongkos_Kerugian_akibat_kerusakan_L, 
#         Jumlah_komponen_terpasang_m=5, 
#         MaterialCode=None, 
#         Material_Description=None, 
#         ABC_Indikator=None,
#         Harga_resale_komponen_O=None, 
#         beta=4
#     )
    
# Model_MinMaxRegret(
#         Ongkos_pemakaian_komponen_H, 
#         Ongkos_Kerugian_akibat_kerusakan_L, 
#         Jumlah_komponen_terpasang_m=5, 
#         MaterialCode=None, 
#         Material_Description=None, 
#         ABC_Indikator=None,
#         Harga_resale_komponen_O=None,
#     )
    
# Model_Poisson(
#         Rata_Rata_Pemesanan_Barang_ModelPoisson_D, 
#         Standar_Deviasi_Barang_ModelPoisson_S, 
#         Lead_Time_ModelPoisson_L, 
#         Ongkos_Pesan_ModelPoisson_A, 
#         Harga_Barang_ModelPoisson_p, 
#         Ongkos_Simpan_ModelPoisson_h, 
#         Ongkos_Kekurangan_Barang_ModelPoisson_Cu,
#         MaterialCode=None, 
#         Material_Description=None, 
#         ABC_Indikator=None
#     )
    
# Model_Q(
#         Rata_Rata_Permintaan_Barang_ModelQ_D , 
#         Lead_Time_ModelQ_L, 
#         Standar_Deviasi_Permintaan_Barang_ModelQ_S, 
#         Ongkos_Pesan_ModelQ_A ,
#         Harga_barang_ModelQ_p,
#         Ongkos_Simpan_ModelQ_h, 
#         Ongkos_kekurangan_inventori_setiap_unit_barang_ModelQ_Cu,
#         MaterialCode=None, 
#         Material_Description=None, 
#         ABC_Indikator=None
#     )
    
# Model_Tchebycheff_TakTentu(
#         Harga_Barang_model_Tchebycheff_p, 
#         Kerugian_Ketidakadaan_barang_model_Tchebycheff_Cu, 
#         Standar_Deviasi_model_Tchebycheff_s, 
#         Rata_Rata_Permintaan_barang_model_Tchebycheff_alpha, 
#         MaterialCode=None, 
#         Material_Description=None, 
#         ABC_Indikator=None
#     )
        
# Model_Wilson(
#         Permintaan_Barang_ModelWilson_D, 
#         Harga_barang_ModelWilson_p, 
#         Ongkos_Pesan_ModelWilson_A, 
#         Lead_Time_ModelWilson_L, 
#         Ongkos_Simpan_ModelWilson_h, 
#         MaterialCode=None, 
#         Material_Description=None, 
#         ABC_Indikator=None
#     )