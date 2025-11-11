import ply.yacc as yacc
from lexer.lexer import tokens


# Contribucion Salvador Muñoz
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
    """expresionBooleana : expresionBooleana operandoBooleando termino
    | bool"""


# contribucion Salvador Muñoz
def p_operandoBooleando(p):
    """operandoBooleando : LOGICAL_AND
    | LOGICAL_OR"""


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

""" while True:
    try:
        s = input("calc > ")
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
 """
