\begin{gather*}
a_1=b_1+c_1\\
a_2=b_2+c_2-d_2+e_2
\end{gather*}

\begin{align}
a_{11}& =b_{11}&
  a_{12}& =b_{12}\\
a_{21}& =b_{21}&
  a_{22}& =b_{22}+c_{22}
\end{align}

\begin{document}
\begin{equation}
P_{ter}(R)=
\begin{cases}
0, & R <= 1 \\
(2.5-R), & 1.5 < R < 2.5 \\
1, & R >= 2.5.
\end{cases}
\end{equation}
\end{document}

# Perincian Algoritma
Laman ini memuat perincian algoritma yang dipakai dalam menentukan nilai indeks HITE bagi suatu eksoplanet, serta modifikasi yang dilakukan terhadap algoritma tersebut sehingga menjadi HITE termodifikasi (M-HITE)

## Asumsi
### ‘Layak Huni’
Dalam teks ini, kelayakhunian didefinisikan sebagai 'layak huni bagi makhluk hidup'. Terdengar cukup sederhana, tapi perlu diingat bahwa kehidupan di planet lain, jika ada, tentu saja bisa memiliki proses-proses biokimia yang berbeda jauh dengan kehidupan yang kita ketahui—sesuatu yang sulit dibayangkan karena contoh bentuk kehidupan yang kita ketahui saat ini baru satu, yaitu kehidupan di Bumi. 
Upaya untuk membayangkan bentuk kehidupan alternatif seperti itu merupakan bidang penelitiannya sendiri. Karena itu, teks ini akan menggunakan definisi kehidupan yang cenderung sederhana, yaitu organisme dengan karakteristik yang kurang lebih mirip dengan yang ada di Bumi: berbasis senyawa karbon dan membutuhkan air. Fokusnya terutama diberikan pada organisme sederhana yang relatif tahan banting seperti **bakteri bersel satu**.

## Data masukan
### Orisinal
- HITE orisinal ditujukan untuk mengevaluasi planet yang ditemukan menggunakan metode transit, sehingga data masukan yang dibutuhkan adalah observabel-observabel transit.
### Termodifikasi
- M-HITE mengubah algoritma penghitungan indeks sehingga bisa digunakan untuk mengevaluasi planet mana pun, tidak terbatas pada yang ditemukan melalui metode transit. 
 
## Syarat kelayakhunian
HITE orisinal mengevaluasi kelayakhunian dengan mengukur probabilitas suatu planet memenuhi dua syarat tertentu. M-HITE tidak melakukan perubahan dalam hal ini. Kedua syarat tersebut adalah: 
### 1. memiliki permukaan padat (bersifat terestrial)
Dalam algoritma HITE, planet yang dianggap layak huni adalah planet yang permukaannya lebih mirip dengan permukaan planet Bumi atau Mars (tersusun dari silikat dan logam) daripada dengan yang ada di planet seperti Jupiter atau Neptunus (tersusun dari gas dan likuida dalam tekanan dan temperatur yang tinggi).

Syarat ini didasarkan pada argumen bahwa untuk mendukung perkembangan makhluk hidup, diperlukan lingkungan yang bisa ajeg dalam satuan waktu yang cukup lama, yang tentunya tidak sesuai dengan permukaan gas dan likuida yang cenderung dinamis. Bahkan kehidupan bawah air seperti yang ada di Bumi pun secara krusial bergantung pada keberadaan kerak samudera yang padat dan relatif stabil.

### 2. memiliki air berfase cair di permukaannya
Selain keberadaan permukaan padat, kelayakhunian suatu planet menurut HITE juga didasarkan pada kemungkinan adanya air berfase cair di permukaan tersebut.

Syarat ini didasarkan pada argumen bahwa air berfase cair merupakan komponen penting bagi makhluk hidup--setidaknya makhluk hidup yang dispesifikasikan teks ini pada bagian [Asumsi].

## Algoritma
### Penghitungan probabilitas planet memiliki permukaan padat
#### Orisinal
Probabilitas suatu planet bersifat terestrial diestimasi melalui model berikut ini, yang hanya menggunakan radius relatif sebagai masukan:

