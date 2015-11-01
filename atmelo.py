
# -----------------------------------------------------------------------------
# ATmelo.py 
#
# ATmelo. lexical and syntax analizer for ATmelo language
# with semantic actions
# Authors. Homero Marin    A00810150
#		   Jonathan Frias  A00810797
# Date. 2015-10-13 18:46 hrs
# -----------------------------------------------------------------------------

#################
#definiciones
###########
##codigos de operacion
# ORBIT = 1
# XORBIT = 2
# ANDBIT = 3
# MULT = 4
# DIV = 5
# SUM = 6
# SUB = 7
# GT = 8
# LT = 9
# DIFERENTEDE = 10
# MAYORIGUALQUE = 11
# MENORIGUALQUE = 12
# ESCRIBEPUERTO = 13
# LEEPUERTO = 14
# IMPRIMECONSOLA = 15
# REGRESA = 16
# GOTO = 17
# GOTOF = 18
# GOTOT = 19

###########################################
#global variables
fileName = "programa1"
globalVars = {}
funcName = ""
localVars = {}
cuadruplos = []

##global Counts 0
##local Counts 1
##temp Counts 2
##cte Counts 3
## 0 - entero  1 - flotante
## 2 - cadena  3 - caracter
## 4 - byte
counts = [[0, 0, 0, 0, 0], #global Counts
		[0, 0, 0, 0, 0], #local Counts
		[0, 0, 0, 0, 0], #temp Counts
		[0, 0, 0, 0, 0]] #cte Counts

##############
#Constants
#############
GLOBALBEGIN = 1000
LOCALBEGIN = 20000
TEMPBEGIN = 40000
CTEBEGIN = 100000

MAXGLOBALS = 3800
MAXLOCALS = 4000
MAXTEMPS = 4000
MAXCTES = 4000

GLOBALSCOPE = 0
LOCALSCOPE = 1
TEMPSCOPE = 2
CTESCOPE = 3

INTPOS = 0
FLOATPOS = 1
STRPOS = 2
CHPOS = 3
BYTEPOS = 4

###############
#utilities
################################################
#utility imports
import sys
from cuboSemantico import cubo
#utility functions

##this function returns the operation code

def opCode(operation):
	opcode = 0
	if operation == "orbit":
		opcode = 1
	elif operation == "xorbit":
		opcode = 2
	elif operation == "andbit":
		opcode = 3
	elif operation == "*":
		opcode = 4
	elif operation == "/":
		opcode = 5
	elif operation == "+":
		opcode = 6
	elif operation == "-":
		opcode = 7
	elif operation == ">":
		opcode = 8
	elif operation == "<":
		opcode = 9
	elif operation == "diferentede":
		opcode = 10
	elif operation == "mayorigualque":
		opcode = 11
	elif operation == "menorigualque":
		opcode = 12
	elif operation == "escribepuerto":
		opcode = 13
	elif operation == "leepuerto":
		opcode = 14
	elif operation == "imprimeconsola":
		opcode = 15
	elif operation == "regresa":
		opcode = 16
	elif operation == "goto":
		opcode = 17
	elif operation == "gotof":
		opcode = 18
	elif operation == "gotot":
		opcode = 19

	return opcode
##this function returns the vars virtual Address
def virtAddr(varID):
	addr = 0
	if not IDexist(varID, localVars):
		if IDexist(varID, globalVars):
			addr = globalVars[varID][1]
	else:
		addr = localVars[varID][1]
	return addr

###this function adds a row to the variable table
def addVar(var, varList):
	varProperties = [var[1], var[2]]
	varList[var[0]] = varProperties

#this function validates if a variable is already declared
#if yes, it ends the program and returns an error message
#if no, it adds the variable to the variables table
def varDeclSemValid(varID, varType, varDir, varList):
	global funcName
	var = [varID, varType, varDir]
	funcName = 'factorial'
	if IDexist(varID, varList):
		sys.exit("Error!, var " + varID + ": " + varType + " already declared")
	else:
		addVar(var, varList)

##this function returns true if a var Exist in the given variable table, false otherwise
def IDexist(ID, varList):
	return ID in varList.keys()
