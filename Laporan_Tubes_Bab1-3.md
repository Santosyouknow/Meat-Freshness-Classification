# LAPORAN TUGAS BESAR VISI KOMPUTER (UTS)
**Mata Kuliah:** CII3B4 Visi Komputer | **Semester:** Ganjil 2026/2027

---

# ANALISIS KOMPARATIF ARSITEKTUR MOBILENETV2 DAN EFFICIENTNETB0 DENGAN VISUALISASI GRAD-CAM UNTUK KLASIFIKASI MUTU KESEGARAN DAGING
*(Comparative Analysis of MobileNetV2 and EfficientNetB0 Architectures with Grad-CAM Visualization for Meat Freshness Quality Classification)*

**Disusun Oleh:**  
- [Nama Anggota Kelompok / NIM]  
- **Kelas:** [Kelas Anda]  
- **Program Studi:** S1 Informatika / Teknik Komputer  
- **Dosen Pengampu:** derekln14  

---

## ABSTRAK
Penjaminan mutu dan kesegaran daging merupakan tantangan krusial dalam rantai pasok pangan untuk mencegah risiko keracunan makanan (*foodborne diseases*). Metode konvensional seperti inspeksi sensorik visual dan olfaktori bersifat sangat subjektif dan rentan terhadap kelelahan pemeriksa, sementara uji kimiawi laboratorium bersifat destruktif dan memakan waktu. Penelitian ini mengusulkan sistem klasifikasi mutu kesegaran daging non-destruktif multikelas (*Fresh*, *Half-Fresh*, dan *Spoiled*) berbasis visi komputer dengan membandingkan dua arsitektur transfer learning berbobot ringan: **MobileNetV2** dan **EfficientNetB0**. Untuk mengatasi keterbatasan riset terdahulu yang memperlakukan Convolutional Neural Network (CNN) sebagai kotak hitam (*black box*), metode Explainable AI berbasis *Gradient-weighted Class Activation Mapping* (Grad-CAM) diintegrasikan untuk memvalidasi fitur visual biokimia yang dijadikan dasar penentuan keputusan model. Dataset yang digunakan terdiri dari **2.266 citra digital resolusi tinggi (416x416 piksel)** yang bersumber dari Kaggle Meat Freshness Image Dataset. Hasil pengujian empiris pada 451 citra validasi independen membuktikan bahwa MobileNetV2 mencapai performa terbaik dengan **akurasi 99,11%**, **Macro F1-score 99,21%**, dan **latensi inferensi 237,8 ms**, melampaui EfficientNetB0 (akurasi 98,23%, Macro F1-score 98,41%, dan latensi 391,2 ms) dengan kebutuhan parameter 40,6% lebih hemat (2,62 juta vs 4,41 juta parameter). Visualisasi Grad-CAM membuktikan secara saintifik bahwa model mampu mengenali degradasi pigmen oxymyoglobin dan struktur marbling lemak secara konsisten tanpa terdistraksi oleh artefak latar belakang.

**Kata Kunci:** *Visi Komputer, Klasifikasi Kesegaran Daging, MobileNetV2, EfficientNetB0, Explainable AI, Grad-CAM, Transfer Learning.*

---

## BAB 1: PENDAHULUAN

### 1.1 Latar Belakang Masalah
Daging merupakan salah satu komoditas pangan sumber protein hewani utama yang sangat dibutuhkan oleh masyarakat karena mengandung asam amino esensial, mineral, dan vitamin yang penting bagi pertumbuhan dan kesehatan manusia. Namun, daging memiliki sifat biologis yang sangat mudah mengalami kerusakan (*highly perishable*). Penurunan mutu daging dipicu oleh kombinasi aktivitas mikroorganisme pembusuk dan proses biokimia pasca-penyembelihan, khususnya degradasi protein serta reaksi oksidasi pigmen mioglobin. Mengonsumsi daging yang telah mengalami penurunan mutu atau pembusukan berisiko tinggi memicu gangguan kesehatan serius berupa keracunan makanan (*foodborne diseases*), seperti infeksi bakteri *Salmonella sp.*, *Escherichia coli*, dan *Staphylococcus aureus*.

