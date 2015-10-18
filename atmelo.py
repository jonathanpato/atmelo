
# -----------------------------------------------------------------------------
# ATmelo.py 
#
# ATmelo. lexical and syntax analizer for ATmelo language
# Authors. Homero Marin    A00810150
#		   Jonathan Frias  A00810797
# Date. 2015-10-13 18:46 hrs
# -----------------------------------------------------------------------------

fileName = "programa1"

#list of tokens
tokens = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'COLON', 
'COMMA', 'SEMICOLON', 'GT', 'LT', 'LCBRACE', 'RCBRACE', 
	'LPAREN', 'RPAREN', 'ID', 'EnteroDecimal', 
	'EnteroHexadecimal', 'EnteroBinario',
	'ConstanteFlotante', 'ConstanteCadena', 
	'ConstanteCaracter',
	]

reserved = {
	'programa': 'PROGRAMA',
	'funcion' : 'FUNCION',
	'sino' : 'SINO',
	'escribePuerto' : 'ESCRIBEPUERTO', 
	'si' : 'SI',
	'ciclo' : 'CICLO',
	'leePuerto' : 'LEEPUERTO',
	'orbit':'ORBIT',
	'andbit':'ANDBIT',
	'xorbit':'XORBIT',
	'imprimeconsola' : 'IMPRIMECONSOLA',
	'b' : 'B',
	'c' : 'C',
	'd' : 'D',
	'entero' : 'ENTERO',
	'flotante' : 'FLOTANTE',
	'cadena' : 'CADENA',
	'caracter' : 'CARACTER',
	'diferentede' : 'DIFERENTEDE',
	'mayorque' : 'MAYORQUE',
	'menorque' : 'MENORQUE',
	'mayorigualque' : 'MAYORIGUALQUE',
	'menorigualque' : 'MENORIGUALQUE',
	'and' : 'AND',
	'or' : 'OR',
	'not' : 'NOT',
	'regresa' : 'REGRESA',
}

#add reserved words to tokens
tokens += list(reserved.values())
#define regular expressions for tokens
#longest string is checked first
t_LCBRACE = r'{'
t_RCBRACE = r'}'
t_GT = r'>'
t_LT = r'<'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'


#declare regular expressions and actions to tokens, it is checked in the order it is type input

def t_EnteroBinario(t):
	r'[0-1]+B'
	return t

def t_EnteroHexadecimal(t):
	r'[0-9a-fA-F]+H'
	return t

def t_ConstanteFlotante(t):
	r'[0-9]+\.[0-9]+'
	try:
		t.value =float(t.value)
	except:
		print("Invalid float token!")
		t.value = 0.0
	return t

def t_EnteroDecimal(t):
	r'[0-9]+'
	try:
		t.value =int(t.value)
	except:
		print("Invalid int token!")
		t.value = 0.0
	return t

def t_ID(t):
	r'[A-Za-z]+'
	t.type = reserved.get(t.value, 'ID') # validate that the pattern is not a reserved words
	return t

	
def t_ConstanteCadena(t):
	r'\"[^\"]*\"'
	return t
def t_ConstanteCaracter(t):
	r'\'(\\?.)?\''
	return t
	
#ignored characters
t_ignore = " \t\r"

def t_COMMENT(t):
	r'\#.*'
	pass
	#no return value, token discarded

def t_newline(t):
	r'\n+'
	#actualizar lineno manualmente
	t.lexer.lineno += t.value.count("\n")
	#actualizar variable global offset
	global offset
	offset = t.lexer.lexpos
offset = 0 #lexpos until last newline


def t_error(t):
	print("Illegal character %c at lineno: %d column: %d\n" %\
	(t.value[0], t.lineno, t.lexpos - offset))
	t.lexer.skip(1)


#build the lexer
import ply.lex as lex
lexer = lex.lex()

precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE'),
	)

#input program filename from terminal
import sys
lineNumber = 1;
program = "";
#read whole file in a string
with open(fileName) as sourceFile:
	for line in sourceFile:
		program = program + line
		sys.stdout.write(str(lineNumber) + line) #print the source code
		lineNumber = lineNumber + 1
sourceFile.close()
lexer.input(program)

#Tokenize
while True:
	tok = lexer.token()
	if not tok:
		break # no more input
	print(tok)


offset = 0  	  #reiniciar offset
lexer.lineno = 1  #reiniciar lineno 
				  #porque se altero
				  #al momento de
				  #encontrar saltos de linea

#parsing grammar rules
#starting rule: program structure
def p_ESTRUCTURA(p):
	'''ESTRUCTURA : Funciones PROGRAMA ID SEMICOLON Variables_Globales LCBRACE Contenido RCBRACE'''
	p[0] = "Analisis de Sintaxis completado!"
	print(p[0])


def p_Funciones(p):
	'''Funciones : NULL
					| EstructuraFuncion
					| EstructuraFuncion Funciones'''
					
