package main

import (
    "fmt"
    "io/ioutil"
)

type Coord struct {
    x   int
    y   int
}

type Room struct {
    Coord
    n   bool
    s   bool
    e   bool
    w   bool
}

func stepRooms(dirRune rune, rooms map[Coord]Room, curRooms map[Coord]bool) (map[Coord]Room, map[Coord]bool) {
    directions := make(map[rune]Coord)

    directions['N'] = Coord{ 0,-1}
    directions['S'] = Coord{ 0, 1}
    directions['E'] = Coord{ 1, 0}
    directions['W'] = Coord{-1, 0}

    newRooms := make(map[Coord]bool)

    for startCoord := range curRooms {
        change := directions[dirRune]
        endCoord := Coord{startCoord.x + change.x, startCoord.y + change.y}

        if _, ok := rooms[endCoord]; !ok {
            newRoom := Room{}
            newRoom.Coord = endCoord
            rooms[endCoord] = newRoom
        }

        startRoom := rooms[startCoord]
        endRoom := rooms[endCoord]

        switch dirRune {
            case 'N':
                startRoom.n = true
                endRoom.s = true
            case 'S':
                startRoom.s = true
                endRoom.n = true
            case 'E':
                startRoom.e = true
                endRoom.w = true
            case 'W':
                startRoom.w = true
                endRoom.e = true
        }

        rooms[startCoord] = startRoom
        rooms[endCoord] = endRoom

        newRooms[endCoord] = true
    }

    return rooms, newRooms

}

func parseRegex(rx string, rooms map[Coord]Room, startRooms map[Coord]bool) (map[Coord]Room, map[Coord]bool, int) {

    curRooms := startRooms

    end := false
    var i int;
    for i = 1; !end; i++ {
        //fmt.Println(rooms)
        
        char := rune(rx[i])
        switch char {
            case 'N', 'S', 'E', 'W':
                rooms, curRooms = stepRooms(char, rooms, curRooms)
            case '|':
                curRooms = startRooms
            case '(':
                var skip int
                rooms, curRooms, skip = parseRegex(rx[i:], rooms, curRooms)
                i = i + skip - 1
            case ')', '$':
                end = true
        }
    }

    return rooms, curRooms, i

}

func strRooms(rooms map[Coord]Room) string{

    minX := 0
    maxX := 0
    minY := 0
    maxY := 0

    for _, v := range rooms {
        if v.x < minX {
            minX = v.x
        }
        if v.x > maxX {
            maxX = v.x
        }
        if v.y < minY {
            minY = v.y
        }
        if v.y > maxY {
            maxY = v.y
        }
    }

    chars := []rune{}

    for i := 0; i <= (maxX - minX + 1)*2 ; i++ {
        chars = append(chars, '#')
    }
    chars = append(chars, '\n')

    for i := minY; i <= maxY; i++ {
        
        for j := 1; j < 3; j++ {
            chars = append(chars, '#')

            for k := minX; k <= maxX; k++ {
                for l := 1; l < 3; l++ {

                    curRoom := rooms[Coord{k, i}]
                    
                    if j == 1 && l == 1 {
                        chars = append(chars, ' ')
                    } else if j == 1 && ((l == 0 && curRoom.w) || (l == 2 && curRoom.e)){
                        chars = append(chars, '|')
                    } else if l == 1 && ((j == 0 && curRoom.n) || (j == 2 && curRoom.s)){
                        chars = append(chars, '-')
                    } else {
                        chars = append(chars, '#')
                    }
                }
            }

            chars = append(chars, '\n')
        }
    }

    return string(chars)
    

}

func testPrint(rx string) {
    rooms := make(map[Coord]Room)
    start := Room{}
    start.Coord = Coord{0,0}

    rooms[start.Coord] = start
    curRooms := make(map[Coord]bool)
    curRooms[start.Coord] = true

    rooms, curRooms, _ = parseRegex(rx, rooms, curRooms)
    fmt.Println(strRooms(rooms))
    fmt.Println("done")

}

func longestPathRegex(regex string) (int,int) {
    rooms := make(map[Coord]Room)
    start := Room{}
    start.Coord = Coord{0,0}

    rooms[start.Coord] = start
    curRooms := make(map[Coord]bool)
    curRooms[start.Coord] = true

    rooms, _, _ = parseRegex(regex, rooms, curRooms)
    fmt.Println(strRooms(rooms))
    return longestPath(0,0, rooms)
}

func longestPath(x int, y int, rooms map[Coord]Room) (int, int) {
    start := Coord{x,y}

    distance := make(map[Coord]int)
    distance[start] = 0

    queue := []Coord{start}

    for len(queue) > 0 {
        current := queue[0]
        nextDist := distance[current] + 1
        if rooms[current].n {
            neighbor := Coord{current.x, current.y - 1}
            if _, ok := distance[neighbor]; !ok {
                distance[neighbor] = nextDist
                queue = append(queue, neighbor)
            }
        }
        if rooms[current].s {
            neighbor := Coord{current.x, current.y + 1}
            if _, ok := distance[neighbor]; !ok {
                distance[neighbor] = nextDist
                queue = append(queue, neighbor)
            }
        }
        if rooms[current].e {
            neighbor := Coord{current.x + 1, current.y}
            if _, ok := distance[neighbor]; !ok {
                distance[neighbor] = nextDist
                queue = append(queue, neighbor)
            }
        }
        if rooms[current].w {
            neighbor := Coord{current.x - 1, current.y}
            if _, ok := distance[neighbor]; !ok {
                distance[neighbor] = nextDist
                queue = append(queue, neighbor)
            }
        }

        queue = queue[1:]
    }

    maxDist := 0
    countThousand := 0

    for key := range rooms {
        if distance[key] > maxDist {
            maxDist = distance[key]
        }
        if distance[key] >= 1000 {
            countThousand++
        }
    }

    return maxDist, countThousand
}

func main() {
    //fmt.Println(parseRegex("^EE|WW(N|S)$"))
    fmt.Println(longestPathRegex("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"))
    fmt.Println(longestPathRegex("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"))
    fmt.Println(longestPathRegex("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"))


    data, _ := ioutil.ReadFile("input")
    a, b := longestPathRegex(string(data))
    fmt.Println("Part A:",a,"\nPart B:",b)
}

