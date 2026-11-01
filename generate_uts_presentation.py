import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path="Presentasi_UTS_Tubes_Visi_Komputer.pptx"):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Definition
    COLOR_DARK_BG = RGBColor(15, 23, 42)       # Slate 900
    COLOR_DARK_CARD = RGBColor(30, 41, 59)     # Slate 800
    COLOR_LIGHT_BG = RGBColor(248, 250, 252)   # Slate 50
    COLOR_CARD_BG = RGBColor(255, 255, 255)    # White
    COLOR_CARD_BORDER = RGBColor(226, 232, 240)# Slate 200
    
    COLOR_PRIMARY_RED = RGBColor(185, 28, 28)  # Crimson Red
    COLOR_ACCENT_RED = RGBColor(220, 38, 38)   # Red 600
    COLOR_ACCENT_BLUE = RGBColor(37, 99, 235)  # Royal Blue 600
    COLOR_ACCENT_GREEN = RGBColor(16, 185, 129)# Emerald Green
    
    COLOR_TEXT_DARK = RGBColor(15, 23, 42)     # Slate 900
    COLOR_TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    COLOR_TEXT_LIGHT = RGBColor(241, 245, 249) # Slate 100
    COLOR_TEXT_WHITE = RGBColor(255, 255, 255) # Pure White

    TITLE_INDONESIAN = "Analisis Komparatif Arsitektur MobileNetV2 dan EfficientNetB0 dengan Visualisasi Grad-CAM untuk Klasifikasi Mutu Kesegaran Daging"
    TITLE_ENGLISH = "Comparative Analysis of MobileNetV2 and EfficientNetB0 Architectures with Grad-CAM Visualization for Meat Freshness Quality Classification"

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.color.rgb = color
        return bg

    def add_header(slide, badge_text, title_text, subtitle_text=None, is_dark=False):
        # Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(4.2), Inches(0.36))
        badge.fill.solid()
        badge.fill.fore_color.rgb = COLOR_PRIMARY_RED if not is_dark else RGBColor(220, 38, 38)
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text.upper()
        p_b.font.size = Pt(11)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_TEXT_WHITE
        p_b.alignment = PP_ALIGN.CENTER

        # Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.7), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(21)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE if is_dark else COLOR_TEXT_DARK

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.size = Pt(12)
            p2.font.color.rgb = COLOR_TEXT_MUTED if not is_dark else RGBColor(148, 163, 184)
            p2.space_before = Pt(2)

    def create_card(slide, left, top, width, height, title, items, badge_title=None, border_color=COLOR_CARD_BORDER, bg_color=COLOR_CARD_BG, is_dark=False):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.22)
        tf.margin_bottom = Inches(0.2)

        p0 = tf.paragraphs[0]
        if badge_title:
            p0.text = f"[{badge_title}] " + title
        else:
            p0.text = title
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_PRIMARY_RED if not is_dark else RGBColor(248, 113, 113)
        p0.space_after = Pt(8)

        for item in items:
            p = tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(11.5)
            p.font.color.rgb = COLOR_TEXT_DARK if not is_dark else COLOR_TEXT_LIGHT
            p.space_after = Pt(4)

        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Theme)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, COLOR_DARK_BG)

    top_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_ACCENT_RED
    top_bar.line.fill.background()

    pill = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.1), Inches(6.0), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 41, 59)
    pill.line.color.rgb = COLOR_ACCENT_RED
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    tf_pill.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = "PRESENTASI PROGRESS TUBES VISI KOMPUTER (UTS)"
    p_pill.font.size = Pt(12)
    p_pill.font.bold = True
    p_pill.font.color.rgb = RGBColor(248, 113, 113)
    p_pill.alignment = PP_ALIGN.CENTER

    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.3), Inches(2.3))
    tf_title = t_box.text_frame
    tf_title.word_wrap = True
    p_t = tf_title.paragraphs[0]
    p_t.text = TITLE_INDONESIAN
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_WHITE
    p_t.space_after = Pt(8)

    p_sub = tf_title.add_paragraph()
    p_sub.text = f"Title in English: \"{TITLE_ENGLISH}\"\nMemenuhi 5 Komponen Wajib Rubrik Penilaian UTS Tubes Visi Komputer"
    p_sub.font.size = Pt(13.5)
    p_sub.font.color.rgb = RGBColor(148, 163, 184)

    info_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.5), Inches(11.3), Inches(2.3))
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    info_card.line.color.rgb = RGBColor(51, 65, 85)
    tf_info = info_card.text_frame
    tf_info.word_wrap = True
    tf_info.margin_left = Inches(0.4)
    tf_info.margin_top = Inches(0.22)

    p_i1 = tf_info.paragraphs[0]
    p_i1.text = "Cakupan Materi Presentasi Progres UTS (Durasi: 20 Menit):"
    p_i1.font.size = Pt(14)
    p_i1.font.bold = True
    p_i1.font.color.rgb = COLOR_TEXT_WHITE
    p_i1.space_after = Pt(6)

    p_i2 = tf_info.add_paragraph()
    p_i2.text = "1. Topik & Rumusan Masalah | 2. Dataset Kaggle (2.266 Citra) | 3. Rancangan Pipeline Deep Learning"
    p_i2.font.size = Pt(12)
    p_i2.font.color.rgb = RGBColor(226, 232, 240)
    p_i2.space_after = Pt(3)

    p_i3 = tf_info.add_paragraph()
    p_i3.text = "4. Hasil Awal Implementasi (MobileNetV2 99.11% vs EfficientNetB0 98.23% + Grad-CAM) | 5. Roadmap Akhir Semester"
    p_i3.font.size = Pt(12)
    p_i3.font.color.rgb = RGBColor(226, 232, 240)
    p_i3.space_after = Pt(3)

    p_i4 = tf_info.add_paragraph()
    p_i4.text = "Disusun Oleh: [Nama Kelompok / NIM Anggota] | Kelas: [Kelas Anda] | Dosen Pengampu: derekln14"
    p_i4.font.size = Pt(12.5)
    p_i4.font.bold = True
    p_i4.font.color.rgb = RGBColor(248, 113, 113)

    # ==========================================
    # SLIDE 2: POIN 1 - TOPIK & LATAR BELAKANG
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, COLOR_LIGHT_BG)
    add_header(slide2, "Poin 1: Topik & Rumusan Masalah", "Topik Penelitian: Urgensi & Latar Belakang Masalah", "Mengapa Inspeksi Kesegaran Daging Otomatis Sangat Penting?")

    create_card(slide2, Inches(0.8), Inches(1.75), Inches(3.65), Inches(5.1), 
                "Keamanan Pangan & Mutu",
                [
                    "Daging merupakan komoditas protein pangan esensial namun bersifat highly perishable (sangat rentan rusak).",
                    "Kerusakan daging dipicu oleh proliferasi mikroba dan oksidasi pigmen mioglobin.",
                    "Daging yang tidak layak konsumsi memicu foodborne diseases (keracunan pangan) yang berbahaya.",
                    "Dibutuhkan sistem inspeksi mutu objektif untuk standardisasi industri karkas dan perlindungan konsumen."
                ], badge_title="URGENSI TOPIK")

    create_card(slide2, Inches(4.8), Inches(1.75), Inches(3.65), Inches(5.1), 
                "Keterbatasan Metode Eksisting",
                [
                    "Metode Sensorik Manual: Mengandalkan mata dan penciuman manusia; bersifat subjektif dan terpengaruh kelelahan.",
                    "Uji Kimiawi Laboratorium (TVB-N & pH): Bersifat destruktif (merusak sampel daging).",
                    "Biaya & Waktu: Membutuhkan reagen mahal dan waktu berhari-hari, tidak dapat digunakan untuk sortir cepat skala massal.",
                    "Orang awam sangat sulit membedakan fase transisi setengah segar (Half-Fresh)."
                ], badge_title="LIMITASI MANUAL")

    create_card(slide2, Inches(8.8), Inches(1.75), Inches(3.65), Inches(5.1), 
                "Solusi Visi Komputer & DL",
                [
                    "Metode Non-Destruktif: Analisis mutu daging secara instan dari citra digital tanpa merusak sampel.",
                    "Objektif & Real-Time: Ekstraksi fitur visual laten secara konsisten dalam hitungan ratusan milidetik.",
                    "Model Ringan (Lightweight): Mampu diimplementasikan pada kamera ponsel pintar atau konveyor sortir industri.",
                    "Transparansi Ilmiah: Dilengkapi visualisasi fitur berbasis Explainable AI (Grad-CAM)."
                ], badge_title="SOLUSI KAMI")

    # ==========================================
    # SLIDE 3: POIN 1 - RUMUSAN MASALAH & GAP RISET
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, COLOR_LIGHT_BG)
    add_header(slide3, "Poin 1: Topik & Rumusan Masalah", "Rumusan Masalah Penelitian & Research Gap", "Keterbatasan Riset Terdahulu dan Pertanyaan Penelitian")

    create_card(slide3, Inches(0.8), Inches(1.75), Inches(5.65), Inches(5.1),
                "Research Gap dari 4 Paper Rujukan",
                [
                    "Kelemahan Paper Terdahulu yang Kami Selesaikan:",
                    "1. Gap Skala Data: Dataset terdahulu sangat kecil (misal: Anshori et al. hanya 180 citra) atau hanya biner kasar (Zuhdi et al.).",
                    "2. Paradoks Arsitektur: Terjebak antara CNN 3-4 layer yang rawan overfitting atau model raksasa VGG-16 (Cakra et al., >138M parameter, >500 MB) yang sangat lambat.",
                    "3. Masalah 'Black-Box': Seluruh paper rujukan tidak memvisualisasikan fitur aktivasi (tidak terbukti apakah melihat daging atau latar belakang piring/cahaya).",
                    "4. Pengabaian Fase Transisi: Fase kritis 'Half-Fresh' sering terabaikan padahal merupakan tanda awal penurunan kualitas."
                ], badge_title="RESEARCH GAP")

    create_card(slide3, Inches(6.85), Inches(1.75), Inches(5.65), Inches(5.1),
                "3 Rumusan Masalah Utama",
                [
                    "Pertanyaan Penelitian (Research Questions):",
                    "",
                    "1. Bagaimana performa komparatif antara arsitektur MobileNetV2 dan EfficientNetB0 dalam mengklasifikasikan kesegaran daging 3 kelas (Fresh, Half-Fresh, Spoiled)?",
                    "",
                    "2. Sejauh mana trade-off antara akurasi klasifikasi dengan efisiensi komputasi (parameter size, bobot model, dan latensi inferensi)?",
                    "",
                    "3. Bagaimana representasi visual Grad-CAM membuktikan keabsahan fitur visual biokimia (warna mioglobin dan marbling lemak) yang dipelajari model?"
                ], badge_title="RUMUSAN MASALAH")

    # ==========================================
    # SLIDE 4: POIN 2 - DATASET YANG DIGUNAKAN
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, COLOR_LIGHT_BG)
    add_header(slide4, "Poin 2: Dataset yang Digunakan", "Karakteristik & Distribusi Dataset (Kaggle)", "Profil Lengkap 2.266 Citra Daging Multi-Class")

    create_card(slide4, Inches(0.8), Inches(1.75), Inches(5.65), Inches(5.1),
                "Statistik & Pembagian Data",
                [
                    "Spesifikasi Dataset:",
                    "• Nama: Kaggle Meat Freshness Image Dataset (Vinayak Shanawad / Roboflow).",
                    "• Format Citra: JPEG RGB, Resolusi Asli 416 x 416 piksel.",
                    "• Total Citra: 2.266 Citra.",
                    "",
                    "Pembagian Data (Train & Validation Split):",
                    "• Training Set (80.1%): 1.815 Citra",
                    "  - Fresh: 675 citra (37.2%)",
                    "  - Half-Fresh: 630 citra (34.7%)",
                    "  - Spoiled: 510 citra (28.1%)",
                    "• Validation Set (19.9%): 451 Citra",
                    "  - Fresh: 178 citra (39.5%)",
                    "  - Half-Fresh: 159 citra (35.3%)",
                    "  - Spoiled: 114 citra (25.3%)",
                    "Distribusi seimbang meminimalkan risiko severe class imbalance."
                ], badge_title="STATISTIK DATASET")

    create_card(slide4, Inches(6.85), Inches(1.75), Inches(5.65), Inches(5.1),
                "Karakteristik Visual 3 Kelas Kesegaran",
                [
                    "Deskripsi Ciri Visual pada Citra:",
                    "",
                    "1. KELAS FRESH (Segar):",
                    "   - Warna merah cerah merata (oxymyoglobin aktif).",
                    "   - Lemak/marbling putih bersih atau krem alami.",
                    "   - Permukaan basah segar tanpa eksudat lendir.",
                    "",
                    "2. KELAS HALF-FRESH (Setengah Segar / Transisi):",
                    "   - Diskolorasi parsial: merah pudar keabu-abuan.",
                    "   - Marbling mulai menguning dan kusam.",
                    "   - Titik paling kritis yang sulit dibedakan indra manusia.",
                    "",
                    "3. KELAS SPOILED (Busuk):",
                    "   - Warna cokelat gelap, kehijauan, hingga kehitaman (metmyoglobin).",
                    "   - Struktur serat dan marbling hancur berlendir."
                ], badge_title="CIRI VISUAL CITRA")

    # ==========================================
    # SLIDE 5: POIN 3 - RANCANGAN METODE & PIPELINE
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, COLOR_LIGHT_BG)
    add_header(slide5, "Poin 3: Rancangan Metode", "Arsitektur Pipeline Sistem Deep Learning", "Alur Preprocessing, Ekstraksi Fitur Transfer Learning, Classifier, hingga XAI")

    create_card(slide5, Inches(0.8), Inches(1.75), Inches(2.7), Inches(5.1),
                "1. Preprocessing",
                [
                    "Input citra RGB 416x416.",
                    "Resizing ke dimensi standar 224x224 piksel.",
                    "Normalisasi piksel rentang [-1, 1] untuk MobileNet dan [0, 255] untuk EfficientNet.",
                    "Data integrity check & stripping EXIF orientation."
                ], badge_title="TAHAP 1")

    create_card(slide5, Inches(3.8), Inches(1.75), Inches(2.7), Inches(5.1),
                "2. Feature Backbone",
                [
                    "Pre-trained ImageNet Feature Extractor.",
                    "Model A: MobileNetV2 (Inverted Residuals with Linear Bottleneck).",
                    "Model B: EfficientNetB0 (Compound Scaling MBConv).",
                    "Frozen backbone untuk transfer learning efisien."
                ], badge_title="TAHAP 2")

    create_card(slide5, Inches(6.8), Inches(1.75), Inches(2.7), Inches(5.1),
                "3. Classifier Head",
                [
                    "GlobalAveragePooling2D.",
                    "Dense 256 + Batch Normalization + ReLU activation.",
                    "Dropout Layer (0.3) sebagai regularisasi.",
                    "Dense 128 + Dropout (0.2).",
                    "Dense 3 + Softmax untuk probabilitas multi-kelas."
                ], badge_title="TAHAP 3")

    create_card(slide5, Inches(9.8), Inches(1.75), Inches(2.7), Inches(5.1),
                "4. Evaluasi & XAI",
                [
                    "Evaluasi pada 451 data validasi independen.",
                    "Metrik: Akurasi, Precision, Recall, Macro F1, Latensi (ms).",
                    "Grad-CAM Heatmap pada layer konvolusi terakhir (out_relu / top_activation).",
                    "Validasi atensi biokimia."
                ], badge_title="TAHAP 4")

    # ==========================================
    # SLIDE 6: POIN 4 - HASIL AWAL IMPLEMENTASI (BENCHMARK)
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, COLOR_LIGHT_BG)
    add_header(slide6, "Poin 4: Hasil Awal Implementasi", "Benchmark Kuantitatif: MobileNetV2 vs. EfficientNetB0", "Hasil Uji Nyata pada 451 Citra Validasi Independen")

    create_card(slide6, Inches(0.8), Inches(1.75), Inches(5.65), Inches(5.1),
                "Tabel Perbandingan Kinerja Lengkap",
                [
                    "Hasil Pengujian Empiris Model:",
                    "• Akurasi Validasi:",
                    "  - MobileNetV2 : 99.11% (447/451 Benar)  --> WINNER",
                    "  - EfficientNetB0 : 98.23% (443/451 Benar)",
                    "• Macro F1-Score:",
                    "  - MobileNetV2 : 99.21%  --> WINNER",
                    "  - EfficientNetB0 : 98.41%",
                    "• Efisiensi Komputasi & Parameter:",
                    "  - MobileNetV2 : 2.62 Juta Params | Model: 4.18 MB",
                    "  - EfficientNetB0 : 4.41 Juta Params | Model: 4.18 MB",
                    "  (MobileNet 40.6% lebih hemat parameter)",
                    "• Kecepatan Inferensi per Citra (CPU):",
                    "  - MobileNetV2 : 237.8 ms  --> WINNER (39.2% Lebih Cepat)",
                    "  - EfficientNetB0 : 391.2 ms",
                    "• Deteksi Daging Busuk (Spoiled):",
                    "  - Kedua model mencapai Precision 100% & Recall 100%!"
                ], badge_title="HASIL EMPIRIS")

    curves_img_path = os.path.abspath("training_curves_comparison.png")
    if os.path.exists(curves_img_path):
        slide6.shapes.add_picture(curves_img_path, Inches(6.75), Inches(1.85), width=Inches(5.8))

    # ==========================================
    # SLIDE 7: POIN 4 - HASIL AWAL: CONFUSION MATRIX
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, COLOR_LIGHT_BG)
    add_header(slide7, "Poin 4: Hasil Awal Implementasi", "Confusion Matrix & Analisis Kesalahan (Error Analysis)", "Evaluasi Mendalam Ketahanan pada Kelas Transisi Kritis (Half-Fresh)")

    cm_img_path = os.path.abspath("confusion_matrices_comparison.png")
    if os.path.exists(cm_img_path):
        slide7.shapes.add_picture(cm_img_path, Inches(0.8), Inches(1.8), width=Inches(6.8))

    create_card(slide7, Inches(7.85), Inches(1.75), Inches(4.7), Inches(5.1),
                "Insight & Analisis Confusion Matrix",
                [
                    "1. Keunggulan pada Kelas Half-Fresh:",
                    "   - MobileNetV2 hanya keliru 2 sampel dari 159 citra (akurasi 98.74%).",
                    "   - EfficientNetB0 keliru 5 sampel dari 159 citra (akurasi 96.86%).",
                    "   - MobileNetV2 terbukti lebih sensitif menangkap tanda awal diskolorasi.",
                    "",
                    "2. Sempurna pada Kelas Spoiled (Busuk):",
                    "   - 114 dari 114 citra daging busuk terprediksi 100% benar pada kedua model.",
                    "   - Zero False Negative: Tidak ada risiko daging busuk terprediksi segar.",
                    "",
                    "3. Stabilitas Konvergensi:",
                    "   - MobileNetV2 mencapai konvergensi stabil pada epoch ke-6 dengan val loss 0.031."
                ], badge_title="INSIGHT KLASIFIKASI")

    # ==========================================
    # SLIDE 8: POIN 4 - HASIL AWAL: GRAD-CAM XAI
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, COLOR_LIGHT_BG)
    add_header(slide8, "Poin 4: Hasil Awal Implementasi", "Visual Grounding Grad-CAM: Membuka Black-Box CNN", "Pembuktian Ilmiah Bahwa Model Mengidentifikasi Fitur Biokimia Daging")

    gradcam_img_path = os.path.abspath("gradcam_comparison.png")
    if os.path.exists(gradcam_img_path):
        slide8.shapes.add_picture(gradcam_img_path, Inches(0.8), Inches(1.8), width=Inches(6.2))

    create_card(slide8, Inches(7.3), Inches(1.75), Inches(5.2), Inches(5.1),
                "Interpretasi Peta Aktivasi Grad-CAM",
                [
                    "1. Validasi Kelas FRESH (Segar):",
                    "   - Area aktivasi warna merah (fokus tinggi) terkonsentrasi pada jaringan daging merah cerah (oxymyoglobin) dan marbling putih bersih.",
                    "",
                    "2. Validasi Kelas HALF-FRESH (Transisi):",
                    "   - Atensi model bergeser ke area bercak diskolorasi (pudar keabu-abuan) di mana degradasi pigmen mulai terjadi.",
                    "",
                    "3. Validasi Kelas SPOILED (Busuk):",
                    "   - Heatmap merah tajam berfokus pada area kehitaman/kehijauan dan dekomposisi tekstur daging yang rusak.",
                    "",
                    "4. Verifikasi Bebas Bias Background:",
                    "   - Area piring, meja, dan pantulan lampu (specular reflection) berwarna biru dingin (aktivasi nol). Membuktikan model bebas dari bias artefak latar belakang!"
                ], badge_title="INTERPRETASI XAI")

    # ==========================================
    # SLIDE 9: POIN 4 - HASIL AWAL: LIVE DEMO INTERAKTIF
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, COLOR_LIGHT_BG)
    add_header(slide9, "Poin 4: Hasil Awal Implementasi", "Demo Program: Inferensi Real-Time & Grad-CAM", "Sistem Siap Diuji Secara Live pada Sesi Presentasi UTS")

    demo_img_path = os.path.abspath("demo_result.png")
    if os.path.exists(demo_img_path):
        slide9.shapes.add_picture(demo_img_path, Inches(0.8), Inches(1.8), width=Inches(6.8))

    create_card(slide9, Inches(7.85), Inches(1.75), Inches(4.7), Inches(5.1),
                "Fitur Demo Program (demo_predict.py)",
                [
                    "Kesiapan Program Demo Live:",
                    "1. Skrip Eksekusi Siap Pakai:",
                    "   - Cukup menjalankan 'python demo_predict.py'.",
                    "   - Menghasilkan prediksi instan dalam hitungan ~200 ms.",
                    "",
                    "2. Output Multi-Informasi:",
                    "   - Menampilkan citra masukan asli.",
                    "   - Overlay peta panas atensi Grad-CAM.",
                    "   - Diagram batang keyakinan probabilitas (Confidence Score) untuk 3 kelas.",
                    "",
                    "3. Verifikasi Transparan:",
                    "   - Dosen dapat menguji gambar apa saja dari dataset secara live saat sesi tanya jawab."
                ], badge_title="LIVE DEMO READY")

    # ==========================================
    # SLIDE 10: POIN 5 - RENCANA PENGERJAAN AKHIR SEMESTER
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, COLOR_LIGHT_BG)
    add_header(slide10, "Poin 5: Rencana Akhir Semester", "Roadmap Pengerjaan Tubes Hingga Akhir Semester", "Tahapan Menuju Final Paper, Deployment, dan Presentasi Akhir")

    create_card(slide10, Inches(0.8), Inches(1.75), Inches(2.7), Inches(5.1),
                "Fase 1: UTS (Selesai)",
                [
                    "• Bab 1-3 Selesai.",
                    "• Dataset 2.266 citra tervalidasi.",
                    "• Implementasi Baseline Transfer Learning (MobileNetV2 & EfficientNetB0).",
                    "• Ekstraksi bukti Grad-CAM.",
                    "• Pembuatan Demo Program."
                ], badge_title="STATUS: 100% SELESAI")

    create_card(slide10, Inches(3.8), Inches(1.75), Inches(2.7), Inches(5.1),
                "Fase 2: Fine-Tuning",
                [
                    "Minggu 10–11:",
                    "• Unfreezing top 20-30 layers MobileNetV2.",
                    "• Fine-tuning dengan learning rate rendah (1e-5).",
                    "• Uji ketahanan variasi pencahayaan sintetis (lighting augmentation).",
                    "• Peningkatan generalisasi."
                ], badge_title="MINGGU 10-11")

    create_card(slide10, Inches(6.8), Inches(1.75), Inches(2.7), Inches(5.1),
                "Fase 3: Quantization",
                [
                    "Minggu 12–13:",
                    "• Konversi model ke TFLite INT8 / FP16.",
                    "• Kompresi model dari 4.18 MB ke <2 MB.",
                    "• Evaluasi latensi inferensi pada perangkat Android / Edge Camera.",
                    "• Pengujian integrasi sistem."
                ], badge_title="MINGGU 12-13")

    create_card(slide10, Inches(9.8), Inches(1.75), Inches(2.7), Inches(5.1),
                "Fase 4: Final Paper",
                [
                    "Minggu 14–15:",
                    "• Penyusunan Bab 4: Hasil & Pembahasan Komprehensif.",
                    "• Penyusunan Bab 5: Kesimpulan & Rekomendasi.",
                    "• Finalisasi Paper Ilmiah format Jurnal Sinta / IEEE.",
                    "• Sidang Akhir Tubes."
                ], badge_title="MINGGU 14-15")

    # ==========================================
    # SLIDE 11: PENUTUP & Q&A (Dark Theme)
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, COLOR_DARK_BG)

    tb11 = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    tb11.fill.solid()
    tb11.fill.fore_color.rgb = COLOR_ACCENT_RED
    tb11.line.fill.background()

    pill11 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.6), Inches(1.4), Inches(4.1), Inches(0.45))
    pill11.fill.solid()
    pill11.fill.fore_color.rgb = RGBColor(30, 41, 59)
    pill11.line.color.rgb = COLOR_ACCENT_RED
    tf_p11 = pill11.text_frame
    tf_p11.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_p11 = tf_p11.paragraphs[0]
    p_p11.text = "SESI TANYA JAWAB (Q & A)"
    p_p11.font.size = Pt(13)
    p_p11.font.bold = True
    p_p11.font.color.rgb = RGBColor(248, 113, 113)
    p_p11.alignment = PP_ALIGN.CENTER

    t_box11 = slide11.shapes.add_textbox(Inches(1.5), Inches(2.1), Inches(10.3), Inches(2.0))
    tf11 = t_box11.text_frame
    tf11.word_wrap = True
    p_end = tf11.paragraphs[0]
    p_end.text = "Terima Kasih Atas Perhatiannya"
    p_end.font.size = Pt(36)
    p_end.font.bold = True
    p_end.font.color.rgb = COLOR_TEXT_WHITE
    p_end.alignment = PP_ALIGN.CENTER
    p_end.space_after = Pt(12)

    p_end_sub = tf11.add_paragraph()
    p_end_sub.text = f"\"{TITLE_INDONESIAN}\""
    p_end_sub.font.size = Pt(16)
    p_end_sub.font.color.rgb = RGBColor(148, 163, 184)
    p_end_sub.alignment = PP_ALIGN.CENTER

    card11 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), Inches(4.4), Inches(8.333), Inches(1.8))
    card11.fill.solid()
    card11.fill.fore_color.rgb = RGBColor(30, 41, 59)
    card11.line.color.rgb = RGBColor(51, 65, 85)
    tf_c11 = card11.text_frame
    tf_c11.word_wrap = True
    tf_c11.margin_top = Inches(0.3)

    p_fb = tf_c11.paragraphs[0]
    p_fb.text = "Kelompok kami siap menjawab pertanyaan dan menerima masukan konstruktif dari Dosen Pengampu demi penyempurnaan Tugas Besar ini."
    p_fb.font.size = Pt(14)
    p_fb.font.color.rgb = RGBColor(226, 232, 240)
    p_fb.alignment = PP_ALIGN.CENTER

    prs.save(output_path)
    print(f"Presentation successfully updated and saved to: {output_path}")

if __name__ == "__main__":
    create_presentation()
