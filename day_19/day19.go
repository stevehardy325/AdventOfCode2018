package main

import (
    "fmt"
    //"io"
    "io/ioutil"
    "strings"
    "strconv"
)

type operation struct {
    opcode func(before [6]int, op operation)([6]int)
    a int
    b int
    c int
}

// --------------------- ADDITION---------------
func addr (before [6]int, op operation) [6]int {
    before[op.c] = before[op.a] + before[op.b]
    return before
}

func addi (before [6]int, op operation) [6]int {
    before[op.c] = before[op.a] + op.b
    return before
}

// --------------------- Multiplication ---------------

func mulr (before [6]int, op operation) [6]int {
    before[op.c] = before[op.a] * before[op.b]
    return before
}

func muli (before [6]int, op operation) [6]int {
    before[op.c] = before[op.a] * op.b
    return before
}

// --------------------- Bitwise AND ---------------

func banr (before [6]int, op operation) [6]int {
    before[op.c] = before[op.a] & before[op.b]
    return before
}

func bani (before [6]int, op operation) [6]int {
    before[op.c] = before[op.a] & op.b
    return before
}

// --------------------- Bitwise OR ---------------

func borr (before [6]int, op operation) [6]int {
    before[op.c] = before[op.a] | before[op.b]
    return before
}

func bori (before [6]int, op operation) [6]int {
    before[op.c] = before[op.a] | op.b
    return before
}

// --------------------- Assignment ---------------

func setr (before [6]int, op operation) [6]int {
    before[op.c] = before[op.a]
    return before
}

func seti (before [6]int, op operation) [6]int {
    before[op.c] = op.a
    return before
}

// --------------------- GreaterThan ---------------

func gtir (before [6]int, op operation) [6]int {
    if op.a > before[op.b] {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}

func gtri (before [6]int, op operation) [6]int {
    if before[op.a] > op.b {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}

func gtrr (before [6]int, op operation) [6]int {
    if before[op.a] > before[op.b] {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}

// --------------------- Equality ---------------

func eqir (before [6]int, op operation) [6]int {
    if op.a == before[op.b] {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}

func eqri (before [6]int, op operation) [6]int {
    if before[op.a] == op.b {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}

func eqrr (before [6]int, op operation) [6]int {
    if before[op.a] == before[op.b] {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}


func parseProgram(filename string) ([]operation,int) {
    data, _ := ioutil.ReadFile(filename)

    program := []operation{}


    operationStrings := strings.Split(string(data), "\n")

    funcNames := make(map[string]func(before [6]int, op operation)([6]int))
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
    pcreg,_ := strconv.Atoi(split[1])

    for i := 1; i < len(operationStrings); i++ {
        split := strings.Split(operationStrings[i], " ")
        var op operation
        op.opcode = funcNames[split[0]]
        op.a,_ = strconv.Atoi(split[1])
        op.b,_ = strconv.Atoi(split[2])
        op.c,_ = strconv.Atoi(split[3])
        program = append(program, op)
    }

    return program, pcreg
}

func runProgram(prog []operation, pcreg int) int {
    registers := [6]int{0,0,0,0,0,0}

    for registers[pcreg] < len(prog) {
        pc := registers[pcreg]


        registers = prog[pc].opcode(registers, prog[pc])

        registers[pcreg]++
        //fmt.Println(registers)
    }

    return registers[0]

}

func test() bool {
    program, pcreg := parseProgram("test_input")
    return runProgram(program, pcreg) == 7
}

func main() {

    if test() {
        fmt.Println("Test Passed")

        program, pcreg := parseProgram("input")
        fmt.Println("Part A:", runProgram(program, pcreg))

    } else {
        fmt.Println("A test failed")
    }

}
