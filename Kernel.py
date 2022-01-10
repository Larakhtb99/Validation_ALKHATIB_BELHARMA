from abc import abstractmethod


class TransitionRelation:
    @abstractmethod
    def initial(self):
        pass

    @abstractmethod
    def next(self, conf):
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


class OSTR:
    def __init__(self, str):
        self.operand = str

    def actions(self, conf):
        return self.operand.actions(conf)

    def execute(self, conf, actions):
        targets = []
        for a in actions(conf):
            target = self.operand.execute(conf, a)
            targets.append(target)
        return targets,self.operand

class ISTR:
    def __init__(self, str):
        self.operand = str

    def actions(self, i,conf):
        actions=self.operand.actions(conf)
        for a in actions:
            if a[0](i):
                actions.append(a)
        return actions
    def execute(self, i, conf, actions):
        targets = []
        for a in actions(conf):
            target = self.operand.execute(conf, a)
            targets.append(target)
        return targets[conf](i)


class kripkeBuchiSTR(SemanticTransitionRelations):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def initial(self):
        return list(map(lambda rc: (None, rc), self.rhs.initial()))

    def get_synchronous_actions(self, kc, bc, io_synca):
        Buchi_actions = self.rhs.actions(kc, bc)
        return io_synca.extend(map(lambda ba: (kc, ba), Buchi_actions))

    def actions(self, source):
        synchronous_actions = []
        Kripke_src, Buchi_src = source  # Kripke_src=source[0] & Buchi_src=source[1]
        if Kripke_src is None:
            for k_target in self.lhs.initial():
                self.get_synchronous_actions(k_target, Buchi_src, synchronous_actions)
            return synchronous_actions
        k_actions = self.lhs.actions(Kripke_src)
        num_actions = len(k_actions)
        for ka in k_actions:
            k_target = self.lhs.execute(Kripke_src, ka)
            if k_target is None:
                num_actions -= 1
            self.get_synchronous_actions(k_target, Buchi_src, synchronous_actions)
        if num_actions == 0:
            self.get_synchronous_actions(Kripke_src, Buchi_src, synchronous_actions)

    def execute(self, action, conf):
        ktarget, baction = action
        _, bsrc = conf
        return ktarget, self.rhs.execute(ktarget, baction, bsrc)


class buchiSemantics(ISTR):
    def __init__(self, ini, d, pred):
        self.initial = ini
        self.delta = d
        self.pred = pred

    def initial(self):
        return self.initial()

    def actions(self, i, c):
        actions = self.delta[c]
        for a in actions:
            if a[0](i):
                actions.append(a)
        return actions

    def execute(self, i, conf, a):
        return a[1]


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


class STR_vers_OSTR:
    def __init__(self, operand):
        self.operand = operand

    def initial(self):
        return self.operand.initial()

    def actions(self, c):
        return self.operand.actions(c)

    def execute(self, source, a):
        target = self.operand.execute(source, a)
        return (source, a, target), target


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
