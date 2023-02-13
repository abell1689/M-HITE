# Saran Pengembangan
Sistem pengindeksan HITE dapat dimodifikasi dalam cara yang berhasil mengeluarkan hasil yang unik, berupa daftar indeks dengan urutan berbeda dari daftar indeks hasil evaluasi HITE orisinal. Urutan yang baru ini mengungkap bahwa ada beberapa eksoplanet yang memiliki kemungkinan tinggi untuk bersifat layak huni, namun terlewatkan oleh HITE orisinal. Namun, tentu masih terdapat banyak hal yang bisa ditingkatkan.

## Pembaruan basis data
Seperti yang telah disebutkan pada bagian Limitasi Basis Data di laman Perincian Algoritma, basis data eksoplanet yang ada masih memiliki banyak _gap_. Bagusnya, _gap_ ini semakin lama semakin sedikit dengan terus berkembangnya teknologi pengamatan dan pemodelan.

Sumber data yang digunakan oleh versi HITE termodifikasi ini berasal dari katalog [exoplanets.org](https://exoplanets.org). Katalog tersebut hanya mencakup eksoplanet yang ditemukan pada tahun 2018 ke bawah. Pembaruan dapat dilakukan dengan beralih ke sumber lain yang lebih mutakhir.

### Sekilas tentang bias pada basis data
Bias utama yang memengaruhi riset mengenai eksoplanet saat ini adalah bias observasi. Tipe planet yang paling banyak ditemukan adalah yang memiliki karakteristik yang membuatnya mudah dideteksi oleh teleskop-teleskop pengamat yang telah beroperasi sekarang, yaitu planet-planet dengan: (1) periode orbit yang sangat singkat; (2) radius yang relatif besar; dan (3) orbit yang tidak eksentrik [Kipping & Sandford 2016].

Karena penelitian ini didasarkan pada basis data yang mengalami bias-bias tersebut, secara umum, kesimpulan yang diambil di sini (derajat kelayakhunian berdasarkan urutan serta korelasi kelayakhunian dengan beberapa parameter keplanetan) hanya berlaku terhadap populasi eksoplanet yang ditemukan oleh instrumen-instrumen yang sama, atau dengan karakteristik yang serupa dengan yang telah tercatat di basis data.

Pada hasil evaluasi M‑HITE, jumlah entri yang bernilai tidak nol hanya sekitar 1.3 persen dari keseluruhan yang dievaluasi. Persentase ini mungkin saja lebih besar jika pendeteksian murni bersifat acak (jika tidak ada bias). Penyebabnya adalah karena M-HITE sangat mengutamakan planet _terrestrial_ yang radiusnya relatif kecil, sementara itu keberadaan bias (2) memperkecil kemungkinan planet seperti itu untuk terdeteksi.

Bias ini berhubungan dengan spesifikasi instrumen yang dimiliki teleskop pengamat serta metode-metode pengamatan yang paling banyak digunakan. Karena itu, beroperasinya teleskop-teleskop di masa depan dengan _range_ yang lebih luas akan meringankan pengaruh bias-bias tersebut.

## Faktor-faktor kelayakhunian lain
HITE dan versi modifikasinya ini mendefinisikan kelayakhunian sebatas pada keberadaan permukaan padat dan air. Evaluasi sekilas terhadap keadaan di Bumi mengingatkan terhadap setidaknya dua faktor lain yang menentukan kelayakhunian suatu planet: keberadaan medan magnet dan satelit alami.

Medan geomagnet melindungi Bumi dari radiasi pada ranah frekuensi sinar-X dan UV, serta dari angin Matahari yang merupakan aliran partikel berenergi tinggi yang dapat merusak tatanan kimia pada biomassa. Karena itu, keberadaan medan ini merupakan sebuah keharusan untuk keberlangsungan kehidupan. Medan magnet seperti ini terbentuk ketika fluida yang konvektif dan konduktif mengalir di interior suatu planet (efek dinamo). Momen magnetik suatu planet dapat diperkirakan menggunakan persamaan berikut [Rodrı́guez-Mozos & Moya 2017]:
$$μ=k_1 ρ_0^{1/2} r_0^3 F^{1/3} d$$
dengan $k_1$ sebuah konstanta, $\rho_0$ adalah densitas lapisan konvektif dalam interior planet, $r_0$ adalah radius inti planet (termasuk lapisan konvektif), $F$ adalah rata-rata dari fluks apung (_buoyancy flux_) dalam aliran fluida konvektif, dan $d$ adalah ketebalan lapisan konvektif. Nilai dari parameter-parameter tersebut untuk Bumi didapatkan melalui riset langsung selama puluhan tahun. Untuk mengetahui nilainya untuk planet-planet yang mengorbit bintang lain, akan dibutuhkan perkembangan dalam pemodelan interior planet.

Sementara itu, keberadaan Bulan sebagai satelit alami Bumi berperan dalam menstabilkan kemiringan sudut dari sumbu rotasi Bumi serta memperpelan laju rotasinya. Keduanya sama-sama memiliki efek mengerem laju perubahan iklim, yang jika terlalu cepat akan memperkecil kemungkinan makhluk hidup bisa beradaptasi dan bertahan hidup [Waltham 2004]. Belum ada bulan eksoplanet yang terdeteksi sampai saat ini. Namun secara teori, pendeteksiannya dapat dilakukan menggunakan teleskop-teleskop pengamat yang telah dan akan beroperasi dalam waktu dekat ini, seperti _Spitzer_ dan _James Webb Space Telescope_, terutama untuk bulan dengan rasio radius bulan-planet lebih dari 0.272 (rasio radius Bulan-Bumi) [Kane 2017].

## Riset terbaru tentang albedo eksoplanet
HITE modifikasi yang dihasilkan pada karya ilmiah ini hanya dapat digunakan untuk mengevaluasi eksoplanet dengan bintang inang tipe G dan M. Pembaruan lebih lanjut dengan mengikutkan riset terbaru tentang albedo eksoplanet perlu dilakukan supaya daftar prioritas yang dihasilkan HITE dapat mengikutkan seluruh eksoplanet yang diketahui.