#next grammar rules are components of the program
def p_EstructuraFuncion(p):
	'''EstructuraFuncion : FUNCION ID LPAREN Parametros RPAREN COLON TIPO SEMICOLON LCBRACE Contenido RCBRACE'''

def p_Parametros(p):
	'''Parametros : Para'''

def p_Para(p):
	'''Para : NULL 
			| TIPO ID 
			| TIPO ID COMMA Para'''

def p_Estatuto(p):
	'''Estatuto :  Estatuto_Asignacion
				| Estatuto_Condicion
				| Estatuto_Escritura_de_puerto
				| Estatuto_Ciclo 
				| Estatuto_Lectura_de_puerto
				| Imprimir
				| Declaracion_de_variables
				| LlamadaFuncion
				| regresaDeFuncion'''

def p_regresaDeFuncion(p):
	'''regresaDeFuncion : REGRESA ID SEMICOLON'''

def p_LlamadaFuncion(p):
	'''LlamadaFuncion : ID LPAREN MULTIARG RPAREN SEMICOLON
						| ID LPAREN RPAREN SEMICOLON'''
	
def p_EstatutoAsignacion(p):
	'''Estatuto_Asignacion : ID EQUALS Expresion SEMICOLON
							| ID EQUALS LlamadaFuncion
							| ID EQUALS TIPO LPAREN ARG RPAREN SEMICOLON''' #casting

def p_DeclaracionDeVariables(p):
	'''Declaracion_de_variables : TIPO COLON ID SEMICOLON
									| TIPO COLON ID EQUALS Expresion SEMICOLON'''
	

def p_EstatutoCondicion(p):
	'''Estatuto_Condicion : SI LPAREN Expresion RPAREN LCBRACE Contenido RCBRACE SINO LCBRACE Contenido RCBRACE'''
							
def p_EstatutoImprimirconsola(p):
	'''Imprimir : IMPRIMECONSOLA MULTIARG SEMICOLON'''
	
def p_MULTIARG(p):
	'''MULTIARG : ARG COMMA MULTIARG
				| ARG'''
				
def p_ARG(p):
	'''ARG : ID
			| CTE'''
			
def p_EstatutoEscrituraDePuerto(p):
	'''Estatuto_Escritura_de_puerto : ESCRIBEPUERTO PUERTO ID SEMICOLON'''

def p_EstatutoLecturaDePuerto(p):
	'''Estatuto_Lectura_de_puerto : ID EQUALS LEEPUERTO PUERTO SEMICOLON'''
	
def p_PUERTO(p):
	'''PUERTO : B 
				| C
				| D'''
	
def p_EstatutoCiclo(p):
	'''Estatuto_Ciclo : CICLO LPAREN Expresion RPAREN LCBRACE Contenido RCBRACE'''
	
def p_Expresion(p):
	'''Expresion : EX'''

def p_EX(p):
	'''EX : Exp Compara Exp
			| NOT Exp Compara Exp
			| Exp'''
	
def p_Compara(p):
	'''Compara : 	  GT
					| LT
					| DIFERENTEDE
					| MAYORQUE
					| MENORQUE
					| MAYORIGUALQUE
					| MENORIGUALQUE
					| AND
					| OR'''

def p_Exp(p):
	'''Exp : Exp PLUS Termino
			| Exp MINUS Termino
			| Exp ORBIT Termino
			| Exp XORBIT Termino
			| Exp ANDBIT Termino
			| Termino'''

def p_Termino(p):
	'''Termino : Termino TIMES Factor
			| Termino DIVIDE Factor
			| Termino AND Factor
			| Factor'''

def p_Factor(p):
	'''Factor : LPAREN Expresion RPAREN
			| CTE
			| ID'''
			
def p_CTE(p):
	'''CTE : Entero
				| ConstanteFlotante
				| ConstanteCadena
				| ConstanteCaracter'''

def p_Entero(p):
	'''Entero : EnteroDecimal
				| EnteroHexadecimal
				| EnteroBinario'''




def p_NULL(p):
	'''NULL : '''

def p_Contenido(p):
	'''Contenido : Estatuto Contenido
					| NULL'''
def p_Variables_Globales(p):
	'''Variables_Globales : R'''
	
def p_R(p):
	'''R : TIPO COLON ID SEMICOLON R
		    | TIPO COLON ID EQUALS Expresion SEMICOLON R
			| NULL'''
			
			


def p_TIPO(p):
	'''TIPO : ENTERO
			| FLOTANTE
			| CADENA
			| CARACTER'''


			


###########################

def p_error(p):
	print("Syntax error at '%s' lineno: '%d' column: '%d'" %\
	(p.value, p.lineno, p.lexpos - offset))

#Build the parser
import ply.yacc as yacc
parser = yacc.yacc()
#parse
parser.parse(program)


offset = 0  	  #reiniciar offset
parser.lineno = 1  #reiniciar lineno 
				  #porque se altero
				  #al momento de
				  #encontrar saltos de linea
