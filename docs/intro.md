# Pengenalan
## Apa itu HITE?
HITE (_Habitability Index for Transiting Exoplanets_) adalah indeks yang mengurutkan eksoplanet berdasarkan probabilitas kelayakhunian/habitabilitasnya. Probabilitas ini ditentukan oleh program HITE. Program ini mengambil beberapa parameter fisis yang diketahui mengenai suatu eksoplanet, kemudian menggunakannya untuk menghitung kemungkinan planet tersebut: a) mempunyai permukaan padat, dan b) memiliki air berfase cair di permukaannya.

:::{admonition} Catatan tentang lisensi
HITE disusun oleh [Rory Barnes](https://github.com/RoryBarnes/HITE) dari University of Washington. Program HITE dibagikan dengan lisensi GNU General Public License v3.0 yang memperbolehkan penggunaan dan perubahan terhadap program tersebut secara bebas. Info lebih lanjut tentang lisensinya bisa diperoleh [di sini](https://github.com/RoryBarnes/HITE/blob/master/LICENSE). Sesuai ketentuan lisensi tersebut, modifikasi dari program HITE ini juga dibagikan dengan lisensi yang sama.
:::

## Tentang M-HITE
Program yang cara kerjanya akan dijelaskan di sini adalah HITE Termodifikasi/_Modified HITE_ (M-HITE). Berikut adalah modifikasi yang telah dilakukan terhadap program HITE sehingga menjadi M-HITE:
1) program telah ditulis ulang, dari C ke Python;
2) besaran-besaran yang pada HITE orisinal dihitung dari variabel observasi (seperti radius planet yang dihitung dari [transit]), pada M-HITE tidak dihitung, tetapi langsung diambil dari basis data [exoplanets.org](exoplanets.org). Hal ini memungkinkan M-HITE untuk mengevaluasi probabilitas kelayakhunian dari planet-planet yang ditemukan melalui metode lain selain metode transit;
3) rentang parameter eksentrisitas (_e_) dan albedo planet (_A_) yang digunakan untuk menghitung probabilitas kelayakhunian _H (e, A)_ tidak disamakan untuk semua planet, tapi diganti dengan data masing-masing planet yang diambil dari  [exoplanets.org](exoplanets.org) beserta rentang ketidakpastiannya;
4) 
5) zeng sasselov


## Daftar Isi
```{tableofcontents}
```





![d4c17bfdecec68f5c2dfaa3d87c636ca.png](d4c17bfdecec68f5c2dfaa3d87c636ca.png)






![62fed7446fefc69ad087c21e7cc92834.png](62fed7446fefc69ad087c21e7cc92834.png)