import os
import pandas as pd
from PIL import Image

train_csv = os.path.join("archive (2)", "Meat Freshness.v1-new-dataset.multiclass", "train", "_classes.csv")
valid_csv = os.path.join("archive (2)", "Meat Freshness.v1-new-dataset.multiclass", "valid", "_classes.csv")

train_df = pd.read_csv(train_csv)
valid_df = pd.read_csv(valid_csv)

train_df.columns = [c.strip() for c in train_df.columns]
valid_df.columns = [c.strip() for c in valid_df.columns]

print("=== STATISTIK DATASET KAGGLE: MEAT FRESHNESS ===")
print(f"Total Sampel Train: {len(train_df)}")
print(f"Total Sampel Valid: {len(valid_df)}")
print(f"Total Keseluruhan : {len(train_df) + len(valid_df)}\n")

print("--- Distribusi Train Set ---")
print(f"Fresh      : {train_df['Fresh'].sum()} ({train_df['Fresh'].sum()/len(train_df)*100:.1f}%)")
print(f"Half-Fresh : {train_df['Half-Fresh'].sum()} ({train_df['Half-Fresh'].sum()/len(train_df)*100:.1f}%)")
print(f"Spoiled    : {train_df['Spoiled'].sum()} ({train_df['Spoiled'].sum()/len(train_df)*100:.1f}%)\n")

print("--- Distribusi Valid Set ---")
print(f"Fresh      : {valid_df['Fresh'].sum()} ({valid_df['Fresh'].sum()/len(valid_df)*100:.1f}%)")
print(f"Half-Fresh : {valid_df['Half-Fresh'].sum()} ({valid_df['Half-Fresh'].sum()/len(valid_df)*100:.1f}%)")
print(f"Spoiled    : {valid_df['Spoiled'].sum()} ({valid_df['Spoiled'].sum()/len(valid_df)*100:.1f}%)\n")

# Check a sample image
sample_img_name = train_df.iloc[0]['filename']
sample_path = os.path.join("archive (2)", "Meat Freshness.v1-new-dataset.multiclass", "train", sample_img_name)
if os.path.exists(sample_path):
    img = Image.open(sample_path)
    print(f"Sample Image: {sample_img_name}")
    print(f"Image Resolution: {img.size} (Width x Height)")
    print(f"Image Format / Mode: {img.format} / {img.mode}")
