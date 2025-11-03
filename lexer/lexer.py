import ply.lex as lex


# Contribucion: Salvador Muñoz
# Palabras reservadas de Go
#Contribucion: Diego bedoya, más palabras reservadas
reserved = {
    "if": "IF",
    "else": "ELSE",
    "for": "FOR",
    "break": "BREAK",
    "continue": "CONTINUE",
    "goto": "GOTO",
    "switch": "SWITCH",
    "case": "CASE",
    "type": "TYPE",
    "struct": "STRUCT",
    "interface": "INTERFACE",
    "func": "FUNC",
    "return": "RETURN",
    "var": "VAR",
    "const": "CONST",
    "package": "PACKAGE",
    "import": "IMPORT",
    "iota": "IOTA",
    "make": "MAKE",
    "int": "INT",
    "default": "DEFAULT",

}


# Contribucion: Salvador Muñoz
# Lista de nombres de tokens
tokens = (
    "INTEGER",
    "FLOAT",
    "PLUS",
    "MINUS",
    "DIVIDE",
    "TIMES",
    "LPAREN",
    "RPAREN",
    "LBRACE",       #Contribucion Diego Bedoya, más tokens
    "RBRACE",
    "ASSIGN",
    "LESSTHAN",
    "SHORTASSIGN",
    "COLON",
    "SEMICOLON",
    "DOT",
    "MODULO",
    "IDENTIFIER",  # Palabra generica, funciones o variables
    "BOOL",
    "MORETHAN",
    "STRING",  # Contribucion: Salvador Muñoz
) + tuple(reserved.values())

# Expresiones regulares para tokens simples
t_PLUS = r"\+"
t_MINUS = r"-"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_DIVIDE = r"/"
t_TIMES = r"\*"
t_MODULO = r"%"
t_MORETHAN = r">"
t_LBRACE = r"\{"   #contribucion: Diego Bedoya, definicion de tokens
t_RBRACE = r"\}"
t_ASSIGN = r"="
t_SHORTASSIGN = r":="
t_LESSTHAN = r"<"
t_COLON = r":"
t_SEMICOLON = r";"
t_DOT = r"\."




""" Se debe ir de lo especifico a lo general """


# Contribucion: Salvador Muñoz
def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    return t


# Contribucion: Salvador Muñoz
# Es importante el orden de las definiciones, el float antes que el entero.
def t_FLOAT(t):
    r"\d+\.\d+"
    return t


def t_INTEGER(t):
    r"\d+"
    t.value = int(t.value)
    return t


# Booleanos
def t_BOOL(t):
    r"\b(true|false)\b"
    return t


# Contribucion: Salvador Muñoz
# Se recomiendo usar funciones para las identificadores
def t_IDENTIFIER(t):
    # Este regex solo valida identificadores si tienen espacio entre ellas, ejm
    # "1.23abc"
    # "abc" NO es identificador porque no tiene espacio entre "1.23"
    r"\b[a-zA-Z][a-zA-Z0-9_]*\b"
    t.type = reserved.get(t.value, "IDENTIFIER")
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


t_ignore = " \t"

# Contribucion: Salvador Muñoz (error guardados en logs)
errores = []


def t_error(t):
    # Guardamos el error pero también devolvemos información estructurada
    errores.append(
        (t.lexer.lineno, f"Error léxico: carácter no reconocido '{t.value[0]}'")
    )
    t.lexer.skip(1)


lexer = lex.lex()


# Contribucion: Salvador Muñoz
# Variable global para almacenar la ruta del log actual
log_actual = None


# Contribucion: Salvador Muñoz
def analizar_codigo(codigo):
    """Devuelve una lista de eventos léxicos (tokens y errores) en orden real."""
    lexer = lex.lex()
    lexer.input(codigo)
    eventos = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        # Guardar el token con su posición (para orden correcto)
        eventos.append((tok.lineno, str(tok)))

    # Agregar errores también con sus líneas
    for linea, err in errores:
        eventos.append((linea, err))

    # Ordenar tokens + errores según su línea de aparición
    eventos.sort(key=lambda e: e[0])
    return eventos


# data = '''1

# 1.123
# 1.123aa
# 3 + 4 * 10
#   + -20 *2 %
# variable
# Variable break
# asd123
# if
# trueeee
# true
# false>>false
# import
# '''

# lexer.input(data)

# while True:
#     tok = lexer.token()
#     if not tok:
#         break      # No more input
#     print(tok)
# print(f"Numero de lineas {lexer.lineno}")
