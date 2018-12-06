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



if __name__ == '__main__':
    main()
