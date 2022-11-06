global adjList
adjList = {}

'''
I used the concept of an adjacency list which I learned from the Graph 
Algorithms slides linked later below.
'''
def createAdjList(width=60, height=40):
    global adjList
    for pixel in range(1, (width*height) + 1):
        adjList[pixel] = set()
    for key in adjList:
        if (key + 1) % (width + 1) != 0:
            if key != (width * height):
                adjList[key].add(key + 1)
        if (key + width) < (width * height):
            adjList[key].add(key + width)
        for elem in adjList[key]:
            adjList[elem].add(key)
    adjList = nodeCleaner(adjList)
    return adjList

def nodeCleaner(adjList):
    startingRows = [None, 22, 24, 28, 19, 19, 19, 14, 13, 19, 15, 15, 17, 18, 
    18, 18, 18, 18, 30, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 11, 8, 9, 10, 
    16, 35, 35, 35, 33, 33, 32, 17, 17, 16, 14, 14, 12, 12, 13, 12, 12, 19, 19, 
    21, 21, 22, 22, 24, 28, 19, 19, 19]
    toRemove = set()
    removedEdges = 0
    for col in range(1, 61):
        startingRow = startingRows[col]
        for row in range(startingRow, 41):
            futile = ((row - 1) * 60) + col
            toRemove.add(futile)
            adjList[futile] = set()
            for key in adjList:
                if futile in adjList[key]:
                    adjList[key].remove(futile)
                    removedEdges += 1
    return adjList

'''
Pseudcode from provided Graph Algorithm Slides were referenced in creation:
https://docs.google.com/presentation/d/1SsmOONf97GHCBrZ1yMT-rOy4UAWq7BYd/edit?
usp=sharing&ouid=104065437106131238803&rtpof=true&sd=true
'''
def bfs(adjList, fish, food):
    visited = dict()
    queue = [fish]
    foodFound = False
    while len(queue) > 0:
        if foodFound: break
        currentNode = queue[0]
        queue.pop(0)
        if currentNode in visited:
            for node in adjList[currentNode]:
                if node not in visited:
                    queue.append(node)
                    visited[node] = currentNode
                    if food in visited:
                        foodFound = True
                        break
            continue
        if currentNode == food:
            foodFound = True
            break
        if currentNode not in visited:
            visited[currentNode] = None
        for neighbor in adjList[currentNode]:
            if neighbor not in visited:
                visited[neighbor] = currentNode
                queue.append(neighbor)
    return extractPath(visited, food)

def extractPath(visited, food):
    path = [food]
    key = food
    while key in visited:
        location = visited[key]
        if location != None:
            path += [location]
            key = location
        if location == None:
            break
    return path[::-1]

def coordToNode(coord, cols = 60):
    y = coord[1]
    x = coord[0]
    node = (cols*((y-1)//10)) + ((x-1)//10) + 1
    return int(node)

def nodeToCoord(node, cols = 60, height = 400, rows = 40, width = 600):
    row = (node // cols) + 1
    col = cols - ((row * cols) - node)
    position = (col * (width/cols), row * (height/rows))
    return [(position[0] - (0.5*width/cols)), (position[1] - (0.5*width/cols))]