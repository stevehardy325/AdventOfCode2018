package main

import "fmt"
import "time"
import "strconv"

//input is 846601 for both parts

func newRecipes(firstElfVal int, secondElfVal int) []int {
	//calculate the list of 1 or 2 new recipes based on the current ones
	basis := firstElfVal + secondElfVal
	if basis < 10 {
		return []int{basis % 10}
	} else {
		return []int{basis / 10, basis % 10}
	}
}

func newPos(elfPos int, recipes []int) int {
	//return the elf pointer for the next round based on the last position
	newElfPos := (elfPos + recipes[elfPos] + 1) % len(recipes)
	return newElfPos
}

func recipesA(lastNum int) []int {
	//part A, what are the next 10 recipes after lastNum ?

	//start data
	elf1 := 0
	elf2 := 1
	recipes := []int{3, 7}
	newRecipeList := []int{}

	//run for ten past the 'last number'
	for len(recipes) < (lastNum + 10) {

		newRecipeList = newRecipes(recipes[elf1], recipes[elf2])

		for i := 0; i < len(newRecipeList); i = i + 1 {
			recipes = append(recipes, newRecipeList[i])
		}

		elf1 = newPos(elf1, recipes)
		elf2 = newPos(elf2, recipes)

	}

	return recipes[lastNum : lastNum+10]
}

func compareLists(list1 []int, list2 []int) bool {
	//return true if the lists contain the same ints, else false
	same := true

	for i := 0; i < len(list1); i++ {
		if list1[i] != list2[i] {
			same = false
			break
		}
	}

	return same
}

func recipesB(lastNumString string) int {
	//Part B, how long will we need to keep making recipes until the integer sequence shows up?
	//returns the number of recipes prior to the first appearce of that sequence

	//start data
	elf1 := 0
	elf2 := 1
	recipes := []int{3, 7}

	//turn the input number into a comparable slice
	comparisonList := []int{}
	for i := 0; i < len(lastNumString); i++ {
		num, err := strconv.ParseInt(lastNumString[i:i+1], 0, 16)
		if err != nil {
			fmt.Println(err)
		}
		comparisonList = append(comparisonList, int(num))
	}

	newRecipeList := []int{}
	prev := 0
	for true {
		//add new recipes
		newRecipeList = newRecipes(recipes[elf1], recipes[elf2])
		for i := 0; i < len(newRecipeList); i = i + 1 {
			recipes = append(recipes, newRecipeList[i])
		}
		elf1 = newPos(elf1, recipes)
		elf2 = newPos(elf2, recipes)

		//only check after the recipes list is long enough
		if len(recipes) >= len(comparisonList) {

			//see if the end of the list matches
			testSlice := recipes[len(recipes)-len(comparisonList):]
			if compareLists(testSlice, comparisonList) { //stop iterating if we found it
				prev = len(recipes) - len(comparisonList)
				break
			}
			//if we added two this time, we need to check from the second-to-last position also
			if len(newRecipeList) > 1 && len(recipes) > len(comparisonList) {
				testSlice := recipes[len(recipes)-len(comparisonList)-1 : len(recipes)-1]
				if compareLists(testSlice, comparisonList) {
					prev = len(recipes) - len(comparisonList) - 1
					break
				}
			}

		}
	}
	return prev
}

func main() {
	start := time.Now()

	fmt.Println("Part A:")
	fmt.Println(recipesA(846601))

	end := time.Now()
	fmt.Println("Runtime: ", end.Sub(start))

	start = time.Now()

	fmt.Println("Part B:")
	fmt.Println(recipesB("846601"))

	end = time.Now()
	fmt.Println("Runtime: ", end.Sub(start))
}
