from collections import deque

from Kernel import STRTR, IsAcceptingProxy


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


def predicate_model_checker(semantic, predicate):
    tr = STRTR(semantic)
    tr = IsAcceptingProxy(tr, predicate)
    return iterative_bfs(tr)
