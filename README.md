Cinephile Movie App

Aplikasi desktop sederhana berbasis PyQt5 untuk mencari informasi film dengan fitur scraping dan manajemen wishlist.

---

Deskripsi

Cinephile adalah aplikasi yang memungkinkan pengguna untuk:

- Mencari film berdasarkan judul
- Melihat detail film seperti rating, durasi, genre, dan platform
- Menyimpan film ke dalam wishlist pribadi
- Mengelola akun sederhana (login & sign up)

Aplikasi ini dibuat sebagai proyek pembelajaran pada mata kuliah Struktur Data / Pemrograman. 
Aplikasi ini belum besifat final dan masih trial dimana pada repo ini kami mencoba untuk scraping beberapa film sehingga ketika diimplementasikan mudah untuk kami pahami.
Ini merupakan hasil pemahaman kami yang coba kami kerjakan ketika sedang libur lebaran kemarin.


---

Fitur Utama

- Search Film
  Mencari film dari IMDb

- Scraping Data
  - IMDb → judul, rating, durasi
  - JustWatch → genre, platform

- Detail Film
  Menampilkan informasi lengkap film

- Wishlist
  - Tambah film ke wishlist
  - Hapus film dari wishlist
  - Wishlist tersimpan per user

- Login & Sign Up (Sederhana)
  Sistem autentikasi menggunakan file JSON

---

Teknologi yang Digunakan
- Python
- PyQt5 (GUI)
- Requests
- JSON (penyimpanan data)
- Web Scraping

---
Cara Menjalankan Aplikasi

1. Clone repository:

git clone https://github.com/username/nama-repo.git

2. Masuk ke folder project:

cd webScrapingFilm

3. Install dependency:

pip install PyQt5 requests

4. Jalankan program:

python main.py

---

Cara Kerja Singkat

1. User melakukan login / sign up
2. User masuk ke dashboard
3. User mencari film
4. Aplikasi melakukan scraping dari:
   - IMDb
   - JustWatch
5. Data ditampilkan ke UI
6. User bisa menambahkan ke wishlist

---

Catatan
- Data user disimpan menggunakan file JSON (bukan database)
- Password belum dienkripsi (masih prototype)
- Scraping bergantung pada struktur website (bisa berubah)

---

Tujuan Project

Project ini dibuat untuk:
- Memahami konsep scraping
- Menerapkan GUI dengan PyQt
- Menggunakan struktur data sederhana
- Mengimplementasikan flow login & wishlist

---

Dokumentasi Aplikasi

<img width="881" height="750" alt="Screenshot 2026-03-23 231721" src="https://github.com/user-attachments/assets/e2a59043-f84f-48b6-8b8e-0aae5aa1fded" />


<img width="862" height="695" alt="Screenshot 2026-03-23 222913" src="https://github.com/user-attachments/assets/41c97c9f-3cc1-46f8-9793-7f600a9bb17e" />



<img width="859" height="694" alt="Screenshot 2026-03-23 222920" src="https://github.com/user-attachments/assets/4e0d7b84-77d9-46b7-b7fe-52ee2f5b016e" />



<img width="875" height="747" alt="Screenshot 2026-03-23 231712" src="https://github.com/user-attachments/assets/ebe7aa30-e88b-4d1d-bbb4-b6632e1bbd4c" />

---

Author
- Kelompok D5
