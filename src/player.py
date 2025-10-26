class ZipPlayer:
    def __init__(self, board):
        """
        board: 2D list where empty cells are ' .' and dots are numbers as strings
        Player always starts on number 1.
        """
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.visited = set()  
        self.next_number = 2 
        self._find_start()

    def _find_start(self):
        """Find the starting position (number 1) and mark it as visited"""
        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x].strip() == "1":
                    self.current_pos = (x, y)
                    self.visited.add(self.current_pos)
                    return
        raise ValueError("No starting position (1) found on the board")

    def move(self, direction):
        """Move the player in one of 'up', 'down', 'left', 'right'"""
        x, y = self.current_pos
        if direction == "up":
            y -= 1
        elif direction == "down":
            y += 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1
        else:
            raise ValueError("Invalid direction")

        # Check bounds
        if not (0 <= x < self.cols and 0 <= y < self.rows):
            print("Move out of bounds!")
            return False

        new_pos = (x, y)
        cell = self.board[y][x].strip()

        if cell.isdigit():
            if int(cell) == self.next_number:
                self.next_number += 1
            elif int(cell) != self.next_number:
                print(f"Must visit number {self.next_number} next! Cannot skip numbers.")
                return False

        self.current_pos = new_pos
        self.visited.add(new_pos)

        if self.check_win():
            print("Congratulations! You completed the puzzle!")
            return True

        return True

    def check_win(self):
        """Check if all numbered dots have been visited in order"""
        total_numbers = max(
            int(cell) for row in self.board for cell in row if cell.strip().isdigit()
        )
        return self.next_number > total_numbers

    def print_board(self):
        """Display the board with current position marked"""
        for y in range(self.rows):
            row_str = ""
            for x in range(self.cols):
                if (x, y) == self.current_pos:
                    row_str += " P " 
                else:
                    row_str += f"{self.board[y][x]:>2}"
            print(row_str)
        print(f"Next number to visit: {self.next_number}")

