# Modifikasi

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