package main

import (
	"fmt"
	"math"
)

type Figura interface {
	Area() float64
	Descripcion() string
}

type Rectangulo struct {
	Ancho  float64
	Alto   float64
}

func (r Rectangulo) Area() float64 {
	return r.Ancho * r.Alto
}

func (r Rectangulo) Descripcion() string {
	return fmt.Sprintf("Rectángulo de %.2f x %.2f", r.Ancho, r.Alto)
}

type Circulo struct {
	Radio float64
}

func (c Circulo) Area() float64 {
	return math.Pi * c.Radio * c.Radio
}

func (c Circulo) Descripcion() string {
	return fmt.Sprintf("Círculo de radio %.2f", c.Radio)
}


type ListaFiguras []Figura


func agregarFigura(lista *ListaFiguras, f Figura) {
	*lista = append(*lista, f)
}

func mostrarFiguras(lista ListaFiguras) {
	for i, f := range lista {
		fmt.Printf("[%d] %s con área %.2f\n", i, f.Descripcion(), f.Area())
	}
}


func main() {
	var figuras ListaFiguras
	var opcion int
	fmt.Println("Ingresa una opcion: ")
	fmt.Scanln(&opcion)

	switch opcion {
	case 1:
		agregarFigura(&figuras, Rectangulo{Ancho: 5, Alto: 3})
	case 2:
		agregarFigura(&figuras, Circulo{Radio: 4})
	default:
		fmt.Println("Opción inválida")
	}

	agregarFigura(&figuras, Rectangulo{Ancho: 2, Alto: 8})
	agregarFigura(&figuras, Circulo{Radio: 1.5})

	fmt.Println("Figuras registradas:")
	mostrarFiguras(figuras)

	if len(figuras) > 3 {
		fmt.Println("Hay varias figuras en la lista.")
	} else {
		fmt.Println("Pocas figuras registradas.")
	}
}
