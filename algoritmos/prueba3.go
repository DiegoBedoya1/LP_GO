package main
import "fmt"

func main(){
	var nombre string
	fmt.Println("Ingresa tu nombre: ")
	fmt.Scanln(nombre)
	if nombre == "andres"{
		fmt.Println("hola andres")
	}else{
		fmt.Println("no te conozco")
	}
}