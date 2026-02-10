"""
This script prepares histology images for downstream cell segmentation

It automatically:
- inverts pixel intensities
- boosts contrast by a fixed factor (default: 1.2)

Input is assumed to be in:
    1_datasets/Colon_Benign_Tissue

The script creates a new output folder inside:
    2_data_preparation/

Raw images are never changed. The processed copies are saved into the new folder.

NOTE:
- If you want a different contrast strength, change the CONTRAST_FACTOR value
  in the CONFIG section below.
"""

from pathlib import Path
import numpy as np
from PIL import Image, UnidentifiedImageError


# -----------------------------
# CONFIG (edit if needed)
# -----------------------------
IN_DIR = Path(r"1_datasets/Colon_Benign_Tissue")

# Change this if you want stronger/weaker contrast (e.g., 1.1 or 1.3)
CONTRAST_FACTOR = 1.2
# -----------------------------

# Output folder will be created here automatically
OUT_DIR = (
    Path(r"2_data_preparation")
    / f"Colon_Benign_Tissue_invert_contrast{str(CONTRAST_FACTOR).replace('.', 'p')}"
)


IMG_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def apply_contrast_uint8(img_u8: np.ndarray, factor: float) -> np.ndarray:
    """
    Contrast around mid-gray 128 for uint8 images:
        out = (img - 128) * factor + 128
    """
    x = img_u8.astype(np.float32)
    y = (x - 128.0) * factor + 128.0
    y = np.clip(y, 0, 255).astype(np.uint8)
    return y


def process_image(path: Path, out_path: Path, contrast_factor: float) -> bool:
    """
    Returns True if processed successfully, False if skipped due to unreadable file.
    """
    try:
        im = Image.open(path)

        # Normalize modes for consistent output
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")

        arr = np.array(im)

        # Ensure uint8
        if arr.dtype != np.uint8:
            arr = np.clip(arr, 0, 255).astype(np.uint8)

        # Invert intensities (always on)
        arr = 255 - arr

        # Contrast boost (always on)
        arr = apply_contrast_uint8(arr, contrast_factor)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(arr).save(out_path)
        return True

    except (UnidentifiedImageError, OSError, ValueError):
        return False


def list_images(folder: Path):
    return sorted(
        [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMG_EXTS]
    )


def main():
    if not IN_DIR.exists():
        raise FileNotFoundError(f"Input folder not found: {IN_DIR.resolve()}")

    paths = list_images(IN_DIR)

    if not paths:
        print(
            f"[WARN] No images found in {IN_DIR.resolve()} with extensions {sorted(IMG_EXTS)}"
        )
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    n_done = 0
    n_bad = 0

    for p in paths:
        # Preserve relative structure if there are subfolders
        rel = p.relative_to(IN_DIR)
        out_path = OUT_DIR / rel

        ok = process_image(p, out_path, contrast_factor=CONTRAST_FACTOR)
        if ok:
            n_done += 1
        else:
            n_bad += 1

    print(f"[INFO] Input folder : {IN_DIR.resolve()}")
    print(f"[INFO] Output folder: {OUT_DIR.resolve()}")
    print(f"[INFO] Contrast factor: {CONTRAST_FACTOR}")
    print("[INFO] Invert: True")
    print(f"[INFO] Processed: {n_done}")
    print(f"[INFO] Unreadable/skipped: {n_bad}")


if __name__ == "__main__":
    main()
