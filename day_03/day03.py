class Rectangle:
<<<<<<< HEAD
    def __init__(self, string, rects):
=======
    def __init__(self, string):
>>>>>>> 1f84f56130a661c8951fa27075a402f3b1f86ea8
        parts = string.split(' ')
        self.id = int(parts[0][1:])
        corners = parts[2].split(',')
        self.x1 = int(corners[0])
        self.y1 = int(corners[1][:-1])
        dims = parts[3].split('x')
<<<<<<< HEAD

=======
>>>>>>> 1f84f56130a661c8951fa27075a402f3b1f86ea8
        self.width = int(dims[0])
        self.height = int(dims[1])
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height
<<<<<<< HEAD
        #self.area = self.width * self.height

        self.overlappers = set()
        for other in rects:
            if self.overlaps(other):
                other.overlappers.add(self)
                self.overlappers.add(other)
=======
        self.area = self.width * self.height
        self.overlaps = False
>>>>>>> 1f84f56130a661c8951fa27075a402f3b1f86ea8

    def overlaps(self, other):
        y_overlap = True
        x_overlap = True
        if self.x1 > other.x2 or self.x2 < other.x1:
            x_overlap = False
        if self.y1 > other.y2 or self.y2 < other.y1:
            y_overlap = False
        return y_overlap and x_overlap

<<<<<<< HEAD
=======
    def contains(self, x, y):
        return (x >= self.x1 and x < self.x2 and y >= self.y1 and y < self.y2)


>>>>>>> 1f84f56130a661c8951fa27075a402f3b1f86ea8
def main():
    filename = "input"
    file = open(filename, "r")

<<<<<<< HEAD
    fabric_squares = dict()
    rects = []

    for line in file:
        r = Rectangle(line, rects)
        for x in range(r.x1, r.x2):
            for y in range(r.y1, r.y2):
                if (x,y) not in fabric_squares:
                    fabric_squares[(x,y)] = 1
                else:
                    fabric_squares[(x,y)] += 1
        rects += [r]

    file.close()

    overlapping = 0
    for square in fabric_squares:
        if fabric_squares[square] > 1:
            overlapping += 1




    print("Overlapping sq inches: ", overlapping)

    for r in rects:
        if len(r.overlappers) == 0:
            print("Claim with no overlaps: " + str(r.id))

=======
    rects = []
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    for line in file:
        r = Rectangle(line)
        rects += [r]
        min_x = min(min_x, r.x1)
        max_x = max(max_x, r.x2)
        min_y = min(min_y, r.y1)
        max_y = max(max_y, r.y2)

    print('{} {} {} {}'.format(min_x, min_y, max_x, max_y))

    overlapping = 0
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            print('{} {}'.format(x, y))
            rects_over_x_y = 0
            for r in rects:
                if r.contains(x,y):
                    rects_over_x_y += 1
            if rects_over_x_y > 1: overlapping += 1


    file.close()

    print("Overlapping sq inches: ", overlapping)

>>>>>>> 1f84f56130a661c8951fa27075a402f3b1f86ea8


if __name__ == '__main__':
    main()
