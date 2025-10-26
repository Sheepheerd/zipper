import easyocr
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import os

def detect_digits_easyocr(image_path, reader=None):
    """
    Enhanced EasyOCR with preprocessing and allowlist:
    - Crops to grayscale, enhances contrast, binarizes for better detection.
    - Uses digit allowlist to force 0-9 only.
    - Saves ALL cropped cells to 'crop_i_j.png' for manual inspection.
    - Takes highest-confidence digit (or first if tie); lowers effective threshold via preprocessing.
    
    Args:
    - image_path (str): Path to image.
    - reader (easyocr.Reader, optional): Pre-initialized.
    
    Returns:
    - np.ndarray: 6x6 string array of digits or ' '.
    """
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)
    
    # Load image
    img = Image.open(image_path).convert('RGB')  # Ensure RGB
    width, height = img.size
    assert width == 410 and height == 410, "Image must be 410x410"
    
    print(f"Loaded image: {width}x{height}")
    
    n = 6
    cell_width = width // n  # 68
    remainder_w = width % n   # 2
    cell_height = height // n  # 68
    remainder_h = height % n   # 2
    
    col_sizes = [cell_width + 1 if j < remainder_w else cell_width for j in range(n)]
    row_sizes = [cell_height + 1 if i < remainder_h else cell_height for i in range(n)]
    
    row_starts = np.cumsum([0] + row_sizes[:-1])
    col_starts = np.cumsum([0] + col_sizes[:-1])
    
    grid = np.full((n, n), ' ', dtype=str)
    
    for i in range(n):
        row_start = row_starts[i]
        row_end = row_start + row_sizes[i]
        
        for j in range(n):
            col_start = col_starts[j]
            col_end = col_start + col_sizes[j]
            
            # Crop RGB
            cell_rgb = img.crop((col_start, row_start, col_end, row_end))
            
            # Preprocess: Grayscale, enhance contrast, binarize
            cell_gray = cell_rgb.convert('L')
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(cell_gray)
            cell_enhanced = enhancer.enhance(2.0)  # Boost by 2x; tune if overkill
            # Binarize (threshold at 128, adjust if needed)
            cell_binary = cell_enhanced.point(lambda p: 0 if p < 128 else 255, '1')
            # Optional: Invert if light digits on dark bg
            # cell_binary = ImageOps.invert(cell_binary)
            
            # Save crop for inspection
            crop_path = f'crop_{i}_{j}.png'
            cell_binary.save(crop_path)
            print(f"Saved {crop_path} for cell [{i},{j}]")
            
            # Run EasyOCR on binary (numpy array)
            results = reader.readtext(np.array(cell_binary), allowlist='0123456789', detail=1)
            
            digit = ' '
            max_conf = -1
            for (bbox, text, conf) in results:
                text = text.strip()
                if len(text) == 1 and text.isdigit():
                    if conf > max_conf:
                        digit = text
                        max_conf = conf
                    print(f"Cell [{i},{j}]: Candidate '{text}' (conf: {conf:.2f})")
            
            if digit != ' ':
                print(f"Cell [{i},{j}]: Selected '{digit}' (best conf: {max_conf:.2f})")
            else:
                print(f"Cell [{i},{j}]: No digit detected")
            
            grid[i, j] = digit
    
    print(f"Final grid:\n{grid}")
    print(f"Detected {np.sum(grid != ' ')} digits total")
    return grid

# Example usage:
grid = detect_digits_easyocr('Zip-answer-100.jpg')
# To ints: np.where(grid == ' ', 0, grid.astype(int))