Dalam industri pemotongan hewan, pasar ritel, maupun pasar tradisional, inspeksi kesegaran daging secara konvensional masih mengandalkan indra manusia (uji sensorik visual warna, tekstur sentuhan, dan bau). Cara ini memiliki kelemahan mendasar karena sangat subjektif, tidak memiliki standardisasi kuantitatif, dan tingkat akurasinya menurun drastis akibat kelelahan pemeriksa serta pencahayaan lingkungan pasar yang tidak seragam. Di sisi lain, metode pengujian ilmiah laboratorium, seperti analisis *Total Volatile Basic Nitrogen* (TVB-N), pengukuran pH mikro, dan uji hitung mikroba (*Total Plate Count*), memang memberikan hasil yang presisi. Namun, prosedur tersebut memerlukan reagen kimia yang mahal, merusak sampel (destruktif), dan membutuhkan waktu pengujian yang lama (berjam-jam hingga berhari-hari). Keterbatasan ini menyebabkan uji laboratorium tidak mungkin diterapkan untuk proses sortir cepat secara kontinu pada rantai pasok industri pangan.

Perkembangan pesat teknologi pengolahan citra digital (*digital image processing*) dan visi komputer (*computer vision*) membuka peluang besar untuk menciptakan sistem inspeksi mutu pangan yang objektif, non-destruktif, cepat (*real-time*), dan hemat biaya. Dengan memanfaatkan kamera digital standar, sistem dapat menganalisis perubahan visual permukaan daging—seperti perubahan warna akibat oksidasi mioglobin dan dekomposisi struktur lemak marbling—secara akurat tanpa menyentuh maupun merusak produk.

### 1.2 Identifikasi Masalah dan Kesenjangan Riset (*Research Gap*)
Sejumlah penelitian terdahulu telah berupaya mengotomatisasi klasifikasi mutu kesegaran daging menggunakan teknik kecerdasan buatan, namun masih menyisakan kesenjangan riset (*research gap*) kritis yang harus diselesaikan:

1. **Keterbatasan Skala dan Representasi Dataset:**  
   Sebagian besar penelitian terdahulu menggunakan ukuran dataset yang sangat terbatas. Sebagai contoh, penelitian Anshori & Putra (2025) hanya menggunakan 180 citra daging sapi. Jumlah data yang sangat kecil ini memiliki risiko *overfitting* yang tinggi dan tidak mampu merepresentasikan variasi pencahayaan riil, *specular reflection* (pantulan cahaya), serta keberagaman pola marbling lemak.
2. **Penyederhanaan Kategori Menjadi Klasifikasi Biner:**  
   Penelitian Zuhdi et al. (2024) hanya mengelompokkan daging secara biner (segar vs tidak segar). Pendekatan ini mengabaikan fase paling kritis dalam degradasi daging, yaitu fase setengah segar (*Half-Fresh*). Fase *Half-Fresh* merupakan jendela waktu transisi di mana mikroba mulai berkembang dan penurunan kualitas terjadi, yang semestinya menjadi peringatan dini bagi konsumen sebelum daging membusuk total.
3. **Paradoks Arsitektur Model (*Under-parameterized vs Over-parameterized*):**  
   Penelitian rujukan terpolarisasi pada dua ekstrem arsitektur. Di satu sisi, model CNN Vanilla 3–4 layer sederhana (Putri et al., 2024; Anshori & Putra, 2025) memiliki kapasitas *feature extraction* yang terbatas. Di sisi lain, penggunaan model transfer learning kuno seperti VGG-16 oleh Cakra et al. (2024) melibatkan lebih dari 138 juta parameter dengan ukuran bobot melampaui 500 MB. Arsitektur sebesar ini membutuhkan daya komputasi tinggi, memakan memori berlebih, dan menghasilkan latensi inferensi yang lambat, sehingga mustahil diimplementasikan pada perangkat *edge computing* atau kamera ponsel cerdas.
