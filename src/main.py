# from wayland_automation.mouse_controller import Mouse
#
# mouse = Mouse()
# mouse.click(100, 200, button="left")  # Perform a left click
# mouse.swipe(100, 200, 400, 500, speed=.1)



# We need to write a program that will take an image, and create
# a list of instruction to execute

from PIL import Image
import numpy as np

TARGET_SIZE = 420
GRID_6 = 6
GRID_7 = 7
CHUNK_6 = 70
CHUNK_7 = 60
WHITE_THRESHOLD = 0.95  # anything >= 0.95 is considered white


def analyze_image(path):
    # Load and scale image
    img = Image.open(path).convert("L")
    img = img.resize((TARGET_SIZE, TARGET_SIZE), Image.NEAREST)

    arr = np.asarray(img, dtype=np.float32) / 255.0

    x, y = 206, 192

    x = min(x, arr.shape[1] - 1)
    y = min(y, arr.shape[0] - 1)

    if arr[y, x] >= WHITE_THRESHOLD:
        grid_size = 6
    else:
        grid_size = 7

    return {"grid_size": grid_size, "pixel_checked": (x, y), "value": arr[y, x]}


if __name__ == "__main__":
    result = analyze_image("input.png")
    print(result)

