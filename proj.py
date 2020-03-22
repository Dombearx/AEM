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


def showPlot(cords, paths, title):
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

    plt.title(title)
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


def greedyRegretCyclePath(matrix, firstPoint):
    print("firstPoint", firstPoint)
    path = []

    currentPoint = firstPoint

    usedVertexes = [firstPoint]

    path.append(currentPoint)

    for _ in range(0, math.ceil(len(matrix) / 2) - 1):
        choosenPoint = None
        regrets = []
        allCosts = {}
        for index, distance in enumerate(matrix[currentPoint]):
            if(index == currentPoint):
                continue
            if(index in usedVertexes):
                continue

            costs = []
            for index2, x in enumerate(path[:-1]):
                y = path[index2 + 1]
                costs.append(((matrix[x, index] +
                               matrix[y, index] - matrix[x, y]), index2))
            costs = sorted(costs, key=lambda x: x[0], reverse=False)
            allCosts[index] = costs
            # print(costs)
            if(len(costs) > 1):
                regrets.append((costs[1][0] - costs[0][0], index))
            else:
                regrets.append((-distance, index))

        regrets = sorted(regrets, key=lambda x: x[0], reverse=True)
        # print(regrets)
        choosenPoint = regrets[0][1]

        currentPoint = choosenPoint

        usedVertexes.append(currentPoint)

        insertIndex = allCosts[choosenPoint]
        if(len(insertIndex) > 0):
            insertIndex = insertIndex[0]
            insertIndex = insertIndex[1] + 1
            #print("insertIndex", insertIndex)
            path.insert(insertIndex, currentPoint)
        else:
            path.append(currentPoint)

    path.append(firstPoint)
    summaryDistance = calculatePathLength(matrix, path)
    return path, summaryDistance


def calculatePathLength(matrix, path):
    summaryDistance = 0
    previousPoint = path[0]
    for vertex in path[1:]:
        summaryDistance += matrix[previousPoint, vertex]
        previousPoint = vertex

    return summaryDistance


def bestGreedyCycleRegretPath(matrix):
    bestDistnace = None
    for firstPoint in range(0, len(matrix) - 1):
        foundPath, foundDistance = greedyRegretCyclePath(matrix, firstPoint)
        if(bestDistnace == None or foundDistance < bestDistnace):
            bestDistnace = foundDistance
            path = foundPath

    return path, bestDistnace


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

    cords = [
        (1, 10, 20),
        (2, 10, 22),
        (3, 15, 1),
        (4, 6, 12),
        (5, 14, 22),
        (6, 15, 2),
        (7, 15, 3),
        (8, 16, 4),
        (9, 16, 5),
        (10, 16, 6),
        (11, 16, 7)
    ]

    cords = readCords("./problems/kroB100.tsp")

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

    #path, summaryDistance = bestGreedyPath(matrix)

    #surfacePath, surfaceSummaryDistance = bestGreedySurfacePath(matrix)

    cyclePath, cycleSummaryDistance = bestGreedyCyclePath(matrix)

    cycleRegretPath, cycleRegretSummaryDistance = bestGreedyCycleRegretPath(
        matrix)

    #print(path, summaryDistance)
    #print(surfacePath, surfaceSummaryDistance)
    print(cyclePath, cycleSummaryDistance)
    print(cycleRegretPath, cycleRegretSummaryDistance)

    # showPlot(cords, (path, surfacePath, cyclePath))
    showPlot(cords, (cycleRegretPath,),
             "Greedy cycle z żalem, kroB100, distance:" + str(cycleRegretSummaryDistance))
