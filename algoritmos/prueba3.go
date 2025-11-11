package main

import "fmt"

func sumaDigitos(num int) int {
	suma := 0
	for num > 0 {
		suma += num % 10
		num /= 10
	}
	return suma
}

func main() {
	fmt.Println(sumaDigitos(12345))
}