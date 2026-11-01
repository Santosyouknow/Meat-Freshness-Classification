import os
import sys
import argparse
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

CLASSES = ["Fresh", "Half-Fresh", "Spoiled"]
CLASS_COLORS = {
    "Fresh": "#10B981",       # Emerald Green
    "Half-Fresh": "#F59E0B",  # Amber/Orange
    "Spoiled": "#EF4444"      # Red
}

def load_inference_models():
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    head_model = tf.keras.models.load_model("mobilenetv2_meat_head.keras")
    return base_model, head_model

def compute_gradcam(img_array, base_model, head_model, last_conv_name='out_relu'):
    grad_model = tf.keras.Model(
        base_model.inputs,
        [base_model.get_layer(last_conv_name).output, base_model.output]
    )
    with tf.GradientTape() as tape:
        conv_output, base_output = grad_model(img_array)
        preds = head_model(base_output)
        pred_index = tf.argmax(preds[0])
        class_score = preds[:, pred_index]

    grads = tape.gradient(class_score, conv_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_output = conv_output[0]
    heatmap = conv_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / (tf.reduce_max(heatmap) + 1e-10)
    return heatmap.numpy(), preds.numpy()[0], int(pred_index)

def overlay_heatmap(img_rgb, heatmap, alpha=0.45):
    heatmap_resized = cv2.resize(heatmap, (img_rgb.shape[1], img_rgb.shape[0]))
    heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    overlay = np.uint8(alpha * heatmap_colored + (1 - alpha) * img_rgb)
    return overlay

def predict_single_image(img_path, base_model, head_model, save_output="demo_result.png", show_window=False):
    if not os.path.exists(img_path):
        print(f"Error: Gambar '{img_path}' tidak ditemukan.")
        return

    # Load and preprocess
    img_bgr = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (224, 224))
    
    img_tensor = preprocess_input(np.expand_dims(img_resized.astype(np.float32), axis=0))

    # Inference & Grad-CAM
    heatmap, probs, pred_idx = compute_gradcam(img_tensor, base_model, head_model)
    overlay = overlay_heatmap(img_resized, heatmap)

    pred_label = CLASSES[pred_idx]
    confidence = probs[pred_idx] * 100

    print("\n" + "="*50)
    print("      DEMO HASIL DETEKSI KESEGARAN DAGING")
    print("="*50)
    print(f"File Citra     : {os.path.basename(img_path)}")
    print(f"Hasil Prediksi : {pred_label.upper()}")
    print(f"Tingkat Keyakinan (Confidence) : {confidence:.2f}%")
    print("-" * 50)
    print("Distribusi Probabilitas Semua Kelas:")
    for cls_name, prob in zip(CLASSES, probs):
        bar_len = int(prob * 30)
        bar_str = "=" * bar_len + "-" * (30 - bar_len)
        print(f"  {cls_name:<11} : [{bar_str}] {prob*100:6.2f}%")
    print("="*50 + "\n")

    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor('#0F172A')

    # 1. Original
    axes[0].imshow(img_resized)
    axes[0].set_title(f"Citra Asli Daging\n({os.path.basename(img_path)})", color='white', fontsize=12, fontweight='bold')
    axes[0].axis('off')

    # 2. Grad-CAM Overlay
    axes[1].imshow(overlay)
    pred_col = CLASS_COLORS.get(pred_label, '#38BDF8')
    axes[1].set_title(f"Peta Aktivasi Grad-CAM\nPrediksi: {pred_label} ({confidence:.1f}%)", color=pred_col, fontsize=12, fontweight='bold')
    axes[1].axis('off')

    # 3. Probabilities Bar Chart
    axes[2].set_facecolor('#1E293B')
    y_pos = np.arange(len(CLASSES))
    colors = [CLASS_COLORS[c] for c in CLASSES]
    bars = axes[2].barh(y_pos, probs * 100, color=colors, height=0.55)
    axes[2].set_yticks(y_pos)
    axes[2].set_yticklabels(CLASSES, color='white', fontsize=11, fontweight='bold')
    axes[2].set_xlabel("Probabilitas (%)", color='white', fontsize=11)
    axes[2].set_xlim(0, 105)
    axes[2].tick_params(colors='white')
    axes[2].grid(axis='x', color='#334155', linestyle='--', alpha=0.7)
    axes[2].set_title("Distribusi Keyakinan Model", color='white', fontsize=12, fontweight='bold')

    for bar, p in zip(bars, probs):
        w = bar.get_width()
        axes[2].text(w + 2, bar.get_y() + bar.get_height()/2, f"{p*100:.1f}%",
                     va='center', color='white', fontweight='bold', fontsize=10)

    plt.tight_layout()
    plt.savefig(save_output, dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"Visualisasi demo berhasil disimpan ke: {save_output}")

    if show_window:
        plt.show()
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live Demo Deteksi Kesegaran Daging")
    parser.add_argument("--image", type=str, default=None, help="Path ke file gambar yang ingin diuji")
    parser.add_argument("--show", action="store_true", help="Tampilkan pop-up window matplotlib")
    args = parser.parse_args()

    print("Memuat model MobileNetV2 dan bobot inferensi...")
    base, head = load_inference_models()

    if args.image is None:
        # Pick a random sample from valid set
        valid_dir = os.path.join("archive (2)", "Meat Freshness.v1-new-dataset.multiclass", "valid")
        all_imgs = [f for f in os.listdir(valid_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if all_imgs:
            test_img = os.path.join(valid_dir, random.choice(all_imgs))
            print(f"Mengambil sampel acak dari validation set: {test_img}")
            predict_single_image(test_img, base, head, show_window=args.show)
        else:
            print("Tidak ada gambar ditemukan di folder valid.")
    else:
        predict_single_image(args.image, base, head, show_window=args.show)