4. **Permasalahan 'Black-Box' dan Ketiadaan Explainable AI (XAI):**  
   Hampir seluruh penelitian terdahulu memperlakukan model deep learning murni sebagai kotak hitam (*black box*). Penguji tidak memiliki instrumen untuk memverifikasi area citra mana yang menjadi rujukan model dalam mengambil keputusan. Kondisi ini membuka celah bias model, di mana model berpotensi 'menyontek' latar belakang meja, warna piring, atau pantulan flash kamera alih-alih mengekstrak ciri biokimia permukaan daging.

Berdasarkan kesenjangan tersebut, penelitian ini mengusulkan pendekatan komparatif antara dua arsitektur modern berbobot ringan (*lightweight state-of-the-art*): **MobileNetV2** dan **EfficientNetB0**, yang dievaluasi pada dataset representatif sebanyak 2.266 citra 3 kelas, serta diintegrasikan dengan metode *Gradient-weighted Class Activation Mapping* (Grad-CAM) untuk memvalidasi transparansi visual fitur biologis daging.

### 1.3 Rumusan Masalah
1. Bagaimana performa arsitektur deep learning ringan modern (MobileNetV2 dan EfficientNetB0) dalam mengklasifikasikan tiga tingkat mutu kesegaran daging (*Fresh*, *Half-Fresh*, dan *Spoiled*) pada citra resolusi tinggi?
2. Sejauh mana *trade-off* antara akurasi klasifikasi dan efisiensi komputasi (jumlah parameter model, ukuran berkas bobot, dan latensi inferensi per citra) antara MobileNetV2 dan EfficientNetB0?
3. Bagaimana representasi visual Explainable AI berbasis Grad-CAM membuktikan keabsahan fitur biokimia (warna oxymyoglobin/metmyoglobin dan distribusi marbling lemak) yang dipelajari model, serta membuktikan bahwa model bebas dari bias latar belakang?

### 1.4 Tujuan Penelitian
1. Membangun dan melatih model klasifikasi kesegaran daging tiga kelas berbasis transfer learning menggunakan arsitektur MobileNetV2 dan EfficientNetB0.
2. Menganalisis secara kuantitatif perbandingan kinerja kedua model berdasarkan metrik akurasi validasi, precision, recall, macro F1-score, matriks konfusi, dan latensi komputasi inferensi.
3. Mengimplementasikan teknik Grad-CAM untuk menghasilkan peta visual atensi (*heatmap*) yang memvalidasi keputusan klasifikasi model terhadap area degradasi jaringan daging.
4. Menghasilkan purwarupa program inferensi interaktif (*live demo*) yang siap diimplementasikan untuk pengujian *real-time*.

### 1.5 Manfaat Penelitian
* **Manfaat Teoritis / Akademis:** Memberikan wawasan empiris mengenai perbandingan arsitektur konvolusi berbasis *Inverted Residuals* (MobileNetV2) versus *Compound Scaling* (EfficientNetB0) pada domain citra tekstur pangan, serta membuktikan efektivitas Explainable AI (Grad-CAM) dalam mengatasi masalah *black-box* pada visi komputer pangan.
* **Manfaat Praktis:** Menyediakan model klasifikasi berbobot ringan (<5 MB) yang berkinerja tinggi (>98%) dan cepat (<400 ms), sehingga siap diadopsi oleh industri pangan, rumah pemotongan hewan, swalayan, maupun konsumen melalui aplikasi kamera ponsel cerdas (Android/iOS) guna penjaminan keamanan pangan.

