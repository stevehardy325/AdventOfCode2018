package main

import (
	"fmt"
	//"io"
	"io/ioutil"
	"strconv"
	"strings"
	"time"
)

type operation struct {
	opcode func(before [6]int, op operation) [6]int
	a      int
	b      int
	c      int
}

// --------------------- ADDITION---------------
func addr(before [6]int, op operation) [6]int {
	before[op.c] = before[op.a] + before[op.b]
	return before
}

func addi(before [6]int, op operation) [6]int {
	before[op.c] = before[op.a] + op.b
	return before
}

// --------------------- Multiplication ---------------

func mulr(before [6]int, op operation) [6]int {
	before[op.c] = before[op.a] * before[op.b]
	return before
}

func muli(before [6]int, op operation) [6]int {
	before[op.c] = before[op.a] * op.b
	return before
}

// --------------------- Bitwise AND ---------------

func banr(before [6]int, op operation) [6]int {
	before[op.c] = before[op.a] & before[op.b]
	return before
}

func bani(before [6]int, op operation) [6]int {
	before[op.c] = before[op.a] & op.b
	return before
}

// --------------------- Bitwise OR ---------------

func borr(before [6]int, op operation) [6]int {
	before[op.c] = before[op.a] | before[op.b]
	return before
}

func bori(before [6]int, op operation) [6]int {
	before[op.c] = before[op.a] | op.b
	return before
}

// --------------------- Assignment ---------------

func setr(before [6]int, op operation) [6]int {
	before[op.c] = before[op.a]
	return before
}

func seti(before [6]int, op operation) [6]int {
	before[op.c] = op.a
	return before
}

// --------------------- GreaterThan ---------------

func gtir(before [6]int, op operation) [6]int {
	if op.a > before[op.b] {
		before[op.c] = 1
	} else {
		before[op.c] = 0
	}
	return before
}

func gtri(before [6]int, op operation) [6]int {
	if before[op.a] > op.b {
		before[op.c] = 1
	} else {
		before[op.c] = 0
	}
	return before
}

func gtrr(before [6]int, op operation) [6]int {
	if before[op.a] > before[op.b] {
		before[op.c] = 1
	} else {
		before[op.c] = 0
	}
	return before
}

// --------------------- Equality ---------------

func eqir(before [6]int, op operation) [6]int {
	if op.a == before[op.b] {
		before[op.c] = 1
	} else {
		before[op.c] = 0
	}
	return before
}

func eqri(before [6]int, op operation) [6]int {
	if before[op.a] == op.b {
		before[op.c] = 1
	} else {
		before[op.c] = 0
	}
	return before
}

func eqrr(before [6]int, op operation) [6]int {
	if before[op.a] == before[op.b] {
		before[op.c] = 1
	} else {
		before[op.c] = 0
	}
	return before
}

func parseProgram(filename string) ([]operation, int) {
	data, _ := ioutil.ReadFile(filename)

	program := []operation{}

	operationStrings := strings.Split(string(data), "\n")

	funcNames := make(map[string]func(before [6]int, op operation) [6]int)
	funcNames["addr"] = addr
	funcNames["addi"] = addi
	funcNames["mulr"] = mulr
	funcNames["muli"] = muli
	funcNames["banr"] = banr
	funcNames["bani"] = bani
	funcNames["borr"] = borr
	funcNames["bori"] = bori
	funcNames["setr"] = setr
	funcNames["seti"] = seti
	funcNames["gtir"] = gtir
	funcNames["gtri"] = gtri
	funcNames["gtrr"] = gtrr
	funcNames["eqir"] = eqir
	funcNames["eqri"] = eqri
	funcNames["eqrr"] = eqrr

	split := strings.Split(operationStrings[0], " ")
	pcreg, _ := strconv.Atoi(split[1])

	for i := 1; i < len(operationStrings); i++ {
		split := strings.Split(operationStrings[i], " ")
		var op operation
		op.opcode = funcNames[split[0]]
		op.a, _ = strconv.Atoi(split[1])
		op.b, _ = strconv.Atoi(split[2])
		op.c, _ = strconv.Atoi(split[3])
		program = append(program, op)
	}

	return program, pcreg
}

func runTranslatedToGo(zeroReg int) (int, int) {
	//the program as translated to Go for performance increases

	termValues := make(map[int]bool)
	var lastVal int
	var firstVal int

	reg := [6]int{zeroReg, 0, 0, 0, 0, 0}

	found := false

	for !found {
		reg[5] = reg[1] | 65536
		reg[1] = 8586263

		for true {
			reg[1] += (reg[5] & 255)
			reg[1] = reg[1] & 16777215
			reg[1] *= 65899
			reg[1] = reg[1] & 16777215

			if 256 > reg[5] {
				break
			} else {
				reg[5] /= 256
			}
		}

		if reg[0] == reg[1] {
			found = true
		}

		if !termValues[reg[1]] {
			if len(termValues) == 0 {
				firstVal = reg[1]
			}
			termValues[reg[1]] = true
			lastVal = reg[1]
		} else {
			break
		}
	}

	time.Sleep(time.Second)
	return firstVal, lastVal

}

func runProgram(prog []operation, pcreg int) int {

	registers := [6]int{0, 0, 0, 0, 0, 0}

	for registers[pcreg] < len(prog) {
		pc := registers[pcreg]

		registers = prog[pc].opcode(registers, prog[pc])

		registers[pcreg]++

		if registers[pcreg] == 28 {
			break
		}

	}

	return registers[1]

}

func main() {

	program, pcreg := parseProgram("input")
	fmt.Println("Part A:", runProgram(program, pcreg))

	_, b := runTranslatedToGo(0)
	fmt.Println("Part B:", b)

}
