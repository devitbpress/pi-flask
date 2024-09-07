from app.calc import Model_Wilson_PolaDeterministik
from app.calc import Model_Tchebycheff_PolaTakTentu
from app.calc import Model_Q_PolaDistribusiNormal
from app.calc import Model_Poisson_PolaPoisson
from app.calc import Model_MinMaxRegret_PolaNonMoving
from app.calc import Model_KerusakanNonLinear_PolaNonMoving
from app.calc import Model_KerusakanLinear_PolaNonMoving
from app.calc import Model_BCR_new

def convert_string_to_number(s):
    if '.' in s:
        return convert_string_to_number(s)
    else:
        return int(s)

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
        required_keys = ["Harga Barang (p) /Unit","Kerugian Ketidakadaan Barang (Cu) /Unit","Standar Deviasi Permintaan Barang (s)","Rata - Rata Permintaan Barang (alpha)"]

        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            harga_barang = item["Harga Barang (p) /Unit"]
            kerugian_ketidakadaan_barang = item["Kerugian Ketidakadaan Barang (Cu) /Unit"]
            standar_deviasi = item["Standar Deviasi Permintaan Barang (s)"]
            rata_rata_permintaan_barang = item["Rata - Rata Permintaan Barang (alpha)"]
            material_code = item["Material Code"]
            material_description = item["Material Description"]
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
        required_keys = ["Ongkos Pemakaian Komponen (H)", "Ongkos Kerugian Akibat Kerusakan (L)", "Jumlah Komponen Terpasang (m)"]
        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            material_code = item["Material Code"]
            material_description = item["Material Description"]
            abc_indikator = item["ABC Indicator"]
            ongkos_pemakaian_komponen = item["Ongkos Pemakaian Komponen (H)"]
            ongkos_kerugian_akibat_kerusakan = item["Ongkos Kerugian Akibat Kerusakan (L)"]
            jumlah_komponen_terpasang = item["Jumlah Komponen Terpasang (m)"]
            
            data_calc.append({
                "regret": Model_MinMaxRegret_PolaNonMoving.Model_MinMaxRegret(
                    ongkos_pemakaian_komponen,
                    ongkos_kerugian_akibat_kerusakan,
                    jumlah_komponen_terpasang,
                    material_code,
                    material_description,
                    abc_indikator
                ),
                "linear": Model_KerusakanLinear_PolaNonMoving.model_kerusakan_linear(
                    ongkos_pemakaian_komponen,
                    ongkos_kerugian_akibat_kerusakan,
                    jumlah_komponen_terpasang,
                    material_code,
                    material_description,
                    abc_indikator
                ),
                "non_linear": Model_KerusakanNonLinear_PolaNonMoving.model_kerusakan_non_linear(
                    ongkos_pemakaian_komponen,
                    ongkos_kerugian_akibat_kerusakan,
                    jumlah_komponen_terpasang,
                    material_code,
                    material_description,
                    abc_indikator,
                )
            })

    if model == "bcr":
        required_keys = ["Harga Komponen (Ho)", "Kerugian Komponen (Co)", "Suku Bunga (I)", "Waktu Sisa Operasi (tahun)"]
        
        for item in data:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                return {"error": f"Missing keys: {', '.join(missing_keys)}"}
            
            material_code = item["Material Code"]
            material_description = item["Material Description"]
            abc_indikator = item["ABC Indicator"]
            harga_komponen = item["Harga Komponen (Ho)"]
            kerugian_komponen = item["Kerugian Komponen (Co)"]
            suku_bunga = item["Suku Bunga (I)"]
            waktu_sisa_operasi = item["Waktu Sisa Operasi (tahun)"]
            
            data_calc.append(Model_BCR_new.Model_Inventori_BCR(
                harga_komponen,
                kerugian_komponen, 
                suku_bunga, 
                waktu_sisa_operasi,
                material_code,
                material_description,
                abc_indikator,
            ))

    return data_calc

