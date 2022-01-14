from Algorithms import predicate_model_checker, iterative_bfs
from Kernel import STRTR, IsAcceptingProxy
from SoupLangage import BehaviorSoup, BehSoupSemantics


class AliceBobConfiguration:
    def __init__(self):
        self.PC_alice = 0
        self.PC_bob = 0

    def __hash__(self):
        return hash(self.PC_alice + self.PC_bob)

    def __eq__(self, other):
        return self.PC_alice == other.PC_alice & self.PC_bob == other.PC_bob

    def __repr__(self):
        return str(self.PC_alice) + str(self.PC_bob)


def counterState():
    soup = BehaviorSoup(AliceBobConfiguration())

    def ItoW_alice(c):
        c.PC_alice = 1

    soup.add("ItoSC_alice", lambda c: c.PC_alice == 0, ItoW_alice)

    def WtoSC_alice(c):
        return 1

    soup.add("WtoSC_alice", lambda c: c.PC_bob == 0 and c.PC_alice == 1, WtoSC_alice)

    def SCtoI_alice(c):
        c.PC_alice = 0

    soup.add("SCtoI_alice", lambda c: c.PC_alice == 1, SCtoI_alice)

    def ItoW_bob(c):
        c.PC_bob = 1

    soup.add("ItoW_bob", lambda c: c.PC_bob == 0, ItoW_bob)

    def WtoSC_bob(c):
        return 1

    soup.add("WtoSC_bob", lambda c: c.PC_alice == 0 and c.PC_bob == 1, WtoSC_bob)

    def SCtoI_bob(c):
        c.PC_bob = 0

    soup.add("SCtoI_bob", lambda c: c.PC_bob == 1, SCtoI_bob)

    return soup


if __name__ == '__main__':
    semantic = BehSoupSemantics(counterState())
    tr = STRTR(semantic)
    tr = IsAcceptingProxy(tr, lambda c: c.PC_alice == 0)
    print(tr.initial())
    print(tr.next(tr.initial()[0]))
    r = predicate_model_checker(semantic, lambda c: c.PC_alice == 1 and c.PC_bob == 1)
    print(r)
    r = predicate_model_checker(semantic, lambda c: len(semantic.actions(c)) == 0)
    print(r)
