from app.calc import Model_Wilson_PolaDeterministik
from app.calc import Model_Tchebycheff_PolaTakTentu
from app.calc import Model_Q_PolaDistribusiNormal
from app.calc import Model_Poisson_PolaPoisson
from app.calc import Model_MinMaxRegret_PolaNonMoving
from app.calc import Model_KerusakanNonLinear_PolaNonMoving
from app.calc import Model_KerusakanLinear_PolaNonMoving
from app.calc import Model_BCR_new

def calc_model(data, model):
    data_calc = []
    
    if model == "wilson":
        required_keys = ["Permintaan Barang (D) Unit/Tahun","Harga Barang (p) /Unit","Ongkos Pesan (A) /Pesan","Lead Time (L) Tahun","Ongkos Simpan (h) /Unit/Tahun","Material Code","Material Description","ABC Indicator"]
        
        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}

            permintaan_barang = item["Permintaan Barang (D) Unit/Tahun"]
            harga_barang = item["Harga Barang (p) /Unit"]
            ongkos_pesan = item["Ongkos Pesan (A) /Pesan"]
            lead_time = item["Lead Time (L) Tahun"]
            ongkos_simpan = item["Ongkos Simpan (h) /Unit/Tahun"]
            material_code = item["Material Code"]
            material_description = item["Material Description"]
            abc_indikator = item["ABC Indicator"]
            
            data_calc.append(Model_Wilson_PolaDeterministik.Model_Wilson(
                permintaan_barang,
                harga_barang, 
                ongkos_pesan, 
                lead_time, 
                ongkos_simpan, 
                material_code,
                material_description,
                abc_indikator
            ))
    
    if model == "tchebycheff":
        required_keys = ["Unit Price","Stock Out Effect","Standar_Deviasi","Rata_Rata/Bulan","Material Code","Material description","ABC Indicator"]

        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            harga_barang = item["Unit Price"]
            kerugian_ketidakadaan_barang = item["Stock Out Effect"]
            standar_deviasi = item["Standar_Deviasi"]
            rata_rata_permintaan_barang = item["Rata_Rata/Bulan"]
            material_code = item["Material Code"]
            material_description = item["Material description"]
            abc_indikator = item["ABC Indicator"]
            
            data_calc.append(Model_Tchebycheff_PolaTakTentu.Model_Tchebycheff_TakTentu(
                harga_barang, 
                kerugian_ketidakadaan_barang, 
                standar_deviasi, 
                rata_rata_permintaan_barang, 
                material_code,
                material_description,
                abc_indikator))
    
    if model == "q":
        required_keys = ["Rata - Rata Permintaan Barang (D) Unit/Tahun","Lead Time (L) Tahun","Standar Deviasi Permintaan Barang (s) Unit/Tahun","Ongkos Pesan (A) /Pesan","Harga Barang (p) /Unit","Ongkos Simpan (h) /Unit/Tahun","Ongkos Kekurangan Inventori (Cu) /Unit/Tahun","Material Code","Material Description","ABC Indicator"]

        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            rata_rata_permintaan_barang =  item['Rata - Rata Permintaan Barang (D) Unit/Tahun']
            lead_time = item['Lead Time (L) Tahun']
            standar_deviasi = item['Standar Deviasi Permintaan Barang (s) Unit/Tahun']
            ongkos_pesan = item['Ongkos Pesan (A) /Pesan']
            harga_barang = item['Harga Barang (p) /Unit']
            ongkos_simpan = item['Ongkos Simpan (h) /Unit/Tahun']
            ongkos_kekurangan_inventori_setiap_unit_barang = item['Ongkos Kekurangan Inventori (Cu) /Unit/Tahun']
            material_code = item['Material Code']
            material_description = item['Material Description']
            abc_indikator = item['ABC Indicator']
            
            data_calc.append(Model_Q_PolaDistribusiNormal.Model_Q(rata_rata_permintaan_barang , 
                lead_time, 
                standar_deviasi, 
                ongkos_pesan ,
                harga_barang,
                ongkos_simpan, 
                ongkos_kekurangan_inventori_setiap_unit_barang,
                material_code, 
                material_description, 
                abc_indikator))
    
    if model == "poisson":
        required_keys = ["Rata - Rata Permintaan Barang (D) Unit/Tahun","Standar Deviasi Permintaan Barang (s) Unit/Tahun","Lead Time (L) Tahun","Ongkos Pesan (A) /Pesan","Harga Barang (p) /Unit","Ongkos Simpan (h) /Unit/Tahun","Ongkos Kekurangan Inventori (Cu) /Unit/Tahun",]
        
        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            rata_rata_pemesanan_barang = item["Rata - Rata Permintaan Barang (D) Unit/Tahun"]
            standar_deviasi_barang = item["Standar Deviasi Permintaan Barang (s) Unit/Tahun"]
            lead_time = item["Lead Time (L) Tahun"]
            ongkos_pesan = item["Ongkos Pesan (A) /Pesan"]
            harga_barang = item["Harga Barang (p) /Unit"]
            ongkos_simpan = item["Ongkos Simpan (h) /Unit/Tahun"]
            ongkos_kekurangan_barang = item["Ongkos Kekurangan Inventori (Cu) /Unit/Tahun"]
            material_code = item["Material Code"]
            material_description = item["Material Description"]
            abc_indikator = item["ABC Indicator"]
            
            data_calc.append(Model_Poisson_PolaPoisson.Model_Poisson(
                rata_rata_pemesanan_barang, 
                standar_deviasi_barang, 
                lead_time,
                ongkos_pesan, 
                harga_barang, 
                ongkos_simpan, 
                ongkos_kekurangan_barang,
                material_code,
                material_description,
                abc_indikator
            ))

    if model == "nonmoving":
        required_keys = ["Unit Price", "Stock Out Effect", "Jumlah Komponen Terpasang"]
        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            ongkos_pemakaian_komponen = item["Unit Price"]
            ongkos_kerugian_akibat_kerusakan = item["Stock Out Effect"]
            jumlah_komponen_terpasang = item["Jumlah Komponen Terpasang"]
            
            data_calc.append({
                "regret": Model_MinMaxRegret_PolaNonMoving.Model_MinMaxRegret(
                    ongkos_pemakaian_komponen,
                    ongkos_kerugian_akibat_kerusakan,
                    jumlah_komponen_terpasang,
                ),
                "linear": Model_KerusakanLinear_PolaNonMoving.model_kerusakan_linear(
                    ongkos_pemakaian_komponen,
                    ongkos_kerugian_akibat_kerusakan,
                    jumlah_komponen_terpasang,
                ),
                "non_linear": Model_KerusakanNonLinear_PolaNonMoving.model_kerusakan_non_linear(
                    ongkos_pemakaian_komponen,
                    ongkos_kerugian_akibat_kerusakan,
                    jumlah_komponen_terpasang,
                )
            })

    if model == "bcr":
        required_keys = ["Unit Price", "Stock Out Effect", "Suku Bunga", "Sisa Tahun Pemakaian"]
        
        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            harga_komponen = item["Unit Price"]
            kerugian_komponen = item["Stock Out Effect"]
            suku_bunga = item["Suku Bunga"]
            waktu_sisa_operasi = item["Sisa Tahun Pemakaian"]
            
            data_calc.append(Model_BCR_new.Model_Inventori_BCR(
                harga_komponen, 
                kerugian_komponen, 
                suku_bunga, 
                waktu_sisa_operasi
            ))

    return data_calc