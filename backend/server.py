import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# -------------------------------
# 🔥 Añadir ruta real de tu proyecto
# -------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "LP_GO"))
sys.path.append(BASE_DIR)

# -------------------------------
# -------------------------------
from lexer.lexer import analizar_codigo
from yacc.parser import parse, errores_semanticos, syntax_errors 




app = Flask(__name__)
CORS(app)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    analysis_type = data.get("type")
    code = data.get("code")

    if analysis_type == "lexical":
        # analizar_codigo devuelve: (eventos, errores)
        # Ignoramos la primera parte (eventos) usando un guion bajo (_)
        _, lista_errores = analizar_codigo(code)

        # Preparamos la LISTA DE MENSAJES DE ERROR
        # e[2] es el 'mensaje' formateado que preparaste en t_error
        mensajes_error = [e[2] for e in lista_errores]

        # Devolvemos un JSON simple que contiene solo la lista de errores.
        return jsonify({
            "errors": mensajes_error,
            "hay_errores": len(mensajes_error) > 0
        })

    elif analysis_type == "syntactic":
        # 1. Ejecutamos el parser. Esto dispara el análisis, 
        #    llena la lista global 'syntax_errors' y retorna el AST (tree).
        tree = parse(code) 

        # 2. Accedemos a la lista global 'syntax_errors' que fue llenada por 'parse'.
        # Formateamos los errores sintácticos (asumiendo que son objetos Error con atributos)
        syntactic_errors_messages = [err for err in syntax_errors]

        return jsonify({
            "syntactic_errors": syntactic_errors_messages, 
            "count": len(syntactic_errors_messages),
            "type": "syntactic"
        })


    
    elif analysis_type == "semantic":
        # 1. Ejecutamos el parser. Esto es MANDATORIO ya que 'parse'
        #    es la función que dispara el análisis semántico (vía yacc/ply)
        #    y llena la lista global 'errores_semanticos'.
        _ = parse(code)

        # 2. La lista 'errores_semanticos' ya contiene los strings formateados.
        #    La accedemos directamente desde el módulo importado.
        
        return jsonify({
            "semantic_errors": errores_semanticos, # Lista de strings ya formateados
            "count": len(errores_semanticos),
            "type": "semantic"
        }) 

    return jsonify({"error": "Tipo de análisis no soportado"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
