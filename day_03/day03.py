class Rectangle:
    def __init__(self, string):
        parts = string.split(' ')
        self.id = int(parts[0][1:])
        corners = parts[2].split(',')
        self.x1 = int(corners[0])
        self.y1 = int(corners[1][:-1])
        dims = parts[3].split('x')
        self.width = int(dims[0])
        self.height = int(dims[1])
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height
        self.area = self.width * self.height
        self.overlaps = False

    def overlaps(self, other):
        y_overlap = True
        x_overlap = True
        if self.x1 > other.x2 or self.x2 < other.x1:
            x_overlap = False
        if self.y1 > other.y2 or self.y2 < other.y1:
            y_overlap = False
        return y_overlap and x_overlap

    def contains(self, x, y):
        return (x >= self.x1 and x < self.x2 and y >= self.y1 and y < self.y2)


def main():
    filename = "input"
    file = open(filename, "r")

    fabric_squares = dict()

    for line in file:
        r = Rectangle(line)
        for x in range(r.x1, r.x2):
            for y in range(r.y1, r.y2):
                if (x,y) not in fabric_squares:
                    fabric_squares[(x,y)] = 1
                else:
                    fabric_squares[(x,y)] += 1


    overlapping = 0
    for square in fabric_squares:
        if fabric_squares[square] > 1:
            overlapping += 1


    file.close()

    print("Overlapping sq inches: ", overlapping)



if __name__ == '__main__':
    main()
