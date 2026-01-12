from modules import Zip, Tango
from solver import Solver
from modules import Downloader


def main():
    print("Choose a mode:")
    print("  1) zip")
    print("  2) queens")
    print("  3) tango")

    choice = input("> ").strip()

    solver = Solver()
    downloader = Downloader()
    grid_size = 0
    if choice == "1":
        zip_mode = Zip()
        filename = downloader.download_image("Zip")
        grid_path, grid_size = zip_mode.build_instructions(filename)

    # elif choice == "2":
    #     queens_mode = Queens()
    #     filename = downloader.download_image("queens")
    #     grid_path = queens_mode.build_instructions(filename)

    elif choice == "3":
        tango_mode = Tango()
        filename = downloader.download_image("Tango")
        grid_path = tango_mode.build_instructions(filename)

    else:
        print("Invalid selection.")
        return

    solver.solve(grid_path, grid_size)





if __name__ == "__main__":
    main()

