import ply.yacc as yacc
from lexer.lexer import tokens, find_column
import os, datetime

# Steven Mirabá
tabla_simbolos = {
    "variables": {},
    "tipos": {"str-funciones": ["lenStr", "toUpper", "toLower", "replace", "split"]},
    "constantes": {},
}

errores_semanticos = []

tipos_reservados = {"int", "float", "uint", "complex", "bool", "string"}


def p_program(p):
    """program : program sentencia
    | sentencia
    """


def p_sentencia(p):
    """sentencia : asignacion
    | asignacion_corta
    | expresion
    | pedirDatos
    | imprimir
    | crearVariable
    | funcion_anonima
    | struct_decl
    | map_decl
    | slice_decl_simple
    | slice_decl
    | if_stmt
    | switch_stmt
    | for_stmt
    | func_con_retorno
    | func_metodo
    | interface_decl
    | crearConstante
    | reasignacion_var
    | importar
    | paquete_declaracion
    """
    print("==== Ejecutando regla sentencia: ====")
    imprimirInformacion(p)
    print(tabla_simbolos)
    p[0] = p[1]


# ++++++++++++++++++++
# Interfaces
# ++++++++++++++++++++


def p_interface_decl(p):
    """interface_decl : TYPE IDENTIFIER INTERFACE LBRACE interface_methods RBRACE"""


def p_interface_methods(p):
    """interface_methods : interface_method interface_methods
    | interface_method"""


def p_interface_method(p):
    """interface_method : IDENTIFIER LPAREN RPAREN"""


# ++++++++++++++++++++
# DEF expresion
# ++++++++++++++++++++


def p_expresion(p):
    """expresion : expresionMatematica
    | expresionBooleana
    | STRING"""
    print("==== Ejecutando regla expresion: ====")
    if p.slice[1].type == "STRING":
        print("Expresion de tipo string")
        p[0] = "string"
    else:
        print("Expresion de tipo no string (bool, numero)")
        p[0] = p[1]


# contribucion Salvador Muñoz


# contribucion Salvador Muñoz
# Forma 4: Declaración Corta
# Combina declaración e inferencia de tipo. Solo
# puede usarse dentro de funciones y si la variable es
# nueva.
def p_asignacionCorta(p):
    """asignacion_corta : IDENTIFIER SHORTASSIGN expresion"""
    nombre = p[1]
    tip = p[3]
    # contribucion Steven Mirabá
    # regla semantica variable no puede tomar nombre de tipo reservado
    nombre_lower = nombre.lower()
    if nombre_lower in tipos_reservados:
        print(
            f"Error semántico: no se puede usar '{nombre}' como Identifier o nombre de variable porque coincide con un tipo de variable reservado."
        )
        return
    if tip != None:
        tabla_simbolos["variables"][nombre] = tip


# contribucion Diego Bedoya
# Inicialización Explícita
# var a int = 1
def p_crearVariable(p):
    """crearVariable : VAR IDENTIFIER tipo ASSIGN expresion"""
    print("==== Ejecutando regla crearvariable: ====")
    nombre = p[2]
    tip = p[3]
    exp = p[5]
    print(p[4])
    # contribucion Steven Mirabá
    # regla semantica variable no puede tomar nombre de tipo reservado
    nombre_lower = nombre.lower()
    if nombre_lower in tipos_reservados:
        print(
            f"Error semántico: no se puede usar '{nombre}' como Identifier o nombre de variable porque coincide con un tipo de variable reservado."
        )
        return

    if tip != exp:
        print(
            f"Error semántico: la variable '{nombre}' es de tipo '{tip} pero se le asigna una expresión de tipo '{exp}"
        )

    tabla_simbolos["variables"][nombre] = tip


def p_crearConstante(p):
    """crearConstante : CONST IDENTIFIER ASSIGN expresion"""
    nombre = p[2]
    tip = p[4]
    # contribucion Steven Mirabá
    # regla semantica variable no puede tomar nombre de tipo reservado
    nombre_lower = nombre.lower()
    if nombre_lower in tipos_reservados:
        print(
            f"Error semántico: no se puede usar '{nombre}' como Identifier o nombre de variable porque coincide con un tipo de variable reservado."
        )
        return
    if tip != None:
        tabla_simbolos["constantes"][nombre] = tip


