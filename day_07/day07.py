class Node:
    def __init__(self, letter):
        self.letter = letter
        self.before = set()
        self.after = set()

    def __lt__(self, other):
        return self.letter < other.letter

    def __repr__(self):
        return self.letter

def link(pre, post):
    pre.after.add(post)
    post.before.add(pre)

def main():
    steps = dict()
    with open("input") as file:
        for line in file:
            split = line.split(' must be finished before step ')
            pre = split[0][-1:]
            post = split[1][0]
            if pre not in steps:
                steps[pre] = Node(pre)
            if post not in steps:
                steps[post] = Node(post)
            link(steps[pre], steps[post])

    print(steps)
    done = set()
    stepsList = list(steps.values())
    order = []
    while(len(stepsList) > 0):
        #print(min([step for step in stepsList if (step.before.issubset(done) or len(step.before) == 0)]), )
        next = min([step for step in stepsList if (step.before.issubset(done) or len(step.before) == 0)])
        order += [next]
        done.add(next)
        stepsList.remove(next)

    print(''.join(str(v) for v in order))



if __name__ == '__main__':
    main()
