from datetime import datetime
import operator

class Event:
    def __init__(self, str):
        split_up = str.split('] ')
        timestamp = split_up[0][1:]
        self.dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
        self.eventstr = split_up[1]

    def __lt__(self, other):
        return self.dt < other.dt

    def __repr__(self):
        return str(self.dt) + ' ' + self.eventstr


class Guard:
    def __init__(self, id):
        self.id = id
        self.sleep_tab = dict()
        self.sleep_count = 0

    def addSleep(self, minute):
        if minute not in self.sleep_tab:
            self.sleep_tab[minute] = 0
        self.sleep_tab[minute] += 1
        self.sleep_count += 1

    def getMostOftenMinute(self):
        return max(self.sleep_tab.items(), key=operator.itemgetter(1))[0]

    def getSleepAtHighestMinute(self):
        return max(self.sleep_tab.values())


    def __lt__(self, other):
        return self.sleep_count < other.sleep_count

    def __repr__(self):
        return str(self.id) + ' ' + str(self.sleep_count)

def main():
    filename = "input"

    events = []
    guardDict = dict()
    current = None
    last_timestamp = None

    with open(filename, "r") as file:
        for line in file:
            events += [Event(line)]

    events.sort()
    #print(events)

    for e in events:
        split_up = e.eventstr.split()
        if e.eventstr.startswith('G'):
            current = int(split_up[1][1:])
        elif e.eventstr.startswith('w'):
            if current not in guardDict:
                guardDict[current] = Guard(current)
            for t in range(last_timestamp, e.dt.minute):
                guardDict[current].addSleep(t)

        last_timestamp = e.dt.minute

    #Strategy 1: Find the guard that has the most minutes asleep.
    # What minute does that guard spend asleep the most?

    guards = list(guardDict.values())
    sleepiest = max(guards)

    sleptMost = sleepiest.getMostOftenMinute()

    print('{}*{}={}'.format(sleepiest.id, sleptMost, sleepiest.id*sleptMost))

    #Strategy 2: Of all guards,
    #which guard is most frequently asleep on the same minute?

    mostOftenSlept = []
    for id in guardDict:
        mostOftenSlept += [[id, guardDict[id].getSleepAtHighestMinute()]]

    mostOftenSlept.sort(reverse=True,key=operator.itemgetter(1))

    part2id = mostOftenSlept[0][0]
    part2weight = mostOftenSlept[0][1]
    sleep_tab = guardDict[part2id].sleep_tab
    for time in sleep_tab:
        if sleep_tab[time] == part2weight:
            part2time = time

    print('{}*{}={}'.format(part2id, part2time, part2id*part2time))



if __name__ == '__main__':
    main()
