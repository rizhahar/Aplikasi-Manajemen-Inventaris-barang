# Fungsi Library
import csv
import os
from datetime import datetime

# Membuat File CSV
FILE_BARANG = 'barang.csv'
FILE_TRANSAKSI = 'transaksi.csv'

# Struktur data global
hash_map_barang = {}
stack_transaksi = []

# Fungsi CSV
def inisialisasi_csv():
    # Membuat kolom dan header File barang
    if not os.path.exists(FILE_BARANG):
        with open(FILE_BARANG, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID_Barang', 'Nama_Barang', 'Stok'])

    # Membuat kolom dan header File transaksi        
    if not os.path.exists(FILE_TRANSAKSI):
        with open(FILE_TRANSAKSI, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID_Transaksi', 'ID_Barang', 'Jenis', 'Jumlah', 'Tanggal'])

# Membaca File CSV
def load_data():
    global hash_map_barang, stack_transaksi
    hash_map_barang.clear()
    stack_transaksi.clear()
    
    # Load ke Hash Map
    with open(FILE_BARANG, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hash_map_barang[row['ID_Barang']] = {
                'nama': row['Nama_Barang'],
                'stok': int(row['Stok'])
            }
            
    # Load ke Stack
    with open(FILE_TRANSAKSI, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stack_transaksi.append({
                'id_transaksi': row['ID_Transaksi'],
                'id_barang': row['ID_Barang'],
                'jenis': row['Jenis'],
                'jumlah': int(row['Jumlah']),
                'tanggal': row['Tanggal']
            })

# Menyimpan data ke file CSV
def save_data():
    # Save dari Hash Map ke barang.csv
    with open(FILE_BARANG, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_Barang', 'Nama_Barang', 'Stok'])
        for id_barang, data in hash_map_barang.items():
            writer.writerow([id_barang, data['nama'], data['stok']])
            
    # Save dari Stack ke transaksi.csv
    with open(FILE_TRANSAKSI, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_Transaksi', 'ID_Barang', 'Jenis', 'Jumlah', 'Tanggal'])
        for trans in stack_transaksi:
            writer.writerow([trans['id_transaksi'], trans['id_barang'], trans['jenis'], trans['jumlah'], trans['tanggal']])

# Fitur CRUD
# Menambahkan data atau barang baru
def tambah_barang():
    print("\n--- TAMBAH BARANG BARU ---")
    
    # Membuat ID barang secara otomatis
    prefix = "A"
    if not hash_map_barang:
        id_barang = f"{prefix}001"
    else:
        daftar_angka = []
        for k in hash_map_barang.keys():
            if k.startswith(prefix) and k[1:].isdigit():
                daftar_angka.append(int(k[1:]))
        
        if daftar_angka:
            next_num = max(daftar_angka) + 1
        else:
            next_num = 1
            
        id_barang = f"{prefix}{next_num:03d}"
    
    print(f"ID Barang Otomatis Terbuat: {id_barang}")
        
    nama = input("Masukkan Nama Barang: ").strip()
    if not nama:
        print("Gagal! Nama barang tidak boleh kosong.")
        return
        
    try:
        stok = int(input("Masukkan Stok Awal: "))
        if stok < 0:
            print("Gagal! Stok tidak boleh kurang dari 0.")
            return
    except ValueError:
        print("Stok harus berupa angka!")
        return
        
    # Menyimpan ke Hash Map
    hash_map_barang[id_barang] = {'nama': nama, 'stok': stok}
    save_data()
    print(f"Barang '{nama}' dengan ID {id_barang} berhasil ditambahkan!")

# Update proses menambahkan dan mengeluarkan barang, lalu memasukannya ke stack
def proses_transaksi(jenis):
    print(f"\n--- BARANG {jenis.upper()} ---")
    id_barang = input("Masukkan ID Barang: ").strip().upper()
    
    if id_barang not in hash_map_barang:
        print("Gagal! Barang tidak ditemukan di Hash Map.")
        return
        
    try:
        jumlah = int(input(f"Masukkan jumlah barang {jenis}: "))
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0!")
            return
    except ValueError:
        print("Jumlah harus berupa angka!")
        return

    # Validasi stok jika barang keluar
    if jenis == 'Keluar' and hash_map_barang[id_barang]['stok'] < jumlah:
        print("Gagal! Stok tidak mencukupi.")
        return

    # Update Hash Map (Stok)
    if jenis == 'Masuk':
        hash_map_barang[id_barang]['stok'] += jumlah
    else:
        hash_map_barang[id_barang]['stok'] -= jumlah

    # Buat Transaksi dan Push ke Stack
    id_trans = f"TRX{len(stack_transaksi)+1:03d}"
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    stack_transaksi.append({
        'id_transaksi': id_trans,
        'id_barang': id_barang,
        'jenis': jenis,
        'jumlah': jumlah,
        'tanggal': tanggal
    })
    
    save_data()
    print(f"Transaksi berhasil! Stok {hash_map_barang[id_barang]['nama']} sekarang: {hash_map_barang[id_barang]['stok']}")

# Fungsi menghapus data barang / delete barang
def hapus_barang():
    print("\n--- HAPUS BARANG ---")
    id_barang = input("Masukkan ID Barang yang akan dihapus: ").strip().upper()
    
    if id_barang in hash_map_barang:
        nama = hash_map_barang[id_barang]['nama']
        del hash_map_barang[id_barang] # Hapus dari Hash Map
        save_data()
        print(f"Barang {nama} (ID: {id_barang}) berhasil dihapus!")
    else:
        print("Barang tidak ditemukan!")

# Fungsi cari barang 
def cari_barang():
    print("\n--- CARI BARANG ---")
    id_barang = input("Masukkan ID Barang yang dicari: ").strip().upper()
    
    # Pencarian langsung menggunakan Hash Map Key
    if id_barang in hash_map_barang:
        data = hash_map_barang[id_barang]
        print(f"\n[DITEMUKAN] ID: {id_barang} | Nama: {data['nama']} | Stok: {data['stok']}")
    else:
        print("\n[TIDAK DITEMUKAN] Barang dengan ID tersebut tidak ada di inventori.")

# Menampilkan stock barang dan mengurutkannya
def laporan_stok_sorting():
    print("\n--- LAPORAN STOK BARANG ---")
    if not hash_map_barang:
        print("Gudang kosong.")
        return

    # Ubah hash map menjadi list untuk keperluan sorting
    list_barang = []
    for id_barang, data in hash_map_barang.items():
        list_barang.append([id_barang, data['nama'], data['stok']])
        
    # Algoritma Bubble Sort (Berdasarkan Stok: Kecil ke Besar)
    n = len(list_barang)
    for i in range(n):
        for j in range(0, n-i-1):
            if list_barang[j][2] > list_barang[j+1][2]:
                # Tukar posisi
                list_barang[j], list_barang[j+1] = list_barang[j+1], list_barang[j]
                
    # Menampilkan hasil
    print(f"{'ID BARANG':<10} | {'NAMA BARANG':<20} | {'STOK':<5}")
    print("-" * 43)
    for barang in list_barang:
        print(f"{barang[0]:<10} | {barang[1]:<20} | {barang[2]:<5}")

# Menampilkan riwayat transaksi
def riwayat_transaksi():
    print("\n--- RIWAYAT TRANSAKSI (STACK) ---")
    if not stack_transaksi:
        print("Belum ada riwayat transaksi.")
        return
        
    print(f"{'ID TRANS':<10} | {'TANGGAL':<20} | {'ID BARANG':<10} | {'JENIS':<7} | {'JUMLAH':<6}")
    print("-" * 65)
    
    # Membaca Stack dari atas (reverse)
    for trans in reversed(stack_transaksi):
        print(f"{trans['id_transaksi']:<10} | {trans['tanggal']:<20} | {trans['id_barang']:<10} | {trans['jenis']:<7} | {trans['jumlah']:<6}")

# Fungsi MENU
def main_menu():
    inisialisasi_csv()
    load_data()
    
    while True:
        print("\n" + "="*35)
        print(" === SISTEM INVENTORI GUDANG === ")
        print("="*35)
        print("1. Tambah Barang Baru ") # fungsi buat data barang
        print("2. Barang Masuk ") # fungsi update barang masuk
        print("3. Barang Keluar ") # fungsi update barang keluar
        print("4. Cari Barang by ID ") # fungsi pencarian barang
        print("5. Laporan & Sorting Stok ") # fungsi melihat stok barang
        print("6. Lihat Riwayat Transaksi ") # lihat riwayat transaksi
        print("7. Hapus Barang ") # fungsi hapus barang
        print("0. Keluar") # fungsi keluar
        print("="*35)
        
        pilihan = input("Pilihan menu (0-7): ").strip()
        
        if pilihan == '1':
            tambah_barang()
        elif pilihan == '2':
            proses_transaksi('Masuk')
        elif pilihan == '3':
            proses_transaksi('Keluar')
        elif pilihan == '4':
            cari_barang()
        elif pilihan == '5':
            laporan_stok_sorting()
        elif pilihan == '6':
            riwayat_transaksi()
        elif pilihan == '7':
            hapus_barang()
        elif pilihan == '0':
            print("Terima kasih telah menggunakan sistem inventori ini!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Jalankan program
if __name__ == "__main__":
    main_menu()