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