def calc_model_manual(data):
    model = data.get("model")
    data_calc = {}
    
    if model == "Q":
        rata_rata_permintaan_barang = convert_string_to_number(data.get('rata_rata_permintaan_barang'))
        lead_time = convert_string_to_number(data.get('lead_time'))
        standar_deviasi = convert_string_to_number(data.get('standar_deviasi'))
        ongkos_pesan = convert_string_to_number(data.get('ongkos_pesan'))
        harga_barang = convert_string_to_number(data.get('harga_barang'))
        ongkos_simpan = convert_string_to_number(data.get('ongkos_simpan'))
        ongkos_kekurangan_inventori_setiap_unit_barang = convert_string_to_number(data.get('ongkos_kekurangan_inventory'))
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")

        data_calc = Model_Q_PolaDistribusiNormal.Model_Q(
                rata_rata_permintaan_barang , 
                lead_time, 
                standar_deviasi, 
                ongkos_pesan ,
                harga_barang,
                ongkos_simpan, 
                ongkos_kekurangan_inventori_setiap_unit_barang,
                material_code,
                material_description,
                abc_indikator
            )
    
    if model == "Poisson":
        rata_rata_pemesanan_barang = convert_string_to_number(data.get("rata_rata_permintaan_barang"))
        standar_deviasi_barang = convert_string_to_number(data.get("standar_deviasi"))
        lead_time = convert_string_to_number(data.get("lead_time"))
        ongkos_pesan = convert_string_to_number(data.get("ongkos_pesan"))
        harga_barang = convert_string_to_number(data.get("harga_barang"))
        ongkos_simpan = convert_string_to_number(data.get("ongkos_simpan"))
        ongkos_kekurangan_barang = convert_string_to_number(data.get("ongkos_kekurangan_inventory"))
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")

        data_calc = Model_Poisson_PolaPoisson.Model_Poisson(
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
            )
    
    if model == "Wilson":
        permintaan_barang = convert_string_to_number(data.get("permintaan_barang"))
        harga_barang = convert_string_to_number(data.get("harga_barang"))
        ongkos_pesan = convert_string_to_number(data.get("ongkos_pesan"))
        lead_time = convert_string_to_number(data.get("lead_time"))
        ongkos_simpan = convert_string_to_number(data.get("ongkos_simpan"))
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        
        data_calc = Model_Wilson_PolaDeterministik.Model_Wilson(
                permintaan_barang,
                harga_barang, 
                ongkos_pesan, 
                lead_time, 
                ongkos_simpan, 
                material_code,
                material_description,
                abc_indikator
            )
    
    if model == "Tchebycheff":
        harga_barang = convert_string_to_number(data.get("harga_barang"))
        kerugian_ketidakadaan_barang = convert_string_to_number(data.get("kerugian_ketidakadaan_barang"))
        standar_deviasi = convert_string_to_number(data.get("standar_deviasi"))
        rata_rata_permintaan_barang = convert_string_to_number(data.get("rata_rata_permintaan_barang"))
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        
        data_calc = Model_Tchebycheff_PolaTakTentu.Model_Tchebycheff_TakTentu(
            harga_barang, 
            kerugian_ketidakadaan_barang, 
            standar_deviasi, 
            rata_rata_permintaan_barang, 
            material_code,
            material_description,
            abc_indikator)
    
    if model == "Regret":
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        ongkos_pemakaian_komponen = convert_string_to_number(data.get("ongkos_pemakaian_komponen"))
        ongkos_kerugian_akibat_kerusakan = convert_string_to_number(data.get("ongkos_kerugian_kerusakan"))
        jumlah_komponen_terpasang = convert_string_to_number(data.get("jumlah_komponen_terpasang"))
        
        data_calc = Model_MinMaxRegret_PolaNonMoving.Model_MinMaxRegret(
                        ongkos_pemakaian_komponen,
                        ongkos_kerugian_akibat_kerusakan,
                        jumlah_komponen_terpasang,
                        material_code,
                        material_description,
                        abc_indikator
                    )
    
    if model == "Linear":
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        ongkos_pemakaian_komponen = convert_string_to_number(data.get("ongkos_pemakaian_komponen"))
        ongkos_kerugian_akibat_kerusakan = convert_string_to_number(data.get("ongkos_kerugian_kerusakan"))
        jumlah_komponen_terpasang = convert_string_to_number(data.get("jumlah_komponen_terpasang"))

        data_calc = Model_KerusakanLinear_PolaNonMoving.model_kerusakan_linear(
                        ongkos_pemakaian_komponen,
                        ongkos_kerugian_akibat_kerusakan,
                        jumlah_komponen_terpasang,
                        material_code,
                        material_description,
                        abc_indikator
                    )
    
    if model == "NonLinear":
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        ongkos_pemakaian_komponen = convert_string_to_number(data.get("ongkos_pemakaian_komponen"))
        ongkos_kerugian_akibat_kerusakan = convert_string_to_number(data.get("ongkos_kerugian_kerusakan"))
        jumlah_komponen_terpasang = convert_string_to_number(data.get("jumlah_komponen_terpasang"))

        data_calc = Model_KerusakanNonLinear_PolaNonMoving.model_kerusakan_non_linear(
                        ongkos_pemakaian_komponen,
                        ongkos_kerugian_akibat_kerusakan,
                        jumlah_komponen_terpasang,
                        material_code,
                        material_description,
                        abc_indikator
                    )
    
    if model == "BCR":
        material_code = data.get("material_code")
        material_description = data.get("material_description")
        abc_indikator = data.get("abc_indikator")
        harga_komponen = convert_string_to_number(data.get("harga_komponen"))
        kerugian_komponen = convert_string_to_number(data.get("kerugian_komponen"))
        suku_bunga = convert_string_to_number(data.get("suku_bunga"))
        waktu_sisa_operasi = convert_string_to_number(data.get("waktu_sisa_operasi"))
        
        data_calc = Model_BCR_new.Model_Inventori_BCR(
                harga_komponen,
                kerugian_komponen, 
                suku_bunga, 
                waktu_sisa_operasi,
                material_code,
                material_description,
                abc_indikator,
            )
    
    return data_calc
