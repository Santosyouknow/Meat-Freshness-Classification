import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_laporan():
    doc = docx.Document()

    # Set Margins (Standard Academic: 1 inch / 2.54 cm all sides)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(30, 41, 59) # Slate Dark

    # Helper function for adding paragraphs with spacing
    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, space_before=0, bold=False, italic=False, font_size=12):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = 1.15
        if text:
            run = p.add_run(text)
            run.bold = bold
            run.italic = italic
            run.font.size = Pt(font_size)
            run.font.name = 'Times New Roman'
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(14)
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(185, 28, 28) # Crimson
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(12.5)
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.italic = True
        run.font.size = Pt(12)
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    # ==========================================
    # COVER / HEADER JUDUL
    # ==========================================
    p_meta = add_p("LAPORAN PROGRES TUGAS BESAR VISI KOMPUTER (UTS)", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, bold=True, font_size=12)
    p_meta.runs[0].font.color.rgb = RGBColor(185, 28, 28)
    
    p_course = add_p("Mata Kuliah: CII3B4 Visi Komputer | Semester Ganjil 2026/2027", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18, italic=True, font_size=11)
    
    p_title = add_p("ANALISIS KOMPARATIF ARSITEKTUR MOBILENETV2 DAN EFFICIENTNETB0 DENGAN VISUALISASI GRAD-CAM UNTUK KLASIFIKASI MUTU KESEGARAN DAGING", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10, bold=True, font_size=16)
    
    p_eng = add_p("Comparative Analysis of MobileNetV2 and EfficientNetB0 Architectures with Grad-CAM Visualization for Meat Freshness Quality Classification", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=20, italic=True, font_size=12)

    # Identitas Penulis Card Box
    p_author = add_p("Disusun Oleh:\n[Nama Anggota Kelompok / NIM]\nKelas: [Kelas Anda]\nProgram Studi Informatika / Teknik Komputer", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24, bold=True, font_size=11)

    # Garis Pembatas
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_after = Pt(16)
    r_div = p_div.add_run("_______________________________________________________________________________")
    r_div.font.color.rgb = RGBColor(203, 213, 225)

    # ==========================================
    # ABSTRAK
    # ==========================================
    add_h2("ABSTRAK")
    add_p("Penjaminan mutu dan kesegaran daging merupakan tantangan krusial dalam rantai pasok pangan untuk mencegah risiko keracunan makanan (foodborne diseases). Metode konvensional seperti inspeksi sensorik visual dan olfaktori bersifat sangat subjektif dan rentan terhadap kelelahan pemeriksa, sementara uji kimiawi laboratorium bersifat destruktif dan memakan waktu. Penelitian ini mengusulkan sistem klasifikasi mutu kesegaran daging non-destruktif multikelas (Fresh, Half-Fresh, dan Spoiled) berbasis visi komputer dengan membandingkan dua arsitektur transfer learning berbobot ringan: MobileNetV2 dan EfficientNetB0. Untuk mengatasi keterbatasan riset terdahulu yang memperlakukan Convolutional Neural Network (CNN) sebagai kotak hitam (black box), metode Explainable AI berbasis Gradient-weighted Class Activation Mapping (Grad-CAM) diintegrasikan untuk memvalidasi fitur visual biokimia yang dijadikan dasar penentuan keputusan model. Dataset yang digunakan terdiri dari 2.266 citra digital resolusi tinggi (416x416 piksel) yang bersumber dari Kaggle Meat Freshness Image Dataset. Hasil pengujian empiris pada 451 citra validasi independen membuktikan bahwa MobileNetV2 mencapai performa terbaik dengan akurasi 99,11%, Macro F1-score 99,21%, dan latensi inferensi 237,8 ms, melampaui EfficientNetB0 (akurasi 98,23%, Macro F1-score 98,41%, dan latensi 391,2 ms) dengan kebutuhan parameter 40,6% lebih hemat (2,62 juta vs 4,41 juta parameter). Visualisasi Grad-CAM membuktikan secara saintifik bahwa model mampu mengenali degradasi pigmen oxymyoglobin dan struktur marbling lemak secara konsisten tanpa terdistraksi oleh artefak latar belakang.", space_after=6)
    
    add_p("Kata Kunci: Visi Komputer, Klasifikasi Kesegaran Daging, MobileNetV2, EfficientNetB0, Explainable AI, Grad-CAM, Transfer Learning.", italic=True, space_after=18)

    # ==========================================
    # BAB 1: PENDAHULUAN
    # ==========================================
    add_h1("BAB 1: PENDAHULUAN")
    
    add_h2("1.1 Latar Belakang Masalah")
    add_p("Daging merupakan salah satu komoditas pangan sumber protein hewani utama yang sangat dibutuhkan oleh masyarakat karena mengandung asam amino esensial, mineral, dan vitamin yang penting bagi pertumbuhan dan kesehatan manusia. Namun, daging memiliki sifat biologis yang sangat mudah mengalami kerusakan (highly perishable). Penurunan mutu daging dipicu oleh kombinasi aktivitas mikroorganisme pembusuk dan proses biokimia pasca-penyembelihan, khususnya degradasi protein serta reaksi oksidasi pigmen mioglobin. Mengonsumsi daging yang telah mengalami penurunan mutu atau pembusukan berisiko tinggi memicu gangguan kesehatan serius berupa keracunan makanan (foodborne diseases), seperti infeksi bakteri Salmonella sp., Escherichia coli, dan Staphylococcus aureus.", space_after=6)
    
    add_p("Dalam industri pemotongan hewan, pasar ritel, maupun pasar tradisional, inspeksi kesegaran daging secara konvensional masih mengandalkan indra manusia (uji sensorik visual warna, tekstur sentuhan, dan bau). Cara ini memiliki kelemahan mendasar karena sangat subjektif, tidak memiliki standardisasi kuantitatif, dan tingkat akurasinya menurun drastis akibat kelelahan pemeriksa serta pencahayaan lingkungan pasar yang tidak seragam. Di sisi lain, metode pengujian ilmiah laboratorium, seperti analisis Total Volatile Basic Nitrogen (TVB-N), pengukuran pH mikro, dan uji hitung mikroba (Total Plate Count), memang memberikan hasil yang presisi. Namun, prosedur tersebut memerlukan reagen kimia yang mahal, merusak sampel (destruktif), dan membutuhkan waktu pengujian yang lama (berjam-jam hingga berhari-hari). Keterbatasan ini menyebabkan uji laboratorium tidak mungkin diterapkan untuk proses sortir cepat secara kontinu pada rantai pasok industri pangan.", space_after=6)
    
    add_p("Perkembangan pesat teknologi pengolahan citra digital (digital image processing) dan visi komputer (computer vision) membuka peluang besar untuk menciptakan sistem inspeksi mutu pangan yang objektif, non-destruktif, cepat (real-time), dan hemat biaya. Dengan memanfaatkan kamera digital standar, sistem dapat menganalisis perubahan visual permukaan daging—seperti perubahan warna akibat oksidasi mioglobin dan dekomposisi struktur lemak marbling—secara akurat tanpa menyentuh maupun merusak produk.", space_after=12)

    add_h2("1.2 Identifikasi Masalah dan Kesenjangan Riset (Research Gap)")
    add_p("Sejumlah penelitian terdahulu telah berupaya mengotomatisasi klasifikasi mutu kesegaran daging menggunakan teknik kecerdasan buatan, namun masih menyisakan kesenjangan riset (research gap) kritis yang harus diselesaikan:", space_after=6)

    gaps = [
        ("1. Keterbatasan Skala dan Representasi Dataset:", "Sebagian besar penelitian terdahulu menggunakan ukuran dataset yang sangat terbatas. Sebagai contoh, penelitian Anshori & Putra (2025) hanya menggunakan 180 citra daging sapi. Jumlah data yang sangat kecil ini memiliki risiko overfitting yang tinggi dan tidak mampu merepresentasikan variasi pencahayaan riil, specular reflection (pantulan cahaya), serta keberagaman pola marbling lemak."),
        ("2. Penyederhanaan Kategori Menjadi Klasifikasi Biner:", "Penelitian Zuhdi et al. (2024) hanya mengelompokkan daging secara biner (segar vs tidak segar). Pendekatan ini mengabaikan fase paling kritis dalam degradasi daging, yaitu fase setengah segar (Half-Fresh). Fase Half-Fresh merupakan jendela waktu transisi di mana mikroba mulai berkembang dan penurunan kualitas terjadi, yang semestinya menjadi peringatan dini bagi konsumen sebelum daging membusuk total."),
        ("3. Paradoks Arsitektur Model ('Under-parameterized' vs 'Over-parameterized'):", "Penelitian rujukan terpolarisasi pada dua ekstrem arsitektur. Di satu sisi, model CNN Vanilla 3-4 layer sederhana (Putri et al., 2024; Anshori & Putra, 2025) memiliki kapasitas feature extraction yang terbatas. Di sisi lain, penggunaan model transfer learning kuno seperti VGG-16 oleh Cakra et al. (2024) melibatkan lebih dari 138 juta parameter dengan ukuran bobot melampaui 500 MB. Arsitektur sebesar ini membutuhkan daya komputasi tinggi, memakan memori berlebih, dan menghasilkan latensi inferensi yang lambat, sehingga mustahil diimplementasikan pada perangkat edge computing atau kamera ponsel cerdas."),
        ("4. Permasalahan 'Black-Box' dan Ketiadaan Explainable AI (XAI):", "Hampir seluruh penelitian terdahulu memperlakukan model deep learning murni sebagai kotak hitam (black box). Penguji tidak memiliki instrumen untuk memverifikasi area citra mana yang menjadi rujukan model dalam mengambil keputusan. Kondisi ini membuka celah bias model, di mana model berpotensi 'menyontek' latar belakang meja, warna piring, atau pantulan flash kamera alih-alih mengekstrak ciri biokimia permukaan daging.")
    ]

    for g_title, g_desc in gaps:
        p_g = doc.add_paragraph()
        p_g.paragraph_format.left_indent = Inches(0.25)
        p_g.paragraph_format.space_after = Pt(4)
        r_gt = p_g.add_run(g_title + " ")
        r_gt.bold = True
        r_gt.font.name = 'Times New Roman'
        r_gd = p_g.add_run(g_desc)
        r_gd.font.name = 'Times New Roman'

    add_p("Berdasarkan kesenjangan tersebut, penelitian ini mengusulkan pendekatan komparatif antara dua arsitektur modern berbobot ringan (lightweight state-of-the-art): MobileNetV2 dan EfficientNetB0, yang dievaluasi pada dataset representatif sebanyak 2.266 citra 3 kelas, serta diintegrasikan dengan metode Gradient-weighted Class Activation Mapping (Grad-CAM) untuk memvalidasi transparansi visual fitur biologis daging.", space_after=12)

    add_h2("1.3 Rumusan Masalah")
    add_p("Berdasarkan latar belakang dan kesenjangan riset yang telah diuraikan, rumusan masalah dalam penelitian ini dirumuskan sebagai berikut:", space_after=6)
    
    questions = [
        "1. Bagaimana performa arsitektur deep learning ringan modern (MobileNetV2 dan EfficientNetB0) dalam mengklasifikasikan tiga tingkat mutu kesegaran daging (Fresh, Half-Fresh, dan Spoiled) pada citra resolusi tinggi?",
        "2. Sejauh mana trade-off antara akurasi klasifikasi dan efisiensi komputasi (jumlah parameter model, ukuran berkas bobot, dan latensi inferensi per citra) antara MobileNetV2 dan EfficientNetB0?",
        "3. Bagaimana representasi visual Explainable AI berbasis Grad-CAM membuktikan keabsahan fitur biokimia (warna oxymyoglobin/metmyoglobin dan distribusi marbling lemak) yang dipelajari model, serta membuktikan bahwa model bebas dari bias latar belakang?"
    ]
    for q in questions:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.left_indent = Inches(0.25)
        p_q.paragraph_format.space_after = Pt(4)
        rq = p_q.add_run(q)
        rq.font.name = 'Times New Roman'

    add_h2("1.4 Tujuan Penelitian")
    add_p("Tujuan yang ingin dicapai melalui penelitian ini adalah:", space_after=6)
    objectives = [
        "1. Membangun dan melatih model klasifikasi kesegaran daging tiga kelas berbasis transfer learning menggunakan arsitektur MobileNetV2 dan EfficientNetB0.",
        "2. Menganalisis secara kuantitatif perbandingan kinerja kedua model berdasarkan metrik akurasi validasi, precision, recall, macro F1-score, matriks konfusi, dan latensi komputasi inferensi.",
        "3. Mengimplementasikan teknik Grad-CAM untuk menghasilkan peta visual atensi (heatmap) yang memvalidasi keputusan klasifikasi model terhadap area degradasi jaringan daging.",
        "4. Menghasilkan purwarupa program inferensi inferensial interaktif (demo) yang siap diimplementasikan untuk pengujian real-time."
    ]
    for obj in objectives:
        p_o = doc.add_paragraph()
        p_o.paragraph_format.left_indent = Inches(0.25)
        p_o.paragraph_format.space_after = Pt(4)
        ro = p_o.add_run(obj)
        ro.font.name = 'Times New Roman'

    add_h2("1.5 Manfaat Penelitian")
    add_p("Penelitian ini diharapkan memberikan kontribusi nyata:", space_after=6)
    add_p("• Manfaat Teoritis / Akademis: Memberikan wawasan empiris mengenai perbandingan arsitektur konvolusi berbasis Inverted Residuals (MobileNetV2) versus Compound Scaling (EfficientNetB0) pada domain citra tekstur pangan, serta membuktikan efektivitas Explainable AI (Grad-CAM) dalam mengatasi masalah black-box pada visi komputer biomedis/pangan.", space_after=4)
    add_p("• Manfaat Praktis: Menyediakan model klasifikasi berbobot ringan (<5 MB) yang berkinerja tinggi (>98%) dan cepat (<400 ms), sehingga siap diadopsi oleh industri pangan, rumah pemotongan hewan, swalayan, maupun konsumen melalui aplikasi kamera ponsel cerdas (Android/iOS) guna penjaminan keamanan pangan.", space_after=12)

    add_h2("1.6 Batasan Masalah")
    add_p("Ruang lingkup dan batasan pada penelitian ini didefinisikan sebagai berikut:", space_after=6)
    add_p("1. Dataset yang digunakan bersumber dari Kaggle Meat Freshness Image Dataset (Vinayak Shanawad / Roboflow) sebanyak 2.266 citra berformat JPEG RGB dengan resolusi asli 416 x 416 piksel.", space_after=3)
    add_p("2. Kelas klasifikasi terdiri dari 3 kelas terpisah: Fresh (Segar), Half-Fresh (Setengah Segar / Mulai Penurunan Mutu), dan Spoiled (Busuk / Tidak Layak Konsumsi).", space_after=3)
    add_p("3. Arsitektur transfer learning yang dikomparasikan dibatasi pada model MobileNetV2 dan EfficientNetB0 dengan bobot terlatih dari ImageNet.", space_after=3)
    add_p("4. Citra masukan pada pipeline inferensi diseragamkan ke ukuran 224 x 224 x 3 piksel.", space_after=3)
    add_p("5. Metode Explainable AI yang digunakan adalah Gradient-weighted Class Activation Mapping (Grad-CAM) yang diekstraksi dari lapisan konvolusi terakhir masing-masing model.", space_after=18)

    # ==========================================
    # BAB 2: TINJAUAN PUSTAKA DAN LANDASAN TEORI
    # ==========================================
    add_h1("BAB 2: TINJAUAN PUSTAKA DAN LANDASAN TEORI")
    
    add_h2("2.1 Tinjauan Pustaka (State-of-the-Art)")
    add_p("Kajian pustaka dilakukan terhadap empat penelitian ilmiah terdahulu yang relevan guna memetakan posisi dan kebaruan penelitian ini:", space_after=6)

    studies = [
        ("Zuhdi, Setiawan, & Saputro (2024)", "meneliti identifikasi kesegaran daging ayam broiler menggunakan metode Convolutional Neural Network (CNN) biner (segar vs busuk). Model yang dikembangkan menghasilkan F1-score yang tinggi (0,87 pada data latih dan 0,99 pada validasi), namun nilai Area Under Curve (AUC) hanya mencapai 0,47. Nilai AUC yang di bawah 0,5 mengindikasikan bahwa model memiliki ketidakstabilan batas keputusan (decision threshold) dan performa yang mendekati tebakan acak pada ambang probabilitas tertentu. Selain itu, penelitian ini tidak memetakan fase transisi setengah segar dan tidak menyediakan visualisasi fitur aktivasi."),
        ("Putri, Rahayu, dkk. (2024)", "mengembangkan aplikasi seluler berbasis Android untuk klasifikasi kesegaran daging sapi menggunakan deep learning CNN dan format TensorFlow Lite. Penelitian ini melaporkan akurasi hingga 100% pada data uji. Namun, akurasi sempurna pada dataset skala kecil mengindikasikan adanya controlled environment yang homogen atau potensi data leakage antar-split data. Model belum diuji terhadap keberagaman tekstur daging pasar riil dan tidak menyajikan analisis latensi komputasi inferensi secara komparatif."),
        ("Anshori, Putra, Lestariningsih, & Lestari (2025)", "menerapkan arsitektur CNN 4-layer konvolusi sederhana untuk mengklasifikasikan kesegaran daging sapi berdasarkan durasi penyimpanan (Grade 1 segar, Grade 2 penyimpanan 7-14 jam, dan Grade 3 penyimpanan >14 jam) dengan akurasi 97,22%. Namun, dataset yang digunakan sangat terbatas, yakni hanya berjumlah 180 citra digital (60 citra per kelas). Model yang dilatih dari awal (from scratch) pada dataset sekecil ini sangat rentan mengalami overfitting bila dihadapkan pada variasi pencahayaan dan pantulan blitz yang berbeda di luar laboratorium."),
        ("Cakra, Samsuddin, & Kahar (2024)", "melakukan klasifikasi kesegaran daging sapi di Pasar Tradisional Mandonga Kota Kendari dengan menerapkan Transfer Learning menggunakan arsitektur VGG-16. Meskipun VGG-16 mampu mencapai akurasi tinggi pada citra pasar lokal, arsitektur ini memiliki lebih dari 138 juta parameter dan ukuran berkas bobot melebihi 500 MB. Bobot yang masif ini menyebabkan konsumsi RAM dan daya yang sangat boros serta latensi inferensi yang lambat, sehingga tidak efisien bila diintegrasikan ke perangkat edge atau smartphone. Model juga bersifat black box tanpa interpretasi atensi visual.")
    ]

    for s_auth, s_desc in studies:
        p_s = doc.add_paragraph()
        p_s.paragraph_format.left_indent = Inches(0.25)
        p_s.paragraph_format.space_after = Pt(4)
        rst = p_s.add_run(f"• {s_auth} ")
        rst.bold = True
        rst.font.name = 'Times New Roman'
        rsd = p_s.add_run(s_desc)
        rsd.font.name = 'Times New Roman'

    add_p("Tabel 2.1 menyajikan pemetaan komparatif antara penelitian rujukan terdahulu dengan penelitian yang diusulkan dalam Tugas Besar ini.", space_after=8)

    # TABEL 2.1: Matriks State of the Art
    t1 = doc.add_table(rows=6, cols=5)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1.autofit = False

    col_widths = [Inches(1.3), Inches(1.2), Inches(1.2), Inches(1.3), Inches(1.6)]
    headers = ["Peneliti & Tahun", "Metode / Arsitektur", "Objek & Kelas", "Skala Dataset", "Celah Riset / Batasan"]
    
    # Header Row
    for i, h_text in enumerate(headers):
        cell = t1.cell(0, i)
        cell.width = col_widths[i]
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_rows = [
        ("Zuhdi et al. (2024)", "Vanilla CNN", "Daging Ayam (2 Kelas)", "Dataset Lokal Terbatas", "AUC hanya 0,47; klasifikasi biner; nir-interpretasi (black-box)."),
        ("Putri et al. (2024)", "CNN + Mobile TFLite", "Daging Sapi (3 Kelas)", "Dataset Studio Kecil", "Klaim akurasi 100% (indikasi overfitting); tidak ada uji efisiensi."),
        ("Anshori & Putra (2025)", "CNN 4-Layer Scratch", "Daging Sapi (3 Kelas)", "180 Citra (Sangat Kecil)", "Data terlalu minim untuk deep learning; tanpa pretrained backbone."),
        ("Cakra et al. (2024)", "Transfer Learning VGG-16", "Daging Sapi Pasar (3 Kelas)", "Dataset Lokal Mandonga", "Model raksasa (>138M parameter, >500 MB); tidak ramah edge/mobile."),
        ("Penelitian Ini (Diusulkan)", "MobileNetV2 vs EfficientNetB0 + Grad-CAM", "Daging Multikelas (Fresh, Half, Spoiled)", "2.266 Citra Resolusi Tinggi", "Multi-model benchmark ringan (<5M params); XAI Grad-CAM membuktikan fitur biokimia.")
    ]

    for row_idx, r_data in enumerate(data_rows, start=1):
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        if row_idx == 5:
            bg_col = "FEF2F2" # Highlight row
        for col_idx, text_val in enumerate(r_data):
            cell = t1.cell(row_idx, col_idx)
            cell.width = col_widths[col_idx]
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text_val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9.5)
            if row_idx == 5:
                r.bold = True
                r.font.color.rgb = RGBColor(185, 28, 28)

    add_p("Tabel 2.1: Matriks Komparasi State-of-the-Art terhadap Penelitian yang Diusulkan.", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=14, italic=True, font_size=10)

    add_h2("2.2 Fisiologi dan Karakteristik Biokimia Kesegaran Daging")
    add_p("Warna visual permukaan daging merupakan indikator utama kesegaran yang dievaluasi oleh konsumen dan sistem visi komputer. Warna daging ditentukan oleh konsentrasi dan status kimiawi pigmen heme protein, yaitu mioglobin (myoglobin). Mioglobin mengalami tiga bentuk transformasi optik utama:", space_after=6)
    add_p("1. Deoxymyoglobin (Fe2+ tanpa O2): Menghasilkan warna merah keunguan gelap, umum ditemukan pada bagian dalam daging atau daging segar tanpa kontak udara.", space_after=3)
    add_p("2. Oxymyoglobin (Fe2+ dengan O2): Terbentuk saat deoxymyoglobin teroksigenasi oleh udara, menghasilkan warna merah cerah merona (cherry-red bloom). Kondisi ini merupakan ciri khas daging segar (Fresh).", space_after=3)
    add_p("3. Metmyoglobin (Fe3+ teroksidasi): Terjadi akibat oksidasi berkelanjutan di mana atom besi bervalensi dua dioksidasi menjadi bervalensi tiga. Metmyoglobin memantulkan spektrum warna cokelat kusam hingga keabu-abuan. Peningkatan metmyoglobin adalah indikasi langsung penurunan mutu (Half-Fresh hingga Spoiled).", space_after=6)
    add_p("Selain warna mioglobin, tekstur marbling (lemak intramuskular) yang tersebar di antara serat otot daging juga menjadi penanda penting. Pada daging segar, lemak marbling tampak putih bersih atau krem solid. Seiring dekomposisi enzimatik dan aktivitas bakteri lipolitik, lemak marbling menguning, melunak, dan hancur, menghasilkan eksudat basah berlendir yang khas pada daging busuk.", space_after=12)

    add_h2("2.3 Deep Learning dan Transfer Learning")
    add_p("Convolutional Neural Network (CNN) adalah arsitektur deep learning yang dirancang khusus untuk memproses data berstruktur grid dua dimensi, seperti citra visual. Operasi konvolusi menggeser kernel filter berbobot di atas citra untuk mengekstrak fitur spasial hierarkis, mulai dari fitur tingkat rendah (tepi, kontur, warna lokal) pada lapisan awal hingga representasi semantik kompleks (tekstur marbling, pola pembusukan) pada lapisan lebih dalam.", space_after=6)
    add_p("Transfer learning adalah paradigma pelatihan machine learning yang memanfaatkan bobot (weights) dari model yang telah dilatih sebelumnya pada dataset raksasa (ImageNet dengan lebih dari 1,4 juta citra dan 1.000 kategori kelas) sebagai dasar ekstraksi fitur pada tugas target baru. Pendekatan ini secara drastis mempercepat konvergensi pelatihan, mencegah kecenderungan overfitting, serta mengatasi kendala keterbatasan sampel pada dataset spesifik.", space_after=12)

    add_h2("2.4 Arsitektur Deep Learning Ringan: MobileNetV2 dan EfficientNetB0")
    add_p("Untuk mendukung deployment pada perangkat komputasi terbatas, penelitian ini mengkaji dua arsitektur state-of-the-art berbobot ringan:", space_after=6)
    add_p("• MobileNetV2 (Sandler et al., 2018): Menggunakan modul inovatif Inverted Residuals with Linear Bottleneck. Tidak seperti residual network konvensional yang menyempitkan kanal di tengah blok, MobileNetV2 memperluas kanal fitur berdimensi rendah ke dimensi tinggi sebelum menerapkan Depthwise Separable Convolution (DWConv 3x3), lalu memproyeksikannya kembali ke dimensi rendah tanpa aktivasi non-linear (linear bottleneck). Desain ini memangkas jumlah operasi floating-point (FLOPs) secara signifikan sembari mempertahankan kekayaan representasi fitur.", space_after=6)
    add_p("• EfficientNetB0 (Tan & Le, 2019): Menerapkan prinsip Compound Scaling, yakni penskalaan seimbang antara kedalaman jaringan (depth), lebar kanal (width), dan resolusi citra input (resolution) menggunakan koefisien gabungan tetap. Blok dasarnya dibangun di atas modul MBConv (Mobile Inverted Bottleneck Convolution) yang diperkuat dengan mekanisme Squeeze-and-Excitation (SE) untuk memberikan pembobotan adaptif pada kanal fitur yang paling informatif.", space_after=12)

    add_h2("2.5 Explainable Artificial Intelligence (XAI) dan Grad-CAM")
    add_p("Sifat black-box pada deep learning menimbulkan keengganan penerapan di industri pangan dan medis karena pengguna tidak dapat memverifikasi alasan logis di balik prediksi model. Gradient-weighted Class Activation Mapping (Grad-CAM) hadir sebagai teknik atribusi visual yang menghasilkan peta lokalisasi berbobot (coarse localization map) yang menyoroti wilayah penting pada citra untuk prediksi kelas tertentu.", space_after=6)
    add_p("Secara matematis, gradien dari skor keluaran kelas target y^c terhadap activation map lapisan konvolusi terakhir A^k dihitung. Bobot kepentingan neuron alpha_k^c diperoleh melalui Global Average Pooling spasial:", space_after=4)
    add_p("alpha_k^c = (1 / Z) * sum_i sum_j (d y^c / d A_ij^k)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11, space_after=4)
    add_p("di mana Z melambangkan luas spasial peta fitur (tinggi x lebar). Selanjutnya, kombinasi linier berbobot dihitung dan disaring menggunakan fungsi aktivasi Rectified Linear Unit (ReLU) guna mempertahankan hanya fitur yang berkontribusi positif terhadap kelas c:", space_after=4)
    add_p("L_Grad-CAM^c = ReLU( sum_k alpha_k^c * A^k )", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=11, space_after=6)
    add_p("Peta panas yang dihasilkan kemudian diinterpolasi bilinear ke resolusi citra asli dan ditumpangkan (overlay) dengan skema colormap JET, di mana warna merah melambangkan atensi tertinggi dan biru melambangkan atensi terendah.", space_after=18)

    # ==========================================
    # BAB 3: METODOLOGI PENELITIAN
    # ==========================================
    add_h1("BAB 3: METODOLOGI PENELITIAN")
    
    add_h2("3.1 Diagram Alur Penelitian (Pipeline Sistem)")
    add_p("Penelitian ini dilaksanakan melalui tahapan berurutan dan terstruktur sebagaimana diilustrasikan dalam alur pipeline:", space_after=6)
    add_p("1. Akuisisi & Partisi Dataset: Pengumpulan dan pemisahan data train dan validasi.", space_after=3)
    add_p("2. Pra-pemrosesan Data: Resizing citra ke 224x224 piksel dan normalisasi kanal warna.", space_after=3)
    add_p("3. Ekstraksi Fitur Transfer Learning: Penggunaan backbone MobileNetV2 dan EfficientNetB0.", space_after=3)
    add_p("4. Pelatihan Classifier Head: Penambahan lapisan Dense, Batch Normalization, Dropout, dan Softmax.", space_after=3)
    add_p("5. Evaluasi Metrik Kinerja: Pengukuran akurasi, F1-score, matriks konfusi, dan latensi inferensi.", space_after=3)
    add_p("6. Analisis Atribusi Visual: Ekstraksi heatmap Grad-CAM untuk pembuktian fitur biokimiawi.", space_after=12)

    add_h2("3.2 Deskripsi dan Karakteristik Dataset")
    add_p("Dataset yang digunakan dalam penelitian ini bersumber dari repositori publik Kaggle: 'Meat Freshness Image Dataset' yang dikurasi oleh Vinayak Shanawad berbasis anotasi multi-kelas Roboflow. Dataset terdiri dari total 2.266 citra digital berwarna (RGB) beresolusi asli 416 x 416 piksel.", space_after=6)
    add_p("Data dibagi secara resmi menjadi dua himpunan independen:", space_after=4)
    add_p("• Training Set (80,1%): 1.815 citra, terdiri dari Fresh (675 citra / 37,2%), Half-Fresh (630 citra / 34,7%), dan Spoiled (510 citra / 28,1%).", space_after=3)
    add_p("• Validation Set (19,9%): 451 citra, terdiri dari Fresh (178 citra / 39,5%), Half-Fresh (159 citra / 35,3%), dan Spoiled (114 citra / 25,3%).", space_after=6)
    add_p("Distribusi kelas yang seimbang ini meminimalkan potensi bias mayoritas kelas (class imbalance bias) selama proses optimasi.", space_after=12)

    add_h2("3.3 Pra-pemrosesan Citra")
    add_p("Setiap citra melalui serangkaian tahapan pra-pemrosesan standar:", space_after=4)
    add_p("1. Pembacaan Citra & Konversi Ruang Warna: Citra dimuat menggunakan modul OpenCV (BGR) dan dikonversi secara eksplisit ke ruang warna RGB.", space_after=3)
    add_p("2. Penskalaan Dimensi (Resizing): Citra asli berukuran 416 x 416 diskalakan secara seragam menggunakan interpolasi area bilinear menjadi 224 x 224 piksel, menyesuaikan dimensi input baku dari arsitektur backbone.", space_after=3)
    add_p("3. Normalisasi Nilai Piksel: Pada model MobileNetV2, nilai piksel dinormalisasi ke rentang [-1, 1]. Pada EfficientNetB0, nilai diskalakan sesuai spesifikasi preprocessing bawaan ImageNet.", space_after=12)

    add_h2("3.4 Perancangan Arsitektur Model")
    add_p("Model yang dikembangkan mengadopsi mekanisme Feature Extractor + Classifier Head:", space_after=4)
    add_p("• Lapisan Dasar (Backbone): Model MobileNetV2 dan EfficientNetB0 yang telah dilatih pada ImageNet digunakan tanpa lapisan fully connected bawaannya (include_top=False). Seluruh bobot backbone dibekukan (trainable=False) untuk menjaga stabilitas representasi fitur umum.", space_after=4)
    add_p("• Global Average Pooling 2D: Merata-ratakan dimensi spasial (7x7) menjadi vektor fitur 1D (1.280 dimensi untuk MobileNetV2 dan 1.000 dimensi untuk EfficientNetB0), secara signifikan mengurangi parameter dibandingkan perataan konvensional (Flatten).", space_after=4)
    add_p("• Lapisan Klasifikasi (Head): Terdiri atas Dense 256 neuron dengan aktivasi ReLU, Batch Normalization untuk percepatan stabilitas gradien, Dropout sebesar 0,3 untuk regularisasi anti-overfitting, Dense 128 neuron dengan Dropout 0,2, dan lapisan keluaran Dense 3 neuron dengan aktivasi Softmax untuk menghasilkan distribusi probabilitas kelas.", space_after=12)

    add_h2("3.5 Konfigurasi Pelatihan dan Parameter Optimasi")
    add_p("Pelatihan model dilakukan menggunakan konfigurasi parameter hiper:", space_after=4)
    add_p("• Fungsi Kerugian (Loss Function): Categorical Crossentropy, dihitung berdasarkan deviasi distribusi probabilitas terprediksi terhadap vektor ground-truth one-hot encoding.", space_after=3)
    add_p("• Algoritma Optimasi: Adam Optimizer dengan laju pembelajaran (learning rate) awal sebesar 0,001.", space_after=3)
    add_p("• Ukuran Batch (Batch Size): 32 sampel per iterasi.", space_after=3)
    add_p("• Jumlah Epoch: 15 epoch.", space_after=12)

    add_h2("3.6 Implementasi Explainable AI (Grad-CAM)")
    add_p("Grad-CAM diimplementasikan dengan memanfaatkan framework komputasi diferensiasi otomatis TensorFlow GradientTape. Layer target konvolusi terakhir yang diekstrak adalah 'out_relu' pada MobileNetV2 dan 'top_activation' pada EfficientNetB0. Gradien kelas terprediksi dihitung terhadap keluaran layer target tersebut, dinormalisasi, lalu diproyeksikan kembali ke dimensi citra asli (224x224 piksel). Heatmap warna JET ditumpangkan dengan koefisien transparansi alfa = 0,45 untuk mempermudah interpretasi visual manusia.", space_after=12)

    add_h2("3.7 Ringkasan Temuan Awal Implementasi (Progres UTS)")
    add_p("Hasil pengujian awal pada 451 citra validasi independen disajikan pada Tabel 3.1:", space_after=6)

    # TABEL 3.1: Hasil Awal Eksperimen
    t2 = doc.add_table(rows=7, cols=3)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2.autofit = False

    col_widths2 = [Inches(2.5), Inches(2.0), Inches(2.0)]
    h2_titles = ["Metrik Kinerja Evaluasi", "MobileNetV2 (Winner)", "EfficientNetB0"]
    for i, ht in enumerate(h2_titles):
        c = t2.cell(0, i)
        c.width = col_widths2[i]
        set_cell_background(c, "1E293B")
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(ht)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_eval = [
        ("Akurasi Validasi Keseluruhan", "99,11% (447/451 benar)", "98,23% (443/451 benar)"),
        ("Macro F1-Score", "99,21%", "98,41%"),
        ("Kecepatan Inferensi per Citra (CPU)", "237,8 ms", "391,2 ms (39,2% Lebih Lambat)"),
        ("Total Parameter Jaringan", "2.620.227 parameter", "4.411.814 parameter"),
        ("Ukuran Berkas Bobot Head", "4,18 MB", "4,18 MB"),
        ("Deteksi Kelas Daging Busuk (Spoiled)", "100% (114/114 Benar)", "100% (114/114 Benar)")
    ]

    for row_idx, (m_name, mb_val, eff_val) in enumerate(data_eval, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        c0 = t2.cell(row_idx, 0)
        c1 = t2.cell(row_idx, 1)
        c2 = t2.cell(row_idx, 2)
        c0.width = col_widths2[0]
        c1.width = col_widths2[1]
        c2.width = col_widths2[2]
        set_cell_background(c0, bg)
        set_cell_background(c1, bg)
        set_cell_background(c2, bg)
        set_cell_margins(c0, top=80, bottom=80, left=100, right=100)
        set_cell_margins(c1, top=80, bottom=80, left=100, right=100)
        set_cell_margins(c2, top=80, bottom=80, left=100, right=100)
        
        p0 = c0.paragraphs[0]; r0 = p0.add_run(m_name); r0.font.name = 'Times New Roman'; r0.font.size = Pt(9.5); r0.bold = True
        p1 = c1.paragraphs[0]; r1 = p1.add_run(mb_val); r1.font.name = 'Times New Roman'; r1.font.size = Pt(9.5); r1.bold = True; r1.font.color.rgb = RGBColor(16, 185, 129)
        p2 = c2.paragraphs[0]; r2 = p2.add_run(eff_val); r2.font.name = 'Times New Roman'; r2.font.size = Pt(9.5)

    add_p("Tabel 3.1: Hasil Awal Benchmark Kuantitatif MobileNetV2 vs EfficientNetB0.", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=14, italic=True, font_size=10)

    # Embed Images if available
    img_curves = os.path.abspath("training_curves_comparison.png")
    if os.path.exists(img_curves):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_curves, width=Inches(5.8))
        add_p("Gambar 3.1: Kurva Akurasi dan Loss Pelatihan MobileNetV2 dan EfficientNetB0 (15 Epoch).", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14, italic=True, font_size=10)

    img_cm = os.path.abspath("confusion_matrices_comparison.png")
    if os.path.exists(img_cm):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_cm, width=Inches(5.8))
        add_p("Gambar 3.2: Matriks Konfusi (Confusion Matrix) MobileNetV2 dan EfficientNetB0 pada 451 Citra Validasi.", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14, italic=True, font_size=10)

    img_gradcam = os.path.abspath("gradcam_comparison.png")
    if os.path.exists(img_gradcam):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_gradcam, width=Inches(5.6))
        add_p("Gambar 3.3: Visualisasi Explainable AI (Grad-CAM) untuk Pembuktian Fitur Biokimia Daging (Fresh, Half-Fresh, dan Spoiled).", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18, italic=True, font_size=10)

    # ==========================================
    # DAFTAR PUSTAKA
    # ==========================================
    add_h1("DAFTAR PUSTAKA")
    
    references = [
        "[1] M. R. Zuhdi, R. F. Setiawan, dan B. I. H. Saputro, \"Identifikasi Kesegaran Daging Ayam Menggunakan Metode Convolutional Neural Network,\" Computer Based Information System (CBIS) Journal, vol. 12, no. 2, hal. 115–124, Sep 2024.",
        "[2] T. E. W. Putri, F. Rahayu, dkk., \"Penerapan Deep Learning Untuk Klasifikasi Kesegaran Daging Sapi Berbasis Mobile Apps,\" Edu Komputika Journal, vol. 11, no. 1, hal. 45–54, 2024.",
        "[3] M. S. Anshori, F. N. Putra, Lestariningsih, dan F. S. Lestari, \"Classification of Beef Freshness Levels Based on Image Using Convolutional Neural Network,\" Jurnal Informatika dan Komputer (JIKO), vol. 8, no. 1, hal. 32–40, Apr 2025.",
        "[4] C. Cakra, S. Samsuddin, dan F. Kahar, \"Klasifikasi Tingkat Kesegaran Daging Sapi Di Pasar Mandonga Kota Kendari Menggunakan Arsitektur Deep Learning VGG-16,\" Simtek : Jurnal Sistem Informasi dan Teknik Komputer, vol. 9, no. 2, hal. 293–298, Okt 2024.",
        "[5] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, dan L.-C. Chen, \"MobileNetV2: Inverted Residuals and Linear Bottlenecks,\" dalam IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2018, hal. 4510–4520.",
        "[6] M. Tan dan Q. V. Le, \"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,\" dalam International Conference on Machine Learning (ICML), 2019, hal. 6105–6114.",
        "[7] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, dan D. Batra, \"Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization,\" International Journal of Computer Vision (IJCV), vol. 128, no. 2, hal. 336–359, 2020.",
        "[8] V. Shanawad, \"Meat Freshness Image Dataset,\" Kaggle Datasets, 2023. [Online]. Tersedia: https://www.kaggle.com/datasets/vinayakshanawad/meat-freshness-image-dataset."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        r = p_ref.add_run(ref)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)

    output_file = "Laporan_Tubes_Bab1-3.docx"
    doc.save(output_file)
    print(f"Laporan DOCX berhasil dibuat: {output_file}")

if __name__ == "__main__":
    create_laporan()
