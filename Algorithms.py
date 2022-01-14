from collections import deque

import Kernel
from Kernel import STRTR, IsAcceptingProxy


def bfs(graph):
    visited = []
    queue = deque()
    init = True
    while len(queue) != 0 | init:
        if init:
            voisin = graph.initial()
        else:
            node = queue.popleft()
            voisin = graph.next(node)
        for n in voisin:
            if n not in visited:
                queue.append(n)
                visited.append(n)
        init = False
    return visited


def find_accepting_bfs(graph):
    visited = []
    queue = deque()
    init = True
    while len(queue) != 0 | init:
        if init:
            voisin = graph.initial()
        else:
            node = queue.popleft()
            voisin = graph.next(node)
        for n in voisin:
            if n not in visited:
                if graph.isAccepting(n):
                    return True, n
                queue.append(n)
                visited.append(n)
        init = False
    return False, n


def get_trace(parents, result, initial):
    status, target = result
    if not status:
        print("L'accepting state n'est pas trouvé ")
        return None
    print(initial, result)

    current_Node = target
    trace = [current_Node]
    while current_Node not in initial:
        current_Node = parents[current_Node]
        trace.append(current_Node)
    print("Trace : ", trace)


def iterative_bfs(graph):
    visited = []
    queue = deque()
    init = True
    while len(queue) != 0 | init:
        if init:
            voisin = graph.initial()
            init = False
        else:
            node = queue.popleft()
            voisin = graph.next(node)
        for n in voisin:
            if n not in visited:
                if graph.isAccepting(n):
                    return True
                queue.append(n)
                visited.append(n)
    return False

def isAccepting_cycle(graph):
    visited = []
    queue = deque()
    init = True
    while len(queue) != 0 or init:
        if init:
            voisin = graph.initial()
            init = False
        else:
            node = queue.popleft()
            voisin = graph.next(node)
        for n in voisin:
            if graph.isAccepting(n):
                if find_cycle(graph, graph.next(n), n):
                    return True
            if n not in voisin:
                visited.add(n)
                queue.append(n)
    return False


def find_cycle(graph, initial, end):
    visited = []
    queue = deque()
    init = True
    while len(queue) != 0 | init:
        if init:
            voisin = initial
            init = False
        else:
            node = queue.popleft()
            voisin = graph.next(node)
        for n in voisin:
            if n not in visited:
                if n == end:
                    return True
                queue.append(n)
                visited.append(n)
    return False

def predicate_model_checker(semantic, predicate):
    tr = STRTR(semantic)
    tr = IsAcceptingProxy(tr, predicate)
    return iterative_bfs(tr)

def model_checker(krypkeSemantic, buchiSemantic):
    compSync = Kernel.kripkeBuchiSTR(krypkeSemantic, buchiSemantic)
    tr = STRTR(compSync)
    tr = IsAcceptingProxy(tr, lambda c:  buchiSemantic.pred(c[1]))
    return isAccepting_cycle(tr)