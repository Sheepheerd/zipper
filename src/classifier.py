import cv2
import numpy as np
import os

# ----------------------------- CONFIG -----------------------------
TEMPLATE_PATHS = [
    'template_1_a.png',
    'template_1_b.png',
    'template_1_c.png',
    'template_1_d.png',
]

PERFECT_MATCH_THRESHOLD = 1.0
# -----------------------------------------------------------------

def is_one(image_path):
    # Load the test image (the chunk you want to classify) in grayscale
    test_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if test_img is None:
        print(f"Error: Could not load image {image_path}")
        return False

    matched = False
    best_score = 0.0
    best_template = None

    for template_path in TEMPLATE_PATHS:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"Warning: Could not load template {template_path}")
            continue

        template_h, template_w = template.shape

        test_resized = cv2.resize(test_img, (template_w, template_h))

        result = cv2.matchTemplate(test_resized, template, cv2.TM_CCOEFF_NORMED)

        _, max_val, _, _ = cv2.minMaxLoc(result)

        print(f"  vs {os.path.basename(template_path)} -> score: {max_val:.5f}")

        if max_val > best_score:
            best_score = max_val
            best_template = template_path

        if max_val >= PERFECT_MATCH_THRESHOLD: 
            matched = True

    print(f"Best score: {best_score:.5f} (with {os.path.basename(best_template)})")

    if matched:
        return True
    else:
        return False


# ----------------------------- USAGE EXAMPLE -----------------------------
if __name__ == "__main__":
    chunk_images = [
        'chunk_1.png',
        'chunk_2.png',
        'chunk_3.png',
        'chunk_4.png',
        'chunk_5.png',
        'chunk_6.png',
        'chunk_7.png',
        'chunk_8.png',
    ]

    for chunk in chunk_images:
        print(f"Testing {chunk}:")
        if is_one(chunk):
            print(f"{chunk} => IT'S A ONE!\n")
        else:
            print(f"{chunk} => not a one\n")
