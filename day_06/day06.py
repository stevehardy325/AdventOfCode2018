def manhattan(x, y, ax, ay):
    return abs(x-ax) + abs(y-ay)


def main():
    filename='input'

    points = []
    max_x = 0
    max_y = 0
    with open(filename, 'r') as file:
        for line in file:
            split_up = line.split(', ')
            points += [[int(split_up[0]),int(split_up[1])]]
            max_x = max(max_x, int(split_up[0]) + 1)
            max_y = max(max_x, int(split_up[1]) + 1)

    distance = dict()
    spaces = dict()

    part2 = [[[None for i in range(len(points))] for j in range(max_y)] for k in range (max_x)]

    for x in range(max_x):
        for y in range(max_y):
            for d in range(len(points)):
                point = points[d]
                dist = manhattan(x, y, point[0], point[1])
                part2[x][y][d] = dist

                if (x,y) not in distance:
                    distance[(x,y)] = dist
                    spaces[(x,y)] = d
                elif distance[(x,y)] == dist:
                    spaces[(x,y)] = None
                elif distance[(x,y)] > dist:
                    distance[(x,y)] = dist
                    spaces[(x,y)] = d

    area = dict()

    for i in spaces:
        point = spaces[i]
        if point is not None:
            if point not in area:
                area[point] = 0
            area[point] += 1

    for y in range(max_y):
        x = 0
        point = spaces[(x,y)]
        area[point] = -1

    for y in range(max_y):
        x = max_x - 1
        point = spaces[(x,y)]
        area[point] = -1

    for x in range(max_x):
        y = 0
        point = spaces[(x,y)]
        area[point] = -1

    for x in range(max_x):
        y = max_y - 1
        point = spaces[(x,y)]
        area[point] = -1

    maximum = max(list(area.values()))
    print(maximum)

    count = 0
    for x in range(max_x):
        for y in range(max_y):
            if sum(part2[x][y]) < 10000:
                count += 1

    print(count)













if __name__ == '__main__':
    main()