def p_tipo(p):
    """tipo : int
    | float
    | complex
    | uint
    | BOOL
    | STRING"""
    p[0] = p[1]


def p_int(p):
    """int : INT
    | INT8
    | INT16
    | INT32
    | INT64"""
    p[0] = "int"


def p_float(p):
    """float : FLOAT32
    | FLOAT64"""
    p[0] = "float"


def p_uint(p):
    """uint : UINT
    | UINT8
    | UINT16
    | UINT32
    | UINT64"""
    p[0] = "uint"


def p_complex(p):
    """complex : COMPLEX64
    | COMPLEX128"""
    p[0] = "complex"


# Contribucion Salvador Muñoz
# Si el tipo no es compatible con la reasignacion, se mantiene el original
def p_reasignacion(p):
    """reasignacion_var :  IDENTIFIER ASSIGN expresion"""
    #     0                  1          2        3
    print("++++++++++++++  Ejectuando regla semantica reasignacion ++++++++++++++++++")
    id = p[1]
    valor = p[3]
    print(f"Id: {id}, valor: {valor}")

    if id not in tabla_simbolos["variables"]:
        print(f"Variable {id} de tipo {valor} no esta definido")
    else:
        if tabla_simbolos["variables"][id] != valor:
            print(
                f"La variable {id} es de tipo {tabla_simbolos['variables'][id]}, pero se intento asignar {valor}"
            )
            # Si el tipo no es compatible con la reasignacion, se mantiene el original
            p[0] = p[1]
        else:
            p[0] = p[3]


# asignacion de tipo ID ID? = 0
def p_asignacion(p):
    """asignacion : IDENTIFIER IDENTIFIER ASSIGN expresion"""
    print("Ejectuando regla semantica asignacion: ")
    nombre = p[1]
    # correcion Steven Mirabá
    tip = p[2]
    # contribucion Steven Mirabá
    # regla semantica variable no puede tomar nombre de tipo reservado
    nombre_lower = nombre.lower()
    if nombre_lower in tipos_reservados:
        print(
            f"Error semántico: no se puede usar '{nombre}' como Identifier o nombre de variable porque coincide con un tipo de variable reservado."
        )
        return
    print("Nombre de asignacion : ", nombre)
    print("Tipo: ", tip)
    tabla_simbolos["variables"][nombre] = tip
    print(tabla_simbolos)
    if (
        nombre in tabla_simbolos["constantes"]
    ):  # Diego Bedoya: regla para evitar la reasignacion de constantes
        print(f"Error semántico: no se puede reasignar constante '{nombre}'.")
    elif nombre not in tabla_simbolos["variables"]:
        print(f"Error semántico: variable '{nombre}' no definida.")
    elif tip != None:
        tabla_simbolos["variables"][nombre] = tip


def p_expresionMatematica(p):
    """expresionMatematica : termino
    | expresionMatematica operando termino"""
    print(f"Ejecutando expresion matematica:")
    if len(p) == 2:
        print("len(p)==2, ejecucion simple de termino")
        p[0] = p[1]
    else:
        left = p[1]
        right = p[3]

        if left == "string" or right == "string":
            print("Error: no se puede sumar string con número")
        elif left == "float" or right == "float":
            p[0] = "float"
        else:
            p[0] = "int"


def p_termino(p):
    """termino : IDENTIFIER
    | numero
    | LPAREN expresionMatematica RPAREN"""  # para permitir (a + b) * 2
    print("Ejecutando regla termino:")
    imprimirInformacion(p)

    if len(p) == 2 and p[1] == "int":
        print("Instance=int valor: ", p[1])
        p[0] = p[1]

    elif len(p) == 2:
        nombre = p[1]
        if nombre not in tabla_simbolos["variables"]:
            print(f"Error semántico: variable '{nombre}' no definida.")
        else:
            p[0] = tabla_simbolos["variables"][nombre]
    elif len(p) == 4:
        p[0] = p[2]


def imprimirInformacion(p):
    print("=== Valores (p[i]) ===")
    for i in range(len(p)):
        print(f"p[{i}] =", p[i])

    print("\n=== Tokens (p.slice) ===")
    for tok in p.slice:
        print(f"type={tok.type}, value={tok.value}")


