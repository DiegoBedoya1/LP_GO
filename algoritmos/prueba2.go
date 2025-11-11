package main

import (
	"fmt"
	"strings"
)

func contarVocales(texto string) int {
	vocales := "aeiouáéíóú"
	contador := 0

	for _, r := range strings.ToLower(texto) {
		if strings.ContainsRune(vocales, r) {
			contador++
		}
	}
	return contador
}

func main() {
	fmt.Println(contarVocales("Programación en Go")) 