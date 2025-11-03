package main
import "fmt"

func main(){
	numeros := 10
	for i := 0; i<numeros; i++{
		if i % 2 == 0{
			fmt.Println("hola mundo")
		}
	}
}