##this function returns the memDir that the new variable would take
##it returns 0 if datatype segment is full
def dataTypeDist(datatype, scope):
	begin = 0
	maxLimit = 0
	scopepos = 0
	typepos = 0
	memDir = 0
	if scope == "GLOBAL":
		begin = GLOBALBEGIN
		maxLimit = MAXGLOBALS
		scopepos = GLOBALSCOPE
	elif scope == "LOCAL":
		begin = LOCALBEGIN
		maxLimit = MAXLOCALS
		scopepos = LOCALSCOPE
	elif scope == "TEMP":
		begin = TEMPBEGIN
		maxLimit = MAXTEMPS
		scopepos = TEMPSCOPE
	elif scope == "CTE":
		begin = CTEBEGIN
		maxLimit = MAXCTES
		scopepos = CTESCOPE

	if datatype == "entero": 
		typepos = INTPOS
	elif datatype == "flotante":
		typepos = FLOATPOS
	elif datatype == "cadena":
		typepos = STRPOS
	elif datatype == "caracter":
		typepos = CHPOS
	elif datatype == "byte":
		typepos = BYTEPOS

	count = Counts[scopepos][typepos]
	typeSectionSize = maxLimit
	if count < maxLimit:
		memDir = begin + typepos*typeSectionSize + count
	return memDir
##################################################
#utility classes
###################################################
class Cuadruplo:
	def __init__(self, operacion, operando1, operando2, resultado):
		self.operacion = operacion
		self.operando1 = operando1
		self.operando2 = operando2
		selft.resultado = resultado

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

###################################################

#list of tokens
tokens = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'COLON', 
'COMMA', 'SEMICOLON', 'GT', 'LT', 'LCBRACE', 'RCBRACE', 
	'LPAREN', 'RPAREN', 'ID', 'EnteroDecimal', 
	'EnteroHexadecimal', 'EnteroBinario',
	'ConstanteFlotante', 'ConstanteCadena', 
	'ConstanteCaracter', 'ConstanteByte',
	]

