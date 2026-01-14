from modules import Zip, Tango, Queens
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
    filename = ""
    if choice == "1":
        zip_mode = Zip()
        filename = downloader.download_image("Zip")
        grid_path, grid_size = zip_mode.build_instructions(filename)

    elif choice == "2":
        queens_mode = Queens()
        filename = downloader.download_image("queens")
        grid_path,grid_size = queens_mode.build_instructions(filename)

    elif choice == "3":
        tango_mode = Tango()
        filename = downloader.download_image("Tango")
        grid_path, grid_size = tango_mode.build_instructions(filename)

    else:
        print("Invalid selection.")
        return

    solver.solve(grid_path, grid_size)
    downloader.cleanup(filename)





if __name__ == "__main__":
    main()

