package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
	//"time"
)

const (
	sandBlock  int = 0
	clayBlock  int = 1
	flowWater  int = 2
	spring     int = 3
	stillWater int = 4
)

func getClayDeposits(filename string) ([][2]int, int, int, int, int) {
	data, _ := ioutil.ReadFile(filename)

	veinStrings := strings.Split(string(data), "\n")

	clayDeposits := make([][2]int, 0)
	var xmin int
	var xmax int
	var ymin int
	var ymax int

	firstRun := true

	for i := 0; i < len(veinStrings); i++ {
		coords := strings.Split(veinStrings[i], ", ")
		l_coord := strings.Split(coords[0], "=")
		r_coords := strings.Split(strings.Split(coords[1], "=")[1], "..")

		var x_start, x_end, y_start, y_end int

		if l_coord[0] == "x" {
			x_coord, _ := strconv.Atoi(l_coord[1])
			if firstRun || xmax <= x_coord {
				xmax = x_coord + 2
			}
			if firstRun || xmin >= x_coord {
				xmin = x_coord - 1
			}

			x_start = x_coord
			x_end = x_coord

			y_start, _ = strconv.Atoi(r_coords[0])
			y_end, _ = strconv.Atoi(r_coords[1])

			if firstRun || y_end >= ymax {
				ymax = y_end + 1
			}
			if firstRun || y_start < ymin {
				ymin = y_start
			}

		} else {
			y_coord, _ := strconv.Atoi(l_coord[1])
			if firstRun || ymax <= y_coord {
				ymax = y_coord + 1
			}
			if firstRun || y_coord < ymin {
				ymin = y_coord
			}

			y_start = y_coord
			y_end = y_coord

			x_start, _ = strconv.Atoi(r_coords[0])
			x_end, _ = strconv.Atoi(r_coords[1])

			if firstRun || xmax <= x_end {
				xmax = x_end + 2
			}
			if firstRun || xmin >= x_start {
				xmin = x_start - 1
			}

		}

		for i := x_start; i <= x_end; i++ {
			for j := y_start; j <= y_end; j++ {
				clayDeposits = append(clayDeposits, [2]int{i, j})
			}

		}

		firstRun = false
	}

	return clayDeposits, xmin, xmax, ymin, ymax
}

func buildGrid(clayDeposits [][2]int, xmin int, xmax int, ymin int, ymax int) [][]int {
	offset := 0 - xmin

	grid := [][]int{}

	for i := 0; i < ymax; i++ {
		row := []int{}
		for j := 0; j < (xmax + offset + 1); j++ {
			row = append(row, sandBlock)
		}
		grid = append(grid, row)
	}

	for i := 0; i < len(clayDeposits); i++ {
		x := clayDeposits[i][0] + offset
		y := clayDeposits[i][1]
		grid[y][x] = clayBlock
	}

	grid[0][500+offset] = spring

	return grid

}

func printGrid(grid [][]int) {

	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid[0]); j++ {
			var strRep string
			if grid[i][j] == sandBlock {
				strRep = " "
			} else if grid[i][j] == flowWater {
				strRep = "|"
			} else if grid[i][j] == clayBlock {
				strRep = "#"
			} else if grid[i][j] == spring {
				strRep = "+"
			} else if grid[i][j] == stillWater {
				strRep = "~"
			}
			print(strRep)
		}
		fmt.Println()
	}
}

func writeGrid(grid [][]int) {
	bytes := []byte{}
	for i := 0; i < len(grid); i++ {

		for j := 0; j < len(grid[0]); j++ {
			var strRep byte
			if grid[i][j] == sandBlock {
				strRep = ' '
			} else if grid[i][j] == flowWater {
				strRep = '|'
			} else if grid[i][j] == clayBlock {
				strRep = '#'
			} else if grid[i][j] == spring {
				strRep = '+'
			} else if grid[i][j] == stillWater {
				strRep = '~'
			}
			bytes = append(bytes, strRep)
		}
		bytes = append(bytes, '\n')
	}

	_ = ioutil.WriteFile("tmp", bytes, 0644)
}

func flowGrid(grid [][]int, minY int) (int, int) {

	run := true
	for run {

		newGrid := [][]int{}

		for i := 0; i < len(grid); i++ {
			row := []int{}
			for j := 0; j < len(grid[0]); j++ {
				row = append(row, sandBlock)
			}
			newGrid = append(newGrid, row)
		}

		for i := 0; i < len(grid); i++ {
			for j := 0; j < len(grid[0]); j++ {
				block := grid[i][j]
				if block == clayBlock {
					newGrid[i][j] = clayBlock
				} else if block == stillWater {
					newGrid[i][j] = stillWater
				} else if block == spring {
					newGrid[i][j] = spring
					newGrid[i+1][j] = flowWater
				} else if block == flowWater {
					if i+1 < len(grid) {
						if grid[i+1][j] != clayBlock && grid[i+1][j] != stillWater {
							newGrid[i+1][j] = flowWater
						} else {
							left := 0
							leftHole := false
							right := 0
							rightHole := false

							for foundLeft := false; !foundLeft; {
								leftOfLeft := grid[i][j-left-1]
								belowLeft := grid[i+1][j-left]
								if leftOfLeft == clayBlock {
									foundLeft = true
									leftHole = false
								}
								if belowLeft != clayBlock && belowLeft != stillWater {
									foundLeft = true
									leftHole = true
								}
								left++
							}

							for foundRight := false; !foundRight; {
								rightOfRight := grid[i][j+right+1]
								belowright := grid[i+1][j+right]
								if rightOfRight == clayBlock {
									foundRight = true
									rightHole = false
								}
								if belowright != clayBlock && belowright != stillWater {
									foundRight = true
									rightHole = true
								}
								right++
							}
							var fillType int
							if leftHole || rightHole {
								fillType = flowWater
							} else {
								fillType = stillWater
							}

							for pos := j - left + 1; pos < j+right; pos++ {
								newGrid[i][pos] = fillType
							}
						}
					}

				}

			}
		}

		changed := false
		for i := 0; i < len(grid) && !changed; i++ {
			for j := 0; j < len(grid[0]) && !changed; j++ {
				if newGrid[i][j] != grid[i][j] {
					changed = true
				}
			}
		}

		//printGrid(newGrid)

		//fmt.Println("\n\n\n\n")

		if !changed {
			run = false
		} else {
			grid = newGrid

		}
		//time.Sleep(time.Second*3)

	}

	countA := 0
	countB := 0
	for i := minY; i < len(grid); i++ {
		for j := 0; j < len(grid[0]); j++ {
			if grid[i][j] == stillWater {
				countA++
				countB++
			} else if grid[i][j] == flowWater {
				countA++
			}
		}
	}
	printGrid(grid)
	writeGrid(grid)

	return countA, countB
}

func main() {
	clayDeposits, xmin, xmax, ymin, ymax := getClayDeposits("input")
	grid := buildGrid(clayDeposits, xmin, xmax, ymin, ymax)
	a, b := flowGrid(grid, ymin)
	fmt.Println("Part A: ", a, "\nPart B: ", b)

}
