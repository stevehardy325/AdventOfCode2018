class Node:
    def __init__(self, letter):
        self.letter = letter
        self.before = set()
        self.after = set()

    def __lt__(self, other):
        return self.letter < other.letter

    def __repr__(self):
        return self.letter

    def __str__(self):
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

    done = set()
    stepsList = list(steps.values())
    order = []
    while(len(stepsList) > 0):
        next = min([step for step in stepsList if step.before.issubset(done)])
        order += [next]
        done.add(next)
        stepsList.remove(next)

    print('Part A: ' + ''.join(str(v) for v in order))

    done = set()
    stepsList = list(steps.values())
    curTime = -1
    nextIndex = 0
    workers = [None for i in range(5)]
    while(len(done) < len(order)):
        curTime += 1
        for i in range(len(workers)):
            worker = workers[i]
            if worker != None:
                worker[1] -= 1
                if worker[1] <= 0:
                    done.add(worker[0])
                    workers[i] = None

        while len([step for step in stepsList if step.before.issubset(done)]) != 0 and None in workers:
            next = min([step for step in stepsList if step.before.issubset(done)])
            time = ord(str(next).lower()) - 96 + 60
            workerIndex = workers.index(None)
            workers[workerIndex] = [next, time]
            stepsList.remove(next)





        print('{}: {}'.format(curTime, workers))


    print('Part B: {}'.format(curTime))



if __name__ == '__main__':
    main()
