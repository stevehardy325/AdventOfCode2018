package main

import (
    "fmt"
    "strings"
    "io/ioutil"
    "time"
)

type landType int

const (
    //the different acre types
    open    landType = 0
    tree    landType = 1
    yard    landType = 2
)

type acre struct {
    //struct for holding data for a 1 acre plot
    x           int
    y           int
    land        landType
}

func areaString(area [][]acre) string {
    //return a string representation of an area map
    bytes := []byte{}
    for i := 0; i < len(area); i++ {
        for j := 0; j < len(area[i]); j++ {

            var charRep byte

            switch lt := area[i][j].land; lt {
                case open: charRep = '.'
                case tree: charRep = '|'
                case yard: charRep = '#'
                default: charRep = '?'
            }

            bytes = append(bytes, charRep)
        }

        bytes = append(bytes, '\n')
    }

    return string(bytes[:len(bytes) - 1])
}

func numAdjacent(x int, y int, area [][]acre, searchLand landType) int {
    //count the number of plots of the given type which are adjacent to the plot at x,y
    count := 0

    for i := -1; i < 2; i++ {
        for j := -1; j < 2; j++ {
            testX := x + j
            testY := y + i

            if  (i != 0 || j != 0) && 
                testY >= 0 && testY < len(area) &&
                testX >= 0 && testX < len(area[testY]) {

                if area[testY][testX].land == searchLand {
                    count++
                }
            }
        }
    }

    return count
}

func openGrows(section acre, area [][]acre) bool {
    //check if an open plot of land grows 

    grows := false
    treeCount := numAdjacent(section.x, section.y, area, tree)
    if treeCount >= 3 {
        grows = true
    }
    return grows
}

func treeCut(section acre, area [][]acre) bool {
    //check if a current acre of trees will become a lumber yard

    cut := false
    yardCount := numAdjacent(section.x, section.y, area, yard)
    if yardCount >= 3 {
        cut = true
    }

    return cut
}

func yardClears(section acre, area [][]acre) bool {
    //check if a lumber yard will run out of trees and clear to open land

    clears := false

    treeCount := numAdjacent(section.x, section.y, area, tree)
    yardCount := numAdjacent(section.x, section.y, area, yard)
    
    if treeCount < 1 || yardCount < 1 {
        clears = true
    }

    return clears
}

func getInitialState(filename string) [][]acre {
    //parse the initial state of a map from a given filename
    //then return that acre map

    area := [][]acre{}
    data, _ := ioutil.ReadFile(filename)
    lines := strings.Split(string(data), "\n")

    for i := 0; i < len(lines); i++ {
        line := lines[i]
        row := []acre{}

        for j := 0; j < len(line); j++ {
            var land landType

            switch character := line[j]; character {
                case byte('.'): land = open
                case byte('#'): land = yard
                case byte('|'): land = tree
            }

            newAcre := acre{j, i, land}
            row = append(row, newAcre)
        }
        area = append(area, row)
    }

    return area
}

func transformArea(initial [][]acre) [][]acre {
    //take a map, return the next iteration of it based on transformation rules

    //transformations all happen at once, so we can't change overwrite the old area
    afterArea := [][]acre{}

    for i := 0; i < len(initial); i++ {
        afterRow := []acre{}

        for j := 0; j < len(initial[i]); j++ {

            section := initial[i][j]
            var afterSection acre
            afterSection.x = j
            afterSection.y = i

            //detemine the new state based on the old state
            switch section.land {
                case open:
                    if openGrows(section, initial) {
                        afterSection.land = tree
                    } else {
                        afterSection.land = open
                    }
                case tree:
                    if treeCut(section, initial) {
                        afterSection.land = yard
                    } else {
                        afterSection.land = tree
                    }
                case yard:
                    if yardClears(section, initial) {
                        afterSection.land = open
                    } else {
                        afterSection.land = yard
                    }
            }

            afterRow = append(afterRow, afterSection)
        }

        afterArea = append(afterArea, afterRow)
    }

    return afterArea
}

func getResouceValue(area [][]acre) int {
    //calculate the "resource value" from a given area map

    treeCount := 0
    yardCount := 0

    for i := 0; i < len(area); i++ {
        for j := 0; j < len(area[i]); j++ {
            switch area[i][j].land {
                case tree: treeCount++
                case yard: yardCount++
            }
        }
    }

    return treeCount * yardCount
}

func checkEqual(a []int, b []int) bool {
    //see if two int slices are equal
    equal := true

    if len(a) == len(b) {
        for i := 0; i < len(a) && equal; i++ {
            if a[i] != b[i] {
                equal = false
            }
        }
    } else {
        equal = false
    }

    return equal
}

func checkLoop(values []int) (bool, int, int) {
    //check to see if the list of values has become cyclical
    //returns whether or not, and if so, the start and period

    found := false
    start := -1
    period := -1

    //only check for loops of lenght 5 or longer
    for i := 5; i <= len(values)/2 && !found; i++ {

        //method: check if the i'th last values in the list are the same as the i'th before that

        a := values[len(values) - i:]
        b := values[len(values)-i*2:len(values) - i]

        if checkEqual(a, b) {
            found = true
            start = len(values)-i*2
            period = i
        }
    }


    return found, start, period
}

func resValNMinutes(filename string, n int, verbose bool) int {
    //calculate the resource value of a given input file after n minutes

    state := getInitialState(filename)
    if verbose {
        fmt.Println("T",0, "\n", areaString(state))
    }

    resValues := []int {getResouceValue(state)}

    foundLoop := false
    var start int
    var period int

    for i:= 1; i <= n && !foundLoop; i++ {
        state = transformArea(state)

        if verbose && i % 1 == 0 {
            //print the state if we requested verbosity
            fmt.Println("T",i, "\n", areaString(state))
            time.Sleep(time.Second/8)
        }

        resValues = append(resValues, getResouceValue(state))

        //cycle-checking for exceptionally long runtimes (like in part B)
        foundLoop, start, period = checkLoop(resValues)
    }


    var resVal int
    if foundLoop {
        //we exited early because of a cycle. we'll have to extrapolate the values

        fmt.Println("Cycle detected. Extrapolating...")
        time.Sleep(time.Second)
        dif := n - start
        cycleState := dif % period

        resVal = resValues[start + cycleState]
    } else {
        resVal = getResouceValue(state)
    }

    return resVal
}

func main() {
    if resValNMinutes("test_input", 10, false) == 1147 {
        fmt.Println("All tests passed")
        time.Sleep(time.Second/4)

        a := resValNMinutes("input", 10, true)
        b := resValNMinutes("input", 1000000000 , true)

        fmt.Println("Part A: ", a)
        fmt.Println("Part B: ", b)
    }
}
