# Dokumentasi M-HITE 
## Selayang Pandang
### Apa itu HITE?
**HITE (_Habitability Index for Transiting Exoplanets_) adalah** indeks/daftar yang mengurutkan eksoplanet menurut probabilitas kelayakhuniannya. Probabilitas ini didefinisikan sebagai kemungkinan planet tersebut: **a) mempunyai permukaan padat**, dan **b) memiliki air berfase cair di permukaannya**. Indeks ini bertujuan untuk menentukan prioritas pengamatan eksoplanet, sehingga sumber daya riset keplanetan luar surya yang terbatas dapat diarahkan untuk mengamati lebih lanjut planet-planet yang ‘menarik secara ilmiah’.

:::{admonition} **Catatan tentang lisensi**
**HITE disusun oleh [Rory Barnes](https://github.com/RoryBarnes/HITE)** dari University of Washington. Program HITE dibagikan dengan lisensi GNU General Public License v3.0 yang memperbolehkan penggunaan dan perubahan terhadap program tersebut secara bebas. Info lebih lanjut tentang lisensinya bisa diperoleh [di sini](https://github.com/RoryBarnes/HITE/blob/master/LICENSE). Sesuai ketentuan lisensi tersebut, modifikasi dari program HITE ini juga dibagikan dengan lisensi yang sama.
:::

## Modifikasi
**Program yang cara kerjanya** akan dijelaskan di sini adalah HITE Termodifikasi/**_Modified HITE_** **(M-HITE)**. Berikut adalah modifikasi yang telah dilakukan terhadap program HITE sehingga menjadi M-HITE:
1) **program telah ditulis ulang**, dari C ke Python;
2) **pengubahan data masukan (penggunaan basis data [exoplanets.org](https://www.exoplanets.org))**;
		Ada besaran-besaran yang pada HITE orisinal dihitung dari variabel observasi (seperti radius planet yang dihitung dari [transit]). Pada M-HITE, besaran-besaran ini tidak dihitung, tetapi langsung diambil dari basis data [exoplanets.org](https://www.exoplanets.org). Hal ini memungkinkan M-HITE untuk mengevaluasi probabilitas kelayakhunian dari planet-planet yang ditemukan melalui metode lain selain metode transit
Contoh: Eksentrisitas planet TRAPPIST-1 e
| M-HITE           | M-HITE |
|:----------------:|:------:|
| 0,05 ≤ _A_ ≤ 0,8 |        |

Rentang parameter eksentrisitas orbit (_e_) dan albedo planet (_A_) yang digunakan untuk menghitung probabilitas layak huni _H (e, A)_ pada HITE orisinal disamakan untuk semua planet. Pada M-HITE, ini diganti dengan rentang ketidakpastian _e_ dan _A_ masing-masing planet yang juga diambil dari [exoplanets.org](http://www.exoplanets.org)
Contoh:  
3) **pengubahan metode kalkulasi keterestrialan planet**;  
		HITE orisinal melakukan ini dengan suatu algoritma _ad-hoc_ yang hanya mempertimbangkan radius planet sebagai masukan. M-HITE mengganti metode ini dengan pemodelan komposisi planet berdasarkan radius dan massa yang dikembangkan oleh Zeng & Sasselov (2013);
4) **penambahan filter/syarat kelayakhunian**
	- asumsi tentang albedo planet terestrial;
    - Diasumsikan bahwa ada rentang nilai albedo planet yang menandakan kecenderungan lebih tinggi untuk bersifat layak huni. Rentang ini tergantung pada temperatur/tipe bintang inang dan radius orbit eksoplanet. Planet dengan _A_ yang berada di luar rentang tersebut akan dianggap tidak layak huni oleh program HITE. Untuk saat ini, rentang albedo ini baru bisa dikalkulasi untuk planet yang mengorbit bintang tipe G atau M
	- *asumsi tentang eksentrisitas orbit yang ekstrem**;
    - eksentrisitas orbit yang ekstrem dianggap menurunkan probabilitas kelayakhunian, sehingga planet dengan _e_ di atas angka tertentu (ditentukan oleh luminositas bintang inang) probabilitas layak huninya diberi penalti dan urutannya cederung turun dalam indeks;


### Daftar Isi
```{tableofcontents}
```





![d4c17bfdecec68f5c2dfaa3d87c636ca.png](misc/d4c17bfdecec68f5c2dfaa3d87c636ca.png)






![62fed7446fefc69ad087c21e7cc92834.png](misc/62fed7446fefc69ad087c21e7cc92834.png)