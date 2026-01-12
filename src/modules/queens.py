from PIL import Image
import numpy as np

TARGET_SIZE = 420
GRID_SIZE = 6
WHITE_THRESHOLD = 0.95
BLACK_THRESHOLD = 0.05


class Queens:
    def build_instructions(self, filename):
        arr, grid_size = analyze_image(filename)

        chunks = split_into_chunks(arr, grid_size)

        
        path = create_path(chunks)
        return path, grid_size


def analyze_image(path):
    """
    """

    img = Image.open(path).convert("L")
    arr = np.asarray(img, dtype=np.float32) / 255.0





    grid_size = 0
    
    x_7 = 200
    y_7 = 233

    x_8 = 205
    y_8 = 205

    x_9 = 183
    y_9 = 183

    
    if arr[y_7][x_7] <= BLACK_THRESHOLD:
        print("Its grid size 7")
        grid_size = 7
    elif arr[y_8][x_8] <= BLACK_THRESHOLD:
        print("Its grid size 8")
        grid_size = 8
    elif arr[y_9][x_9] <= BLACK_THRESHOLD:
        print("Its grid size 9")
        grid_size = 9

    img = img.resize((TARGET_SIZE, TARGET_SIZE), Image.NEAREST)

    return arr, grid_size


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

def create_path(chunks):
    """
    """
    # x, y = 30, 30
    # path = []
    #
    # for i in range(len(chunks)):
    #     for j in range(len(chunks[i])):
    #         path.append((i, j))
    #
    # for row_idx, row in enumerate(chunks):
    #     for col_idx, chunk in enumerate(row):  
    #         h, w = chunk.shape
    #         if y < h and x < w:
    #             if chunk[y, x] >= WHITE_THRESHOLD:
    #                 path.append((row_idx, col_idx)) 
    # print(path)    
    # return path

