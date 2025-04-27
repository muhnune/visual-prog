# MINI PROJECT VISUAL PROGRAMMING 2025

### Muhammad Nune Huria Sakti

### F1D022075

## A. Deskripsi Singkat Topik Aplikasi

Sistem Inventori Barang adalah aplikasi berbasis desktop yang dikembangkan menggunakan Python dengan framework PyQt6. Aplikasi ini bertujuan untuk membantu pengguna dalam mengelola data inventaris barang, seperti menambahkan, mengedit, menghapus, mencari, serta mengelompokkan barang berdasarkan kategori tertentu. Selain itu, aplikasi ini juga mendukung fitur ekspor dan impor data dalam format CSV, sehingga memudahkan backup dan migrasi data.
Database yang digunakan adalah SQLite, yang bersifat ringan dan praktis untuk kebutuhan lokal (offline).

## B. Langkah-Langkah Pengembangan Aplikasi

Berikut langkah-langkah dalam mengembangkan aplikasi ini:

### 1. Perencanaan dan Analisis Kebutuhan

Menentukan fitur-fitur utama yang dibutuhkan, seperti input data barang, tampilan tabel, pencarian, ekspor/impor data, serta pembuatan ringkasan (summary) data inventaris.

### 2. Pembuatan Struktur Database

o Membuat file db.py yang berisi class DatabaseManager.
o Membuat tabel items di SQLite untuk menyimpan atribut barang seperti kode, nama, stok, harga, kategori, catatan, created_at, dan updated_at.
o Menambahkan fitur trigger database untuk mengupdate otomatis kolom updated_at setiap ada perubahan data.

### 3. Pembuatan Antarmuka Pengguna (GUI)

o Menggunakan PyQt6 untuk membangun antarmuka berbasis QMainWindow.
o Membuat tab navigasi untuk pemisahan fungsi input/edit data dan tampilan tabel data.
o Menyediakan form input dengan validasi dasar seperti batas maksimal karakter dan pilihan kategori.
o Membuat tabel (QTableWidget) untuk menampilkan data inventaris secara real-time.
o Menyediakan bagian pencarian dengan filter berdasarkan kategori, kode, nama, atau catatan.

### 4. Implementasi Fungsi-Fungsi Utama

o Fungsi tambah barang (add_item).
o Fungsi edit barang (update_item).
o Fungsi hapus barang (delete_item).
o Fungsi pencarian barang (search_items).
o Fungsi ekspor data ke CSV (export_data).
o Fungsi impor data dari CSV (import_data).
o Menampilkan ringkasan data (jumlah jenis barang, total stok, total nilai inventori).

### 5. Penambahan Fitur Tambahan

o Tampilan ringkasan dan update waktu terakhir perubahan data.
o Dialog bantuan penggunaan aplikasi.
o Menu “Tentang Aplikasi” yang menampilkan informasi developer.

### 6. Testing dan Debugging

o Melakukan uji coba pada setiap fungsi utama untuk memastikan tidak ada error.
o Menyesuaikan tampilan agar nyaman digunakan (user-friendly).

## C. Penjelasan Fungsi Utama Aplikasi

### Berikut fungsi-fungsi utama dalam aplikasi:

Tambah Data : Barang Pengguna dapat menginput data barang baru seperti kode, nama, stok, harga, kategori, dan catatan.
Edit Data Barang : Pengguna dapat mengubah informasi barang yang sudah ada berdasarkan kode barang.
Hapus Data Barang : Pengguna dapat menghapus satu atau beberapa data barang yang dipilih dari tabel.
Pencarian Data : Fitur pencarian memudahkan pengguna untuk mencari barang berdasarkan filter (kode, nama, kategori, catatan) dan kata kunci.
Export Data : Data inventaris dapat diekspor ke file CSV untuk kebutuhan backup atau pelaporan.
Import Data : Data dari file CSV dapat diimpor ke aplikasi untuk memperbarui atau menambahkan data inventaris.
Ringkasan Data : Menampilkan total jumlah jenis barang, total stok, dan total nilai inventori dalam bentuk rupiah.
Backup Database : Disediakan opsi backup database secara langsung (pada sisi DatabaseManager, untuk pengembangan lanjutan).
Antarmuka Modern : Dengan desain yang rapi, responsive, dan menggunakan PyQt6 untuk user experience yang lebih baik.

## D. Screenshot Aplikasi
