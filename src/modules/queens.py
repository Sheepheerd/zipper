from PIL import Image
import numpy as np
import cv2

TARGET_SIZE = 420
GRID_SIZE = 6
WHITE_THRESHOLD = 0.95
BLACK_THRESHOLD = 0.05


class Queens:
    def build_instructions(self, filename):
        arr, grid_size = analyze_image(filename)


        
        path = create_path(arr, grid_size, filename)
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


# REFACTOR LATER TO SPERATE FUNCS
def create_path(arr, grid_size, filename):
    path = []

    if grid_size == 7:
        crown_template = 'images/9-crown.png'
    elif grid_size == 8:
        crown_template = 'images/8-crown.png'
    elif grid_size == 9:
        crown_template = 'images/9-crown.png'
    else:
        raise ValueError("Undefined queens size")

    crown_template_img = cv2.imread(crown_template)
    solution = cv2.imread(filename)

    template_gray = cv2.cvtColor(crown_template_img, cv2.COLOR_BGR2GRAY)
    solution_gray = cv2.cvtColor(solution, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(
        solution_gray,
        template_gray,
        cv2.TM_CCOEFF_NORMED
    )

    threshold = 0.5
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    img_h, img_w = solution_gray.shape
    cell_w = img_w / grid_size
    cell_h = img_h / grid_size

    t_h, t_w = template_gray.shape

    path_set = set()

    for x_px, y_px in locations:
        cx = x_px + t_w // 2
        cy = y_px + t_h // 2

        col = int(cx // cell_w)
        row = int(cy // cell_h)

        if 0 <= row < grid_size and 0 <= col < grid_size:
            path_set.add((row, col))

    path = list(path_set)
    double_path = list()
    for value in path:
        double_path.append(value)
        double_path.append(value)
    return double_path

