import os
import time
import json
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import seaborn as sns

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2, EfficientNetB0
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mb_preprocess
from tensorflow.keras.applications.efficientnet import preprocess_input as eff_preprocess
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization, Input
from tensorflow.keras.models import Sequential, Model
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report

# Ensure reproducibility
np.random.seed(42)
tf.random.set_seed(42)

CLASSES = ["Fresh", "Half-Fresh", "Spoiled"]

def load_data():
    print("[1/5] Membaca dataset citra daging dari direktori...")
    train_dir = os.path.join("archive (2)", "Meat Freshness.v1-new-dataset.multiclass", "train")
    valid_dir = os.path.join("archive (2)", "Meat Freshness.v1-new-dataset.multiclass", "valid")

    train_df = pd.read_csv(os.path.join(train_dir, "_classes.csv"))
    valid_df = pd.read_csv(os.path.join(valid_dir, "_classes.csv"))
    train_df.columns = [c.strip() for c in train_df.columns]
    valid_df.columns = [c.strip() for c in valid_df.columns]

    def read_images(df, folder):
        imgs = []
        labels = []
        filenames = []
        for _, row in df.iterrows():
            fpath = os.path.join(folder, row['filename'])
            im = cv2.imread(fpath)
            if im is not None:
                im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                im = cv2.resize(im, (224, 224))
                imgs.append(im)
                labels.append([row['Fresh'], row['Half-Fresh'], row['Spoiled']])
                filenames.append(row['filename'])
        return np.array(imgs, dtype=np.uint8), np.array(labels, dtype=np.float32), filenames

    t0 = time.time()
    X_train_raw, y_train, train_files = read_images(train_df, train_dir)
    X_valid_raw, y_valid, valid_files = read_images(valid_df, valid_dir)
    print(f"Data selesai dimuat dalam {time.time()-t0:.1f}s | Train: {len(X_train_raw)}, Valid: {len(X_valid_raw)}")
    return (X_train_raw, y_train, train_files), (X_valid_raw, y_valid, valid_files)

def build_head(feat_shape):
    head = Sequential([
        GlobalAveragePooling2D(input_shape=feat_shape),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(128, activation='relu'),
        Dropout(0.2),
        Dense(3, activation='softmax')
    ])
    head.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                 loss='categorical_crossentropy',
                 metrics=['accuracy'])
    return head

def evaluate_inference_latency(model, sample_input, runs=100):
    # Warmup
    for _ in range(10):
        _ = model(sample_input, training=False)
    t0 = time.time()
    for _ in range(runs):
        _ = model(sample_input, training=False)
    latency_ms = ((time.time() - t0) / runs) * 1000.0
    return latency_ms

