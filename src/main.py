from generator import ZipPuzzle
from player import ZipPlayer

grid_size = 6
puzzle = ZipPuzzle(grid_size, dot_count=10)

def main():
    if puzzle.generate_path():
        dots = puzzle.generate_dots()
        print(f"Generated Zip Puzzle ({grid_size}x{grid_size}):")
        puzzle.print_puzzle(dots)
        board = puzzle.dots_to_2d(dots)



        player = ZipPlayer(board)
        player.print_board()
        player.move("right")
        player.print_board()
        player.move("down")
        player.print_board()
        # print(puzzle.number_to_position(1))
    else:
        print("Failed to generate puzzle.")

if __name__ == "__main__":
    main()
