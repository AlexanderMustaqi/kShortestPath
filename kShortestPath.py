import copy


def dijkstra(graph, src, end): #Dijkstra to be used in YENksp()
    #Initialized List
    n = len(graph)
    dist = [float("inf")] * n
    dist[src] = 0
    path = ["-"] * n
    path[src] = str(src)
    visited = [False] * n
    #Enter loop
    for _ in range(n):

        #Select shortest path
        min_distance = float("inf")
        current_node = -1
        for i in range(n):
            if dist[i] < min_distance and not visited[i]:
                current_node = i
                min_distance = dist[i]
        #If current_node == -1 break
        if current_node == -1:
            break

        visited[current_node] = True

        #Enter column loop
        for j in range(n):
            weight = graph[current_node][j]
            if weight > 0 and not visited[j]:
                if dist[j] > dist[current_node]+weight:
                    dist[j] = dist[current_node]+weight
                    path[j] = path[current_node] + str(j)

    return path[end], dist[end]


def yen(graph, src, end, k):

    A = [[""] * k, [0] * k] #Create and initialize A
    Apath = A[0] #Set the paths of A to a variable to make the code more readable
    Adistance = A[1] #Set the distances of A to a variable to make code more readable

    initial_path = dijkstra(graph, src, end) #Finding and storing the shortest path
    Apath[0] = initial_path[0]               #to prepare A for the loop
    Adistance[0] = initial_path[1]

    saveWeights = []

    for a in range(len(Apath)):
        #print(f"Before:\n{graph[0]}\n{graph[1]}\n{graph[2]}\n{graph[3]}\n{graph[4]}\n{graph[5]}\n")

        #print(A)
        B = [[], []] #Creating list B without initializing it, since we don't know how much
                     #space we need
        Bpath = B[0]
        Bdistance = B[1]
        n = len(graph)
        cpy_graph = copy.deepcopy(graph)
        links = [[] for _ in range(n)] #Creating list links to store previously
        selectedPath = Apath[a]
        length = len(selectedPath)
        rootPath = ""
        rootDistance = 0
        for i in range(length-1):
            #Storing spurNode and nextNode
            INTspurNode = int(selectedPath[i])
            spurNode = selectedPath[i]
            nextNode = selectedPath[i+1]
            INTnextNode = int(nextNode)
            #Removing links
            if links[INTspurNode]:
                for j in range(len(links[INTspurNode])):
                    linkNode = links[INTspurNode][j][0]
                    if linkNode == INTnextNode:
                        pass
                    else:
                        cpy_graph[INTspurNode][linkNode] = 0
                        cpy_graph[linkNode][INTspurNode] = 0
            currentVertexWeight = cpy_graph[INTspurNode][INTnextNode]
            #Altering graph for dijkstra
            cpy_graph[INTnextNode][INTspurNode] = 0
            cpy_graph[INTspurNode][INTnextNode] = 0
            #Running dijkstra and storing results in B
            dijkstra_output = dijkstra(cpy_graph, INTspurNode, end)
            if (rootPath + dijkstra_output[0]) not in Apath:
                Bpath.append((rootPath + dijkstra_output[0]))
                Bdistance.append((rootDistance + dijkstra_output[1]))
            #Restoring links
            if links[INTspurNode]:
                for j in range(len(links[INTspurNode])):
                    linkNode = links[INTspurNode][j][0]
                    if linkNode == INTnextNode:
                        pass
                    else:
                        linkWeight = links[INTspurNode][j][1]
                        cpy_graph[INTspurNode][linkNode] = linkWeight
                        cpy_graph[linkNode][INTspurNode] = linkWeight
            #Updating rootPath, rootDistance and links
            rootPath += spurNode
            rootDistance += currentVertexWeight
            links[INTspurNode].append((INTnextNode, currentVertexWeight))

        #Getting B's shortest paths
        min_distance = float("inf")
        min_pointer = -1
        for j in range(len(Bpath)):
            if Bdistance[j] < min_distance and Bdistance[j] != 0:
                min_distance = Bdistance[j]
                min_pointer = j
        if min_pointer == -1:
            break
        ApathCounter = 0
        for j in range(len(Apath)):
            if Apath[j] == "":
                ApathCounter = j
                break
        for j in range(len(Bpath)):
            if ApathCounter >= k:
                return A
            if Bdistance[j] == min_distance:
                Apath[ApathCounter] = Bpath[j]
                Adistance[ApathCounter] = Bdistance[j]
                ApathCounter += 1

    return A


sampleMartix = [[0, 0, 5, 0, 0],
                [0, 0, 0, 3, 7],
                [5, 0, 0, 1, 0],
                [0, 3, 1, 0, 1],
                [0, 7, 0, 1, 0]]
k = 3

matrixLength = len(sampleMartix)
results = []
for i in range(matrixLength):
    for j in range(i+1, matrixLength):
        result = yen(sampleMartix, i, j, k)
        results.append([(i, j), result])

print(f"{results}")
