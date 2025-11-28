import sys
import os
from flask import Flask, request, jsonify

# -------------------------------
# 🔥 Añadir ruta real de tu proyecto
# -------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "LP_GO"))
sys.path.append(BASE_DIR)

# -------------------------------
# 🔥 Importar tus analizadores reales
#     (cambia estos imports según tu estructura)
# -------------------------------
from lexer.lexer import tokenize
from parser.parser import parse
from semantic.semantic import semantic_analysis


app = Flask(__name__)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    analysis_type = data.get("type")
    code = data.get("code")

    if analysis_type == "lexical":
        result = tokenize(code)

        # Asegurar JSON serializable
        output = [{"token": t.type, "value": t.value} for t in result]

        return jsonify({"output": output})

    elif analysis_type == "syntactic":
        tree, errors = parse(code)

        output = [
            {"linea": err.line, "columna": err.column, "mensaje": err.msg}
            for err in errors
        ]

        return jsonify({"output": output})

    elif analysis_type == "semantic":
        errors = semantic_analysis(code)

        output = [
            {"linea": err.line, "columna": err.column, "mensaje": err.msg}
            for err in errors
        ]

        return jsonify({"output": output})

    return jsonify({"output": []})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
