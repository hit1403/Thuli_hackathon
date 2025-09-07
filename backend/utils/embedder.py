
import os
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import pandas as pd

import cv2
import numpy as np
from sklearn.cluster import KMeans
# Paths relative to project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # backend/
DATA_CSV = os.path.join(BASE_DIR, "data", "cleaned_fashion.csv")
IMAGE_DIR = os.path.join(BASE_DIR, "data", "images")
OUTPUT_PKL = os.path.join(BASE_DIR, "data", "fashion_with_embeddings_fixed.pkl")

# Load CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")



def extract_dominant_colors(image_path, k=3):
    """Extract k dominant colors from an image and return as hex codes."""
    try:
        img = Image.open(image_path).convert("RGB")
        img = np.array(img)
        img = cv2.resize(img, (150, 150))  # downscale for speed
        img = img.reshape((-1, 3))

        kmeans = KMeans(n_clusters=k, random_state=42).fit(img)
        colors = kmeans.cluster_centers_.astype(int)

        # Convert to hex codes
        hex_colors = [
            "#{:02x}{:02x}{:02x}".format(r, g, b) for r, g, b in colors
        ]
        return hex_colors
    except Exception as e:
        print(f"⚠️ Error extracting colors from {image_path}: {e}")
        return []

def get_embedding(image_path: str):
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt", padding=True)
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
        return image_features.squeeze().cpu().numpy()
    except Exception as e:
        print(f"⚠️ Error processing {image_path}: {e}")
        return None

if __name__ == "__main__":
    # Load dataset
    df = pd.read_csv(DATA_CSV)

    # Build image paths
    df["image_path"] = df["id"].astype(str) + ".jpg"
    df["image_path"] = df["image_path"].apply(lambda x: os.path.join(IMAGE_DIR, x))

    # Optional: take subset (avoid all 44k images)
    df = df.sample(2000, random_state=42).reset_index(drop=True)

    embeddings = []
    colors = []

    for idx, row in df.iterrows():
        if os.path.exists(row["image_path"]):
            emb = get_embedding(row["image_path"])
            col = extract_dominant_colors(row["image_path"], k=3)
        else:
            print(f"❌ Missing file: {row['image_path']}")
            emb, col = None, []
        
        embeddings.append(emb)
        colors.append(col)

    df["embedding"] = embeddings
    df["dominant_colors"] = colors


    df.to_pickle(OUTPUT_PKL)

    print(f"✅ Saved embeddings to {OUTPUT_PKL}")
