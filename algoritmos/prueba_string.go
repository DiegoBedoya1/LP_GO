package main

import "fmt"

func main() {

    // ------------------------------
    //  CASOS CORRECTOS (STRING)
    // ------------------------------
    var nombre string = "espol"

    // método permitido → length()
    long := nombre.length()

    // método permitido → upper()
    up := nombre.upper()

    fmt.Println(long)
    fmt.Println(up)

    // ------------------------------
    //  CASOS INCORRECTOS
    //  (estos deben generar ERROR SEMÁNTICO)
    // ------------------------------

    var x int = 50
    var y float64 = 3.14
    var flag bool = true

    //int no tiene .length()
    a := x.length()

    //float no tiene .upper()
    b := y.upper()

    //bool no tiene .length()
    c := flag.length()

    //string no tiene .reverse() (método inexistente)
    d := nombre.reverse()
}
