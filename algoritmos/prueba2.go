package main
import "fmt"
type Operacion func(balance int , cantidad int) int 

func main() {
	suma := crearOperacion("sumar")
	resultado := suma(10,5)
	fmt.Println("El resultado de la suma es: ",resultado)
}

func crearOperacion(tipo string)Operacion{
	switch tipo{
	case "sumar":
		return func(num1 int, num2 int) int{
			return num1+num2
		}
	case "restar":
		return func(num1 int, num2 int) int{
			return num1- num2
		}
	default:
		return func(num1 int, num2 int)int{
			return num1*num2
		}
	}
}
