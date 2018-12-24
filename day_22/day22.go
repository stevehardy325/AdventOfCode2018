package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strconv"
)

type regType int

const (
	rocky 	regType = 0
	narrow	regType = 1
	wet		regType = 2
)

type Region struct {
	rtype	regType
	x		int
	y		int
	geol	int
	ero		int
}

type Cavern [][]Region


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

	for y:=0; y <= targetY; y++ {
		row := []Region {}
		for x := 0; x <= targetX; x++ {
			newReg := Region{}
			row = append(row, newReg)
		}
		cave = append(cave, row)
	}

	for y:=0; y <= targetY; y++ {
		row := []Region {}
		for x := 0; x <= targetX; x++ {
			newReg := makeRegion(x, y, cave, depth, targetX, targetY)
			cave[y][x] = newReg
		}
		cave = append(cave, row)
	}

	return cave
}

func (cave Cavern) riskLevel() int {
	count := 0
	for y:= 0; y < len(cave); y++ {
		for x := 0; x < len(cave[y]); x++ {
			switch reg := cave[y][x]; reg.rtype {
				case wet:
					count += 1
				case narrow:
					count += 2
			}

		}
	}
	return count
}

func runFile(filename string) int {
	depth, x, y := parseFile(filename)
	cave := mapCave(depth, x, y)
	return cave.riskLevel()
}

func main() {

	fmt.Println("Part A:")
	fmt.Println(runFile("input"))

}