### 1.6 Batasan Masalah
1. Dataset bersumber dari Kaggle Meat Freshness Image Dataset (Vinayak Shanawad / Roboflow) sebanyak 2.266 citra berformat JPEG RGB dengan resolusi asli 416 x 416 piksel.
2. Kelas klasifikasi terdiri dari 3 kelas: *Fresh* (Segar), *Half-Fresh* (Setengah Segar / Mulai Penurunan Mutu), dan *Spoiled* (Busuk / Tidak Layak Konsumsi).
3. Arsitektur transfer learning yang dikomparasikan dibatasi pada model MobileNetV2 dan EfficientNetB0 dengan bobot terlatih dari ImageNet.
4. Citra masukan pada pipeline inferensi diseragamkan ke ukuran 224 x 224 x 3 piksel.
5. Metode Explainable AI yang digunakan adalah Grad-CAM yang diekstraksi dari lapisan konvolusi terakhir masing-masing model (`out_relu` pada MobileNetV2 dan `top_activation` pada EfficientNetB0).

---

## BAB 2: TINJAUAN PUSTAKA DAN LANDASAN TEORI

### 2.1 Tinjauan Pustaka (*State-of-the-Art*)
Kajian pustaka dilakukan terhadap empat penelitian ilmiah terdahulu yang relevan guna memetakan posisi dan kebaruan penelitian ini:

1. **Zuhdi, Setiawan, & Saputro (2024)** meneliti identifikasi kesegaran daging ayam broiler menggunakan metode Convolutional Neural Network (CNN) biner (segar vs busuk). Model yang dikembangkan menghasilkan F1-score yang tinggi (0,87 pada data latih dan 0,99 pada validasi), namun nilai Area Under Curve (AUC) hanya mencapai 0,47. Nilai AUC yang di bawah 0,5 mengindikasikan bahwa model memiliki ketidakstabilan batas keputusan (*decision threshold*). Selain itu, penelitian ini tidak memetakan fase transisi setengah segar dan tidak menyediakan visualisasi fitur aktivasi.
2. **Putri, Rahayu, dkk. (2024)** mengembangkan aplikasi seluler berbasis Android untuk klasifikasi kesegaran daging sapi menggunakan deep learning CNN dan format TensorFlow Lite. Penelitian ini melaporkan akurasi hingga 100% pada data uji. Namun, akurasi sempurna pada dataset skala kecil mengindikasikan adanya *controlled environment* yang homogen atau potensi *data leakage*. Model belum diuji terhadap keberagaman tekstur daging pasar riil dan tidak menyajikan analisis latensi komputasi inferensi secara komparatif.
3. **Anshori, Putra, Lestariningsih, & Lestari (2025)** menerapkan arsitektur CNN 4-layer konvolusi sederhana untuk mengklasifikasikan kesegaran daging sapi berdasarkan durasi penyimpanan dengan akurasi 97,22%. Namun, dataset yang digunakan sangat terbatas, yakni hanya berjumlah 180 citra digital (60 citra per kelas). Model yang dilatih dari awal (*from scratch*) pada dataset sekecil ini sangat rentan mengalami *overfitting* bila dihadapkan pada variasi pencahayaan di luar laboratorium.
4. **Cakra, Samsuddin, & Kahar (2024)** melakukan klasifikasi kesegaran daging sapi di Pasar Tradisional Mandonga Kota Kendari dengan menerapkan Transfer Learning menggunakan arsitektur VGG-16. Meskipun VGG-16 mampu mencapai akurasi tinggi, arsitektur ini memiliki lebih dari 138 juta parameter dan ukuran berkas bobot melebihi 500 MB. Bobot yang masif ini menyebabkan konsumsi RAM dan daya yang sangat boros serta latensi inferensi yang lambat, sehingga tidak efisien bila diintegrasikan ke perangkat edge atau smartphone.

