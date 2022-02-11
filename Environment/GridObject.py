from .Perception import Perception


class Grid:

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.grid = [[[] for _ in range(dimensions)] for _ in range(dimensions)]
        self.perceptions = [[[] for _ in range(dimensions)] for _ in range(dimensions)]

    def __str__(self):
        gridstr = "-" * 80 + "\n|"
        for i, row in enumerate(self.grid):
            for cell in row:
                l = len(cell)
                if l == 0:
                    gridstr += " " * 7
                else:
                    gridstr += str([obj for obj in cell])
                gridstr += "|"
            if (i < self.dimensions - 1):
                gridstr += "\n" + "-" * 80 + "\n|"
            else:
                gridstr += "\n" + "-" * 80

        return gridstr

    def set_coord(self, grid, coord, value):
        for coord_i in coord:
            x, y = coord_i
            if grid[y][x] == None:
                grid[y][x] = []
            grid[y][x].append(value)

    def set_perception(self, grid, coord, value):
        perc = Perception("grid", value, 1, 0, 0)
        for coord_i in coord:
            x, y = coord_i
            if grid[y][x] == None:
                grid[y][x] = []
            grid[y][x].append(perc)

    def get_perc(self, coord):
        for coord_i in coord:
            x, y = coord_i
            return self.perceptions[y][x]

    def get_coord(self, value):
        ret_vals = []
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                cell = self.grid[j][i]
                if any(o == value for o in cell):
                    ret_vals.append((j, i))
        return ret_vals

    def get_coord_and_remove_val(self, value):
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                cell = self.grid[i][j]
                self.grid[i][j] = [x for x in cell if not x == value ]

    def neighboursOf(self, coord):
        temp_list = []
        for coordinate in coord:
            left = coordinate[0] - 1, coordinate[1]
            right = coordinate[0] + 1, coordinate[1]
            bottom = coordinate[0], coordinate[1] - 1
            up = coordinate[0], coordinate[1] + 1
            for coord in [left, right, bottom, up]:
                if coord[0] > (self.dimensions - 1) or coord[0] < 0 or coord[1] > (self.dimensions - 1) or coord[1] < 0:
                    continue
                else:
                    temp_list.append(coord)
        return temp_list
