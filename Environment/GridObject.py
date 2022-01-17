class Grid:

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.grid = [[""] * dimensions for _ in range(dimensions)]
        self.perceptions = [[""] * dimensions for _ in range(dimensions)]

    def __str__(self):
        gridstr = "-" * 80 + "\n|"
        for i,row in enumerate(self.grid):
            for el in row:
                l = len(el)
                if l == 0:
                    gridstr += " "*7
                elif l == 1:
                    gridstr += "   " + el + "   "
                elif l == 3:
                    gridstr += "  " + el + "  "
                elif l == 5:
                    gridstr += " " + el + " "
                else:
                    gridstr += el
                gridstr += "|"
            if(i<self.dimensions-1):
                gridstr += "\n" + "-" * 80 + "\n|"
            else:
                gridstr += "\n" + "-" * 80

        return gridstr

    def set_coord(self, coord, value):
        for coord_i in coord:
            x, y = coord_i
            if self.grid[x][y] == "":
                self.grid[x][y] += value
            else:
                self.grid[x][y] += ("+" + value)

    def set_perc(self, coord, value):
        for coord_i in coord:
            x, y = coord_i
            if self.perceptions[x][y] == "":
                self.perceptions[x][y] += value
            else:
                self.perceptions[x][y] += ("+" + value)

    def get_perc(self, coord):
        for coord_i in coord:
            x, y = coord_i
            return self.perceptions[x][y]

    def get_coord(self, grid, value):
        ret_vals = []
        for i, e in enumerate(grid):
            for j, e_2 in enumerate(e):
                f = e_2.find(value)
                l = e_2.rfind(value)
                if f == -1 or l == -1:
                    continue
                elif f == l:
                    ret_vals.append((i,j))
                else:
                    num = ((l - f)/2)+1
                    for _ in range(int(num)):
                        ret_vals.append((i, j))
        return ret_vals

        # raise ValueError("{!r} is not in list".format(value))


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