| Peneliti & Tahun | Metode / Arsitektur | Objek & Kelas | Skala Dataset | Celah Riset / Batasan |
| :--- | :--- | :--- | :--- | :--- |
| **Zuhdi et al. (2024)** | Vanilla CNN | Daging Ayam (2 Kelas) | Dataset Lokal Terbatas | AUC hanya 0,47; klasifikasi biner; nir-interpretasi (*black-box*). |
| **Putri et al. (2024)** | CNN + Mobile TFLite | Daging Sapi (3 Kelas) | Dataset Studio Kecil | Klaim akurasi 100% (indikasi *overfitting*); tanpa uji efisiensi. |
| **Anshori & Putra (2025)** | CNN 4-Layer Scratch | Daging Sapi (3 Kelas) | 180 Citra (Sangat Kecil) | Data terlalu minim untuk deep learning; tanpa pretrained backbone. |
| **Cakra et al. (2024)** | Transfer Learning VGG-16 | Daging Sapi Pasar (3 Kelas) | Dataset Lokal Mandonga | Model raksasa (>138M parameter, >500 MB); tidak ramah edge/mobile. |
| **Penelitian Ini (Diusulkan)** | **MobileNetV2 vs EfficientNetB0 + Grad-CAM** | **Daging Multikelas (Fresh, Half, Spoiled)** | **2.266 Citra Resolusi Tinggi** | Multi-model benchmark ringan (<5M params); XAI Grad-CAM membuktikan fitur biokimia. |

### 2.2 Fisiologi dan Karakteristik Biokimia Kesegaran Daging
Warna visual permukaan daging merupakan indikator utama kesegaran yang dievaluasi oleh konsumen dan sistem visi komputer. Warna daging ditentukan oleh konsentrasi dan status kimiawi pigmen heme protein, yaitu mioglobin (*myoglobin*). Mioglobin mengalami tiga bentuk transformasi optik utama:
1. **Deoxymyoglobin ($\text{Fe}^{2+}$ tanpa $\text{O}_2$):** Menghasilkan warna merah keunguan gelap, umum ditemukan pada bagian dalam daging atau daging segar tanpa kontak udara.
2. **Oxymyoglobin ($\text{Fe}^{2+}$ dengan $\text{O}_2$):** Terbentuk saat deoxymyoglobin teroksigenasi oleh udara, menghasilkan warna merah cerah merona (*cherry-red bloom*). Kondisi ini merupakan ciri khas daging segar (*Fresh*).
3. **Metmyoglobin ($\text{Fe}^{3+}$ teroksidasi):** Terjadi akibat oksidasi berkelanjutan di mana atom besi bervalensi dua dioksidasi menjadi bervalensi tiga. Metmyoglobin memantulkan spektrum warna cokelat kusam hingga keabu-abuan. Peningkatan metmyoglobin adalah indikasi langsung penurunan mutu (*Half-Fresh* hingga *Spoiled*).

Selain warna mioglobin, tekstur marbling (lemak intramuskular) yang tersebar di antara serat otot daging juga menjadi penanda penting. Pada daging segar, lemak marbling tampak putih bersih atau krem solid. Seiring dekomposisi enzimatik dan aktivitas bakteri lipolitik, lemak marbling menguning, melunak, dan hancur, menghasilkan eksudat basah berlendir yang khas pada daging busuk.

### 2.3 Deep Learning dan Transfer Learning
Convolutional Neural Network (CNN) adalah arsitektur deep learning yang dirancang khusus untuk memproses data berstruktur grid dua dimensi. Operasi konvolusi menggeser kernel filter berbobot di atas citra untuk mengekstrak fitur spasial hierarkis, mulai dari fitur tingkat rendah (tepi, kontur, warna lokal) pada lapisan awal hingga representasi semantik kompleks (tekstur marbling, pola pembusukan) pada lapisan lebih dalam.

