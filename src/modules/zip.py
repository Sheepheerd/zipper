from PIL import Image
import numpy as np
import cv2


TARGET_SIZE = 420
WHITE_THRESHOLD = 0.80

TEMPLATE_DIR = 'templates/zip'

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

class Zip:
    def build_instructions(self, filename):
        arr, grid_size = analyze_image(filename)

        chunks = split_into_chunks(arr, grid_size)

        start_chunk = find_starting_chunk(chunks, filename)


        edge_map = build_edge_map(chunks)

        path_grid = trace_path(start_chunk, edge_map)

        return path_grid, grid_size



def find_starting_chunk(chunks, filename):
    grid_size = len(chunks)
    chunk_size = 420 // grid_size

    template = cv2.imread(f'{TEMPLATE_DIR}/6-1.png')
    solution = cv2.imread(filename)

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    solution_gray = cv2.cvtColor(solution, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(
        solution_gray,
        template_gray,
        cv2.TM_CCOEFF_NORMED
    )

    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    threshold = 0.85
    if max_val < threshold:
        raise ValueError("Starting chunk not found with sufficient confidence")

    x_px, y_px = max_loc 

    t_h, t_w = template_gray.shape
    cx = x_px + t_w // 2
    cy = y_px + t_h // 2

    col = cx // chunk_size
    row = cy // chunk_size

    if not (0 <= row < grid_size and 0 <= col < grid_size):
        raise IndexError("Computed chunk index out of bounds")

    return row, col

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


def analyze_image(path):
    """
    Load the image, normalize it, and determine whether it represents
    a 6x6 or 7x7 grid by sampling a known diagnostic pixel.
    """

    img = Image.open(path).convert("L")
    img = img.resize((TARGET_SIZE, TARGET_SIZE), Image.NEAREST)

    arr = np.asarray(img, dtype=np.float32) / 255.0

    # middle of the image, might need to fix if the zip can have images greater than 6 and 7 ;)
    x6, y6, = 203, 215
    x7, y7 = 233, 178
    x8, y8 = 94, 273

    # x, y = 205, 205
    # x2, y2 = 206, 179

    # x6 = min(x, arr.shape[1] - 1)
    # y6 = min(y, arr.shape[0] - 1)
    # x7 = min(x, arr.shape[1] - 1)
    # y7 = min(y, arr.shape[0] - 1)
    # x8 = min(x, arr.shape[1] - 1)
    # y8 = min(y, arr.shape[0] - 1)

    if arr[y8, x8] >= WHITE_THRESHOLD:
        grid_size = 8
    elif arr[y6, x6] >= WHITE_THRESHOLD:
        grid_size = 6
    elif arr[y7, x7] >= WHITE_THRESHOLD:
        grid_size = 7
    else:
        grid_size = 9

    return arr, grid_size

def build_edge_map(chunks):
    """
    Build a grid of edge-activity dictionaries.
    """

    grid_size = len(chunks)
    edge_map = [[None]*grid_size for _ in range(grid_size)]

    for r in range(grid_size):
        for c in range(grid_size):
            edges, _ = chunk_edge_activity(chunks[r][c])
            edge_map[r][c] = edges

    return edge_map

def trace_path(start, edge_map):
    """
    Traces a single non-branching path through the grid.

    Args:
        start: (row, col) tuple
        edge_map: grid_size × grid_size × dict of {edge_dir: bool}

    Returns:
        list of (row, col) tuples in visit order
    """
    path = []

    r, c = start
    entry_edge = None

    path.append((r, c))
    grid_size = len(edge_map)

    while True:
        edges = edge_map[r][c]

        if entry_edge is None:
            exit_edges = [e for e, active in edges.items() if active]
        else:
            exit_edges = [
                e for e, active in edges.items()
                if active and e != entry_edge
            ]

        if not exit_edges:
            break

        if len(exit_edges) > 1:
            raise RuntimeError(
                f"Branching path detected at ({r}, {c})"
            )

        exit_edge = exit_edges[0]
        dr, dc = DIRECTIONS[exit_edge]
        nr, nc = r + dr, c + dc

        if not (0 <= nr < grid_size and 0 <= nc < grid_size):
            break

        r, c = nr, nc
        entry_edge = OPPOSITE[exit_edge]

        path.append((r, c))

    print(path)
    return path

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



