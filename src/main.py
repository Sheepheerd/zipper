from PIL import Image
import numpy as np

TARGET_SIZE = 420
GRID_6 = 6
GRID_7 = 7
CHUNK_6 = 70
CHUNK_7 = 60
WHITE_THRESHOLD = 0.95

DELAY_BETWEEN_CLICKS = 0.05
SCALE_FACTOR = 1.6
GRID_SIZE = 7

DIRECTIONS = {
    "top":    (-1,  0),
    "bottom": ( 1,  0),
    "left":   ( 0, -1),
    "right":  ( 0,  1),
}

OPPOSITE = {
    "top": "bottom",
    "bottom": "top",
    "left": "right",
    "right": "left",
}

import requests
from datetime import datetime, timedelta


def download_image(url, save_as):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=12)
        
        if response.status_code == 200:
            # Optional: check if it's actually an image
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type:
                print(f"Warning: Response is not an image (Content-Type: {content_type})")
                return False
            
            with open(save_as, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Successfully saved: {save_as}")
            print(f"File size: {len(response.content) / 1024:.1f} KB")
            return True
        
        else:
            print(f"Failed – HTTP {response.status_code}")
            if response.status_code == 404:
                print("Puzzle image for today may not be uploaded yet.")
            return False
            
    except Exception as e:
        print(f"Download error: {e}")
        return False


def analyze_image(path):
    """
    Load the image, normalize it, and determine whether it represents
    a 6x6 or 7x7 grid by sampling a known diagnostic pixel.
    """

    img = Image.open(path).convert("L")
    img = img.resize((TARGET_SIZE, TARGET_SIZE), Image.NEAREST)

    arr = np.asarray(img, dtype=np.float32) / 255.0

    # middle of the image
    x, y = 206, 192

    x = min(x, arr.shape[1] - 1)
    y = min(y, arr.shape[0] - 1)

    if arr[y, x] >= WHITE_THRESHOLD:
        grid_size = 6
    else:
        grid_size = 7

    return arr, grid_size

def build_edge_map(chunks):
    """
    Build a grid of edge-activity dictionaries.
    """

    grid_size = len(chunks)
    edge_map = [[None]*grid_size for _ in range(grid_size)]

    for r in range(grid_size):
        for c in range(grid_size):
            edges, active_count = chunk_edge_activity(chunks[r][c])
            edge_map[r][c] = edges

    return edge_map


def trace_path(start, edge_map):
    grid_size = len(edge_map)

    path_grid = [[-1]*grid_size for _ in range(grid_size)]

    r, c = start["row"], start["col"]
    entry_edge = OPPOSITE[start["edge"]]
    step = 0

    while True:
        path_grid[r][c] = step
        step += 1

        edges = edge_map[r][c]

        exit_edges = [
            e for e, active in edges.items()
            if active and e != entry_edge
        ]

        if not exit_edges:
            break

        if len(exit_edges) > 1:
            raise RuntimeError("Branching path detected")

        exit_edge = exit_edges[0]
        dr, dc = DIRECTIONS[exit_edge]
        nr, nc = r + dr, c + dc

        if not (0 <= nr < grid_size and 0 <= nc < grid_size):
            break

        r, c = nr, nc
        entry_edge = OPPOSITE[exit_edge]

    return path_grid

def chunk_is_empty(chunk):
    """
    A chunk is considered empty if all its pixels are white.
    """
    return np.all(chunk >= WHITE_THRESHOLD)

def chunk_edge_activity(chunk):
    """
    Determine which edges of a chunk contain non-white pixels.

    Returns:
        edges: dict[str, bool]
        active_count: int
    """

    h, w = chunk.shape

    edges = {
        "top": False,
        "bottom": False,
        "left": False,
        "right": False,
    }

    for x in range(w):
        if chunk[0, x] < WHITE_THRESHOLD:
            edges["top"] = True
        if chunk[h - 1, x] < WHITE_THRESHOLD:
            edges["bottom"] = True

    for y in range(h):
        if chunk[y, 0] < WHITE_THRESHOLD:
            edges["left"] = True
        if chunk[y, w - 1] < WHITE_THRESHOLD:
            edges["right"] = True

    active_count = sum(edges.values())
    return edges, active_count



def find_starting_chunk(chunks, direction="top"):
    """
    Finds first non-empty chunk with exactly one active edge,
    searching either from top or from bottom.
    """
    grid_size = len(chunks)
    
    for r in range(grid_size):
        for c in range(grid_size):
            chunk = [] 
            if direction == "top":
                chunk = chunks[r][c]
            elif direction == "bottom":
                chunk = chunks[grid_size - r - 1][grid_size - c - 1]

            if chunk_is_empty(chunk):
                continue
                
            edges, active_count = chunk_edge_activity(chunk)
            print(edges, active_count)
            
            if active_count == 1:
                edge = next(iter(k for k, v in edges.items() if v))

                if direction == "top":
                    return {"row": r, "col": c, "edge": edge}
                if direction == "bottom":
                    return {"row": grid_size - r - 1, "col": grid_size - c - 1, "edge": edge}
                
    return None

def split_into_chunks(arr, grid_size):
    """
    Split the normalized image array into a grid of equally sized chunks.
    Returns a 2D list of chunks.
    """

    chunk_size = TARGET_SIZE // grid_size
    chunks = []

    for row in range(grid_size):
        row_chunks = []
        for col in range(grid_size):
            y0 = row * chunk_size
            y1 = y0 + chunk_size
            x0 = col * chunk_size
            x1 = x0 + chunk_size

            chunk = arr[y0:y1, x0:x1]
            row_chunks.append(chunk)

        chunks.append(row_chunks)

    return chunks



# CLICKER PART

from wayland_automation.mouse_controller import Mouse

import subprocess
import sys
import time


def to_physical(logical_x, logical_y, logical_w=None, logical_h=None):
    """Convert logical → physical coordinates"""
    x = round(logical_x * SCALE_FACTOR)
    y = round(logical_y * SCALE_FACTOR)
    if logical_w is not None and logical_h is not None:
        w = round(logical_w * SCALE_FACTOR)
        h = round(logical_h * SCALE_FACTOR)
        return x, y, w, h
    return x, y

def get_selection():
    try:
        # slurp outputs: "X Y W H" (top-left + size)
        output = subprocess.check_output(["slurp", "-f", "%x %y %w %h"], text=True).strip()
        x, y, w, h = map(int, output.split())
        return x, y, w, h
    except subprocess.CalledProcessError:
        print("Selection cancelled or slurp failed", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("Error: 'slurp' not found → please install it!", file=sys.stderr)
        sys.exit(1)


def get_grid_cell(x: int, y: int, w: int, h: int, grid_x: int, grid_y: int, grid_size: int = 6) -> tuple[int, int]:
    """Convert grid coordinates (0..5, 0..5) → screen coordinates""" 
    cell_w = w // grid_size
    cell_h = h // grid_size
    
    # Center of the cell
    center_x = x + (grid_x * cell_w) + (cell_w // 2)
    center_y = y + (grid_y * cell_h) + (cell_h // 2)
    
    return to_physical(center_x, center_y)


def find_position(grid, target):
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == target:
                return row_idx, col_idx
    return None 


def main():
    REFERENCE_DATE = datetime(2026, 1, 9)
    REFERENCE_NUMBER = 298

    today = datetime.now().date()
    today_dt = datetime.combine(today, datetime.min.time())

    days_diff = (today_dt - REFERENCE_DATE).days

    # today_number = REFERENCE_NUMBER + days_diff
    today_number = 298

    base_url = "https://tryhardguides.com/wp-content/uploads/2025/05/Zip-answer-"
    image_url = f"{base_url}{today_number}.jpg"

    filename = f"zip_answer_{today_number}.png"

    print(f"Today's date: {today.strftime('%Y-%m-%d')}")
    print(f"LinkedIn ZIP Puzzle number: #{today_number}")
    print(f"Downloading from: {image_url}\n")


    success = download_image(image_url, filename)
    
    if not success:
        print("\nTip: Try running again later – TryHardGuides usually uploads early in the day.")
        print("You can also check manually: https://tryhardguides.com/linkedin-zip-answer-today/")


    # ANSWER PART

    arr, grid_size = analyze_image(filename)

    chunks = split_into_chunks(arr, grid_size)

    # start_top = find_starting_chunk(chunks, "top")
    start_bottom = find_starting_chunk(chunks,"bottom")


    edge_map = build_edge_map(chunks)

    # path_grid = trace_path(start_top, edge_map)

    path_grid = trace_path(start_bottom, edge_map)


    # CLICKER PART

    result = get_selection()
    if result is None:
        return

    log_x, log_y, log_w, log_h = result


    print(f"Logical  (what slurp sees) : {log_x},{log_y}  {log_w}×{log_h}")
    phys_x, phys_y, phys_w, phys_h = to_physical(log_x, log_y, log_w, log_h)
    print(f"Physical (real pixels)     : {phys_x},{phys_y}  {phys_w}×{phys_h}")


    # WRAP IN FOR LOOP TO PRESS EACH COL IN THE CORRECT ORDER

    path_grid = trace_path(start_bottom, edge_map)

    mouse = Mouse()

    for i in range(GRID_SIZE * GRID_SIZE):
        target_row, target_col = find_position(path_grid, i)
        click_x, click_y = get_grid_cell(
            log_x, log_y, log_w, log_h,
            grid_x=target_col,
            grid_y=target_row,
            grid_size=GRID_SIZE
        )

        print(f"→ {i}/{len(path_grid)}   Cell [{target_col},{target_row}] "
              f"→ physical ({click_x}, {click_y})")

        mouse.click(click_x, click_y, button="left")

        if i < GRID_SIZE * GRID_SIZE:
            print("   waiting...")
            time.sleep(DELAY_BETWEEN_CLICKS)

    print("\nSequence complete! ✓")



if __name__ == "__main__":
    main()

