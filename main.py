from abc import abstractmethod
from collections import deque

class TransitionRelation:
    @abstractmethod
    def initial(self):
        pass

    @abstractmethod
    def next(self,conf):
        pass

class myGraph(TransitionRelation):
    def __init__(self, G, initial):
        self.model=G
        self.start=initial
    def initial(self):
        return self.start

    def next(self,conf):
        return self.model[conf]

class NFA(TransitionRelation):

    @abstractmethod
    def initial(self):
        pass

    @abstractmethod
    def next(self, conf):
        pass

    @abstractmethod
    def isAccepting(self, conf):
        pass

class MyNFA(NFA):
    def __init__(self, G, initial,final):
        self.model=G
        self.start=initial
        self.final=final

    def initial(self):
        return self.start

    def next(self,conf):
        return self.model[conf]

    def isAccepting(self,conf):
        return conf in self.final

class BFS:

    def iterative_bfs(graph:TransitionRelation):
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
class safety:
    def iterative_bfs(graph:NFA):
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

if __name__ == "__main__":
    G = {
        '1': ['2'],
        '2': ['3'],
        '3': ['3'],
        '4': ['2','5'],
        '5': ['5']
    }
    start=['2']
    graph=myGraph(G,start)
    print(BFS.iterative_bfs(graph))
    nfa=MyNFA(G,start, ['5'])
    print(safety.iterative_bfs(nfa))

