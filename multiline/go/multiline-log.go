package main

import (
	"fmt"
	"os"
	"time"
)

func main() {
	//var test []string

	//fmt.Printf("the first string is: %s", test[0])

	newLog := `this is the first line
	this is the second line
	this is the third line
	`
	for true {
		fmt.Fprint(os.Stderr, time.Now(), newLog)
		time.Sleep(10 * time.Second)
	}

}
