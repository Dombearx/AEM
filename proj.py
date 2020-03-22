import math
import pprint as pp
import numpy as np
import matplotlib.pyplot as plt


def readCords(path):
    cords = []
    with open(path) as f:
        line = f.readline()
        while("NODE_COORD_SECTION" not in line):
            line = f.readline()
        line = f.readline()
        while("EOF" not in line):
            data = line.split(" ")
            number = int(data[0])
            x = int(data[1])
            y = int(data[2])
            cords.append((number, x, y))
            line = f.readline()
    return cords


def calculateDistance(dist1, dist2):
    distance = 0
    for cord1, cord2 in zip(dist1, dist2):
        distance += pow(cord1 - cord2, 2)

    return round((math.sqrt(distance)))


if __name__ == "__main__":
    cords = readCords("./problems/kroA100.tsp")
    """
    cords = [
        (1, 10, 20),
        (2, 10, 22),
        (3, 15, 1),
        (4, 6, 12)
    ]
    """
    w = h = len(cords)
    matrix = [[0 for x in range(w)] for y in range(h)]
    matrix = np.zeros((w, h), dtype="int32")
    pp.pprint(matrix)

    for cord1 in cords:
        number1, x1, y1 = cord1
        for cord2 in cords:
            number2, x2, y2 = cord2
            matrix[number1 - 1, number2 -
                   1] = calculateDistance((x1, y1), (x2, y2))

    pp.pprint(matrix)

    path = [1, 2, 3, 4, 1]

    x = [x for (number, x, y) in cords]
    y = [y for (number, x, y) in cords]
    plt.scatter(x, y)

    print(x)
    print(y)
    previousPoint = path[0]
    for nextPoint in path[1:]:
        print([x[previousPoint - 1], y[previousPoint - 1]])
        print([x[nextPoint - 1], y[nextPoint - 1]])
        plt.plot([x[previousPoint - 1], x[nextPoint - 1]],
                 [y[previousPoint - 1], y[nextPoint - 1]], 'green')
        previousPoint = nextPoint
        #plt.plot([10, 10], [20, 22], 'green')
    plt.show()
