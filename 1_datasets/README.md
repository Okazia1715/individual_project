# Dataset Documentation

## Dataset Overview

This project uses a subset of the **LC25000 – Lung and Colon Cancer Histopathological Images**
dataset.

The original dataset consists of **25,000 histopathological RGB images** distributed evenly
across **five tissue classes** (5,000 images per class).
All images are stored in **JPEG format** with a resolution of **768 × 768 pixels**.

The images were generated from an original collection of **HIPAA-compliant and validated
histopathological sources** and expanded to 25,000 samples using data augmentation techniques.

**Original tissue classes:**

1. Lung benign tissue  
2. Lung adenocarcinoma  
3. Lung squamous cell carcinoma  
4. Colon adenocarcinoma  
5. Colon benign tissue  

> *“All images are de-identified, HIPAA compliant, validated, and freely available for download
> to AI researchers.”*  
> — Borkowski et al., 2019

**Kaggle dataset link:**  
*[https://www.kaggle.com/datasets/biplobdey/lung-and-colon-cancer]*

**Original publication:**  
*[https://arxiv.org/abs/1912.12142v1]*

---

## Dataset Usage in This Project

Although the original dataset contains five tissue classes, **this project uses only a single
subset**:

> **Colon benign tissue (class #5)**

Only images belonging to this class are included in the analysis and modeling pipeline.
All other tissue classes are excluded from this project.

The dataset is used for computer vision and machine learning experiments focused on
histopathological image analysis.

---

## Dataset Storage

The original, unmodified dataset is stored in a dedicated raw data folder named:
Lung_and_Colon_Cancer/
