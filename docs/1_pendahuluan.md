# Pendahuluan

## Latar Belakang

Planet-planet luar surya telah (dan sedang) ditemukan dalam jumlah yang membuat pengamatan intensif tidak memungkinkan untuk dilakukan secara merata terhadap setiap planet, terutama untuk pengamatan yang bertujuan mengungkap potensi keberadaan makhluk hidup di permukaan planet-planet tersebut. Indeks kelayakhunian dapat menjadi panduan dalam memprioritaskan planet-planet yang menarik untuk diamati lebih lanjut. Salah satu sistem indeks seperti itu adalah _Habitability Index for Transiting Exoplanets_ (HITE).

Perkembangan dalam pengamatan dan pemodelan mengenai planet luar surya sejak saat HITE disusun membuka kemungkinan untuk memperbarui beberapa komponen HITE dan membuatnya lebih akurat dan inklusif. *Modified* HITE (M-HITE) yang dijelaskan dalam dokumentasi ini adalah HITE dengan proses data masukan yang disederhanakan  dan algoritma yang disuplemen dengan subrutin dari beberapa literatur penelitian keplanetan luar surya.

M-HITE diharapkan dapat menghasilkan sistem pengindeksan yang lebih akurat dalam memberikan gambaran kelayakhunian planet luar surya untuk keperluan pemrioritasan observasi.

## Tutorial Teknis

### Instalasi *environment*

Program M-HITE dikembangkan menggunakan IDE Jupyter Notebook. Jika perangkat yang akan digunakan belum memiliki instalasi Python, disarankan untuk menginstal Python bersamaan dengan Jupyter Notebook melalui distribusi Anaconda atau Miniconda.

**Dependensi**. M-HITE juga membutuhkan *package* Python berikut ini:
- pandas
- numpy
- scipy

### Berkas
Berkas-berkas yang diperlukan untuk menjalankan M-HITE dapat diunduh di [sini](https://github.com/abell1689/M-HITE/raw/main/docs/M-HITE.zip) Berkas-berkas tersebut adalah:
- `main.ipynb`
	- berkas utama yang berisi algoritma penghitungan indeks
	- bisa dibuka dan diubah menggunakan Jupyter Notebook
	- berkas yang isinya dijelaskan pada laman {doc}`3_perincian_kode`.
- `exoplanet.csv`
	- berkas yang berisi data planet luar surya
	- didapat dari [exoplanets.org](exoplanets.org)
	- digunakan sebagai sumber data masukan dalam `main.ipynb`
	- kolom yang tidak digunakan oleh M-HITE bisa dihilangkan untuk membuatnya lebih rapi
	- bisa di-filter dan dibuat sub-daftar sesuai karakteristik planet yang ingin dibuatkan daftar indeks
	- disediakan pula `exoplanets_noKOI.csv` (berkas yang sama tapi tanpa mengikutkan _Kepler object of interest_ (KOI), planet-planet luar surya yang belum cukup terkonfirmasi keberadaannya)
- `zsboundaries.csv`
	- berkas yang berisi tabel nilai radius dan massa
	- diadaptasi dari Zeng & Sasselov (2013)
	- digunakan untuk menentukan komposisi penyusun planet (dan apakah planet bersifat terestrial atau tidak)
- `out.txt`
	- berkas untuk menyimpan hasil pengindeksan

### Langkah pertama
Ekstrak unduhan dan simpan semua berkas dalam satu folder.
Jalankan Jupyter Notebook (dari command prompt atau Anaconda launcher) dan buka `main.ipynb`.

### *Live sandbox*
Pada dokumentasi ini disediakan juga *live sandbox* yang langsung bisa digunakan tanpa menginstal apapun. (Ikon roket –> Live Code)