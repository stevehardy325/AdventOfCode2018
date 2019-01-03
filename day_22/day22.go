package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strconv"
    	"math"
    	"container/heap"
    	"time"
)

// ========================== Constants

type regType int
type toolType int

const (
	rocky 	regType = 0
	narrow	regType = 1
	wet		regType = 2

    gear    toolType = 0
    torch   toolType = 1
    neither toolType = 2
)

// ======================== Region Struct, Methods, and Constructor

type Region struct {
	rtype	regType
	x		int
	y		int
	geol	int
	ero		int
}

func (reg Region) acceptableTools() []toolType {
    var tools []toolType

    switch reg.rtype {
        case rocky:     tools = []toolType {gear, torch}
        case wet:       tools = []toolType {gear, neither}
        case narrow:    tools = []toolType {torch, neither}
    }
    return tools
}

func makeRegion(x int, y int, cave Cavern, depth int, targetX int, targetY int) *Region {
	newReg := Region{}
	newReg.x = x
	newReg.y = y
	//calculate geologic
	if x == 0 && y == 0 {
		newReg.geol = 0
	} else if y == targetY && x == targetX {
		newReg.geol = 0
	} else if y == 0 {
		newReg.geol = x * 16807
	} else if x == 0 {
		newReg.geol = y * 48271
	} else {
		newReg.geol = cave[y-1][x].ero  * cave[y][x-1].ero
	}
	//calculate erosion
	newReg.ero = (newReg.geol + depth) % 20183
	switch (newReg.ero % 3) {
		case 0: newReg.rtype = rocky
		case 1: newReg.rtype = wet
		case 2: newReg.rtype = narrow
	}

	return &newReg
}

// =================== NavRegion and Priority Queue for Dijkstra's

type NavRegion struct {
    *Region
    tool toolType
}

type PQNavRegion struct {
    NavRegion
    dist float64
}

type PriorityQueue []PQNavRegion
func (pq PriorityQueue) Len() int {return len(pq)}
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].dist < pq[j].dist }
func (pq PriorityQueue) Swap(i,j int) { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PriorityQueue) Push(i interface{}) { *pq = append(*pq, i.(PQNavRegion)) } 
func (pq *PriorityQueue) Pop() interface {} {
    old := *pq
    n := len(old)
    popped := old[n-1]
    *pq = old[0:n-1]
    return popped
}

//  =================== Cavern Struct for holding Regions

type Cavern [][]*Region

func mapCave(depth int, targetX int, targetY int) Cavern {
    //Constructor for a Cavern
	
    extendedX := targetX + 25
    extendedY := targetY + 25

    //make the slice grid first
    cave := make(Cavern, extendedY+1)
	for y:=0; y <= extendedY; y++ {
        cave[y] = make([]*Region, extendedX+1)
	}

    //now we populate
	for y:=0; y <= extendedY; y++ {
		for x := 0; x <= extendedX; x++ {
			newReg := makeRegion(x, y, cave, depth, targetX, targetY)
			cave[y][x] = newReg
		}
	}

	return cave
}

func (cave Cavern) riskLevel(x int, y int) int {
    //calculate the total risk level (for part A)
	count := 0
    num := 0
	for i:= 0; i <= y; i++ {
		for j := 0; j <= x; j++ {
            num += 1
			switch reg := cave[i][j]; reg.rtype {
				case wet:
					count += 1
				case narrow:
					count += 2
			}
		}
	}
	return count
}

func (cave Cavern) getNeighbors(reg NavRegion) []NavRegion {
    //return a list of all neighboring NavRegions
    //this includes (current coordinate) + (alternative tool)
    //and (adjacent coordinates) + (current tool)
    x := reg.x
    y := reg.y

    //only x's and y's inside the cave are valid
    minX := max(x-1,0)
    minY := max(y-1,0)
    maxX := min(x+1,len(cave[0])-1)
    maxY := min(y+1,len(cave)-1)

    //determine the other acceptable tool
    curTool := reg.tool
    var otherTool toolType
    validTools := reg.Region.acceptableTools()
    if curTool == validTools[0] {
        otherTool = validTools[1]
    } else {
        otherTool = validTools[0]
    }

    //populate the neighbor list
    neighbors := []NavRegion {}
    for i := minY; i <= maxY; i++ {
        for j := minX; j <= maxX; j++ {
            if (i == y && j == x) { 
                neighbors = append(neighbors, NavRegion {cave[i][j], otherTool})
            } else if (i == y || j == x) {
                neighbors = append(neighbors, NavRegion {cave[i][j], curTool})
            }
        }
    }

    return neighbors
}