reserved = {
	'programa': 'PROGRAMA',
	'funcion' : 'FUNCION',
	'sino' : 'SINO',
	'escribepuerto' : 'ESCRIBEPUERTO', 
	'si' : 'SI',
	'ciclo' : 'CICLO',
	'leepuerto' : 'LEEPUERTO',
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
	'byte' : 'BYTE',
	'diferentede' : 'DIFERENTEDE',
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

def t_Byte(t):
	r'[0-1]{8}B'
	return t

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
	'''Estructura : Funciones PROGRAMA ID seenIDprograma SEMICOLON Variables_Globales LCBRACE Declaracion_de_variables Contenido RCBRACE programExit'''
	p[0] = "Analisis de Sintaxis completado!"
	print(p[0])

def p_seenIDprograma(p):
	'''seenIDprograma : '''
	global localVars
	global funcName
	funcName = p[-1]
	localVars = {}

def p_programExit(p):
	'''programExit : '''
	global funcName
	global globalVars
	global localVars
	del localVars
	del globalVars
	del funcName

def p_Funciones(p):
	'''Funciones : NULL
					| EstructuraFuncion Funciones'''
					
#next grammar rules are components of the program
def p_EstructuraFuncion(p):
	'''EstructuraFuncion : FUNCION ID seenIDfunc LPAREN Parametros \
	RPAREN COLON TIPO SEMICOLON LCBRACE Declaracion_de_variables \
	Contenido REGRESA Expresion SEMICOLON RCBRACE funcExit'''

def p_seenIDfunc(p):
	'''seenIDfunc : '''
	global localVars
	global funcName
	funcName = p[-1]
	localVars = {}

def p_funcExit(p):
	'''funcExit : '''
	global funcName
	global localVars
	del localVars
	funcName = ""

def p_Parametros(p):
	'''Parametros : Para
				| NULL'''

def p_Para(p):
	'''Para : TIPO ID seenIDparam
			| TIPO ID seenIDparam COMMA Para'''

def p_seenIDparam(p):
	'''seenIDparam : '''
	# global localVars
	# varDeclSemValid(p[-1], p[-2], localVars)

def p_Estatuto(p):
	'''Estatuto :  Estatuto_Asignacion
				| Estatuto_Condicion
				| Estatuto_Escritura_de_puerto
				| Estatuto_Lectura_de_puerto
				| Estatuto_Ciclo 
				| Imprimir
				| LlamadaFuncion'''


def p_LlamadaFuncion(p):
	'''LlamadaFuncion : ID LPAREN MULTIARG RPAREN SEMICOLON
						| ID LPAREN RPAREN SEMICOLON'''
	
def p_EstatutoAsignacion(p):
	'''Estatuto_Asignacion : ID EQUALS AssignOption'''
	# if not IDexist(p[1], localVars):
	# 	if not IDexist(p[1], globalVars):
	# 		sys.exit("var " + p[1] + " does not exist. Aborting..")
	# typeMismatch = False
	# if not (IDexist(p[1], localVars)):
	# 	if(globalVars[p[1][0]] != p[3]):
	# 		typeMismatch = True
	# 	elif(localVars[p[1]][0]] != p[3]):
	# 			typeMismatch = True
				
	# if typeMismatch:
	# 	sys.exit("Error!, type mismatch..")

def p_AssignOption(p):
	'''AssignOption : Expresion SEMICOLON
					| TIPO LPAREN Expresion RPAREN SEMICOLON''' #casting
	# typeMismatch = False
	# if len(p) == 3:
	# 	if (p[1] == 'x'):
	# 		typeMismatch = True
	# 	p[0] = p[1]
	# if typeMismatch:
	# 	sys.exit("Error!, type mismatch..")

def p_DeclaracionDeVariables(p):
	'''Declaracion_de_variables : TIPO COLON ID seenIDdeclVar SEMICOLON
									| TIPO COLON ID seenIDdeclVar EQUALS Expresion SEMICOLON
									| NULL'''
	# typeMismatch = False
	# if len(p) == 8:
	# 	if (p[6] == 'x'):
	# 		typeMismatch = True
	# 	elif not (IDexist(p[3], localVars):
	# 		if(globalVars[p[3]][0] != p[6]):
	# 			typeMismatch = True
	# 	elif(localVars[p[3]][0] != p[6]):
	# 			typeMismatch = True
	# if typeMismatch:
	# 	sys.exit("Error!, type mismatch..")

def p_seenIDdeclVar(p):
	'''seenIDdeclVar : '''

	# global localVars
	# global Counts
	# typepos = 0
	# datatype = p[-3]
	# ID = p[-1]
	# if datatype == "entero": 
	# 	typepos = INTPOS
	# elif datatype == "flotante":
	# 	typepos = FLOATPOS
	# elif datatype == "cadena":
	# 	typepos = STRPOS
	# elif datatype == "caracter":
	# 	typepos = CHPOS
	# elif datatype == "byte":
	# 	typepos = BYTEPOS

	# counts = Counts[LOCALSCOPE][typepos]
	# if counts < MAXLOCALS:
	# 	varDeclSemValid(ID, datatype, dataTypeDist(datatype, "LOCAL"), localVars)
	# 	counts = counts + 1
	# 	Counts[LOCALSCOPE][typepos] = counts
	# else:
	# 	sys.exit("Error, demasiadas variables globales!")

def p_EstatutoCondicion(p):
	'''Estatuto_Condicion : SI LPAREN Expresion RPAREN \
	LCBRACE Contenido RCBRACE OptionalElse'''

def p_OptionalElse(p):
	'''OptionalElse : SINO LCBRACE Contenido RCBRACE
					| NULL'''
							
def p_EstatutoImprimirconsola(p):
	'''Imprimir : IMPRIMECONSOLA MULTIARG SEMICOLON'''
	
def p_MULTIARG(p):
	'''MULTIARG : Expresion COMMA MULTIARG
				| Expresion'''
				
			
def p_EstatutoEscrituraDePuerto(p):
	'''Estatuto_Escritura_de_puerto : ESCRIBEPUERTO PUERTO argPuerto SEMICOLON'''
	
	
def p_ArgPuerto(p):
	'''argPuerto : ID
				| ConstanteByte'''
	p[0] = p[1]
def p_EstatutoLecturaDePuerto(p):
	'''Estatuto_Lectura_de_puerto : LEEPUERTO PUERTO ID SEMICOLON'''
	
def p_PUERTO(p):
	'''PUERTO : B 
				| C
				| D'''
	
def p_EstatutoCiclo(p):
	'''Estatuto_Ciclo : CICLO LPAREN Expresion RPAREN \
	LCBRACE Contenido RCBRACE'''
	
def p_Expresion(p):
	'''Expresion : superExp
				| NOT superExp'''
	p[0] = p[1]

def p_superExp(p):
	'''superExp : EX logica EX
				| EX'''
	# global cuadruplos
	# if len(p) == 4:
	# 	p[0] = cubo(p[1], p[3], p[2])
	# 	cuadruplo = Cuadruplo(opCode(p[2]), virtAddr(p[1]), virtAddr(p[3]))
	# else:
	# 	p[0] = p[1]

def p_logica(p):
	'''logica : AND
			| OR'''

def p_EX(p):
	'''EX : Exp Compara Exp
			| Exp'''
	# global cuadruplos
	# if len(p) == 4:
	# 	p[0] = cubo(p[1], p[3], p[2])
	# 	cuadruplo = Cuadruplo(opCode(p[2]), virtAddr(p[1]), virAddr(p[3]))
	# else:
	# 	p[0] = p[1]
	
def p_Compara(p):
	'''Compara : 	  GT
					| LT
					| DIFERENTEDE
					| MAYORIGUALQUE
					| MENORIGUALQUE'''
	p[0] = p[1]


def p_bitOp(p):
	'''bitOp : bitOp ORBIT Factor
			| bitOp XORBIT Factor
			| bitOp ANDBIT Factor
			| Factor'''
	# global cuadruplos
	# if len(p) == 4:
	# 	cuadruplo = Cuadruplo(opCode(p[2]), virtAddr(p[1]), virtAddr(p[3]))
	# 	cuadruplos.append(cuadruplo)
	# else:
	# 	p[0] = p[1]

def p_Exp(p):
	'''Exp : Exp PLUS Termino
			| Exp MINUS Termino
			| Termino'''
	# if len(p) == 4:
	# 	p[0] = cubo(p[1], p[3], p[2])
	# else:
	# 	p[0] = p[1]

def p_Termino(p):
	'''Termino : Termino TIMES bitOp
			| Termino DIVIDE bitOp
			| bitOp'''
	# if len(p) == 4:
	# 	p[0] = cubo(p[1], p[3], p[2])
	# else:
	# 	p[0] = p[1]

def p_Factor(p):
	'''Factor : LPAREN MULTIARG RPAREN
			| ID LPAREN MULTIARG RPAREN
			| CTE
			| IDoperand'''
	# if len(p) == 4:
	# 	p[0] = p[2]
	# else:
	# 	p[0] = p[1]

def p_IDoperand(p):
	'''IDoperand : ID'''
	# if not IDexist(p[1], localVars):
	# 	if not IDexist(p[1], globalVars):
	# 		sys.exit("Error!, trying to operate with " + p[1] + " but it does note exist..")
	# 	else:
	# 		p[0] = globalVars[p[1]][0]
	# else:
	# 	p[0] = localVars[p[1]][0]

def p_CTE(p):
	'''CTE : Entero
				| CteFlotante
				| CteCadena
				| CteCaracter
				| CteByte'''
	p[0] = p[1]

def p_CteByte(p):
	'''CteByte : ConstanteByte'''
	

def p_CteCaracter(p):
	'''CteCaracter : ConstanteCaracter'''
	p[0] = 'char'

def p_CteCadena(p):
	'''CteCadena : ConstanteCadena'''
	p[0] = 'string'

def p_CteFlotante(p):
	'''CteFlotante : ConstanteFlotante'''
	p[0] = 'float'

def p_Entero(p):
	'''Entero : EnteroDecimal
				| EnteroHexadecimal
				| EnteroBinario'''
	p[0] = 'int'



def p_NULL(p):
	'''NULL : '''

def p_Contenido(p):
	'''Contenido : Estatuto Contenido
					| NULL'''

def p_Variables_Globales(p):
	'''Variables_Globales : R'''
	
def p_R(p):
	'''R : TIPO COLON ID seenIDglobVar globDeclOption SEMICOLON R
			| NULL'''

def p_globDeclOption(p):
	'''globDeclOption : NULL 
		| Expresion'''

			
def p_seenIDglobVar(p):
	'''seenIDglobVar : '''
	# global globalVars
	# global Counts
	# typepos = 0
	# datatype = p[-3]
	# ID = p[-1]
	# if datatype == "entero": 
	# 	typepos = INTPOS
	# elif datatype == "flotante":
	# 	typepos = FLOATPOS
	# elif datatype == "cadena":
	# 	typepos = STRPOS
	# elif datatype == "caracter":
	# 	typepos = CHPOS
	# elif datatype == "byte":
	# 	typepos = BYTEPOS

	# counts = Counts[GLOBALSCOPE][typepos]
	# if counts < MAXGLOBALS:
	# 	varDeclSemValid(ID, datatype, dataTypeDist(datatype, "GLOBAL"), globalVars)
	# 	counts = counts + 1
	# 	Counts[GLOBALSCOPE][typepos] = counts
	# else:
	# 	sys.exit("Error, demasiadas variables globales!")

def p_TIPO(p):
	'''TIPO : ENTERO
			| FLOTANTE
			| CADENA
			| CARACTER
			| BYTE'''
	p[0]=p[1];
	

			


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
