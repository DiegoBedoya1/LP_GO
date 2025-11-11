import ply.yacc as yacc
from lexer.lexer import tokens
import os, datetime


# contribucion Salvador Muñoz
def p_sentencia(p):
    """sentencia : asignacion
    | asignacion_corta
    | expresion
    | pedirDatos
    | imprimir
    | crearVariable
    | funcion_anonima
    """


# contribucion Salvador Muñoz


def p_lista_sentencias(p):
    """lista_sentencias : sentencia
    | lista_sentencias sentencia"""


# contribucion Salvador Muñoz
def p_asignacionCorta(p):
    """asignacion_corta : IDENTIFIER SHORTASSIGN expresion"""


# contribucion Diego Bedoya
def p_crearVariable(p):
    """crearVariable : VAR IDENTIFIER tipo ASSIGN expresion"""


def p_tipo(p):
    """tipo : int
    | float
    | complex
    | uint
    | bool
    | STRING"""


def p_int(p):
    """int : INT
    | INT8
    | INT16
    | INT32
    | INT64"""


def p_float(p):
    """float : FLOAT32
    | FLOAT64"""


def p_uint(p):
    """uint : UINT
    | UINT8
    | UINT16
    | UINT32
    | UINT64"""


def p_complex(p):
    """complex : COMPLEX64
    | COMPLEX128"""


# Contribucion Salvador Muñoz
# asignacion de tipo ID = 0
def p_asignacion(p):
    """asignacion : IDENTIFIER ASSIGN expresion"""


def p_expresion(p):
    """expresion : expresionMatematica
    | expresionBooleana
    | STRING"""


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
def p_valor(p):
    """ valor: STRING
    | bool
    | numero
    """


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


# contribucion Diego Bedoya
def p_pedirDatos(p):
    """pedirDatos : FMT DOT SCANLN LPAREN AMPERSAND IDENTIFIER RPAREN"""


def p_imprimir(p):
    """imprimir : FMT DOT PRINTLN LPAREN valores RPAREN"""


def p_valores(p):
    """valores : IDENTIFIER
    | IDENTIFIER COMA valores
    |"""  # linea vacia significa que es opcional


#Estructuras de datos
#contribucion Steven Mirabá
#Struct
def p_struct_decl(p):
    '''struct_decl : TYPE IDENTIFIER STRUCT LBRACE struct_fields RBRACE'''

def p_struct_fields(p):
    '''struct_fields : struct_fields struct_field
                     | struct_field'''
    
def p_struct_field(p):
    '''struct_field : IDENTIFIER IDENTIFIER'''

#contribucion Diego Bedoya
#map
def p_map_decl(p):
    '''map_decl : IDENTIFIER SHORTASSIGN MAP LBRACKET IDENTIFIER RBRACKET IDENTIFIER LBRACE lista_pares RBRACE'''

def p_lista_pares(p):
    '''lista_pares : par_map  COMA lista_pares
                   | par_map'''
   

def p_par_map(p):
    '''par_map : STRING COLON expresion'''
    

#Estructuras de control
#contribucion Steven Mirabá
#if / else
def p_if_stmt(p):
    """if_stmt : IF expresionBooleana block else_opt"""
    
def p_elif_chain(p):
    '''elif_chain : elif_chain ELSE IF expresionBooleana block
                  | ELSE IF expresionBooleana block
                  | empty'''

def p_else_opt(p):
    '''else_opt : ELSE block
                | empty'''

#contribucion Diego Bedoya 
#switch
def p_switch_stmt(p):
    '''switch_stmt : SWITCH expresion LBRACE case_clauses default_clause RBRACE'''

def p_case_clauses(p):
    '''case_clauses : case_clause case_clauses
                    | case_clause
                    | empty'''

def p_case_clause(p):
    '''case_clause : CASE expresion COLON sentencia'''

def p_default_clause(p):
    '''default_clause : DEFAULT COLON sentencia
                |empty'''
    

# Tipo de funciones
# contribucion Steven Mirabá
# metodo asociado a struct
def p_func_metodo(p):
    '''func_metodo : FUNC LPAREN IDENTIFIER IDENTIFIER RPAREN IDENTIFIER LPAREN RPAREN LBRACE sentencias RBRACE'''

def p_lista_parametros(p):
    """lista_parametros : parametro COMA lista_parametros  
    | parametro
    | empty"""

# Salvador Muñoz 
def p_funcion_anonima(p):
    """funcion_anonima : FUNC LPAREN arg_funcion RPAREN LBRACE sentencias RBRACE llamadaopcional """

def p_llamada_opcional(p):
    """llamadaopcional : LPAREN argllamadaopcional RPAREN
    | empty"""

def p_argllamadaopcional(p):
    """argllamadaopcional : IDENTIFIER
    | argllamadaopcional COMA IDENTIFIER
    """



def p_arg_funcion(p):
    """arg_funcion : IDENTIFIER tipo
    | arg_funcion COMA IDENTIFIER tipo
    | empty"""


def p_parametro(p):
    '''parametro : IDENTIFIER IDENTIFIER'''

#contribucion Diego Bedoya
#funcion de retorno simple
def p_func_con_retorno(p):
    '''func_con_retorno : FUNC IDENTIFIER LPAREN lista_parametros RPAREN IDENTIFIER LBRACE sentencia RETURN retorno RBRACE'''
def p_retorno(p):
    """ retorno : valor | IDENTIFIER
    """


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

#Struct
def p_struct_decl(p):
    '''struct_decl : TYPE IDENTIFIER STRUCT LBRACE struct_fields RBRACE'''

def p_struct_fields(p):
    '''struct_fields : struct_fields struct_field
                     | struct_field'''
    
def p_struct_field(p):
    '''struct_field : IDENTIFIER IDENTIFIER'''
 """


def p_block(p):
    """block : LBRACE sentencias RBRACE"""


def p_sentencias(p):
    """sentencias : sentencias sentencia
    | sentencia
    | empty"""


def p_empty(p):
    "empty :"


syntax_errors = []


def p_error(p):
    msg = f"Syntax error at token '{p.value}' (type={p.type})"
    syntax_errors.append(msg)


# Build the parser
parser_obj = yacc.yacc()

# while True:
#     try:
#         s = input("calc > ")
#     except EOFError:
#         break
#     if not s:
#         continue
#     result = parser_obj.parse(s)
#     print(result)
