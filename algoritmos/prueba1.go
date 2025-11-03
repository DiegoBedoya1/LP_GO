package main

import "fmt"

func main() {
    var x int = 10
    var y float64 = 20.5
    var flag bool = true

    if x > 5 {
        fmt.Println("x es mayor que 5")
    } else {
        fmt.Println("x es menor o igual que 5")
    }

    for i := 0; i < x; i++ {
        fmt.Println(i)
    }

    result := x + int(y)
    fmt.Println("Resultado:", result)
}