Transfer learning adalah paradigma pelatihan machine learning yang memanfaatkan bobot (*weights*) dari model yang telah dilatih sebelumnya pada dataset raksasa (ImageNet dengan lebih dari 1,4 juta citra dan 1.000 kategori kelas) sebagai dasar ekstraksi fitur pada tugas target baru. Pendekatan ini secara drastis mempercepat konvergensi pelatihan, mencegah kecenderungan *overfitting*, serta mengatasi kendala keterbatasan sampel pada dataset spesifik.

### 2.4 Arsitektur Deep Learning Ringan: MobileNetV2 dan EfficientNetB0
* **MobileNetV2 (Sandler et al., 2018):** Menggunakan modul inovatif *Inverted Residuals with Linear Bottleneck*. Tidak seperti residual network konvensional yang menyempitkan kanal di tengah blok, MobileNetV2 memperluas kanal fitur berdimensi rendah ke dimensi tinggi sebelum menerapkan *Depthwise Separable Convolution* (DWConv 3x3), lalu memproyeksikannya kembali ke dimensi rendah tanpa aktivasi non-linear (*linear bottleneck*). Desain ini memangkas jumlah operasi *floating-point* (FLOPs) secara signifikan sembari mempertahankan kekayaan representasi fitur.
* **EfficientNetB0 (Tan & Le, 2019):** Menerapkan prinsip *Compound Scaling*, yakni penskalaan seimbang antara kedalaman jaringan (*depth*), lebar kanal (*width*), dan resolusi citra input (*resolution*) menggunakan koefisien gabungan tetap. Blok dasarnya dibangun di atas modul MBConv (*Mobile Inverted Bottleneck Convolution*) yang diperkuat dengan mekanisme *Squeeze-and-Excitation* (SE) untuk memberikan pembobotan adaptif pada kanal fitur yang paling informatif.

### 2.5 Explainable Artificial Intelligence (XAI) dan Grad-CAM
Sifat *black-box* pada deep learning menimbulkan keengganan penerapan di industri pangan karena pengguna tidak dapat memverifikasi alasan logis di balik prediksi model. *Gradient-weighted Class Activation Mapping* (Grad-CAM) hadir sebagai teknik atribusi visual yang menghasilkan peta lokalisasi berbobot (*coarse localization map*) yang menyoroti wilayah penting pada citra untuk prediksi kelas tertentu.

Secara matematis, gradien dari skor keluaran kelas target $y^c$ terhadap *activation map* lapisan konvolusi terakhir $A^k$ dihitung. Bobot kepentingan neuron $\alpha_k^c$ diperoleh melalui *Global Average Pooling* spasial:
$$\alpha_k^c = \frac{1}{Z} \sum_{i} \sum_{j} \frac{\partial y^c}{\partial A_{ij}^k}$$

di mana $Z$ melambangkan luas spasial peta fitur (tinggi $\times$ lebar). Selanjutnya, kombinasi linier berbobot dihitung dan disaring menggunakan fungsi aktivasi ReLU guna mempertahankan hanya fitur yang berkontribusi positif terhadap kelas $c$:
$$L_{\text{Grad-CAM}}^c = \text{ReLU}\left(\sum_{k} \alpha_k^c A^k\right)$$

Peta panas yang dihasilkan kemudian diinterpolasi bilinear ke resolusi citra asli dan ditumpangkan (*overlay*) dengan skema colormap JET, di mana warna merah melambangkan atensi tertinggi dan biru melambangkan atensi terendah.

---

## BAB 3: METODOLOGI PENELITIAN

