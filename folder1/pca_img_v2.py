"""
PCA on Images — with visualizations and CSV score export
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Config
IMG_SIZE   = (128, 128) # resize all images to this
n_components  = 15      # number of PC
N_SHOW_PC = 15          # how many principal component images to display
IMG_DIR = "/Users/drizzleinthebottle/Documents/1 rok ads/semestr 2/ekstrakcja danych/repozytorium/folder1/zdjecia"
OUTPUT_CSV = "pca_scores.sqlite3"


def load_images(folder: str = IMG_DIR) -> tuple[np.ndarray, list[str]]:
    """Load all jpg/png images, flatten to 1-D vectors."""

    exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    # adjust index after split
    paths = sorted(p for p in Path(IMG_DIR).iterdir() if p.suffix.lower() in exts and str(p).split("_")[4] == '0.png')

    vectors, names = [], []
    for p in paths:
        img = Image.open(p).convert("RGB").resize(IMG_SIZE) # L for Grayscale
        vectors.append(np.array(img, dtype=np.float32).flatten())
        names.append(os.path.basename(p))

    print(f"Loaded {len(names)} images")
    return np.stack(vectors), names


def run_pca(X: np.ndarray, n_components: int):
    """Standardise then run PCA."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    n_components = min(n_components, X.shape[0], X.shape[1])
    pca = PCA(n_components=n_components, random_state=42)
    scores = pca.fit_transform(X_scaled)
    return pca, scores, scaler


def save_scores(scores: np.ndarray, names: list[str]):
    """Save PC scores + file names to CSV."""
    cols = [f"PC{i+1}" for i in range(scores.shape[1])]
    df = pd.DataFrame(scores, columns=cols)
    df.insert(0, "filename", names)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Scores saved → {OUTPUT_CSV}")


# Visualisations
def plot_explained_variance(pca: PCA):
    """Scree plot + cumulative explained variance."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    pcs = range(1, len(pca.explained_variance_ratio_) + 1)

    axes[0].bar(pcs, pca.explained_variance_ratio_ * 100)
    axes[0].set(title="Explained Variance per PC",
                xlabel="Principal Component", ylabel="Variance (%)")

    axes[1].plot(pcs, np.cumsum(pca.explained_variance_ratio_) * 100, marker="o")
    axes[1].axhline(90, color="red", linestyle="--", label="90% threshold")
    axes[1].set(title="Cumulative Explained Variance",
                xlabel="Number of PCs", ylabel="Cumulative Variance (%)")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig("explained_variance.png", dpi=120)
    plt.show()
    print("Plot saved → explained_variance.png")


def plot_pc_images(pca: PCA):
    """Visualise the first N principal components as images."""
    n = min(N_SHOW_PC, pca.n_components_)
    fig, axes = plt.subplots(1, n, figsize=(3 * n, 3))
    if n == 1:
        axes = [axes]

    for i, ax in enumerate(axes):
        pc_img = pca.components_[i].reshape(*IMG_SIZE, 3) # Change 3 to 1 for greyscale and change ax.imshow(pc_img, cmap="gray")
        # normalise to [0, 1] for display
        pc_img = (pc_img - pc_img.min()) / (pc_img.max() - pc_img.min() + 1e-8)
        ax.imshow(pc_img)
        ax.set_title(f"PC {i+1}")
        ax.axis("off")

    plt.suptitle("Principal Component Images", fontsize=13)
    plt.tight_layout()
    plt.savefig("pc_images.png", dpi=120)
    plt.show()
    print("Plot saved → pc_images.png")


def plot_scatter(scores: np.ndarray, names: list[str]):
    """2-D scatter of the first two PCs."""
    plt.figure(figsize=(8, 6))
    plt.scatter(scores[:, 0], scores[:, 1], alpha=0.7, edgecolors="k", linewidths=0.4)

    for i, name in enumerate(names):
        plt.annotate(name, (scores[i, 0], scores[i, 1]),
                     fontsize=7, alpha=0.6,
                     xytext=(4, 4), textcoords="offset points")

    plt.xlabel("PC 1")
    plt.ylabel("PC 2")
    plt.title("Image PCA — PC1 vs PC2")
    plt.tight_layout()
    plt.savefig("pca_scatter.png", dpi=120)
    plt.show()
    print("Plot saved → pca_scatter.png")


def main():
    # Load
    X, names = load_images()

    # PCA
    pca, scores, _ = run_pca(X, n_components)
    print(f"PCA done — kept {pca.n_components_} components "
          f"({pca.explained_variance_ratio_.sum()*100:.1f}% variance)")

    # Save CSV
    save_scores(scores, names)

    # Plots
    # plot_explained_variance(pca)
    plot_pc_images(pca)
    # if scores.shape[1] >= 2:
    #     plot_scatter(scores, names)


if __name__ == "__main__":
    main()

# 77, 76, 181, 182