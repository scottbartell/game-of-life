import copy
import curses
import time


class Game:
    def __init__(self):
        self.grid = self.init_grid()

    @staticmethod
    def init_grid():
        return [
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def get_neighbors(self, x, y):
        neighbors = []
        moves = [[1, 0],
                 [-1, 0],
                 [0, 1],
                 [0, -1],
                 [1, 1],
                 [1, -1],
                 [-1, 1],
                 [-1, -1]]
        for move in moves:
            nx = x + move[0]
            ny = y + move[1]
            if self.are_valid_coords(ny, ny):
                neighbors.append([nx, ny])
        return neighbors

    def number_live_neighbors(self, neighbors):
        values = map(lambda neighbor: self.grid[neighbor[0]][neighbor[1]], neighbors)
        return values.count(1)

    def are_valid_coords(self, x, y):
        max_length = len(self.grid) - 1
        return 0 <= x <= max_length and 0 <= y <= max_length

    @staticmethod
    def get_new_status(current_status, number_live_neighbors):
        if current_status == 1:
            if number_live_neighbors < 2:
                return 0
            elif number_live_neighbors == 2 or number_live_neighbors == 3:
                return 1
            elif number_live_neighbors > 3:
                return 0
        else:
            if number_live_neighbors == 3:
                return 1
            else:
                return 0

    def tick(self):
        updated_grid = copy.copy(self.grid)

        number_of_rows = len(self.grid)
        number_of_columns = len(self.grid[0])
        for row_number in range(number_of_rows):
            for column_number in range(number_of_columns):
                x = row_number - 1
                y = column_number - 1
                neighbors = self.get_neighbors(x, y)
                number_live_neighbors = self.number_live_neighbors(neighbors)

                current_status = self.grid[x][y]
                new_status = self.get_new_status(current_status, number_live_neighbors)
                updated_grid[x][y] = new_status

        self.grid = updated_grid

    def to_string(self):
        string = ""
        for row in self.grid:
            string += " ".join(str(x) for x in row) + "\n"
        return string


def main():
    game = Game()

    def run(window):
        for _ in range(20):
            window.addstr(0, 0, game.to_string())
            game.tick()
            window.refresh()
            time.sleep(1)

    curses.wrapper(run)

if __name__ == "__main__": main()
