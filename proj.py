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


def showPlot(cords, paths):
    x = [x for (number, x, y) in cords]
    y = [y for (number, x, y) in cords]
    plt.scatter(x, y)

    colors = ["green", "red", "blue", "yellow"]

    for i, (x1, y1) in enumerate(zip(x, y)):
        plt.annotate(i + 1, (x1, y1))

    for path, color in zip(paths, colors):
        previousPoint = path[0]
        for nextPoint in path[1:]:
            plt.plot([x[previousPoint], x[nextPoint]],
                     [y[previousPoint], y[nextPoint]], color)
            previousPoint = nextPoint
    plt.show()


def greedyPath(matrix, firstPoint):
    path = []

    currentPoint = firstPoint

    usedVertexes = [firstPoint]

    path.append(currentPoint)

    for _ in range(0, math.ceil(len(matrix) / 2) - 1):
        bestDistance = None
        choosenPoint = None

        for index, distance in enumerate(matrix[currentPoint]):
            if(index == currentPoint):
                continue
            if(index in usedVertexes):
                continue

            if(bestDistance == None or distance < bestDistance):
                bestDistance = distance
                choosenPoint = index

        currentPoint = choosenPoint

        usedVertexes.append(currentPoint)

        path.append(currentPoint)

    path.append(firstPoint)
    summaryDistance = calculatePathLength(matrix, path)
    return path, summaryDistance


def greedySurfacePath(matrix, firstPoint):
    path = []

    currentPoint = firstPoint

    usedVertexes = [firstPoint]

    path.append(currentPoint)

    for _ in range(0, math.ceil(len(matrix) / 2) - 1):
        bestDistance = None
        choosenPoint = None

        for index, distance in enumerate(matrix[currentPoint]):
            if(index == currentPoint):
                continue
            if(index in usedVertexes):
                continue

            calculatedDistance = distance + matrix[index, firstPoint]

            if(bestDistance == None or calculatedDistance < bestDistance):
                bestDistance = calculatedDistance
                choosenPoint = index

        currentPoint = choosenPoint

        usedVertexes.append(currentPoint)

        path.append(currentPoint)

    path.append(firstPoint)
    summaryDistance = calculatePathLength(matrix, path)
    return path, summaryDistance


def greedyCyclePath(matrix, firstPoint):
    path = []

    currentPoint = firstPoint

    usedVertexes = [firstPoint]

    path.append(currentPoint)

    for _ in range(0, math.ceil(len(matrix) / 2) - 1):
        bestDistance = None
        choosenPoint = None

        for index, _ in enumerate(matrix[currentPoint]):
            if(index == currentPoint):
                continue
            if(index in usedVertexes):
                continue

            calculatedDistance = matrix[firstPoint, index] + \
                matrix[currentPoint, index] - \
                matrix[firstPoint, currentPoint]

            if(bestDistance == None or calculatedDistance < bestDistance):
                bestDistance = calculatedDistance
                choosenPoint = index

        currentPoint = choosenPoint

        usedVertexes.append(currentPoint)

        path.append(currentPoint)

    path.append(firstPoint)
    summaryDistance = calculatePathLength(matrix, path)
    return path, summaryDistance


def calculatePathLength(matrix, path):
    summaryDistance = 0
    previousPoint = path[0]
    for vertex in path[1:]:
        summaryDistance += matrix[previousPoint, vertex]

    return summaryDistance


def bestGreedyCyclePath(matrix):
    bestDistnace = None
    for firstPoint in range(0, len(matrix) - 1):
        foundPath, foundDistance = greedyCyclePath(matrix, firstPoint)
        if(bestDistnace == None or foundDistance < bestDistnace):
            bestDistnace = foundDistance
            path = foundPath

    return path, bestDistnace


def bestGreedySurfacePath(matrix):
    bestDistnace = None
    for firstPoint in range(0, len(matrix) - 1):
        foundPath, foundDistance = greedySurfacePath(matrix, firstPoint)
        if(bestDistnace == None or foundDistance < bestDistnace):
            bestDistnace = foundDistance
            path = foundPath

    return path, bestDistnace


def bestGreedyPath(matrix):
    bestDistnace = None
    for firstPoint in range(0, len(matrix) - 1):
        foundPath, foundDistance = greedyPath(matrix, firstPoint)
        if(bestDistnace == None or foundDistance < bestDistnace):
            bestDistnace = foundDistance
            path = foundPath

    return path, bestDistnace


if __name__ == "__main__":
    cords = readCords("./problems/kroB100.tsp")
    """
    cords = [
        (1, 10, 20),
        (2, 10, 22),
        (3, 15, 1),
        (4, 6, 12),
        (5, 14, 22),
        (6, 15, 2),
        (7, 15, 3),
        (8, 16, 4)
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

    path, summaryDistance = bestGreedyPath(matrix)

    surfacePath, surfaceSummaryDistance = bestGreedySurfacePath(matrix)

    cyclePath, cycleSummaryDistance = bestGreedyCyclePath(matrix)

    print(path, summaryDistance)
    print(surfacePath, surfaceSummaryDistance)
    print(cyclePath, cycleSummaryDistance)

    #showPlot(cords, (path, surfacePath, cyclePath))
    showPlot(cords, (cyclePath,))
