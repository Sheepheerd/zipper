from modules import Zip
from solver import Solver


def main():
    print("Choose a mode:")
    print("  1) zip")
    print("  2) queens")
    print("  3) tango")

    choice = input("> ").strip()

    solver = Solver()

    if choice == "1":
        zip_mode = Zip()
        filename = zip_mode.download_image()
        grid_path = zip_mode.build_instructions(filename)

    # elif choice == "2":
    #     queens_mode = Queens()
    #     filename = queens_mode.download_image()
    #     grid_path = queens_mode.build_instructions(filename)
    #
    # elif choice == "3":
    #     tango_mode = Tango()
    #     filename = tango_mode.download_image()
    #     grid_path = tango_mode.build_instructions(filename)

    else:
        print("Invalid selection.")
        return

    solver.solve(grid_path)





if __name__ == "__main__":
    main()

