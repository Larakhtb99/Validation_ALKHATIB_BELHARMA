from Algorithms import predicate_model_checker, iterative_bfs
from Kernel import STRTR, IsAcceptingProxy
from SoupLangage import BehaviorSoup, BehSoupSemantics


class CounterConfiguration:
    def __init__(self):
        self.PC=0

    def __hash__(self):
        return hash(self.PC)

    def __eq__(self, other):
        return self.PC == other.PC

    def __repr__(self):
        return str(self.PC)


def counter(maxi):
    soup=BehaviorSoup(CounterConfiguration())

    def inc(c):
        c.PC = c.PC+1
    soup.add("inc", lambda c: c.PC < maxi, inc)

    def reset(c):
        c.PC = 0
    soup.add("reset", lambda c: c.PC >= maxi, reset)
    return soup


if __name__ == '__main__':

    semantic = BehSoupSemantics(counter(3))
    tr = STRTR(semantic)
    tr = IsAcceptingProxy(tr, lambda c: c.PC == 2)
    print(iterative_bfs(tr))
    print(tr.initial())
    print(tr.next(tr.initial()[0]))

    r = predicate_model_checker(semantic, lambda c: c.PC == 0)
    print(r)
    r = predicate_model_checker(semantic, lambda c: c.PC == 50)
    print(r)
