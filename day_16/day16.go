package main

import (
    "fmt"
    //"io"
    "io/ioutil"
    "strings"
    "regexp"
    "strconv"
)

type operation struct {
    opcode int
    a int
    b int
    c int
}

func createCopy (source [4]int) [4]int {
    var new [4]int
    for i := 0; i < 4; i++ {
        new[i] = source[i]
    }
    return new
}

// --------------------- ADDITION---------------
func addr (before [4]int, op operation) [4]int {
    before[op.c] = before[op.a] + before[op.b]
    return before
}

func addi (before [4]int, op operation) [4]int {
    before[op.c] = before[op.a] + op.b
    return before
}

// --------------------- Multiplication ---------------

func mulr (before [4]int, op operation) [4]int {
    before[op.c] = before[op.a] * before[op.b]
    return before
}

func muli (before [4]int, op operation) [4]int {
    before[op.c] = before[op.a] * op.b
    return before
}

// --------------------- Bitwise AND ---------------

func banr (before [4]int, op operation) [4]int {
    before[op.c] = before[op.a] & before[op.b]
    return before
}

func bani (before [4]int, op operation) [4]int {
    before[op.c] = before[op.a] & op.b
    return before
}

// --------------------- Bitwise OR ---------------

func borr (before [4]int, op operation) [4]int {
    before[op.c] = before[op.a] | before[op.b]
    return before
}

func bori (before [4]int, op operation) [4]int {
    before[op.c] = before[op.a] | op.b
    return before
}

// --------------------- Assignment ---------------

func setr (before [4]int, op operation) [4]int {
    before[op.c] = before[op.a]
    return before
}

func seti (before [4]int, op operation) [4]int {
    before[op.c] = op.a
    return before
}

// --------------------- GreaterThan ---------------

func gtir (before [4]int, op operation) [4]int {
    if op.a > before[op.b] {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}

func gtri (before [4]int, op operation) [4]int {
    if before[op.a] > op.b {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}

func gtrr (before [4]int, op operation) [4]int {
    if before[op.a] > before[op.b] {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}

// --------------------- Equality ---------------

func eqir (before [4]int, op operation) [4]int {
    if op.a == before[op.b] {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}

func eqri (before [4]int, op operation) [4]int {
    if before[op.a] == op.b {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}

func eqrr (before [4]int, op operation) [4]int {
    if before[op.a] == before[op.b] {
        before[op.c] = 1
    } else {
        before[op.c] = 0
    }
    return before
}


func countWorksLike(before [4]int, op operation, after [4]int, functions [16]func([4]int, operation)([4]int), opcodeMatches [16][16]bool) (int, [16][16]bool) {
    count := 0

    for i:=0; i<16; i++ {
        if functions[i](before, op) == after {
            count++
        } else {
            opcodeMatches[op.opcode][i] = false
        }
    }

    return count,opcodeMatches
}

func parseStrNumArray(numStrings []string) ([4]int, operation, [4]int) {
    var before [4]int
    var op operation
    var after [4]int

    for i:=0; i < 4; i++ {
        before[i],_ = strconv.Atoi(numStrings[i])
    }

    op.opcode,_ = strconv.Atoi(numStrings[4])
    op.a,_ = strconv.Atoi(numStrings[5])
    op.b,_ = strconv.Atoi(numStrings[6])
    op.c,_ = strconv.Atoi(numStrings[7])
    
    for i:=8; i < 12; i++ {
        after[i-8],_ = strconv.Atoi(numStrings[i])
    }

    return before, op, after
}

func run_samples(filename string) (int, [16][16]bool) {
    dat, err := ioutil.ReadFile(filename)
    regex, _ := regexp.Compile("\\d+")
    count := 0
    
    var matchArr [16][16]bool
    for i := 0; i < 16; i++ {
        for j:=0; j < 16; j++ {
            matchArr[i][j] = true
        }
    }

    if err == nil {
        functions :=  [16]func([4]int, operation)([4]int){addr, addi, mulr, muli, banr, bani, borr, bori,setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr}

        samples := strings.Split(string(dat), "\n\n")

        for i := 0; i < len(samples); i++ {
            nums := regex.FindAllString(samples[i], -1 )

            before, op, after := parseStrNumArray(nums)


            var behavesLikeNum int = 0
            behavesLikeNum,matchArr = countWorksLike(before, op, after, functions, matchArr)

            if behavesLikeNum >= 3 {
                count++
            }
        }
    }
    
    return count, matchArr
    
}

func determineMatches(matchArr [16][16]bool) [16]func([4]int, operation)([4]int) {
    for k := 0; k < 16; k++ {
        for i := 0; i < 16; i++ {
            count := 0
            num :=0
            for j := 0; j < 16; j++ {
                if matchArr[i][j] {
                    count++
                    num = j
                }
            }

            if count == 1 {
                for j := 0; j < i; j++ {
                    matchArr[j][num] = false
                }
                for j := i+1; j < 16; j++ {
                    matchArr[j][num] = false
                }
            }

        }
    }

    var opcodeFuncs [16]func([4]int, operation)([4]int)

    functionNames :=  [16]string{"addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori" , "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"}
    
    functions :=  [16]func([4]int, operation)([4]int){addr, addi, mulr, muli, banr, bani, borr, bori,setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr}

    for i := 0; i < 16; i++ {
        fmt.Printf("\nOpcode %d: \n", i)
        for j := 0; j < 16; j++ {
            if matchArr[i][j] {
                fmt.Println(functionNames[j])
                opcodeFuncs[i] = functions[j]
            }
        }
    }

    return opcodeFuncs

}

func run_program(filename string, opCodeFuncs [16]func([4]int, operation)([4]int)) int {
    data, err := ioutil.ReadFile(filename)
    registers := [4]int{0,0,0,0}

    if err == nil {
        

        regex, _ := regexp.Compile("\\d+")
        operationStrings := strings.Split(string(data), "\n")

        for i := 0; i < len(operationStrings); i++ {
            numStrings := regex.FindAllString(operationStrings[i], -1)
            
            var op operation
            op.opcode,_ = strconv.Atoi(numStrings[0])
            op.a,_ = strconv.Atoi(numStrings[1])
            op.b,_ = strconv.Atoi(numStrings[2])
            op.c,_ = strconv.Atoi(numStrings[3])

            registers = opCodeFuncs[op.opcode](registers, op)

        }


    }

    return registers[0]
}

func test() bool {
    test_res, _ :=  run_samples("test_sample")
    return test_res == 1
}

func main() {
    
    if test() {
        res, matchArr  := run_samples("sample_opcodes")
        fmt.Printf("Part A: %d\n",res)
        opCodeFuncs := determineMatches(matchArr)
        result := run_program("program", opCodeFuncs)
        fmt.Printf("\nPart B: %d\n",result)

    } else {
        fmt.Println("A test failed")
    }
  
}

