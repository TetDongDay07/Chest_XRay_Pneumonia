# Pneumonia Detection from Chest X-rays (ResNet18)

Binary classification (NORMAL vs PNEUMONIA) on the Kaggle _Chest X-Ray Images (Pneumonia)_ dataset, with a focus on **checking whether the model learns real signal or dataset shortcuts**.

> Research/learning project. Not a diagnostic tool.

## Setup

- **Data:** pediatric chest X-rays, single source. The original 16-image validation folder was merged into train, then split **by patient ID** (80/20) to avoid leakage. Validation: 1,047 images (270 NORMAL / 777 PNEUMONIA). Test: original test set, 624 images (234 / 390), used once.
- **Model:** ImageNet-pretrained ResNet18 last block, Data augmentation, class-weighted loss, cosine LR, early stopping on validation AUC. Seed 36.
- **Augmentation variants:** `none`, `shortcut` (random resized crop with aspect jitter, blur, affine, color jitter, random border dropout).
- **Operating point:** threshold chosen on validation for recall >= 0.95 (0.764 for aug and 0.695 for none_aug)

## Findings

**1. Validation is too easy.** All models reach val AUC 0.998-0.9998. A gradient-boosting model using only image width, height, mean and std gets **AUC 0.954** (val) and 0.915 (test). In validation, images with height <= 890 px are 99% pneumonia (520 vs 5).

**2. The CNN uses the image periphery.** For the no-augmentation model:

| Check                                       | Result                    |
| ------------------------------------------- | ------------------------- |
| Grad-CAM border energy (NORMAL / PNEUMONIA) | 0.249 / 0.354             |
| AUC with only the four corners visible      | 0.90 (full image: 0.9998) |

**3. Shortcut-targeted augmentation reduces this reliance (does not remove it).**

||none|shortcut|
|---|---|---|
|Corners-only AUC|0.901|0.833|
|Border-energy gap between classes|0.146|0.036|

## Test results (thresholds fixed on validation)

| Model          | AUC (95% CI)         | Recall | Specificity |
| -------------- | -------------------- | ------ | ----------- |
| `aug_shortcut` | 0.979 [0.967, 0.99]  | 0.982  | 0.885       |
| `aug_none`     | 0.940 [0.919, 0.959] | 0.997  | 0.543       |


## Conclusions

- Validation AUC is a poor guide here; test AUC is lower (0.977 / 0.948).
- The CNN carries information beyond size and brightness, and shortcut-aware augmentation helps on test.
- The model is still not independent of image size, so it should not be claimed to detect pneumonia independently of acquisition cues.

## Limitations

Single seed; single-source pediatric data; test set from the same source; several augmentation components changed at once; test inspected after the single evaluation for error analysis only.

## Future work

Size-balanced or propensity-weighted training, multiple seeds, external validation data, lung segmentation to mask non-lung regions.