def check_conversion_imp(nombre, tipo_destino, tipo_origen):
    """Detecta si se está intentando convertir implicitamente entre tipos de datos distintos"""
    if tipo_destino != tipo_origen:
        print(
            f"Error semántico: conversión implícita no permitida de '{tipo_origen}' a '{tipo_destino}' en '{nombre}'"
        )


def p_operando(p):
    """operando : PLUS
    | MINUS
    | TIMES
    | DIVIDE
    | MODULO"""


def p_numero(p):
    """numero : INTEGER
    | FLOAT"""
    print("Ejecutando regla numero:")
    if isinstance(p[1], int):
        print("Numero p ", p[1], " es entero")
        p[0] = "int"
    else:
        print("Numero p ", p[1], " es float")
        p[0] = "float"


def p_boolean(p):
    """bool_literal : BOOLEAN"""
    p[0] = "bool"


# Valor solo se usa en funciones?
def p_valor(p):
    """valor : STRING
    | BOOLEAN
    | INTEGER
    | FLOAT
    | IDENTIFIER
    """
    print("========== Regla de valor ejectuada: ==========")
    if isinstance(p[1], int):
        p[0] = "int"
    elif isinstance(p[1], float):
        p[0] = "float"
    elif p.slice[1].type == "STRING":
        p[0] = "string"
    elif isinstance(p[1], bool):
        p[0] = "bool"
    else:
        nombre = p[1]
        if nombre not in tabla_simbolos["variables"]:
            print(f"Error semántico: la variable {nombre} no ha sido definida")
        else:
            p[0] = tabla_simbolos["variables"][nombre]


# contribucion Steven Mirabá
# funciones de string
# def p_valor_string_metodos(p):
#     """valorString : IDENTIFIER DOT IDENTIFIER LPAREN RPAREN"""
#     nombre = p[1]
#     metodo = p[3]

#     if nombre not in tabla_simbolos["variables"]:
#         print(f"Error semántico: la variable '{nombre}' no ha sido definida.")
#     elif tabla_simbolos["variables"][nombre] != "string":
#         print(f"Error semántico: la variable '{nombre}' no es de tipo 'string'.")
#     else:
#         if metodo in tabla_simbolos["tipos"]["str-funciones"]:
#             p[0] = "string"
#         else:
#             print(
#                 f'Error semántico: el método "{metodo}" no es válido para variables de tipo "string".'
#             )


# contribucion Salvador Muñoz
def p_expresionBooleana(p):
    """expresionBooleana : expresionMatematica operandoBooleano expresionMatematica
    | expresionBooleana operador_logico expresionBooleana
    | bool_literal"""
    p[0] = "bool"


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


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                       Import                                     #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


def p_import(p):
    """importar : importacion_simple
    | importacion_compuesta"""


def p_importacion_simple(p):
    """importacion_simple : IMPORT STRING"""


def p_importacion_compuesta(p):
    """importacion_compuesta : IMPORT LPAREN strings RPAREN"""


def p_strings(p):
    """strings : STRING
    | strings COMA STRING"""


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                       Package                                     #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def p_paquete_declaracion(p):
    """paquete_declaracion : PACKAGE IDENTIFIER"""


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                       Estrucuturas de datos                                    #
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# contribucion Steven Mirabá
# Struct
def p_struct_decl(p):
    """struct_decl : TYPE IDENTIFIER STRUCT LBRACE struct_fields RBRACE"""
    p[2]


def p_struct_fields(p):
    """struct_fields : struct_fields struct_field
    | struct_field"""


def p_struct_field(p):
    """struct_field : IDENTIFIER IDENTIFIER"""


# contribucion Diego Bedoya
# map
def p_map_decl(p):
    """map_decl : IDENTIFIER SHORTASSIGN MAP LBRACKET IDENTIFIER RBRACKET IDENTIFIER LBRACE lista_pares RBRACE"""


def p_lista_pares(p):
    """lista_pares : par_map  COMA lista_pares
    | par_map"""


def p_par_map(p):
    """par_map : STRING COLON expresion"""


