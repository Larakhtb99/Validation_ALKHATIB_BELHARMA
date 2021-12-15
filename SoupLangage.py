import copy

from Kernel import SemanticTransitionRelations


class Behavior:
    def __init__(self, n, a, g):
        self.name = n
        self.action = a
        self.guard = g


class BehaviorSoup:
    def __init__(self, conf):
        self.initial = conf
        self.behaviors = []

    def add(self, n, g, a):
        self.behaviors.append(Behavior(n, a, g))


class BehSoupSemantics(SemanticTransitionRelations):

    def __init__(self, program):
        self.soup = program

    def initial(self):
        return [self.soup.initial]

    def actions(self, conf):
        return list(map(lambda beh: beh.action,
                        filter(lambda beh: beh.guard(conf),
                               self.soup.behaviors)))

    def execute(self, c, a):
        target = copy.deepcopy(c)
        r = a(target)
        return target
