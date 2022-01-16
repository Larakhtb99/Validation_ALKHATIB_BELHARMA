import copy
import sys

from Kernel import IdentityProxy, STRTR, TransitionRelation, AcceptingSet
from SoupLangage import BehSoupSemantics, BehaviorSoup


class Stack:
    def __init__(self, m):
        self.capacity = m
        self.top = -1
        self.array = [0] * m


def createStack(capacity):
    stack = Stack(capacity)
    return stack


def isFull(stack):
    return (stack.top == (stack.capacity - 1))


def isEmpty(stack):
    return (stack.top == -1)


def push(stack, item):
    if (isFull(stack)):
        return
    stack.top += 1
    stack.array[stack.top] = item


def Pop(stack):
    if (isEmpty(stack)):
        return -sys.maxsize
    Top = stack.top
    stack.top -= 1
    return stack.array[Top]


def moveDisksBetweenTwoPoles(src, dest, s, d):
    pole1TopDisk = Pop(src)
    pole2TopDisk = Pop(dest)
    if (pole1TopDisk == -sys.maxsize):
        push(src, pole2TopDisk)
        moveDisk(d, s, pole2TopDisk)
    elif (pole2TopDisk == -sys.maxsize):
        push(dest, pole1TopDisk)
        moveDisk(s, d, pole1TopDisk)
    elif (pole1TopDisk > pole2TopDisk):
        push(src, pole1TopDisk)
        push(src, pole2TopDisk)
        moveDisk(d, s, pole2TopDisk)
    else:
        push(dest, pole2TopDisk)
        push(dest, pole1TopDisk)
        moveDisk(s, d, pole1TopDisk)


def moveDisk(fromPeg, toPeg, disk):
    print("Move the disk", disk, "from '", fromPeg, "' to '", toPeg, "'")


def tohIterative(num_of_disks, src, aux, dest):
    s, d, a = 'S', 'D', 'A'

    if (num_of_disks % 2 == 0):
        temp = d
        d = a
        a = temp
    total_num_of_moves = int(pow(2, num_of_disks) - 1)

    # Larger disks will be pushed first
    for i in range(num_of_disks, 0, -1):
        push(src, i)

    for i in range(1, total_num_of_moves + 1):
        if (i % 3 == 1):
            moveDisksBetweenTwoPoles(src, dest, s, d)

        elif (i % 3 == 2):
            moveDisksBetweenTwoPoles(src, aux, s, a)

        elif (i % 3 == 0):
            moveDisksBetweenTwoPoles(aux, dest, a, d)


def is_accepted(c):
    nbDisks = max(max(c))

    if len(c[-1]) != nbDisks:
        return False
    for k in range(nbDisks):
        if c[-1][k] != nbDisks - k:
            return False
    return True


def hanoi_soap(nbStacks, nbDisks):
    i_conf = HanoiConfiguration(nbStacks, nbDisks)
    soup = BehaviorSoup(i_conf)
    for i in range(nbStacks):
        for j in range(nbStacks):
            soup.add(f'{i}-{j}', guarde_def(i, j), action_def(i, j))
    return soup


def guarde_def(s, t):
    return lambda c: len(c[s]) and (len(c[t]) == 0 or c[s][-1] < c[t][-1])


def action_def(s, t):
    def action(c):
        disk = c[s].pop()
        c[t].append(disk)

    return action


class Hanoi(TransitionRelation, AcceptingSet):
    def __init__(self, nbStacks, nbDisks):
        self.nbDisks = nbDisks
        self.nbStacks = nbStacks

    def initial(self):
        return [HanoiConfiguration(self.nbStacks, self.nbDisks)]

    def next(self, n):
        next_states = []
        for i in range(self.nbStacks):
            new_node = copy.deepcopy(n)
            if new_node[i]:
                disk = new_node[i].pop()
                for j in range(self.nbStacks):
                    if i != j and (not new_node[j] or new_node[j][-1] > disk):
                        temp = copy.deepcopy(new_node)
                        temp[j].append(disk)
                        next_states.append(temp)
        return next_states

    def is_accepting(self, c):
        k = 0
        if not c[-1]:
            return False
        for disk in c[-1]:
            if disk != self.nbDisks - k:
                return False
            k = k + 1
        return True


class HanoiConfiguration(list):
    def __init__(self, nbStacks, nbDisks):
        list.__init__(self, [[(nbDisks - i) for i in range(nbDisks)]] + [[] for _ in range(nbStacks - 1)])

    def __hash__(self):
        hash = 0
        maxi = max(self)[0]
        for stack in self:
            hash += sum(stack) * maxi
            maxi *= 2
        return hash

    def __eq__(self, conf):
        if len(self) != len(conf):
            return False
        for i in range(len(self)):
            if len(self[i]) != len(conf[i]):
                return False
            for j in range(len(self[i])):
                if conf[i][j] != self[i][j]:
                    return False
        return True


if __name__ == '__main__':
    num_of_disks = 4
    hanoi_tower = IdentityProxy(Hanoi(3, 3))
    init = hanoi_tower.initial()[0]
    for i, j in [(0, 2), (0, 1), (2, 1), (0, 2), (1, 0), (1, 2), (0, 2)]:
        guard = guarde_def(i, j)
        action = action_def(i, j)
        g = guard(init)
        if g:
            a = action(init)
        print(f'{i},{j} : {"Vrai" if g else "Faux"} -> {init}')

    print("-------------------------")
    print("Soup")
    soup = hanoi_soap(3, 3)
    Behavior_Soup = BehSoupSemantics(soup)
    init = Behavior_Soup.initial()[0]
    print("First State: ", init)
    actions = Behavior_Soup.actions(init)

    if actions:
        for action in actions:
            execute = Behavior_Soup.execute(init, action)
            print("Output : ", execute)

    str = STRTR(Behavior_Soup)
    init = str.initial()[0]
    next = str.next(init)
    print("After ", init, ": ", next)
