class Node:
    def __init__(self):
        self.childcount = None
        self.metacount = None
        self.children = []
        self.metadata = []

    def process(self, strList):
        self.childcount = int(strList[0])
        self.metacount = int(strList[1])
        start = 2
        for i in range(self.childcount):
            child = Node()
            start += child.process(strList[start:])
            self.children += [child]
        for i in range(self.metacount):
            self.metadata += [int(strList[start])]
            start += 1
        return start

    def size(self):
        return self.metacount + sum(child.size() for child in self.children)

    def totalA(self):
        a = sum(self.metadata)
        b = sum(child.totalA() for child in self.children)
        return a + b

    def totalB(self):
        if self.childcount == 0:
            a = sum(self.metadata)
        else:
            a = 0
            for index in self.metadata:
                if index <= len(self.children) and index > 0:
                    a += self.children[index-1].totalB()
        return a


def main():
    node = Node()
    with open('input') as file:
        for line in file:
            split = line.split()
            node.process(split)
    print('Part A: {}'.format(str(node.totalA())))
    print('Part B: {}'.format(str(node.totalB())))





if __name__ == '__main__':
    main()
