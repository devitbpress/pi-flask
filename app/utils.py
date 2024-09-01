import json
import pandas as pd

from reza.Model_Wilson_PolaDeterministik import Model_Wilson
from reza.Model_Tchebycheff_PolaTakTentu import Model_Tchebycheff_TakTentu
from reza.Model_Q_PolaDistribusiNormal import Model_Q
from reza.Model_Poisson_PolaPoisson import Model_Poisson
from reza.Model_MinMaxRegret_PolaNonMoving import Model_MinMaxRegret
from reza.Model_KerusakanNonLinear_PolaNonMoving import model_kerusakan_non_linear
from reza.Model_KerusakanLinear_PolaNonMoving import model_kerusakan_linear
from reza.Model_BCR_new import Model_Inventori_BCR

df = pd.read_excel('training/non-moving.xlsx')
data_dict = df.to_dict(orient='records')
data_calc = []

# wilson - pola deterministik
# for obj in data_dict:
#     permintaan_barang = obj.get("permintaan_barang")
#     harga_barang = obj.get("harga_barang")
#     ongkos_pesan = obj.get("ongkos_pesan")
#     lead_time = obj.get("lead_time")
#     ongkos_simpan = obj.get("ongkos_simpan")
#     material_code = obj.get("material_code")
#     material_description = obj.get("material_description")
#     abc_indikator = obj.get("abc_indikator")

#     data_calc.append(Model_Wilson(
#         permintaan_barang,
#         harga_barang, 
#         ongkos_pesan, 
#         lead_time, 
#         ongkos_simpan, 
#         material_code,
#         material_description,
#         abc_indikator))

# tchebycheff - pola tak tentu
# for obj in data_dict:
#     harga_barang = obj.get("harga_barang")
#     kerugian_ketidakadaan_barang = obj.get("kerugian_ketidakadaan_barang")
#     standar_deviasi = obj.get("standar_deviasi")
#     rata_rata_permintaan_barang = obj.get("rata_rata_permintaan_barang")
#     material_code = obj.get("material_code")
#     material_description = obj.get("material_description")
#     abc_indikator = obj.get("abc_indikator")

#     data_calc.append(Model_Tchebycheff_TakTentu(
#         harga_barang, 
#         kerugian_ketidakadaan_barang, 
#         standar_deviasi, 
#         rata_rata_permintaan_barang, 
#         material_code,
#         material_description,
#         abc_indikator))

# q - pola distribusi normal
# for obj in data_dict:
#     rata_rata_permintaan_barang = obj.get('rata_rata_permintaan_barang')
#     lead_time = obj.get('lead_time')
#     standar_deviasi = obj.get('standar_deviasi')
#     ongkos_pesan = obj.get('ongkos_pesan')
#     harga_barang = obj.get('harga_barang')
#     ongkos_simpan = obj.get('ongkos_simpan')
#     ongkos_kekurangan_inventori_setiap_unit_barang = obj.get('ongkos_kekurangan_inventori_setiap_unit_barang')
#     material_code = obj.get('material_code')
#     material_description = obj.get('material_description')
#     abc_indikator = obj.get('abc_indikator')

#     data_calc.append(Model_Q(rata_rata_permintaan_barang , 
#             lead_time, 
#             standar_deviasi, 
#             ongkos_pesan ,
#             harga_barang,
#             ongkos_simpan, 
#             ongkos_kekurangan_inventori_setiap_unit_barang,
#             material_code, 
#             material_description, 
#             abc_indikator))

# poisson - pola poisson
# for obj in data_dict:
#     rata_rata_pemesanan_barang = obj.get("Rata - Rata Permintaan Barang (D) Unit/Tahun")
#     standar_deviasi_barang = obj.get("Standar Deviasi Permintaan Barang (s) Unit/Tahun")
#     lead_time = obj.get("Lead Time (L) Tahun")
#     ongkos_pesan = obj.get("Ongkos Pesan (A) /Pesan")
#     harga_barang = obj.get("Harga Barang (p) /Unit")
#     ongkos_simpan = obj.get("Ongkos Simpan (h) /Unit/Tahun")
#     ongkos_kekurangan_barang = obj.get("Ongkos Kekurangan Inventori (Cu) /Unit/Tahun")
#     material_code = obj.get("Material Code")
#     material_description = obj.get("Material Description")
#     abc_indikator = obj.get("ABC Indicator")

#     data_calc.append(Model_Poisson(rata_rata_pemesanan_barang, 
#                 standar_deviasi_barang, 
#                 lead_time,
#                 ongkos_pesan, 
#                 harga_barang, 
#                 ongkos_simpan, 
#                 ongkos_kekurangan_barang,
#                 material_code,
#                 material_description,
#                 abc_indikator))

# regret, linear, non linear - pola non moving
# for obj in data_dict:
#     ongkos_pemakaian_komponen = obj.get("Unit Price")
#     ongkos_kerugian_akibat_kerusakan = obj.get("Stock Out Effect")
#     jumlah_komponen_terpasang = obj.get("Jumlah Komponen Terpasang")

#     data_calc.append({
#         "regret": Model_MinMaxRegret(
#         ongkos_pemakaian_komponen,
#         ongkos_kerugian_akibat_kerusakan,
#         jumlah_komponen_terpasang,),
#         "linear": model_kerusakan_linear(
#         ongkos_pemakaian_komponen,
#         ongkos_kerugian_akibat_kerusakan,
#         jumlah_komponen_terpasang,),
#         "non_linear": model_kerusakan_non_linear(
#         ongkos_pemakaian_komponen,
#         ongkos_kerugian_akibat_kerusakan,
#         jumlah_komponen_terpasang,)
#     })


# # bcr - pola bcr
# for obj in data_dict:
#     harga_komponen = obj.get("Unit Price")
#     kerugian_komponen = obj.get("Stock Out Effect")
#     suku_bunga = obj.get("Suku Bunga")
#     waktu_sisa_operasi = obj.get("Sisa Tahun Pemakaian")

#     data_calc.append(Model_Inventori_BCR(
#         harga_komponen, 
#         kerugian_komponen, 
#         suku_bunga, 
#         waktu_sisa_operasi))


with open('result/kalkulator.json', 'w') as json_file:
    json.dump(data_calc, json_file, indent=4)