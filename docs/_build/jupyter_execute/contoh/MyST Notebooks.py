#!/usr/bin/env python
# coding: utf-8

# # Penjelasan Kode
# 
# Jupyter Book also lets you write text-based notebooks using MyST Markdown.
# See [the Notebooks with MyST Markdown documentation](https://jupyterbook.org/file-types/myst-notebooks.html) for more detailed instructions.
# This page shows off a notebook written in MyST Markdown.
# 
# ## An example cell
# 
# With MyST Markdown, you can define code cells with a directive like so:

# In[1]:


print(2 + 2)


# When your book is built, the contents of any `{code-cell}` blocks will be
# executed with your default Jupyter kernel, and their outputs will be displayed
# in-line with the rest of your content.
# 
# ```{seealso}
# Jupyter Book uses [Jupytext](https://jupytext.readthedocs.io/en/latest/) to convert text-based files to notebooks, and can support [many other text-based notebook files](https://jupyterbook.org/file-types/jupytext.html).
# ```
# 
# ## Create a notebook with MyST Markdown
# 
# MyST Markdown notebooks are defined by two things:
# 
# 1. YAML metadata that is needed to understand if / how it should convert text files to notebooks (including information about the kernel needed).
#    See the YAML at the top of this page for example.
# 2. The presence of `{code-cell}` directives, which will be executed with your book.
# 
# That's all that is needed to get started!
# 
# ## Quickly add YAML metadata for MyST Notebooks
# 
# If you have a markdown file and you'd like to quickly add YAML metadata to it, so that Jupyter Book will treat it as a MyST Markdown Notebook, run the following command:
# 
# ```
# jupyter-book myst init path/to/markdownfile.md
# ```
# 
# 
# 
# # Pendahuluan
# 
# Mengantisipasi penggunaan berkas lain selain yang disediakan
# 
# #      1.      Instalasi
# 
# Program ini menggunakan bahasa pemrograman Python dengan IDE Jupyter Notebook. Jupyter Notebook dapat diperoleh sebagai bagian dari Anaconda.
# 
# #      2.      Program
# 
# ## a.   Mengimpor library yang dibutuhkan
# 
# pandas untuk
# 
# math untuk
# 
# ## b.  Mendefinisikan konstanta
# 
# ## c.    Mendefinisikan fungsi (akan dijelaskan lebih lanjut saat fungsi digunakan)
# 
# ## d.  Mengimpor data eksoplanet dari berkas CSV
# 
# (Berkas yang digunakan bisa juga berupa tipe berkas lainnya XLS, XLSX, dll. Gunakan perintah pandas yang sesuai)
# 
# exo = pd.read_csv (r’[alamat berkas data eksoplanet]’) membaca berkas dan menyalin datanya ke dalam sebuah objek dataframe dengan nama exo
# 
# dtype = {“judul kolom” : “str”} menspesifikasikan tipe data pada kolom yang mempunyai tipe data bervariasi (_mixed types_), mencegah galat yang akan ditandai oleh pesan seperti berikut:
# ![sss](Pasted%20image%2020220427005640.png)
# Jika menerima pesan galat seperti di atas, spesifikasikan tipe data dari kolom-kolom yang tertera pada Columns (_) have mixed types.  (dtype bisa berupa “str”, int, dll.)
# 
# exo = exo.set_index(“NAME”) mengatur agar kolom dengan judul ‘NAME’ pada berkas CSV (dan pada dataframe exo) digunakan sebagai indeks baris untuk keseluruhan tabel. Jadi massa dari eksoplanet CoRoT-1 b, misalnya, bisa diperoleh dari dataframe exo dengan perintah exo.loc[CoRoT-1 b, “MASS”]; akan berguna saat [mengambil data planet individu dari dataframe exo](#_Mengambil_data_planet).
# 
# ![](Pasted%20image%2020220427005755.png)
# 
# drop = False supaya kolom dengan judul NAME tersebut tidak dihapus dari dataframe exo setelah dijadikan indeks baris.
# 
# exoList = pd.DataFrame(exo, columns=['NAME']) membuat dataframe baru yang hanya berisikan kolom ‘NAME’.
# 
# exoList = exoList['NAME'].values.tolist() mengubah dataframe exoList menjadi list; akan digunakan sebagai ‘daftar presensi’ planet saat menghitung indeks habitabilitas.
# 
# ## e.   Mengimpor daftar batas-batas Zeng-Sasselov dari berkas CSV
# 
# zs = pd.read_csv (r’[alamat berkas data batas-batas Zeng-Sasselov]’) membaca berkas dan menyalin datanya ke dalam sebuah objek dataframe dengan nama zs.
# 
# zs = zs.set_index(“SORT”) mengatur agar kolom dengan judul ‘SORT’ pada berkas CSV (dan pada dataframe zs) digunakan sebagai indeks baris untuk keseluruhan tabel; digunakan dalam fungsi untuk menghitung probabilitas sifat terestrial planet (fprocky).
# 
# zsList = pd.DataFrame(zs, columns=['SORT]) membuat dataframe baru yang hanya berisikan kolom ‘SORT’.
# 
# zsList = zsList['SORT'].values.tolist() mengubah dataframe zsList ke dalam bentuk list; akan digunakan pada _loop_ pencarian batas-batas Zeng-Sasselov.
# 
# ## f.   Penghitungan nilai indeks kelayakhunian
# 
# habIndexList = [] membuat daftar kosong untuk menampung daftar nilai indeks kelayakhunian dari semua planet yang akan dievaluasi.
# 
# for exoName in exoList: memulai _loop_ yang akan mengisi _value_ dari variabel exoName dengan satu nama planet dari exoList, mengumpulkan data-data planet tersebut dari dataframe exo, kemudian menghitung indeks kelayakhuniannya. Setelah itu, variabel exoName akan diisi dengan nama planet berikutnya, dst.
# 
# ### Mengambil data planet individu dari pandas dataframe exo
# 
# ·         _variabel_ = exo.loc [exoName, “_nama_ _kolom_”] digunakan untuk mengambil data dari sel dataframe exo.
# 
# ·         Misal, rStar = exo.loc [exoName, rStar] digunakan untuk mengambil data radius bintang inang dari planet yang namanya sedang mengisi _value_ exoName pada iterasi tersebut.
# 
# ·         **Konversi satuan ke dalam satuan SI jika dibutuhkan**        
# 
# ·        
# 
# if math.isnan(rPlanet) == 1:
# 
#     depth = exo.loc[exoName, "DEPTH"]
# 
#     rPlanet = math.sqrt(depth)*rStar
# 
#  
# 
#   
# 
# Jika kolom “R” (radius planet) untuk suatu planet bukan berupa angka (karena kosong, misalnya), hitung radius planet dari _transit depth_ (kolom “DEPTH”) dan radius bintang inang.
# 
# if math.isnan(mPlanet) == 1:
# 
#         if rPlanet/REARTH <= 1:
# 
#             mPlanet = ((rPlanet/REARTH)**3.268)*MEARTH
# 
#         else rPlanet/REARTH > 1:
# 
#             mPlanet = ((rPlanet/REARTH)**3.65)*MEARTH
# 
# Catatan tentang _transit depth_: Saat planet transit di depan bintang inangnya, kecerlangan bintang yang teramati dari Bumi akan berkurang; fraksi antara kecerlangan awal dan kecerlangan saat transit disebut _transit depth_; pengurangan kecerlangan tersebut berkaitan dengan radius relatif antara planet dan bintang inang, sehingga radius planet dapat diperoleh jika radius bintang diketahui.
# 
# ·          
# 
# 
# M_p/M_⊕ ={■((R_p/R_⊕ )^3,268&,&R_p≤1R_⊕,@(R_p/R_⊕ )^3,65&,&R_p>1R_⊕.)┤  
# 
#  = massa planet
# 
# = massa Bumi
# 
#  = radius planet
# 
# = radius Bumi
# 
# Jika kolom “M” (massa planet) untuk suatu planet bukan berupa angka (karena kosong, misalnya), hitung massa planet menggunakan _scaling law_ berikut (Sotin _et al_. 2007 dalam  Barnes _et al_. 2015):
# 
#  
# 
# ### Menentukan batas atas dan batas bawah F_OLR
# 
# Asumsi:
# 
# fMin adalah batas fluks minimum yang diterima oleh planet sehingga air dapat bertahan di permukaannya dalam fase cair. Nilainya didapat dari pemodelan proses konvektif-radiatif di atmosfer dan dianggap sama untuk planet dengan 0,1 hingga 5 kali massa Bumi (67 W/m2). Dalam program ini, nilainya dianggap sama untuk semua planet (karena planet dengan massa lebih dari 5 kali massa Bumi hampir pasti bernilai indeks nol anyway)
# 
# fMax = A*SB*(LH2O/(RGAS*math.log(pStar*math.sqrt(K0/(2*PLINE*surfGrav)))))**4
# 
# fMax adalah batas fluks maksimum, pasangan dari fMin. Nilainya didapat dari persamaan berikut:  
# 
# F_max=Bσ(l/2R"ln" (P_* √(κP_0 g)) )^4
# 
# , dengan P_*=P_ref e^(l/(RT_ref )). 
# 
# Keterangan lebih lanjut bisa dilihat di Pierrehumbert (2010) dan Barnes _et al_. (2015).
# 
# pRocky = fpRocky(mPlanet, rPlanet) menghitung probabilitas sifat _terrestrial_ menggunakan fungsi fpRocky.
# 
# #### Penjelasan fungsi fpRocky
# 
# def fpRocky (mPlanet,rPlanet): masukan dari fungsi ini adalah massa planet dan radius planet
# 
# mPlanet = mPlanet/MEARTH & rPlanet = rPlanet/REARTH mengonversi satuan ke dalam kelipatan dari massa Bumi/radius Bumi
# 
# fpRocky menghitung probabilitas keterestrialan  menurut persamaan berikut:
# 
# T_(m_p ) "(" R_p ")"={■("1" ,&"untuk"  R_p≤μ_(1,m_p )@"exp" (-"1" /"2"  ((R_p-μ_(1,m_p ))/σ_(m_p ) )^2 ),&"untuk"  μ_(1,m_p )<R_p<μ_(2,m_p )@"0" ,&"untuk"  μ_(2,m_p )≤R_p "," )┤
# 
# Nilai dari μ_1, μ_2,  σ bergantung pada m_p (massa planet) sehingga harus dihitung untuk setiap planet.
# 
# μ_1 adalah radius minimal dari
# 
# pRocky = 0 mendefinisikan variabel pRocky
# 
# ### Menghitung probabilitas sifat _terrestrial_
# 
# ### Menentukan batas-batas albedo
# 
# •             khusus untuk planet dengan tipe bintang inang M atau G ### Menghitung F_OLR
# 
# ## c. Keluaran
# 
# # 3. Pengolahan Data