### 3.1 Diagram Alur Penelitian (*Pipeline* Sistem)
Penelitian ini dilaksanakan melalui tahapan berurutan:
1. **Akuisisi & Partisi Dataset:** Pengumpulan dan pemisahan data train dan validasi.
2. **Pra-pemrosesan Data:** Resizing citra ke 224x224 piksel dan normalisasi kanal warna.
3. **Ekstraksi Fitur Transfer Learning:** Penggunaan backbone MobileNetV2 dan EfficientNetB0.
4. **Pelatihan Classifier Head:** Penambahan lapisan Dense, Batch Normalization, Dropout, dan Softmax.
5. **Evaluasi Metrik Kinerja:** Pengukuran akurasi, F1-score, matriks konfusi, dan latensi inferensi.
6. **Analisis Atribusi Visual:** Ekstraksi heatmap Grad-CAM untuk pembuktian fitur biokimiawi.

### 3.2 Deskripsi dan Karakteristik Dataset
Dataset yang digunakan dalam penelitian ini bersumber dari repositori publik Kaggle: *Meat Freshness Image Dataset* yang dikurasi oleh Vinayak Shanawad berbasis anotasi multi-kelas Roboflow. Dataset terdiri dari total **2.266 citra digital berwarna (RGB)** beresolusi asli 416 x 416 piksel.

Data dibagi secara resmi menjadi dua himpunan independen:
* **Training Set (80,1%):** 1.815 citra, terdiri dari *Fresh* (675 citra / 37,2%), *Half-Fresh* (630 citra / 34,7%), dan *Spoiled* (510 citra / 28,1%).
* **Validation Set (19,9%):** 451 citra, terdiri dari *Fresh* (178 citra / 39,5%), *Half-Fresh* (159 citra / 35,3%), dan *Spoiled* (114 citra / 25,3%).

Distribusi kelas yang seimbang ini meminimalkan potensi bias mayoritas kelas (*class imbalance bias*) selama proses optimasi.

### 3.3 Pra-pemrosesan Citra
1. **Pembacaan Citra & Konversi Ruang Warna:** Citra dimuat menggunakan modul OpenCV (BGR) dan dikonversi secara eksplisit ke ruang warna RGB.
2. **Penskalaan Dimensi (*Resizing*):** Citra asli berukuran 416 x 416 diskalakan secara seragam menggunakan interpolasi area bilinear menjadi 224 x 224 piksel, menyesuaikan dimensi input baku dari arsitektur backbone.
3. **Normalisasi Nilai Piksel:** Pada model MobileNetV2, nilai piksel dinormalisasi ke rentang $[-1, 1]$. Pada EfficientNetB0, nilai diskalakan sesuai spesifikasi preprocessing bawaan ImageNet.

### 3.4 Perancangan Arsitektur Model
Model yang dikembangkan mengadopsi mekanisme *Feature Extractor + Classifier Head*:
* **Lapisan Dasar (Backbone):** Model MobileNetV2 dan EfficientNetB0 yang telah dilatih pada ImageNet digunakan tanpa lapisan *fully connected* bawaannya (`include_top=False`). Seluruh bobot backbone dibekukan (`trainable=False`) untuk menjaga stabilitas representasi fitur umum.
* **Global Average Pooling 2D:** Merata-ratakan dimensi spasial (7x7) menjadi vektor fitur 1D (1.280 dimensi untuk MobileNetV2 dan 1.000 dimensi untuk EfficientNetB0), secara signifikan mengurangi parameter dibandingkan perataan konvensional (*Flatten*).
* **Lapisan Klasifikasi (Head):** Terdiri atas Dense 256 neuron dengan aktivasi ReLU, Batch Normalization untuk percepatan stabilitas gradien, Dropout sebesar 0,3 untuk regularisasi anti-overfitting, Dense 128 neuron dengan Dropout 0,2, dan lapisan keluaran Dense 3 neuron dengan aktivasi Softmax untuk menghasilkan distribusi probabilitas kelas.

### 3.5 Konfigurasi Pelatihan dan Parameter Optimasi
* **Fungsi Kerugian (*Loss Function*):** Categorical Crossentropy.
* **Algoritma Optimasi:** Adam Optimizer dengan laju pembelajaran (*learning rate*) awal sebesar 0,001.
* **Ukuran Batch (*Batch Size*):** 32 sampel per iterasi.
* **Jumlah Epoch:** 15 epoch.

