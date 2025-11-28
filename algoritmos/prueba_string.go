package main

import "fmt"

func main() {

    // STRUCT
    type Persona struct {
        nombre string
        edad   int
    }

    type Animal struct 
    {
        especie string
        edad int


    // IF / ELSE IF / ELSE
    x := 10
    if x > 10 {
        fmt.Println("ok")
    } else if x < 5 {
        fmt.Println("ok")
    } else {
        fmt.Println("ok")
    }

    if x > 10 
        fmt.Println("error")


    // MÉTODO ASOCIADO A STRUCT
    type Persona2 struct {
        nombre string
    }

    func (p Persona2) hablar() {
        fmt.Println("hola")
    }

    func (Persona2) saludar 
    {
        fmt.Println("error")
    }


    // MÉTODOS STRING
    var nombre string = "espol"
    good1 := nombre.lenStr()
    good2 := nombre.toUpper()
    fmt.Println(good1)
    fmt.Println(good2)

    var a int = 10
    var b float64 = 3.2
    var c bool = true

    bad1 := a.lenStr()
    bad2 := b.toUpper()
    bad3 := c.lenStr()
    bad4 := nombre.reverse()


    // NOMBRES RESERVADOS
    var int string = "x"
    var bool int = 10
    float := 3.14
    var STRING int = 5

    var indice int = 20
}
