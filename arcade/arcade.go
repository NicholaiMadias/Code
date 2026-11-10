package main

import (
	"fmt"
	"math/rand"
)

func main() {
	first, second := rand.Intn(6)+1, rand.Intn(6)+1
	result := fmt.Sprintf("Rolled %d + %d = %d", first, second, first+second)
	if first == second {
		result += " - Doubles! You win!"
	}
	fmt.Println(result)
}
