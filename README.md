Kalkulator Aljabar Linear (Matrix Calculator)

Deskripsi

Kalkulator Aljabar Linear adalah aplikasi berbasis GUI (Graphical User Interface) yang dikembangkan menggunakan Python, NumPy, dan PyQt5 untuk melakukan perhitungan aljabar linear.
Aplikasi ini mendukung operasi matriks, operasi vektor, serta penyelesaian Sistem Persamaan Linear (SPL) dengan validasi input yang aman dan hasil perhitungan yang akurat.

Proyek ini dikembangkan sebagai bagian dari pembelajaran Aljabar Linear dan Pemrograman, dengan tujuan mengimplementasikan konsep matematika ke dalam aplikasi nyata berbasis GUI.

Fitur Aplikasi
Operasi Matriks
1. Penjumlahan dan pengurangan matriks
2. Perkalian matriks
3. Transpose matriks
4. Determinan matriks
5. Invers matriks (jika memenuhi syarat)

Operasi Vektor
1. Penjumlahan dan pengurangan vektor
2. Perkalian skalar
3. Perhitungan vektor dasar

Sistem Persamaan Linear (SPL)
1. Penyelesaian SPL menggunakan metode matriks
2. Validasi hasil (solusi unik, banyak solusi, atau tidak ada solusi)
3. Penanganan input tidak valid

Antarmuka GUI
1. Dibangun menggunakan PyQt5
2. Input dinamis sesuai ukuran matriks/vektor
3. Navigasi halaman (Welcome, Matrix, Vector, SPL)
4. Riwayat perhitungan
   
Teknologi yang Digunakan
1. Python 3
2. NumPy – komputasi numerik dan aljabar linear
3. PyQt5 – antarmuka grafis (GUI)

Struktur Folder Project
007_DeviMaulani_KalkulatorMatriks/
│
├── core/
│   ├── app.py            # Main application logic
│   ├── history.py        # Penyimpanan dan manajemen riwayat
│   ├── state.py          # Manajemen state aplikasi
│   ├── theme.py          # Pengaturan tema aplikasi
│   └── __init__.py
│
├── views/
│   ├── welcome_view.py   # Halaman awal
│   ├── matrix_view.py    # Tampilan operasi matriks
│   ├── vector_view.py    # Tampilan operasi vektor
│   ├── spl_view.py       # Tampilan penyelesaian SPL
│   └── __init__.py
│
├── widgets/
│   ├── dynamic_inputs.py # Widget input dinamis matriks/vektor
│   └── __init__.py
│
└── README.md


Tujuan Pengembangan
1. Mengimplementasikan konsep aljabar linear ke dalam aplikasi Python
2. Mengembangkan aplikasi GUI menggunakan PyQt5
3. Melatih pemrograman modular dan terstruktur
4. Menyediakan alat bantu pembelajaran matematika yang interaktif

Pengembang
Devi Maulani
Mahasiswa D4 Teknik Informatika Politeknik Negeri Bandung 

Lisensi
Proyek ini dikembangkan untuk keperluan akademik dan pembelajaran.
Bebas digunakan dan dikembangkan lebih lanjut dengan mencantumkan sumber.
