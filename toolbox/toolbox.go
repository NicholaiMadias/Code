package main

import (
	"fmt"
	"os"
	"strings"
	"unicode/utf8"
)

// reverseRunes reverses Unicode code points rather than UTF-8 bytes.
func reverseRunes(value string) string {
	runes := []rune(value)
	for left, right := 0, len(runes)-1; left < right; left, right = left+1, right-1 {
		runes[left], runes[right] = runes[right], runes[left]
	}
	return string(runes)
}

func main() {
	text := strings.Join(os.Args[1:], " ")
	if utf8.ValidString(text) && text != "" {
		fmt.Println(reverseRunes(text))
	}
}
