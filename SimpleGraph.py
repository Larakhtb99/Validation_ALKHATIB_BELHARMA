
from Kernel import TransitionRelation, AcceptingSet


class SimpleGraph(TransitionRelation):

    def __init__(self, G, initial):
        self.model=G
        self.start=initial
    def initial(self):
        return self.start

    def next(self,conf):
        return self.model[conf]

class MyNFA(SimpleGraph,AcceptingSet):
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