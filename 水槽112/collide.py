collisions = set()

def getNodes(col, startingRow, rows=40, cols=60):
    for row in range(startingRow, rows + 1):
        node = col + (row * cols)
        collisions.add(node)

def collisionBuilder(rows=40, cols=60):
    startingRows = [None, 1, 1, 1, 1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 
        10, 10, 10, 10, 10, 10, 31, 31, 31, 31, 31, 31, 31, 6, 6, 6, 6, 6, 6, 
        6, 6, 6, 30, 30, 30, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 16, 16, 16, 
        16, 16, 16, 16, 16]
    for col in range(1, cols+1):
        startingRow = startingRows[col]
        getNodes(col, startingRow, rows=40, cols=60)

collisionBuilder()