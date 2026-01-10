from wayland_automation.mouse_controller import Mouse
import subprocess
import sys
import time

DELAY_BETWEEN_CLICKS = 0.01
SCALE_FACTOR = 1.6
GRID_SIZE = 7


class Solver:
    def __init__(self) -> None:
        self.mouse = Mouse()

    def solve(self, path_grid):
        result = get_selection()
        if result is None:
            return

        log_x, log_y, log_w, log_h = result


        print(f"Logical  (what slurp sees) : {log_x},{log_y}  {log_w}×{log_h}")
        phys_x, phys_y, phys_w, phys_h = to_physical(log_x, log_y, log_w, log_h)
        print(f"Physical (real pixels)     : {phys_x},{phys_y}  {phys_w}×{phys_h}")


        # WRAP IN FOR LOOP TO PRESS EACH COL IN THE CORRECT ORDER


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

            self.mouse.click(click_x, click_y, button="left")

            if i < GRID_SIZE * GRID_SIZE:
                print("   waiting...")
                time.sleep(DELAY_BETWEEN_CLICKS)

        print("\nSequence complete! ✓")

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
