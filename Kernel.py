import copy
from abc import abstractmethod


class TransitionRelation:
    @abstractmethod
    def initial(self):
        pass

    @abstractmethod
    def next(self,conf):
        pass

class AcceptingSet:

    @abstractmethod
    def initial(self):
        pass

    @abstractmethod
    def next(self, conf):
        pass

    @abstractmethod
    def isAccepting(self, conf):
        pass


class SemanticTransitionRelations:
    def initial(self):
        pass

    def actions(self, conf):
        pass

    def execute(self, conf, actions):
        pass


class STRTR:
    def __init__(self, str):
        self.operand = str

    def initial(self):
        return self.operand.initial()

    def next(self, c):
        targets = []
        for a in self.operand.actions(c):
            target = self.operand.execute(c, a)
            targets.append(target)
        return targets


class IdentityProxy(object):
    def __init__(self, operand):
        super().__init__()
        self.operand = operand

    def initial(self):
        return self.operand.initial()

    def next(self, c):
        return self.operand.next(c)


class IsAcceptingProxy(IdentityProxy):
    def __init__(self, operand, predicate):
        super().__init__(operand)
        self.predicate = predicate

    def isAccepting(self, c):
        return self.predicate(c)