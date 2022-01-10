from Algorithms import predicate_model_checker, iterative_bfs
from Kernel import STRTR, IsAcceptingProxy
from SoupLangage import BehaviorSoup, BehSoupSemantics


class AliceBobConfiguration:
    def __init__(self):
        self.PC_alice = 0
        self.PC_bob = 0
        self.Flag_alice = 0
        self.Flag_bob = 0

    def __hash__(self):
        return hash(self.PC_alice + self.PC_bob)+(self.Flag_alice+self.Flag_bob)

    def __eq__(self, other):
        return self.PC_alice == other.PC_alice and self.PC_bob == other.PC_bob and self.Flag_bob == other.Flag_bob and self.Flag_alice ==other.Flag_alice

    def __repr__(self):
        return str(self.PC_alice) + str(self.PC_bob)


def AliceBob():
    soup = BehaviorSoup(AliceBobConfiguration())

    def ItoW_alice(c):
        c.PC_alice = 1
        c.Flag_alice = 1

    soup.add("ItoSC_alice", lambda c: c.PC_alice == 0, ItoW_alice)

    def WtoSC_alice(c):
        c.PC_alice = 2
        c.Flag_alice = 1

    soup.add("WtoSC_alice", lambda c: c.PC_bob != 2 and c.PC_alice == 1, WtoSC_alice)

    def SCtoI_alice(c):
        c.PC_alice = 0
        c.Flag_alice = 0

    soup.add("SCtoI_alice", lambda c: c.PC_alice == 2, SCtoI_alice)

    def ItoW_bob(c):
        c.PC_bob = 1
        c.Flag_bob = 1

    soup.add("ItoW_bob", lambda c: c.PC_bob == 0, ItoW_bob)

    def WtoSC_bob(c):
        c.PC_bob = 2
        c.Flag_bob = 1

    soup.add("WtoSC_bob", lambda c: c.PC_bob == 1 and c.PC_alice != 2, WtoSC_bob)

    def SCtoI_bob(c):
        c.PC_bob = 0
        c.Flag_bob = 0

    soup.add("SCtoI_bob", lambda c: c.PC_bob == 2, SCtoI_bob)

    return soup


def a_in_cs(c):
    return c.PC_alice == 2


def b_in_cs(c):
    return c.PC_bob == 2


def exclusion_buchi():
    delta = {0: [(lambda c: True, 0), lambda c: a_in_cs(c) and b_in_cs(c), 1], 1: [(lambda c: True, 1)]}
    return 0, delta, lambda c: c == 1


if __name__ == '__main__':
    semantic = BehSoupSemantics(AliceBob())
    #print(tr.initial())
    #print(tr.next(tr.initial()[0]))
    r = predicate_model_checker(semantic, lambda c: c.PC_alice == 2 and c.PC_bob == 2)
    print(r)
    r = predicate_model_checker(semantic, lambda c: len(semantic.actions(c)))
    print(r)