### 3.6 Implementasi Explainable AI (Grad-CAM)
Grad-CAM diimplementasikan dengan memanfaatkan framework komputasi diferensiasi otomatis TensorFlow `GradientTape`. Layer target konvolusi terakhir yang diekstrak adalah `out_relu` pada MobileNetV2 dan `top_activation` pada EfficientNetB0. Gradien kelas terprediksi dihitung terhadap keluaran layer target tersebut, dinormalisasi, lalu diproyeksikan kembali ke dimensi citra asli (224x224 piksel). Heatmap warna JET ditumpangkan dengan koefisien transparansi $\alpha = 0,45$ untuk mempermudah interpretasi visual manusia.

### 3.7 Ringkasan Temuan Awal Implementasi (Progres UTS)
Hasil pengujian empiris pada 451 citra validasi independen:

| Metrik Kinerja Evaluasi | MobileNetV2 (Winner 🏆) | EfficientNetB0 |
| :--- | :---: | :---: |
| **Akurasi Validasi Keseluruhan** | **99,11%** (447/451 benar) | **98,23%** (443/451 benar) |
| **Macro F1-Score** | **99,21%** | **98,41%** |
| **Kecepatan Inferensi per Citra (CPU)** | **237,8 ms** | **391,2 ms** (39,2% Lebih Lambat) |
| **Total Parameter Jaringan** | **2.620.227 parameter** | **4.411.814 parameter** |
| **Ukuran Berkas Bobot Head** | **4,18 MB** | **4,18 MB** |
| **Deteksi Daging Busuk (*Spoiled*)** | **100% (114/114 Benar)** | **100% (114/114 Benar)** |

---

## DAFTAR PUSTAKA

[1] M. R. Zuhdi, R. F. Setiawan, dan B. I. H. Saputro, "Identifikasi Kesegaran Daging Ayam Menggunakan Metode Convolutional Neural Network," *Computer Based Information System (CBIS) Journal*, vol. 12, no. 2, hal. 115–124, Sep 2024.  
[2] T. E. W. Putri, F. Rahayu, dkk., "Penerapan Deep Learning Untuk Klasifikasi Kesegaran Daging Sapi Berbasis Mobile Apps," *Edu Komputika Journal*, vol. 11, no. 1, hal. 45–54, 2024.  
[3] M. S. Anshori, F. N. Putra, Lestariningsih, dan F. S. Lestari, "Classification of Beef Freshness Levels Based on Image Using Convolutional Neural Network," *Jurnal Informatika dan Komputer (JIKO)*, vol. 8, no. 1, hal. 32–40, Apr 2025.  
[4] C. Cakra, S. Samsuddin, dan F. Kahar, "Klasifikasi Tingkat Kesegaran Daging Sapi Di Pasar Mandonga Kota Kendari Menggunakan Arsitektur Deep Learning VGG-16," *Simtek : Jurnal Sistem Informasi dan Teknik Komputer*, vol. 9, no. 2, hal. 293–298, Okt 2024.  
[5] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, dan L.-C. Chen, "MobileNetV2: Inverted Residuals and Linear Bottlenecks," dalam *IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2018, hal. 4510–4520.  
[6] M. Tan dan Q. V. Le, "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks," dalam *International Conference on Machine Learning (ICML)*, 2019, hal. 6105–6114.  
[7] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, dan D. Batra, "Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization," *International Journal of Computer Vision (IJCV)*, vol. 128, no. 2, hal. 336–359, 2020.  
[8] V. Shanawad, "Meat Freshness Image Dataset," *Kaggle Datasets*, 2023. [Online]. Tersedia: https://www.kaggle.com/datasets/vinayakshanawad/meat-freshness-image-dataset.
