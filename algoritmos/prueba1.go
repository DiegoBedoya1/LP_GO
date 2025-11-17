package main

import "fmt"

func main() {
    var x int = 10
    var y float64 = 20.5
    var flag bool = true
    var b = c
    x = "Error"
    y = 1
    // Test de Comentario no deberia aparecer en logs // Esto deberia segir siendo un comentario
    "String" "String2"

    array [1,2,3,"hola"]

    


    /* Comentario de bloque
    no deberia aparecer en los losgs */
    if x > 5 {
        fmt.Println("x es mayor que 5")
    } else {
        fmt.Println("x es menor o igual que 5")
    }

    for i := 0; i < x; i++ {
        fmt.Println(i)
    }

    func() {
        var msg string = "Hola desde una funcion anonima"
        fmt.Println(msg)
    }()

    result := x + int(y)
    fmt.Println("Resultado:", result)
}
