from PIL import Image
import numpy as np


TARGET_SIZE = 420
GRID_6 = 6
GRID_7 = 7
CHUNK_6 = 70
CHUNK_7 = 60
WHITE_THRESHOLD = 0.95

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

        # start_top = find_starting_chunk(chunks, "top")
        start_bottom = find_starting_chunk(chunks,"bottom")


        edge_map = build_edge_map(chunks)

        # path_grid = trace_path(start_top, edge_map)
        path_grid = trace_path(start_bottom, edge_map)
        print(path_grid)
        return path_grid, grid_size





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

    # middle of the image
    x, y = 205, 205

    x = min(x, arr.shape[1] - 1)
    y = min(y, arr.shape[0] - 1)

    if arr[205, 205] >= WHITE_THRESHOLD:
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
    """
    Traces a single non-branching path through the grid.
    
    Args:
        start: dict with 'row', 'col', and 'edge' (entry edge)
        edge_map: grid_size × grid_size × dict of {edge_dir: bool}
    
    Returns:
        list of (row, col) tuples in visit order, starting with the start position
    """
    path = []
    r, c = start["row"], start["col"]
    entry_edge = OPPOSITE[start["edge"]]
    
    path.append((r, c))

    grid_size = len(edge_map)

    while True:
        edges = edge_map[r][c]
        
        exit_edges = [
            e for e, active in edges.items()
            if active and e != entry_edge
        ]

        if not exit_edges:
            break

        if len(exit_edges) > 1:
            raise RuntimeError("Branching path detected at ({}, {})".format(r, c))

        exit_edge = exit_edges[0]
        dr, dc = DIRECTIONS[exit_edge]
        nr, nc = r + dr, c + dc

        if not (0 <= nr < grid_size and 0 <= nc < grid_size):
            break

        r, c = nr, nc
        entry_edge = OPPOSITE[exit_edge] 
       
        path.append((r, c))
    return path

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