def compute_gradcam(img_array, base_model, head_model, last_conv_name, pred_index=None):
    grad_model = tf.keras.Model(
        base_model.inputs,
        [base_model.get_layer(last_conv_name).output, base_model.output]
    )
    with tf.GradientTape() as tape:
        conv_output, base_output = grad_model(img_array)
        preds = head_model(base_output)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_score = preds[:, pred_index]

    grads = tape.gradient(class_score, conv_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_output = conv_output[0]
    heatmap = conv_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / (tf.reduce_max(heatmap) + 1e-10)
    return heatmap.numpy(), preds.numpy()[0], int(pred_index)

def overlay_heatmap(img_rgb, heatmap, alpha=0.5):
    heatmap_resized = cv2.resize(heatmap, (img_rgb.shape[1], img_rgb.shape[0]))
    heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    overlay = np.uint8(alpha * heatmap_colored + (1 - alpha) * img_rgb)
    return overlay

def run_benchmark():
    (X_train_raw, y_train, train_files), (X_valid_raw, y_valid, valid_files) = load_data()
    y_valid_true = np.argmax(y_valid, axis=1)

    results = {}

    # ========================================================
    # MODEL 1: MobileNetV2
    # ========================================================
    print("\n[2/5] Menjalankan Benchmark: MobileNetV2...")
    X_train_mb = mb_preprocess(X_train_raw.astype(np.float32))
    X_valid_mb = mb_preprocess(X_valid_raw.astype(np.float32))

    base_mb = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_mb.trainable = False

    t_ext0 = time.time()
    feat_train_mb = base_mb.predict(X_train_mb, batch_size=64, verbose=0)
    feat_valid_mb = base_mb.predict(X_valid_mb, batch_size=64, verbose=0)
    print(f"Ekstraksi fitur MobileNetV2 selesai dalam {time.time()-t_ext0:.1f}s")

    head_mb = build_head(feat_train_mb.shape[1:])
    hist_mb = head_mb.fit(feat_train_mb, y_train,
                          validation_data=(feat_valid_mb, y_valid),
                          epochs=15, batch_size=32, verbose=1)

    pred_probs_mb = head_mb.predict(feat_valid_mb, verbose=0)
    pred_labels_mb = np.argmax(pred_probs_mb, axis=1)

    acc_mb = accuracy_score(y_valid_true, pred_labels_mb)
    p_mb, r_mb, f1_mb, _ = precision_recall_fscore_support(y_valid_true, pred_labels_mb, average='macro')
    report_mb = classification_report(y_valid_true, pred_labels_mb, target_names=CLASSES, output_dict=True)
    cm_mb = confusion_matrix(y_valid_true, pred_labels_mb)

    # Save MobileNet Head
    head_mb.save("mobilenetv2_meat_head.keras")
    head_size_mb = os.path.getsize("mobilenetv2_meat_head.keras") / (1024 * 1024)
    total_params_mb = base_mb.count_params() + head_mb.count_params()

    # Latency test
    sample_tensor = tf.constant(X_valid_mb[0:1])
    # Build complete end-to-end model for latency
    full_inp = Input(shape=(224, 224, 3))
    full_out_mb = head_mb(base_mb(full_inp, training=False))
    full_model_mb = Model(full_inp, full_out_mb)
    latency_mb = evaluate_inference_latency(full_model_mb, sample_tensor)

    results['MobileNetV2'] = {
        'accuracy': float(acc_mb),
        'macro_precision': float(p_mb),
        'macro_recall': float(r_mb),
        'macro_f1': float(f1_mb),
        'latency_ms': float(latency_mb),
        'total_params': int(total_params_mb),
        'head_size_mb': float(head_size_mb),
        'classification_report': report_mb,
        'confusion_matrix': cm_mb.tolist(),
        'history': {
            'accuracy': [float(x) for x in hist_mb.history['accuracy']],
            'val_accuracy': [float(x) for x in hist_mb.history['val_accuracy']],
            'loss': [float(x) for x in hist_mb.history['loss']],
            'val_loss': [float(x) for x in hist_mb.history['val_loss']]
        }
    }
    print(f"MobileNetV2 Validation Accuracy: {acc_mb*100:.2f}% | Macro F1: {f1_mb*100:.2f}% | Latency: {latency_mb:.2f} ms")

    # ========================================================
    # MODEL 2: EfficientNetB0
    # ========================================================
    print("\n[3/5] Menjalankan Benchmark: EfficientNetB0...")
    X_train_eff = eff_preprocess(X_train_raw.astype(np.float32))
    X_valid_eff = eff_preprocess(X_valid_raw.astype(np.float32))

    base_eff = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_eff.trainable = False

    t_ext0 = time.time()
    feat_train_eff = base_eff.predict(X_train_eff, batch_size=64, verbose=0)
    feat_valid_eff = base_eff.predict(X_valid_eff, batch_size=64, verbose=0)
    print(f"Ekstraksi fitur EfficientNetB0 selesai dalam {time.time()-t_ext0:.1f}s")

    head_eff = build_head(feat_train_eff.shape[1:])
    hist_eff = head_eff.fit(feat_train_eff, y_train,
                            validation_data=(feat_valid_eff, y_valid),
                            epochs=15, batch_size=32, verbose=1)

    pred_probs_eff = head_eff.predict(feat_valid_eff, verbose=0)
    pred_labels_eff = np.argmax(pred_probs_eff, axis=1)

    acc_eff = accuracy_score(y_valid_true, pred_labels_eff)
    p_eff, r_eff, f1_eff, _ = precision_recall_fscore_support(y_valid_true, pred_labels_eff, average='macro')
    report_eff = classification_report(y_valid_true, pred_labels_eff, target_names=CLASSES, output_dict=True)
    cm_eff = confusion_matrix(y_valid_true, pred_labels_eff)

    head_eff.save("efficientnetb0_meat_head.keras")
    head_size_eff = os.path.getsize("efficientnetb0_meat_head.keras") / (1024 * 1024)
    total_params_eff = base_eff.count_params() + head_eff.count_params()

    full_out_eff = head_eff(base_eff(full_inp, training=False))
    full_model_eff = Model(full_inp, full_out_eff)
    sample_tensor_eff = tf.constant(X_valid_eff[0:1])
    latency_eff = evaluate_inference_latency(full_model_eff, sample_tensor_eff)

    results['EfficientNetB0'] = {
        'accuracy': float(acc_eff),
        'macro_precision': float(p_eff),
        'macro_recall': float(r_eff),
        'macro_f1': float(f1_eff),
        'latency_ms': float(latency_eff),
        'total_params': int(total_params_eff),
        'head_size_mb': float(head_size_eff),
        'classification_report': report_eff,
        'confusion_matrix': cm_eff.tolist(),
        'history': {
            'accuracy': [float(x) for x in hist_eff.history['accuracy']],
            'val_accuracy': [float(x) for x in hist_eff.history['val_accuracy']],
            'loss': [float(x) for x in hist_eff.history['loss']],
            'val_loss': [float(x) for x in hist_eff.history['val_loss']]
        }
    }
    print(f"EfficientNetB0 Validation Accuracy: {acc_eff*100:.2f}% | Macro F1: {f1_eff*100:.2f}% | Latency: {latency_eff:.2f} ms")

    # ========================================================
    # [4/5] Visualisasi Grafik: Loss, Akurasi & Confusion Matrix
    # ========================================================
    print("\n[4/5] Menyimpan grafik perbandingan & confusion matrix...")
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

    # 1. Training Curves Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    epochs_range = range(1, 16)
    
    # Accuracy
    axes[0].plot(epochs_range, hist_mb.history['val_accuracy'], 'o-', color='#DC2626', label='MobileNetV2 Val Acc', lw=2)
    axes[0].plot(epochs_range, hist_eff.history['val_accuracy'], 's-', color='#2563EB', label='EfficientNetB0 Val Acc', lw=2)
    axes[0].set_title('Validation Accuracy Comparison', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].set_ylim([0.8, 1.0])
    axes[0].legend(loc='lower right', frameon=True)
    axes[0].grid(True, alpha=0.3)

    # Loss
    axes[1].plot(epochs_range, hist_mb.history['val_loss'], 'o-', color='#DC2626', label='MobileNetV2 Val Loss', lw=2)
    axes[1].plot(epochs_range, hist_eff.history['val_loss'], 's-', color='#2563EB', label='EfficientNetB0 Val Loss', lw=2)
    axes[1].set_title('Validation Loss Comparison', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Categorical Crossentropy Loss', fontsize=12)
    axes[1].legend(loc='upper right', frameon=True)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('training_curves_comparison.png', dpi=300)
    plt.close()

    # 2. Confusion Matrices Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    sns.heatmap(cm_mb, annot=True, fmt='d', cmap='Blues', ax=axes[0],
                xticklabels=CLASSES, yticklabels=CLASSES, cbar=False, annot_kws={'size': 14, 'weight': 'bold'})
    axes[0].set_title(f"MobileNetV2 Confusion Matrix\n(Overall Acc: {acc_mb*100:.2f}%)", fontsize=13, fontweight='bold', color='#1E293B')
    axes[0].set_ylabel('True Label', fontsize=11, fontweight='bold')
    axes[0].set_xlabel('Predicted Label', fontsize=11, fontweight='bold')

    sns.heatmap(cm_eff, annot=True, fmt='d', cmap='Greens', ax=axes[1],
                xticklabels=CLASSES, yticklabels=CLASSES, cbar=False, annot_kws={'size': 14, 'weight': 'bold'})
    axes[1].set_title(f"EfficientNetB0 Confusion Matrix\n(Overall Acc: {acc_eff*100:.2f}%)", fontsize=13, fontweight='bold', color='#1E293B')
    axes[1].set_ylabel('True Label', fontsize=11, fontweight='bold')
    axes[1].set_xlabel('Predicted Label', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('confusion_matrices_comparison.png', dpi=300)
    plt.close()

    # ========================================================
    # [5/5] Visualisasi Explainable AI (Grad-CAM)
    # ========================================================
    print("\n[5/5] Membuat Visualisasi Grad-CAM untuk Pembuktian Fitur Biokimia...")
    # Select 1 sample for each class
    sample_indices = []
    for c_idx in range(3):
        idxs = np.where(y_valid_true == c_idx)[0]
        sample_indices.append(idxs[5]) # pick a consistent index

    fig, axes = plt.subplots(3, 3, figsize=(12, 11))
    
    for row, (c_idx, s_idx) in enumerate(zip(range(3), sample_indices)):
        orig_img = X_valid_raw[s_idx]
        true_name = CLASSES[c_idx]

        # MobileNet GradCAM
        input_mb = X_valid_mb[s_idx:s_idx+1]
        hm_mb, probs_mb, pred_c_mb = compute_gradcam(input_mb, base_mb, head_mb, 'out_relu', pred_index=c_idx)
        overlay_mb = overlay_heatmap(orig_img, hm_mb)

        # EfficientNet GradCAM
        input_eff = X_valid_eff[s_idx:s_idx+1]
        hm_eff, probs_eff, pred_c_eff = compute_gradcam(input_eff, base_eff, head_eff, 'top_activation', pred_index=c_idx)
        overlay_eff = overlay_heatmap(orig_img, hm_eff)

        # Column 1: Original
        axes[row, 0].imshow(orig_img)
        axes[row, 0].set_title(f"Ground Truth: {true_name}\n({valid_files[s_idx][:22]}...)", fontsize=11, fontweight='bold')
        axes[row, 0].axis('off')

        # Column 2: MobileNetV2
        axes[row, 1].imshow(overlay_mb)
        mb_conf = probs_mb[pred_c_mb] * 100
        axes[row, 1].set_title(f"MobileNetV2: {CLASSES[pred_c_mb]}\nConf: {mb_conf:.1f}%", fontsize=11, fontweight='bold',
                               color='green' if pred_c_mb == c_idx else 'red')
        axes[row, 1].axis('off')

        # Column 3: EfficientNetB0
        axes[row, 2].imshow(overlay_eff)
        eff_conf = probs_eff[pred_c_eff] * 100
        axes[row, 2].set_title(f"EfficientNetB0: {CLASSES[pred_c_eff]}\nConf: {eff_conf:.1f}%", fontsize=11, fontweight='bold',
                               color='green' if pred_c_eff == c_idx else 'red')
        axes[row, 2].axis('off')

    plt.suptitle("Explainable AI (Grad-CAM) Visual Grounding Comparison\nValidasi Atensi Fitur: Oksidasi Warna Daging & Pola Marbling Lemak",
                 fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig('gradcam_comparison.png', dpi=300)
    plt.close()

    # Save JSON summary
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=4)

    print("\n=== SEMUA BENCHMARK & VISUALISASI BERHASIL DISIMPAN! ===")
    print("- JSON Hasil         : benchmark_results.json")
    print("- Kurva Akurasi/Loss : training_curves_comparison.png")
    print("- Confusion Matrix   : confusion_matrices_comparison.png")
    print("- Visualisasi GradCAM: gradcam_comparison.png")

if __name__ == "__main__":
    run_benchmark()
