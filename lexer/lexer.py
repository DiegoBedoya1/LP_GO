import ply.lex as lex


# Contribucion: Salvador Muñoz
# Palabras reservadas de Go
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'goto': 'GOTO',
    'switch': 'SWITCH',
    'case': 'CASE',
    'type': 'TYPE',
    'struct': 'STRUCT',
    'interface': 'INTERFACE',
    'func': 'FUNC',
    'return': 'RETURN',
    'var': 'VAR',
    'const': 'CONST',
    'package': 'PACKAGE',
    'import': 'IMPORT'
}


# Contribucion: Salvador Muñoz
# Lista de nombres de tokens
tokens = (
    "INTEGER",
    "FLOAT",
    'PLUS',
    'MINUS',
    'DIVIDE',
    'TIMES',
    'LPAREN',
    'RPAREN',
    "MODULO",
    "VARIABLE",
    "BOOL",
    "MORETHAN",
) + tuple(reserved.values())

# Expresiones regulares para tokens simples
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DIVIDE = r'/'
t_TIMES = r'\*'
t_MODULO = r"%"
t_MORETHAN = r">"

# Contribucion: Salvador Muñoz
# Es importante el orden de las definiciones, el float antes que el entero.
""" Se debe ir de lo especifico a lo general """
def t_FLOAT(t):
    r"\d+\.\d+"
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Booleanos
def t_BOOL(t):
    r'\b(true|false)\b'
    return t

# Contribucion: Salvador Muñoz
# Se recomiendo usar funciones para las variables
def t_VARIABLE(t):
    # Este regex solo valida variables si tienen espacio entre ellas, ejm
    # "1.23abc"
    # "abc" NO es variable porque no tiene espacio entre "1.23" 
    r'\b[a-z][a-zA-Z0-9_]*\b'
    t.type = reserved.get(t.value,"VARIABLE")
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print(f"El componente lexico {t.value[0]} no existe")
    t.lexer.skip(1)

lexer = lex.lex()

data = '''1

1.123
1.123aa
3 + 4 * 10
  + -20 *2 %
variable
Variable break
asd123 
if
trueeee
true
false>>false
import
'''

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
print(f"Numero de lineas {lexer.lineno}")