func (cave Cavern) timeBetween(a NavRegion, b NavRegion) float64 {
    //the time 'distance' between two Navigational regions
    var timeBetween float64

    if a.tool == b.tool {
        timeBetween = 1
    } else {
        timeBetween = 7
    }
    
    return timeBetween
}

func (cave Cavern) dijkstra(x int, y int) int {
    //a variation of dijkstra's algorithm, but using NavRegions (which include tools)
    //rather than pure regional coordinates


    //initialize the hashtables and priority queue
    unvisited :=    make(map[NavRegion]bool) //using in place of a set datatype
    distance :=     make(map[NavRegion]float64)
    prev :=         make(map[NavRegion]NavRegion)
    pq :=           new(PriorityQueue)
    heap.Init(pq)
    
    for i := 0; i < len(cave); i++ {
        for j := 0; j < len(cave[i]); j++ {
            reg := cave[i][j]
            for _, tool := range reg.acceptableTools() {
                nav := NavRegion {reg, tool}
                unvisited[nav] = true
                distance[nav] = math.Inf(1)
                pqnav := PQNavRegion{nav, math.Inf(1)}
                heap.Push(pq, pqnav)
            }
        }
    }

    start := NavRegion {cave[0][0], torch}
    distance[start] = 0
    unvisited[start] = true
    pqnav := PQNavRegion{start, 0}
    heap.Push(pq, pqnav)

    //run until we either run out of valid spaces or hit the target
    hitTarget := false
    for len(unvisited) > 0 && !hitTarget {
        min := heap.Pop(pq)
        selected := min.(PQNavRegion).NavRegion
        
        if selected == (NavRegion{cave[y][x], torch}) {
            //we found the target, so we can end
            hitTarget = true
        } else if _, exists := unvisited[selected]; exists {
            //only run on yet-unvisited nodes
            delete(unvisited, selected)
            neighbors := cave.getNeighbors(selected)

            for i := 0; i < len(neighbors); i++ {
                n := neighbors[i]

                if _, exists := unvisited[n]; exists {

                    alt := distance[selected] + cave.timeBetween(selected, n)
                    if alt < distance[n] {
                        distance[n] = alt
                        prev[n] = selected
                        //we also want to push to the priority queue, which tracks shortest distances
                        pqnav := PQNavRegion{n, alt}
                        heap.Push(pq, pqnav)
                    }
                }
            }
        }
    }

    return int(distance[NavRegion{cave[y][x], torch}])
}

// ========================= General Functions

func parseFile(filename string) (int, int, int) {
	data, _ := ioutil.ReadFile(filename)

	r, _ := regexp.Compile("\\d+")
	nums := r.FindAllString(string(data), -1)

	depth,_ := strconv.Atoi(nums[0])
	x,_ := strconv.Atoi(nums[1])
	y,_ := strconv.Atoi(nums[2])

	return depth, x, y
}

func min(a int, b int) int {
    if a < b {
        return a
    } else {
        return b
    }
}

func max(a int, b int) int {
    if a > b {
        return a
    } else {
        return b
    }
}

func runFile(filename string) int {
	depth, x, y := parseFile(filename)
	cave := mapCave(depth, x, y)
	return cave.riskLevel(x, y)
}

func distFile(filename string) int {
	depth, x, y := parseFile(filename)
	cave := mapCave(depth, x, y)
	return cave.dijkstra(x, y)
}

func main() {
    var start time.Time
    var end time.Time

    fmt.Println("Running Day 22")

    start = time.Now()
	fmt.Print("Part A: \t")
	fmt.Println(runFile("input"))
    end = time.Now()
    fmt.Println("Runtime:\t", end.Sub(start))

    start = time.Now()
    fmt.Print("Part B: \t")
    fmt.Println(distFile("input"))
    end = time.Now()
    fmt.Println("Runtime:\t", end.Sub(start))

}
