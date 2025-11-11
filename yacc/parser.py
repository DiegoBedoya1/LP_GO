import ply.yacc as yacc
from lexer.lexer import tokens


# contribucion Salvador Muñoz
def p_sentencia(p):
    """sentencia : asignacion
    | asignacion_corta
    | expresion"""


# contribucion Salvador Muñoz
def p_asignacionCorta(p):
    """asignacion_corta : IDENTIFIER SHORTASSIGN expresion"""

#contribucion Diego Bedoya
def p_crearVariable(p):
    '''crearVariable : VAR IDENTIFIER tipo ASSIGN expresion
    '''
def p_tipo(p):
    '''tipo: 
    '''


# Contribucion Salvador Muñoz
# asignacion de tipo ID = 0
def p_asignacion(p):
    """asignacion : IDENTIFIER ASSIGN expresion"""


def p_expresion(p):
    """expresion : expresionMatematica
    | expresionBooleana
    | STRING
    """


def p_expresionMatematica(p):
    """expresionMatematica : termino
    | expresionMatematica operando termino"""


def p_termino(p):
    """termino : IDENTIFIER
    | numero
    | LPAREN expresionMatematica RPAREN"""  # para permitir (a + b) * 2


def p_operando(p):
    """operando : PLUS
    | MINUS
    | TIMES
    | DIVIDE
    | MODULO"""


def p_numero(p):
    """numero : INTEGER
    | FLOAT"""


def p_boolean(p):
    """bool : TRUE
    | FALSE"""


# contribucion Salvador Muñoz
def p_expresionBooleana(p):
    """expresionBooleana : expresionMatematica operandoBooleano expresionMatematica
    | expresionBooleana operador_logico expresionBooleana
    | bool"""


# contribucion Salvador Muñoz
def p_operandoBooleano(p):
    """operandoBooleano : EQUALS
    | NOT_EQUALS
    | MORE_EQUAL
    | LESS_EQUAL
    | MORETHAN
    | LESSTHAN"""


def p_operador_logico(p):
    """operador_logico : LOGICAL_AND
    | LOGICAL_OR"""

#contribucion Diego Bedoya
def p_pedirDatos(p):
    ''' pedirDatos : 'fmt' DOT 'Scanln' LPAREN AMPERSAND IDENTIFIER RPAREN
    '''
def p_imprimir(p):
    '''imprimir : 'fmt' DOT 'Println' LPAREN IDENTIFIER RPAREN
    '''

""" def p_expression_plus(p):
    "expression : expression PLUS term"
    p[0] = p[1] + p[3]


def p_expression_minus(p):
    "expression : expression MINUS term"
    p[0] = p[1] - p[3]


def p_expression_term(p):
    "expression : term"
    p[0] = p[1]


def p_term_times(p):
    "term : term TIMES factor"
    p[0] = p[1] * p[3]


def p_term_div(p):
    "term : term DIVIDE factor"
    p[0] = p[1] / p[3]


def p_term_factor(p):
    "term : factor"
    p[0] = p[1]


def p_factor_num(p):
    "factor : NUMBER"
    p[0] = p[1]


def p_factor_expr(p):
    "factor : LPAREN expression RPAREN"
    p[0] = p[2]
 """


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser_obj = yacc.yacc()

while True:
    try:
        s = input("calc > ")
    except EOFError:
        break
    if not s:
        continue
    result = parser_obj.parse(s)
    print(result)
