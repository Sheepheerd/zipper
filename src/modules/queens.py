import numpy as np
import cv2

TEMPLATE_DIR = 'templates/queens'

class Queens:
    def build_instructions(self, filename):        

        grid_size = infer_grid_size(filename)

        path = create_path(grid_size, filename)
        return path, grid_size


def infer_grid_size(filename):
    counts = count_queens(filename)

    for grid_size, count in counts.items():
        if count == grid_size:
            return grid_size

    raise RuntimeError(
        f"Could not infer grid size from queen counts: {counts}"
    )

# REFACTOR THIS
def count_queens(filename):
    candidates = {
        7: f'{TEMPLATE_DIR}/7-crown.png',
        8: f'{TEMPLATE_DIR}/8-crown.png',
        9: f'{TEMPLATE_DIR}/9-crown.png',
    }

    solution = cv2.imread(filename)
    solution_gray = cv2.cvtColor(solution, cv2.COLOR_BGR2GRAY)

    img_h, img_w = solution_gray.shape

    results = {}

    for grid_size, template_path in candidates.items():
        template = cv2.imread(template_path)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(
            solution_gray,
            template_gray,
            cv2.TM_CCOEFF_NORMED
        )

        threshold = 0.5
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        cell_w = img_w / grid_size
        cell_h = img_h / grid_size

        t_h, t_w = template_gray.shape

        queens = set()

        for x_px, y_px in locations:
            cx = x_px + t_w // 2
            cy = y_px + t_h // 2

            col = int(cx // cell_w)
            row = int(cy // cell_h)

            if 0 <= row < grid_size and 0 <= col < grid_size:
                queens.add((row, col))

        results[grid_size] = len(queens)

    return results



# REFACTOR LATER TO SPERATE FUNCS
def create_path(grid_size, filename):
    path = []

    if grid_size == 7:
        crown_template = f'{TEMPLATE_DIR}/7-crown.png'
    elif grid_size == 8:
        crown_template = f'{TEMPLATE_DIR}/8-crown.png'
    elif grid_size == 9:
        crown_template = f'{TEMPLATE_DIR}/9-crown.png'
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

