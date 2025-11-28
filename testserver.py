import requests
import json
import time

# URL de tu endpoint de Flask (asumiendo que corre en localhost:5000)
API_URL = "http://127.0.0.1:5000/api/analyze"

# ----------------------------------------------------------------------
# Código de Prueba
# - Contiene un error léxico (carácter desconocido '$')
# - Contiene un error sintáctico (falta ';' después de 'var')
# - Contiene un error semántico (uso de método no válido en 'int')
# ----------------------------------------------------------------------
CODIGO_DE_PRUEBA = """
var x: int = 10;
var y: string = "hello";
var z: int;
z = 5 + x;
y.uppercase(); // Método válido para string

$ # Carácter léxico inválido

x.toUpperCase(); // Error semántico: toUpperCase no existe en int
var a: int; var b: int // Error sintáctico: Falta ;
"""

def make_analysis_request(analysis_type, code):
    """Envía la solicitud POST a la API de Flask."""
    payload = {
        "type": analysis_type,
        "code": code
    }
    
    print(f"\n--- Probando Análisis: {analysis_type.upper()} ---")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        response.raise_for_status() # Lanza error para códigos 4xx/5xx
        
        # Formatear e imprimir la respuesta
        print(f"Estado HTTP: {response.status_code}")
        
        try:
            data = response.json()
            # Usamos pprint para una salida JSON legible
            print("Respuesta JSON:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Error: La respuesta no es un JSON válido.")
            print(f"Respuesta cruda: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"ERROR al conectar con Flask: {e}")
        print("Asegúrate de que tu aplicación Flask esté corriendo en http://127.0.0.1:5000")

def main():
    print("Iniciando pruebas del Analizador de Lenguaje...")
    time.sleep(1)

    # 1. Prueba de Análisis Léxico
    make_analysis_request("lexical", CODIGO_DE_PRUEBA)

    # 2. Prueba de Análisis Sintáctico (debería encontrar errores)
    make_analysis_request("syntactic", CODIGO_DE_PRUEBA)
    
    # 3. Prueba de Análisis Semántico (debería encontrar errores)
    make_analysis_request("semantic", CODIGO_DE_PRUEBA)
    
    print("\n--- Pruebas Finalizadas ---")

if __name__ == "__main__":
    main()