$$P_ter (R)={("1" ,R≤"1,5" @("2,5" -R),"1,5" <R<"2,5" @"0" ,R≥"2,5" .)}$$




$R$ adalah radius relatif, perbandingan antara radius planet $(R_p)$ dengan radius Bumi ($R_⊕$):

### Penghitungan probabilitas planet bisa memiliki air berfase cair di permukaan

### Penghitungan probabilitas kelayakhunian (*H*)




## Modifikasi

3) program HITE memerlukan data eksentrisitas (_e_) dan albedo planet (_A_) untuk menghitung probabilitas kelayakhunian _H (e, A)_. Pada HITE orisinal, kedua parameter ini dianggap tidak diketahui. Nilai _H (e, A)_ dievaluasi menggunakan pasangan _e_ dan _A_ dalam rentang tertentu yang seragam. 


Berikut adalah modifikasi yang telah dilakukan terhadap program HITE sehingga menjadi M-HITE:
1) **program telah ditulis ulang**, dari C ke Python;
2) **pengubahan data masukan (penggunaan basis data [exoplanets.org](https://www.exoplanets.org))**; **Program HITE orisinal**, sesuai namanya, berfokus pada eksoplanet yang ditemukan melalui **metode transit**. Karena itu, HITE orisinal menggunakan beberapa variabel observasi yang hanya bisa didapat melalui metode tersebut (misal: penggunaan *transit depth* untuk mendapatkan radius planet). Modifikasi dilakukan sehingga nilai dari parameter-parameter ini tidak dihitung, tapi langsung diambil dari basis data [exoplanets.org](https://www.exoplanets.org). Hal ini memungkinkan M-HITE untuk mengevaluasi probabilitas kelayakhunian dari planet-planet yang ditemukan melalui metode lain;
3) modifikasi di atas juga mengubah proses kalkulasi nilai indeks. Pada HITE orisinal, rentang parameter eksentrisitas orbit (_e_) dan albedo planet (_A_) yang digunakan untuk menghitung probabilitas layak huni _H (e, A)_  disamakan untuk semua planet. Pada M-HITE, nilai-nilai tersebut diganti dengan rentang ketidakpastian _e_ dan _A_ masing-masing planet dari [exoplanets.org](http://www.exoplanets.org)
Contoh: Perubahan data eksentrisitas
| Planet | HITE orisinal | M-HITE |
|:------:|:-------------:|:------:|
| Kepler-427 b | 0,05 ≤ _e_ ≤ 0,8 | 0,00 ≤ _e_ ≤ 0,57 |
| WASP-14 b | 0,05 ≤ _e_ ≤ 0,8 | 0,003 ≤ _e_ ≤ 0,003 |
| GJ 625 b | 0,05 ≤ _e_ ≤ 0,8 | 0,09 ≤ _e_ ≤ 0,012
4) **pengubahan metode kalkulasi keterestrialan planet**;  
		HITE orisinal melakukan ini dengan suatu algoritma _ad-hoc_ yang hanya mempertimbangkan radius planet sebagai masukan. M-HITE mengganti metode ini dengan pemodelan komposisi planet berdasarkan radius dan massa yang dikembangkan oleh Zeng & Sasselov (2013);
5) **penambahan filter/syarat kelayakhunian**
	- asumsi tentang albedo planet terestrial;
    - Diasumsikan bahwa ada rentang nilai albedo planet yang menandakan kecenderungan lebih tinggi untuk bersifat layak huni. Rentang ini tergantung pada temperatur/tipe bintang inang dan radius orbit eksoplanet. Planet dengan _A_ yang berada di luar rentang tersebut akan dianggap tidak layak huni oleh program HITE. Untuk saat ini, rentang albedo ini baru bisa dikalkulasi untuk planet yang mengorbit bintang tipe G atau M
	- *asumsi tentang eksentrisitas orbit yang ekstrem**;
    - eksentrisitas orbit yang ekstrem dianggap menurunkan probabilitas kelayakhunian, sehingga planet dengan _e_ di atas angka tertentu (ditentukan oleh luminositas bintang inang) probabilitas layak huninya diberi penalti dan urutannya cederung turun dalam indeks;