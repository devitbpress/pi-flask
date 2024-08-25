# perhitungan model Tchebycheff

# Pendekatan Tchebycheff digunakan untuk persoalan yang diketahui ekspektasi dan variansi permintaannya saja tanpa diketahui probabilitas terjadinya dan bentuk distribusinya. 
# Menurut Tchebycheff untuk random variabel y yang mempunyai rata-rata α dan standar deviasi s akan dihitung ukuran lot pemesanan yang optimal pada (q0) yakni sebesar
# q0 =  α + k.s
# dengan k adalah
# power(2Cu/(p*s),(1/3))
#  dengan nilai 
# Cu      -> kerugian sparepart pada saat terjadinya kerusakan unit/hari
# p       -> harga pemakaian komponen suku cadang

# berdasarkan model klasifikasi yang telah dilakukan sebelum, dipilih sample
# material code         : 6205705
# material description  : SENSOR,LIQ LVL:VEGAPULS21;RA-222-2RQ
# ABC Indicator         : C
# unit price (p)        : Rp 20.100.000 unit/hari
# kerugian  (cu)        : 
# standar deviasi (s)   : 0.516398	unit/bulan
# rata -rata   (α)      : 0.333333  unit/bulan


# Harga_Barang_model_Tchebycheff_p = 20100000
# Kerugian_Ketidakadaan_barang_model_Tchebycheff_Cu = Harga_Barang_model_Tchebycheff_p *100 #saya asumsikan dulu untuk mengetes perhitungan
# Standar_Deviasi_model_Tchebycheff_s = 0.516398
# Rata_Rata_Permintaan_barang_model_Tchebycheff_alpha = 0.333333

def Model_Tchebycheff_TakTentu(Harga_Barang_model_Tchebycheff_p, 
                               Kerugian_Ketidakadaan_barang_model_Tchebycheff_Cu, 
                               Standar_Deviasi_model_Tchebycheff_s, 
                               Rata_Rata_Permintaan_barang_model_Tchebycheff_alpha, 
                               MaterialCode=None, Material_Description=None, ABC_Indikator=None):
    
    # Perhitungan parameter model Tchebycheff
    model_Tchebycheff_k = pow(2 * Kerugian_Ketidakadaan_barang_model_Tchebycheff_Cu / 
                              (Harga_Barang_model_Tchebycheff_p * Standar_Deviasi_model_Tchebycheff_s), 1/3)
    
    model_Tchebycheff_q0 = round(Rata_Rata_Permintaan_barang_model_Tchebycheff_alpha + 
                                 model_Tchebycheff_k * Standar_Deviasi_model_Tchebycheff_s, 0)
    
    # # Print hasil
    # print(f"----------------------------------------------------------------------------------------------")
    # print(f"Model Pola Tak - Tentu: Model Tchebycheff\n")
    # print(f"material code         : {MaterialCode}") 
    # print(f"material Description  : {Material_Description}")
    # print(f"ABC Indicator         : {ABC_Indikator}")
    # print(f"----------------------------------------------------------------------------------------------\n")
    
    # print(f"Dengan MODEL TCHEBYCHEFF ukuran Lot Pemesanan optimal adalah {int(model_Tchebycheff_q0)}")
    # print(f"----------------------------------------------------------------------------------------------")

    # Simpan hasil dalam dictionary
    hasil_model_Tchebycheff_TakTentu = {
        "Material Code": MaterialCode,
        "Material Description": Material_Description,
        "ABC Indicator": ABC_Indikator,
        "Harga Barang (p) /Unit": Harga_Barang_model_Tchebycheff_p,
        "Kerugian Ketidakadaan Barang (Cu) /Unit": Kerugian_Ketidakadaan_barang_model_Tchebycheff_Cu,
        "Standar Deviasi Permintaan Barang (s)": Standar_Deviasi_model_Tchebycheff_s,
        "Rata - Rata Permintaan Barang (alpha)": Rata_Rata_Permintaan_barang_model_Tchebycheff_alpha,
        "Nilai K Model Tchebycheff": model_Tchebycheff_k,
        "Lot Pemesanan Optimal (q0)": model_Tchebycheff_q0
    }
    return hasil_model_Tchebycheff_TakTentu

