package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strconv"
   	"math"
)

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

type Region struct {
	rtype	regType
	x		int
	y		int
	geol	int
	ero		int
}

type NavRegion struct {
    Region
    tool toolType
}

type Cavern [][]Region

func acceptableTools(reg Region) []toolType {
    var tools []toolType

    switch reg.rtype {
        case rocky:     tools = []toolType {gear, torch}
        case wet:       tools = []toolType {gear, neither}
        case narrow:    tools = []toolType {torch, neither}
    }
    return tools
}


func makeRegion(x int, y int, cave Cavern, depth int, targetX int, targetY int) Region {
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

	return newReg
}

func parseFile(filename string) (int, int, int) {
	data, _ := ioutil.ReadFile(filename)

	r, _ := regexp.Compile("\\d+")
	nums := r.FindAllString(string(data), -1)

	depth,_ := strconv.Atoi(nums[0])
	x,_ := strconv.Atoi(nums[1])
	y,_ := strconv.Atoi(nums[2])

	return depth, x, y
}

func mapCave(depth int, targetX int, targetY int) Cavern {
	cave := Cavern {}
    extendedX := targetX + 25
    extendedY := targetY + 25
    
	for y:=0; y <= extendedY; y++ {
		row := []Region {}
		for x := 0; x <= extendedX; x++ {
			newReg := Region{}
			row = append(row, newReg)
		}
		cave = append(cave, row)
	}

	for y:=0; y <= extendedY; y++ {
		for x := 0; x <= extendedX; x++ {
			newReg := makeRegion(x, y, cave, depth, targetX, targetY)
			cave[y][x] = newReg
		}
	}

	return cave
}

func (cave Cavern) riskLevel(x int, y int) int {
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

func getMinimumNode(unvisited map[NavRegion]bool, distance map[NavRegion]float64) NavRegion {
    minDist := math.Inf(1)
    for key := range unvisited {
        dist := distance[key]
        if dist < minDist {
            minDist = dist
        }
    }

    var selected NavRegion
    for key := range unvisited {
        if distance[key] == minDist {
            selected = key
            break
        }
    }

    return selected
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

func (cave Cavern) getNeighbors(reg NavRegion) []NavRegion {
    x := reg.x
    y := reg.y

    minX := max(x-1,0)
    minY := max(y-1,0)
    maxX := min(x+1,len(cave[0])-1)
    maxY := min(y+1,len(cave)-1)

    curTool := reg.tool
    var otherTool toolType
    validTools := acceptableTools(reg.Region)
    if curTool == validTools[0] {
        otherTool = validTools[1]
    } else {
        otherTool = validTools[0]
    }

    neighbors := []NavRegion {}

    for i := minY; i <= maxY; i++ {
        for j := minX; j <= maxX; j++ {
            if !(i == y && j == x) { 
                neighbors = append(neighbors, NavRegion {cave[i][j], otherTool})
            } else if (i == y || j == x) {
                neighbors = append(neighbors, NavRegion {cave[i][j], curTool})
            }
        }
    }

    return neighbors
}

func (cave Cavern) length(a NavRegion, b NavRegion) float64 {
    var length float64

    if a.tool == b.tool {
        length = 1
    } else {
        length = 7
    }
    
    return length
}

func (cave Cavern) djikstra(x int, y int) int {
    unvisited := make(map[NavRegion]bool)
    distance := make(map[NavRegion]float64)
    prev := make(map[NavRegion]NavRegion)

    
    for i := 0; i < len(cave); i++ {
        for j := 0; j < len(cave[i]); j++ {
            reg := cave[i][j]
            for _, tool := range acceptableTools(reg) {
                nav := NavRegion {reg, tool}
                unvisited[nav] = true
                distance[nav] = math.Inf(1)
            }
            
        }
    }

    start := NavRegion {cave[0][0], torch}

    distance[start] = 0

    for len(unvisited) > 0 {
        fmt.Println("Left:", len(unvisited))
        selected := getMinimumNode(unvisited, distance)
        delete(unvisited, selected)

        if selected == (NavRegion{cave[y][x], torch}) {
            break
        }

        neighbors := cave.getNeighbors(selected)
        for i := 0; i < len(neighbors); i++ {
            n := neighbors[i]
            if _, exists := unvisited[n]; exists {
                alt := distance[selected] + cave.length(selected, n)
                if alt < distance[n] {
                    distance[n] = alt
                    prev[n] = selected
                }
            }
        }
    }

    
    return int(distance[NavRegion{cave[y][x], torch}])
}

func runFile(filename string) int {
	depth, x, y := parseFile(filename)
	cave := mapCave(depth, x, y)
	return cave.riskLevel(x, y)
}

func distFile(filename string) int {
	depth, x, y := parseFile(filename)
	cave := mapCave(depth, x, y)
	return cave.djikstra(x, y)
}

func main() {

	fmt.Println("Part A:")
	fmt.Println(runFile("input"))
    fmt.Println(distFile("input"))

}
