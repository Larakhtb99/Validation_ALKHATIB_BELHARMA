from collections import deque

from Kernel import STRTR, IsAcceptingProxy


def bfs(graph):
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

def find_accepting_bfs(graph):
    visited = []
    queue = deque()
    init=True
    while len(queue)!= 0 | init:
        if init:
            voisin = graph.initial()
        else:
            node = queue.popleft()
            voisin=graph.next(node)
        for n in voisin:
            if n not in visited:
                if graph.isAccepting(n):
                    return False,n
                queue.append(n)
                visited.append(n)
        init=False
    return True,n

def get_trace(parents, result, initial):
    status,target = result
    if not status :
        print("L'accepting state n'est pas trouvé ")
        return None
    print (initial,result)

    current_Node = target
    trace = [current_Node]
    while current_Node not in initial:
        current_Node = parents[current_Node]
        trace.append(current_Node)

    print("Trace : ", trace)

def iterative_bfs(graph):
    visited = []
    queue = deque()
    init=True
    while len(queue)!= 0 | init:
        if init:
            voisin = graph.initial()
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