# slice
# salvador Muñoz
# var id []id
def p_slice_decl_simple(p):
    """slice_decl_simple : VAR IDENTIFIER ASSIGN LBRACKET RBRACKET IDENTIFIER"""


# var id = []id{expresion,...}
def p_slice_decl(p):
    """slice_decl : VAR IDENTIFIER ASSIGN LBRACKET RBRACKET IDENTIFIER LBRACE lista_valores RBRACE"""


def p_lista_valores(p):
    """lista_valores : lista_valores COMA expresion
    | expresion"""


# Estructuras de control
# contribucion Steven Mirabá
# if / else
def p_if_stmt(p):
    """if_stmt : IF expresionBooleana block else_opt"""


def p_elif_chain(p):
    """elif_chain : elif_chain ELSE IF expresionBooleana block
    | ELSE IF expresionBooleana block
    | empty"""


def p_else_opt(p):
    """else_opt : ELSE block
    | empty"""


# contribucion Diego Bedoya
# switch
def p_switch_stmt(p):
    """switch_stmt : SWITCH expresion LBRACE case_clauses default_clause RBRACE"""


def p_case_clauses(p):
    """case_clauses : case_clauses case_clause
    | case_clause
    | empty"""


def p_case_clause(p):
    """case_clause : CASE expresion COLON sentencia"""


def p_default_clause(p):
    """default_clause : DEFAULT COLON sentencia
    | empty"""


# For
def p_for_stmt(p):
    """for_stmt : FOR for_header block"""


def p_for_header(p):
    """for_header : asignacion_corta SEMICOLON expresionBooleana SEMICOLON incremento
    | empty"""


def p_incremento(p):
    """incremento : IDENTIFIER INCREMENT
    | IDENTIFIER DECREMENT"""


# Tipo de funciones
# contribucion Steven Mirabá
# metodo asociado a struct
def p_func_metodo(p):
    """func_metodo : FUNC LPAREN IDENTIFIER IDENTIFIER RPAREN IDENTIFIER LPAREN RPAREN LBRACE sentencias RBRACE"""


def p_lista_parametros(p):
    """lista_parametros : parametro COMA lista_parametros
    | parametro
    | empty"""


# Salvador Muñoz
def p_funcion_anonima(p):
    """funcion_anonima : FUNC LPAREN arg_funcion RPAREN LBRACE sentencias RBRACE llamadaopcional"""


def p_llamada_opcional(p):
    """llamadaopcional : LPAREN argllamadaopcional RPAREN
    | empty"""


def p_argllamadaopcional(p):
    """argllamadaopcional : IDENTIFIER
    | argllamadaopcional COMA IDENTIFIER
    """


def p_arg_funcion(p):
    """arg_funcion : IDENTIFIER IDENTIFIER
    | arg_funcion COMA IDENTIFIER IDENTIFIER
    | empty"""


def p_parametro(p):
    """parametro : IDENTIFIER IDENTIFIER"""


# contribucion Diego Bedoya
# funcion de retorno simple
def p_func_con_retorno(p):
    """func_con_retorno : FUNC IDENTIFIER LPAREN lista_parametros RPAREN IDENTIFIER LBRACE sentencia RETURN retorno RBRACE"""


def p_retorno(p):
    """retorno : valor"""


def p_block(p):
    """block : LBRACE sentencias RBRACE"""


def p_sentencias(p):
    """sentencias : sentencias sentencia
    | sentencia
    | empty"""


def p_empty(p):
    "empty :"


syntax_errors = []

data = ""


def p_error(p):
    if p:  # Hay un token problemático
        # Línea del token
        line = p.lineno

        # Columna calculada usando lexpos
        col = find_column(data, p)

        msg = (
            f"Syntax error: token '{p.value}' "
            f"(type={p.type}) en línea {line}, columna {col}"
        )
        syntax_errors.append(msg)
        print(msg)
    else:
        # Error por fin de archivo (EOF)
        msg = "Syntax error at EOF (End of File)"
        syntax_errors.append(msg)
        print(msg)


# Build the parser
parser_obj = yacc.yacc()


def parse(texto):
    global data
    data = texto
    return parser_obj.parse(texto)


while True:
    try:
        s = input("calc > ")
    except EOFError:
        break
    if not s:
        continue
    result = parser_obj.parse(s)
    print(result)
