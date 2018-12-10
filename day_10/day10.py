import re
import time

def main():
    points = dict()
    vels = dict()
    nums = re.compile(r"[+-]?\d+(?:\.\d+)?")
    id = 0

    with open('input') as file:
        for line in file:
            id += 1
            parsed = nums.findall(line)
            x = int(parsed[0])
            y = int(parsed[1])
            xvel = int(parsed[2])
            yvel = int(parsed[3])
            points[id] = (x, y)
            vels[id] = (xvel, yvel)

    #print(points)

    stop = False
    prevArea = None
    time = 0
    while True:
        #time.sleep(1)
        newPoints = dict()
        for point in points:
            x = points[point][0]
            y = points[point][1]
            xvel = vels[point][0]
            yvel = vels[point][1]

            x += xvel
            y += yvel
            newPoints[point] = (x, y)

        max_x = max(point[0] for point in newPoints.values())
        max_y = max(point[1] for point in newPoints.values())
        min_x = min(point[0] for point in newPoints.values())
        min_y = min(point[1] for point in newPoints.values())
        xdif = max_x-min_x
        ydif = max_y-min_y
        area = xdif * ydif
        #print('{} {}'.format(area, min_x))

        if prevArea != None and area > prevArea:
            print("FOUND")
            for j in range(min_y,max_y):
                row = ''
                for i in range(min_x,max_x):
                    if (i,j) in points.values():
                        row += 'X'
                    else:
                        row += ' '
                print(row)
            print('Time: {}'.format(time))
            break
        else:
            time += 1
            prevArea = area
            points = newPoints
if __name__ == '__main__':
    main()
