from collections import deque


def iterative_bfs(graph):
    visited = []
    queue = deque()
    init=True
    while len(queue)!=0 | init:
        if init:
            voisin=graph.initial()
        else:
            node = queue.popleft()
            voisin=graph.next(node)
        for n in voisin:
            if n not in visited:
                queue.append(n)
                visited.append(n)
        init=False
    return visited

def iterative_bfs(graph):
    visited = []
    queue = deque()
    init=True
    while len(queue)!=0 | init:
        if init:
            voisin=graph.initial()
        else:
            node = queue.popleft()
            voisin=graph.next(node)
        for n in voisin:
            if n not in visited:
                if graph.isAccepting(n):
                    return False
                queue.append(n)
                visited.append(n)
        init=False
    return True