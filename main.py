import os
import datetime
from lexer import lexer as lx # Importamos lexer

#Contribucion: Salvador Muñoz
def cargar_archivos_go(carpeta):
    """Devuelve una lista con el contenido de todos los archivos .go en la carpeta."""
    archivos = []
    for nombre in os.listdir(carpeta):
        if nombre.endswith(".go"):
            ruta = os.path.join(carpeta, nombre)
            with open(ruta, "r", encoding="utf-8") as f:
                archivos.append((nombre, f.read()))
    return archivos

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    carpeta_algoritmos = os.path.join(base_dir, "algoritmos")
    carpeta_logs = os.path.join(base_dir, "logs")

    # Crear carpeta logs si no existe
    os.makedirs(carpeta_logs, exist_ok=True)

    # Cargar todos los archivos .go
    archivos = cargar_archivos_go(carpeta_algoritmos)
    if not archivos:
        print("No se encontraron archivos .go en la carpeta 'algoritmos'.")
        return

    # Pedir usuario de GitHub
    usuario_git = input("Ingrese su usuario de GitHub: ").strip()
    if not usuario_git:
        print("Usuario inválido.")
        return

    # Generar nombre del archivo de log
    fecha_hora = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_log = f"lexico-{usuario_git}-{fecha_hora}.txt"
    ruta_log = os.path.join(carpeta_logs, nombre_log)

    # Analizar cada archivo y guardar resultados
    with open(ruta_log, "w", encoding="utf-8") as log:
        for nombre_archivo, codigo in archivos:
            log.write(f"=== Archivo: {nombre_archivo} ===\n\n")

            eventos = lx.analizar_codigo(codigo)
            for _, linea in eventos:
                log.write(linea + "\n")

            log.write("\n" + "-" * 50 + "\n\n")



    print(f"Analisis completado. Log guardado en '{nombre_log}'")

if __name__ == "__main__":
    main()
