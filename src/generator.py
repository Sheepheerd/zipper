import random

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Dot:
    def __init__(self, position, number):
        self.position = position
        self.number = number

class ZipPuzzle:
    def __init__(self, grid_size, dot_count=None):
        self.grid_size = grid_size
        self.grid = [[False] * grid_size for _ in range(grid_size)]
        self.path = []
        self.visited = set()
        self.dot_count = dot_count or max(4, grid_size // 2)
        self._last_dots = []

    def generate_path(self):
        self.path = []
        self.visited = set()
        start = Position(0, 0)
        if self._hamiltonian_path(start):
            return True
        return False

    def _hamiltonian_path(self, pos):
        key = (pos.x, pos.y)
        if key in self.visited:
            return False

        self.visited.add(key)
        self.path.append(pos)
        self.grid[pos.y][pos.x] = True

        if len(self.path) == self.grid_size * self.grid_size:
            return True

        neighbors = self._sorted_neighbors(pos)
        for n in neighbors:
            if self._hamiltonian_path(n):
                return True

        self.visited.remove(key)
        self.path.pop()
        self.grid[pos.y][pos.x] = False
        return False

    def _sorted_neighbors(self, pos):
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        candidates = []
        for dx, dy in directions:
            nx, ny = pos.x + dx, pos.y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and (nx, ny) not in self.visited:
                count = sum(
                    0 <= nx+dx2 < self.grid_size and
                    0 <= ny+dy2 < self.grid_size and
                    (nx+dx2, ny+dy2) not in self.visited
                    for dx2, dy2 in directions
                )
                candidates.append((count, Position(nx, ny)))
        random.shuffle(candidates)
        candidates.sort(key=lambda x: x[0])
        return [p for _, p in candidates]

    def generate_dots(self):
        if not self.path:
            raise ValueError("Path not generated yet.")
        dots = []
        total = len(self.path)

        first_index = random.randint(0, total//4)  
        dots.append(Dot(self.path[first_index], 1))

        for i in range(1, self.dot_count-1):
            index = first_index + i * (total - first_index) // (self.dot_count - 1)
            index = min(index, total-2)
            dots.append(Dot(self.path[index], i+1))

        # last dot is always at end
        dots.append(Dot(self.path[-1], self.dot_count))

        self._last_dots = dots
        return dots

    def print_puzzle(self, dots):
        dot_map = {(d.position.x, d.position.y): d.number for d in dots}
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                if (x,y) in dot_map:
                    row.append(f"{dot_map[(x,y)]:2}")
                else:
                    row.append(" .")
            print(" ".join(row))

    def dots_to_2d(self, dots):
        col = []
        dot_map = {(d.position.x, d.position.y): d.number for d in dots}
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                if (x,y) in dot_map:
                    row.append(f"{dot_map[(x,y)]:2}")
                else:
                    row.append(" .")
            col.append(row)

        return col

    def number_to_position(self, number, dots=None):
        """
        Return the (x,y) coordinates of a dot with the given number.
        If dots is None, uses the last generated dots.
        """
        if dots is None:
            if not hasattr(self, "_last_dots") or not self._last_dots:
                raise ValueError("No dots generated yet.")
            dots = self._last_dots
        for d in dots:
            if d.number == number:
                return (d.position.x, d.position.y)
        raise ValueError(f"Dot with number {number} not found.")

    def distance_to_next_number(self, number, dots=None):
        """
        Return the Manhattan distance from the current number to the next number in the sequence.
        """
        if dots is None:
            if not hasattr(self, "_last_dots") or not self._last_dots:
                raise ValueError("No dots generated yet.")
            dots = self._last_dots

        # find current and next
        current_pos = None
        next_pos = None
        for d in dots:
            if d.number == number:
                current_pos = d.position
            if d.number == number + 1:
                next_pos = d.position
        if current_pos is None:
            raise ValueError(f"Dot with number {number} not found.")
        if next_pos is None:
            return 0  # or None, if this is the last number
        # Manhattan distance
        return abs(current_pos.x - next_pos.x) + abs(current_pos.y - next_pos.y)

