
# -----------------------------------------------------------------------------
# ATmelo.py 
#
# ATmelo. lexical and syntax analizer for ATmelo language
# with semantic actions
# Authors. Homero Marin    A00810150
#		   Jonathan Frias  A00810797
# Date. 2015-10-13 18:46 hrs
# -----------------------------------------------------------------------------
##################################################
#utility classes
###################################################
class Cuadruplo:
	def __init__(self, operacion, operando1, operando2, resultado):
		self.operacion = operacion
		self.operando1 = operando1
		self.operando2 = operando2
		self.resultado = resultado

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
         
class VariableRecord:
 	def __init__(self, nombre, tipo, dirVirtual):
 		self.nombre = nombre
 		self.tipo = tipo
 		self.dirVirtual = dirVirtual

class ConstantRecord:
	def __init__(self, dirVirtual, tipo, valor):
		self.dirVirtual = dirVirtual;
		self.tipo = tipo;
		self.valor = valor;

class ProcessRecord:
 	def __init__(self, nombre, tipoRetorno, tablaVars, paramList, numberOfVars, numberOfParams, beginningCuad):
 		self.nombre = nombre
 		self.tipoRetorno = tipoRetorno
 		self.tablaVars = tablaVars
 		self.paramList = paramList
 		self.numberOfVars = numberOfVars
 		self.numberOfParams = numberOfParams
 		self.beginningCuad = beginningCuad

class Parameter:
	def __init__(self, nombre, tipo, dirVirtual):
		self.nombre = nombre;
		self.tipo = tipo;
		self.dirVirtual = dirVirtual;

###################################################

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
tablaConstantes = {}
globalVars = {}
localVars = {}
processDir = {}
listaParametrica = []
funcName = ""
programName = ""
funcRetType = ""
numberOfVars = 0
numberOfParams = 0
cuadruplos = []
contCuadruplos = 0;
pilaSaltos = Stack();
pilaTipos = Stack();
pilaResultados = Stack();
pilamultiarg = Stack();
MemoriaEjecucion = {}
pilaEjecucion = Stack();
#r for rows
#c for columns
##global Counts r0
##local Counts r1
##temp Counts r2
##cte Counts r3
## c0 - entero  c1 - flotante
## c2 - cadena  c3 - caracter
## c4 - byte
Counts = [[0, 0, 0, 0, 0, 0], #global Counts  <entero, flotante, cadena, caracter, byte, booleano>
		[0, 0, 0, 0, 0, 0], #local Counts <entero, flotante, cadena, caracter, byte, booleano>
		[0, 0, 0, 0, 0, 0], #temp Counts <entero, flotante, cadena, caracter, byte, booleano>
		[0, 0, 0, 0, 0, 0]] #cte Counts <entero, flotante, cadena, caracter, byte, booleano>

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

INT = 0
FLOAT = 1
STR = 2
CH = 3
BYTE = 4
BOOLEANO = 5

###############
#utilities
################################################
#utility imports
import sys
import re
from cuboSemantico import cubo
#utility functions

def functionExist(ID):
	return ID in processDir.keys();

##this function returns the operation code
def scopeType(datatype):
	typep = ""
	if datatype == "entero": 
		typep = INT
	elif datatype == "flotante":
		typep = FLOAT
	elif datatype == "cadena":
		typep = STR
	elif datatype == "caracter":
		typep = CH
	elif datatype == "byte":
		typep = BYTE
	elif datatype == "booleano":
		typep = BOOLEANO
	return typep

def getType(dato):
    dato = str(dato);
    tipo = ""
    if re.search(r'[0-1]{8}B', dato):
        tipo = "byte"
    elif re.search(r'[0-9]+\.[0-9]+', dato):
        tipo = "flotante"
    elif re.search('[0-9a-fA-F]+H', dato) or re.search('[0-9]+', dato):
        tipo = "entero"
    elif re.search(r'Verdadero|Falso', dato):
        tipo = "booleano"
    elif re.search(r'\'(\\?.)?\'', dato):
        tipo = "caracter"
    elif re.search(r'\"[^\"]*\"', dato):
        tipo = "cadena"

    if isType(dato):
        tipo = dato;
    return tipo

def isType(dato):
	flag = False;
	if dato == "entero" or dato == "flotante" or dato == "booleano" or dato == "cadena" or dato == "caracter" or dato == "byte":
		flag = True;
	return flag

def getTypeFromDir(aDir):
	datatype = ""
	maxLimit = 0
	begin = 0
	if aDir > GLOBALBEGIN and aDir < LOCALBEGIN:
		maxLimit = MAXGLOBALS;
		begin = GLOBALBEGIN;
	elif aDir > LOCALBEGIN and aDir < TEMPBEGIN:
		maxLimit = MAXLOCALS;
		begin = LOCALBEGIN;
	elif aDir > TEMPBEGIN and aDir < CTEBEGIN:
		maxLimit = MAXTEMPS;
		begin = TEMPBEGIN;
	elif aDir >= CTEBEGIN:
		maxLimit = MAXCTES;
		begin = CTEBEGIN;

	if (aDir - maxLimit*BOOLEANO  - begin) >= 0:
		datatype = "booleano";
	elif (aDir - maxLimit*BYTE - begin) >= 0:
		datatype = "byte";
	elif (aDir - maxLimit*CH - begin) >= 0:
		datatype = "caracter";
	elif (aDir - maxLimit*STR - begin) >= 0:
		datatype = "cadena";
	elif (aDir - maxLimit*FLOAT - begin) >= 0:
		datatype = "flotante";
	elif (aDir - maxLimit*INT - begin) >= 0:
		datatype = "entero";

	return datatype
def findIDinParamList(mutObj): #list: item0 is ID to search item1 is returned pos
	found = False;
	ID = mutObj[0];
	cont = 0;
	for param in listaParametrica:
		if param.nombre == ID:
			found = True;
			mutObj[1] = cont;
			break;
		cont = cont + 1;
	return found;

def opCode(operation):
	opcode = -1
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
	elif operation == "GOTO":
		opcode = 17
	elif operation == "GOTOF":
		opcode = 18
	elif operation == "GOTOT":
		opcode = 19
	elif operation == "=":
		opcode = 20
	elif operation == "and":
		opcode = 21
	elif operation == "or":
		opcode = 22
	elif operation == "not":
		opcode = 23
	elif operation == "regresaValor":
		opcode = 24

	return opcode
##this function returns the vars virtual Address
def IDvirtAddr(varID):
	addr = -1
	if not IDexist(varID, localVars):
		if not IDexist(varID, globalVars):
			mutObj = [varID, ""]; #0:ID 1:POS
			if funcName != "" and programName != funcName and findIDinParamList(mutObj):
				addr = listaParametrica[int(mutObj[1])].dirVirtual;
		else:
			addr = globalVars[varID].dirVirtual;
	else:
		addr = localVars[varID].dirVirtual;
	return addr

def getIDtype(varID):
	datatype = "none"
	if not IDexist(varID, localVars):
		if not IDexist(varID, globalVars):
			mutObj = [varID, ""] #0:ID 1:POS
			if funcName != "" and programName != funcName and findIDinParamList(mutObj):
				datatype = listaParametrica[int(mutObj[1])].tipo;
		else:
			datatype = globalVars[varID].tipo;
	else:
		datatype = localVars[varID].tipo;
	return datatype




##this function returns true if a var Exist in the given variable table, false otherwise
def IDexist(ID, varList):
	return ID in varList.keys()
##this function returns the memDir that the new variable would take
##it returns 0 if datatype segment is full
def dataTypeDist(datatype, scope):
	begin = 0
	maxLimit = 0
	scopeIndex = 0
	typeIndex = 0
	memDir = 0
	if scope == "GLOBAL":
		begin = GLOBALBEGIN
		maxLimit = MAXGLOBALS
		scopeIndex = GLOBALSCOPE
	elif scope == "LOCAL":
		begin = LOCALBEGIN
		maxLimit = MAXLOCALS
		scopeIndex = LOCALSCOPE
	elif scope == "TEMP":
		begin = TEMPBEGIN
		maxLimit = MAXTEMPS
		scopeIndex = TEMPSCOPE
	elif scope == "CTE":
		begin = CTEBEGIN
		maxLimit = MAXCTES
		scopeIndex = CTESCOPE

	if datatype == "entero": 
		typeIndex = INT
	elif datatype == "flotante":
		typeIndex = FLOAT
	elif datatype == "cadena":
		typeIndex = STR
	elif datatype == "caracter":
		typeIndex = CH
	elif datatype == "byte":
		typeIndex = BYTE
	elif datatype == "booleano":
		typeIndex = BOOLEANO

	count = Counts[scopeIndex][typeIndex]
	typeSectionSize = maxLimit
	if count < maxLimit:
		memDir = begin + typeIndex*typeSectionSize + count
	return memDir


#list of tokens
tokens = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'COLON', 
'COMMA', 'SEMICOLON', 'GT', 'LT', 'LCBRACE', 'RCBRACE', 
	'LPAREN', 'RPAREN', 'ID', 'EnteroDecimal', 
	'EnteroHexadecimal', 
	'ConstanteFlotante', 'ConstanteCadena', 
	'ConstanteCaracter', 'ConstanteByte', 'ConstanteBooleano'
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
	'booleano' : 'BOOLEANO',
	'sintipo' : 'SINTIPO',
	'diferentede' : 'DIFERENTEDE',
	'mayorigualque' : 'MAYORIGUALQUE',
	'menorigualque' : 'MENORIGUALQUE',
	'igualque' : 'IGUALQUE',
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

def t_ConstanteBooleano(t):
	r'Verdadero|Falso'
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
	global programName
	programName = p[-1]
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
	RPAREN numberOfParams COLON TIPO seenTipo SEMICOLON LCBRACE Declaracion_de_variables variablesDeclared \
	beginningOfFunc Contenido REGRESA optionFuncExp SEMICOLON RCBRACE funcExit'''
	global cuadruplos
	global contCuadruplos
	global pilaTipos
	global pilaResultados
	optionExp = p[18];
	retVal = False;
	if optionExp != None:
		retVal = True;
	if retVal:
		valorDir = pilaResultados.pop()
		pilaTipos.pop()
		cuadruplo = Cuadruplo(opCode("regresaValor"), valorDir, "", "");
		cuadruplos.append(cuadruplo);
		contCuadruplos = contCuadruplos + 1;
	cuadruplo = Cuadruplo(opCode("regresa"),"","","");
	cuadruplos.append(cuadruplo);
	contCuadruplos = contCuadruplos + 1;

def p_optionFuncExp(p):
	'''optionFuncExp : Expresion
						| NULL'''
	p[0] = p[1]

def p_seenTipo(p):
	'''seenTipo : '''
	global funcRetType
	funcRetType = p[-1];

def p_numberOfParams(p):
	'''numberOfParams : '''
	global numberOfParams
	numberOfParams = len(listaParametrica);

def p_variablesDeclared(p):
	'''variablesDeclared : '''
	global numberOfVars
	numberOfVars = len(localVars);

def p_beginningOfFunc(p):
	'''beginningOfFunc : '''
	global processDir
	global localVars
	global listaParametrica
	beginningCuad = contCuadruplos
	processRecord = ProcessRecord(funcName, funcRetType, localVars, listaParametrica, numberOfVars, numberOfParams, beginningCuad);
	processDir[funcName] = processRecord;

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
	global listaParametrica
	global processDir
	del localVars
	del listaParametrica
	del processDir[funcName].tablaVars
	funcName = ""

def p_Parametros(p):
	'''Parametros : Para
				| NULL'''

def p_Para(p):
	'''Para : TIPO ID seenIDparam
			| TIPO ID seenIDparam COMMA Para'''
	global listaParametrica
	global Counts
	tipo = p[1];
	ID = p[2];
	typep = scopeType(tipo);
	counts = Counts[LOCALSCOPE][typep];
	tempDir = ""
	if counts < MAXLOCALS:
		tempDir = dataTypeDist(tipo, "LOCAL");
		counts = counts + 1;
		Counts[LOCALSCOPE][typep] = counts;
	else:
		exit("too many local variables!");

	param = Parameter(ID, tipo, tempDir);
	listaParametrica.append(param)

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
	global cuadruplos
	global contCuadruplos
	global Counts
	global tablaConstantes
	global pilaResultados
	global pilaTipos
	ID = p[1];
	if not IDexist(ID, localVars):
		if not IDexist(ID, globalVars):
			mutObj = [p[1],""]; #LIST[0] = ID  LIST[1] = POS
			if funcName != "" and not (funcName != "" and programName != funcName and findIDinParamList(mutObj)):
				sys.exit("var " + ID + " does not exist. Aborting..")
			else:
				IDType = listaParametrica[int(mutObj[1])].tipo;
		else:
			IDType = globalVars[ID].tipo;
	else:
		IDType = localVars[ID].tipo;
	ExpType = getType(p[3]);
	dir1 = pilaResultados.pop()
	if functionExist(dir1):
		ExpType = pilaTipos.peek();
	if IDType != ExpType:
		exit("Error!, type mismatch.. line number: " + str(p.lexer.lineno));
	oper = p[2]
	res = p[1]
	op1 = p[3]
	opcode = opCode(oper);
	# print pilaResultados.items
	pilaTipos.pop()
	resDir = IDvirtAddr(res);
	if isType(op1):
		if not functionExist(dir1):
			dir1 = cuadruplos[-1].resultado;
	else:
		mutObj = [op1, ""];
		if IDexist(op1, localVars) or IDexist(op1, globalVars) or (funcName != "" and programName != funcName and findIDinParamList(mutObj)):
			dir1 = IDvirtAddr(op1);

	cuadruplo = Cuadruplo(opcode, dir1, "", resDir);
	cuadruplos.append(cuadruplo);
	contCuadruplos = contCuadruplos + 1;

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
					| TIPO LPAREN Expresion RPAREN SEMICOLON''' #castingf
	if len(p) == 3:
		p[0] = p[1]
		
	# typeMismatch = False
	# if len(p) == 3:
	# 	if (p[1] == 'x'):
	# 		typeMismatch = True
	# 	p[0] = p[1]
	# if typeMismatch:
	# 	sys.exit("Error!, type mismatch..")

def p_DeclaracionDeVariables(p):
	'''Declaracion_de_variables : TIPO COLON ID seenIDdeclVar SEMICOLON Declaracion_de_variables
									| TIPO COLON ID seenIDdeclVar EQUALS Expresion SEMICOLON Declaracion_de_variables
									| NULL'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global pilaResultados
	global pilaTipos
	global tablaConstantes
	if len(p) == 9:
		oper = p[5];
		opcode = opCode(oper);
		res = p[3];
		resDir = IDvirtAddr(res);
		op1 = p[6]
		dir1 = pilaResultados.pop();
		pilaTipos.pop();
		if isType(op1):
			dir1 = cuadruplos[-1].resultado;
		else:
			if IDexist(op1, localVars) or IDexist(op1, globalVars):
				dir1 = IDvirtAddr(op1);

		cuadruplo = Cuadruplo(opcode, dir1, "", resDir);
		cuadruplos.append(cuadruplo);
		contCuadruplos = contCuadruplos + 1;

		
		

def p_seenIDdeclVar(p):
	'''seenIDdeclVar : '''
	global localVars
	global Counts
	datatype = p[-3]
	ID = p[-1]
	typep = scopeType(datatype);
	counts = Counts[LOCALSCOPE][typep]
	if counts < MAXLOCALS:
		# varDeclSemValid(ID, datatype, dataTypeDist(datatype, "LOCAL"), localVars)
		varRecord = VariableRecord(ID, datatype, dataTypeDist(datatype, "LOCAL"));
		localVars[ID] = varRecord;
		counts = counts + 1
		Counts[LOCALSCOPE][typep] = counts
	else:
		sys.exit("Error, demasiadas variables locales!")

def p_EstatutoCondicion(p):
	'''Estatuto_Condicion : SI LPAREN Expresion Rparen \
	LCBRACE Contenido RCBRACE OptionalElse FINCOND'''
	
def p_Rparen(p):
	'''Rparen : RPAREN'''
	global pilaSaltos
	global cuadruplos
	global contCuadruplos
	global pilaResultados
	global pilaTipos
	pilaResultados.pop();
	pilaTipos.pop();
	# print pilaResultados.items
	# print pilaTipos.items
	expresion = pilaResultados.pop();
	tipo = pilaTipos.pop()
	if tipo != "booleano":
		exit("Error type Mismatch! :(");
	else:
	    cuadruplo = Cuadruplo(opCode("GOTOF"), expresion, "", "");
	    cuadruplos.append(cuadruplo);
	    contCuadruplos = contCuadruplos + 1;
	    # print contCuadruplos
	    pilaSaltos.push(contCuadruplos-1);
	    # print len(cuadruplos)
	    
def p_OptionalElse(p):
	'''OptionalElse : Sino LCBRACE Contenido RCBRACE
					| NULL'''
def p_Sino(p):
	'''Sino : SINO'''
	global contCuadruplos
	global cuadruplos
	global pilaSaltos
	falso = pilaSaltos.pop()
	cuadruplo = Cuadruplo(opCode("GOTO"),"","","");
	cuadruplos.append(cuadruplo);
	contCuadruplos = contCuadruplos + 1;
	pilaSaltos.push(contCuadruplos-1);
	cuadruplos[falso].resultado = contCuadruplos;

	
def p_FINCOND(p):
	'''FINCOND :'''
	global cuadruplos
	salida = pilaSaltos.pop();
	# print salida
	# print len(cuadruplos)
	cuadruplos[salida].resultado = contCuadruplos;
	
def p_EstatutoImprimirconsola(p):
	'''Imprimir : IMPRIMECONSOLA MULTIARG SEMICOLON'''
	global cuadruplos
	global contCuadruplos
	global pilamultiarg
	global pilaTipos

	# print pilamultiarg.size()
	while not pilamultiarg.isEmpty():
	 	cuadruplo = Cuadruplo(opCode("imprimeconsola"), pilamultiarg.pop(), "", "");
		cuadruplos.append(cuadruplo);
		contCuadruplos = contCuadruplos + 1;
		pilaTipos.pop()
		
		
	
	
def p_MULTIARG(p):
	'''MULTIARG : Expresion COMMA MULTIARG
				| Expresion'''
	global pilamultiarg
	global pilaTipos
	global pilaResultados
	global Counts
	global tablaConstantes
	tempDir = pilaResultados.pop();
	datatype = ""
	if IDexist(p[1], localVars) or IDexist(p[1], globalVars):
		tempDir = IDvirtAddr(p[1]);
	else:
		if isType(p[1]):
			tempDir = cuadruplos[-1].resultado;

	pilaTipos.pop();
	pilamultiarg.push(tempDir)
	pilaTipos.push(getType(p[1]))

def p_EstatutoEscrituraDePuerto(p):
	'''Estatuto_Escritura_de_puerto : ESCRIBEPUERTO PUERTO argPuerto SEMICOLON'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global tablaConstantes
	datatype = "";
	IDorCte = p[3];
	dir1 = ""
	if(IDexist(IDorCte, localVars) or IDexist(IDorCte, globalVars)):
		dir1 = IDvirtAddr(IDorCte);
		datatype = getIDtype(IDorCte);
		if datatype != "byte":
			exit("error! type mismatch, type must be byte");
	else:
		datatype = getType(IDorCte);
		if datatype != "byte":
			exit("error! type mismatch, type must be byte");
		typep = scopeType(datatype);	
		counts = Counts[CTESCOPE][typep]
		if counts < MAXCTES:
			dir1 = dataTypeDist(datatype, "CTE");
			constante = ConstantRecord(dir1, datatype, op1);
			tablaConstantes[dir1] = constante
			counts = counts + 1;
			Counts[CTESCOPE][typep] = counts;

	cuadruplo = Cuadruplo(opCode("escribepuerto"), dir1, "", p[2]);
	cuadruplos.append(cuadruplo);
	contCuadruplos = contCuadruplos + 1;
	
def p_ArgPuerto(p):
	'''argPuerto : ID
				| ConstanteByte'''
	p[0] = p[1]

def p_EstatutoLecturaDePuerto(p):
	'''Estatuto_Lectura_de_puerto : LEEPUERTO PUERTO ID SEMICOLON'''
	global cuadruplos
	global contCuadruplos
	global Counts
	datatype = "byte";
	typep = scopeType(datatype);	
	counts = Counts[TEMPSCOPE][typep]
	if counts < MAXTEMPS:
		tempVirtAddress = dataTypeDist("byte", "TEMP");
		cuadruplo = Cuadruplo("leepuerto", p[2], "", tempVirtAddress);
		Counts[TEMPSCOPE][typep] = counts + 1;
		cuadruplos.append(cuadruplo);
		contCuadruplos = contCuadruplos + 1;
		if not IDexist(p[3], localVars):
			if not IDexist(p[3], globalVars):
				exit("error variable not declared! lineno: " + str(p.lexer.lineno));
			else:
				tempIDVirtAddress = globalVars[p[3]].dirVirtual;
		else:
			tempIDVirtAddress = localVars[p[3]].dirVirtual;
	else:
		exit("too many temp variables!");	
	cuadruplo = Cuadruplo(opCode("="), tempVirtAddress, "", tempIDVirtAddress);
	cuadruplos.append(cuadruplo);
	contCuadruplos = contCuadruplos + 1;

def p_PUERTO(p):
	'''PUERTO : B 
				| C
				| D'''
	p[0] = p[1]

def p_EstatutoCiclo(p):
	'''Estatuto_Ciclo : CICLO whileMpsaltos LPAREN Expresion RPAREN whileSpsaltos\
	LCBRACE Contenido RCBRACE whilefin'''

def p_whilefin(p):
    '''whilefin : '''
    global cuadruplos
    global contCuadruplos
    global pilaSaltos
    falso = pilaSaltos.pop()
    retorno = pilaSaltos.pop()
    # print "retorno: " + str(retorno)
    # print "falso: " + str(falso)
    cuadruplo = Cuadruplo(opCode("GOTO"), "", "", retorno);
    cuadruplos.append(cuadruplo);
    contCuadruplos = contCuadruplos + 1;
    #arreglo de objetos
    #rellenar falso
    cuadruplos[falso].resultado = contCuadruplos;
   
def p_whileMpsaltos(p): 
	'''whileMpsaltos : '''
	global pilaSaltos
	pilaSaltos.push(contCuadruplos);
	
		
def p_whileSpsaltos(p):	
	'''whileSpsaltos : '''
	global cuadruplos
	global pilaSaltos
	global contCuadruplos
	tipo = pilaTipos.pop();
	if tipo != "booleano":
	    exit("Error type Mismatch! :(");
	else:
	    resultadoExp = pilaResultados.pop();
	    cuadruplo = Cuadruplo(opCode("GOTOF"), resultadoExp, "", "");
	    cuadruplos.append(cuadruplo);
	    contCuadruplos = contCuadruplos + 1;
	    pilaSaltos.push(contCuadruplos-1);
	
def p_Expresion(p):
	'''Expresion : superExp
				| NOT superExp'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global pilaResultados
	global pilaTipos
	global tablaConstantes
	if len(p) == 3:
		datatype = getType(p[2]);
		typep = scopeType(datatype);
		if(datatype != "booleano"):
			exit("type mismatch operand must be boolean!");	
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
		# varDeclSemValid(ID, datatype, dataTypeDist(datatype, "GLOBAL"), globalVars)
			opcode = opCode(p[1]);
			op1 = pilaResultados.pop()
			dir1 = op1
			tempVirtAddress = dataTypeDist(datatype, "TEMP");
			pilaTipos.pop();
			pilaTipos.push(getTypeFromDir(tempVirtAddress));
			pilaResultados.push(tempVirtAddress);
			cuadruplo = Cuadruplo(opcode, dir1, "", tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
		p[0] = p[2]
	else:
		p[0] = p[1]
		dato = p[0]
		op1 = dato
		res = ""
		tipo = getType(p[0]);
		if functionExist(dato):
			res = dato;
			tipo = processDir[dato].tipoRetorno;
		else:
			mutObj = [dato,""]#0:ID 1:POS
			if IDexist(dato, localVars) or IDexist(dato, globalVars) or (funcName != "" and programName != funcName and findIDinParamList(mutObj)):
				res = IDvirtAddr(dato);
			elif not isType(dato):
				datatype = getType(dato);
				typep = scopeType(datatype);
				# print dato
				# print datatype
				# print typep
				counts = Counts[CTESCOPE][typep];
				if counts < MAXCTES:
					res = dataTypeDist(datatype, "CTE");
					constante = ConstantRecord(res, datatype, op1);
					tablaConstantes[res] = constante;
					counts = counts + 1;
					Counts[CTESCOPE][typep] = counts;
				else:
					exit("too many constants error!");
		# print res		
		pilaResultados.push(res);
		pilaTipos.push(tipo);
def p_superExp(p):
	'''superExp : EX logica EX
				| EX'''
	global pilaTipos
	global pilaResultados
	global cuadruplos
	global contCuadruplos
	global Counts
	global tablaConstantes
	if len(p) == 4:
		# tipoOP1 = pilaTipos.pop()
		# tipoOP2 = pilaTipos.pop()
		# print "tipoOperador1: " + tipoOP1
		# print "tipoOperador2: " + tipoOP2
		oper1 = ""
		oper2 = ""
		if IDexist(p[1], localVars):
			oper1 = localVars[p[1]].tipo;
		elif IDexist(p[1], globalVars):
			oper1 = globalVars[p[1]].tipo;
		else:
			oper1 = p[1];

		if IDexist(p[3], localVars):
			oper2 = localVars[p[3]].tipo;
		elif IDexist(p[3], globalVars):
			oper2 = globalVars[p[3]].tipo;
		else:
			oper2 = p[3];

		resType = cubo(p[2], oper1, oper2)
		
		if resType == "x":
			exit("error: type mismatch! Invalid operation lineno : " + str(p.lexer.lineno));
		typep = scopeType(resType);	
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
		# varDeclSemValid(ID, datatype, dataTypeDist(datatype, "GLOBAL"), globalVars)
			opcode = opCode(p[2]);
			op1 = p[1];
			op2 = p[3];
			dir1 = ""
			dir2 = ""

			if IDexist(op1, localVars) or IDexist(op1, globalVars):
				dir1 = IDvirtAddr(op1);
			else:
				datatype = getType(op1);
				if Counts[CTESCOPE][scopeType(datatype)] < MAXCTES:
					dir1 = dataTypeDist(datatype, "CTE");
					constante = ConstantRecord(dir1, datatype, op1);
					tablaConstantes[dir1] = constante
					Counts[CTESCOPE][scopeType(datatype)] = Counts[CTESCOPE][scopeType(datatype)] + 1;
				else:
					exit("too many constant variables!");

			if IDexist(op2, localVars) or IDexist(op2, globalVars):
				dir2 = IDvirtAddr(op2);
			else:
				datatype = getType(op2);
				if Counts[CTESCOPE][scopeType(datatype)] < MAXCTES:
					dir2 = dataTypeDist(datatype, "CTE");
					constante = ConstantRecord(dir2, datatype, op2);
					tablaConstantes[dir2] = constante
					Counts[CTESCOPE][scopeType(datatype)] = Counts[CTESCOPE][scopeType(datatype)] + 1;
				else:
					exit("too many constant variables!");

			tempVirtAddress = dataTypeDist(resType, "TEMP");
			pilaTipos.pop();
			pilaTipos.push(resType);
			pilaResultados.pop();
			pilaResultados.push(tempVirtAddress);
			#cuadruplo = Cuadruplo(p[2], p[1], p[3], tempVirtAddress);
			cuadruplo = Cuadruplo(opcode, dir1, dir2, tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
		else:
			sys.exit("Error, demasiadas variables temporales!")
		p[0] = resType;
	else:
		p[0] = p[1]


def p_logica(p):
	'''logica : AND
			| OR'''
	p[0] = p[1]
	
def p_EX(p):
	'''EX : Exp Compara Exp
			| Exp'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global pilaTipos
	global pilaResultados
	global tablaConstantes
	if len(p) == 4:
		# tipoOP1 = pilaTipos.pop()
		# tipoOP2 = pilaTipos.pop()
		# print "tipoOperador1: " + tipoOP1
		# print "tipoOperador2: " + tipoOP2
		oper1 = ""
		oper2 = ""
		if IDexist(p[1], localVars):
			oper1 = localVars[p[1]].tipo;
		elif IDexist(p[1], globalVars):
			oper1 = globalVars[p[1]].tipo;
		else:
			oper1 = p[1];

		if IDexist(p[3], localVars):
			oper2 = localVars[p[3]].tipo;
		elif IDexist(p[3], globalVars):
			oper2 = globalVars[p[3]].tipo;
		else:
			oper2 = p[3];

		resType = cubo(p[2], oper1, oper2)
		
		if resType == "x":
			exit("error: type mismatch! Invalid operation lineno : " + str(p.lexer.lineno));
		typep = scopeType(resType);	
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
		# varDeclSemValid(ID, datatype, dataTypeDist(datatype, "GLOBAL"), globalVars)
			opcode = opCode(p[2]);
			op1 = p[1];
			op2 = p[3];
			dir1 = ""
			dir2 = ""
			datatype = ""
			if IDexist(op1, localVars) or IDexist(op1, globalVars):
				dir1 = IDvirtAddr(op1);
			else:
				datatype = getType(op1);
				if Counts[CTESCOPE][scopeType(datatype)] < MAXCTES:
					dir1 = dataTypeDist(datatype, "CTE");
					constante = ConstantRecord(dir1, datatype, op1);
					tablaConstantes[dir1] = constante
					Counts[CTESCOPE][scopeType(datatype)] = Counts[CTESCOPE][scopeType(datatype)] + 1;
				else:
					exit("too many constant variables!");

			if IDexist(op2, localVars) or IDexist(op2, globalVars):
				dir2 = IDvirtAddr(op2);
			else:
				datatype = getType(op2);
				if Counts[CTESCOPE][scopeType(datatype)] < MAXCTES:
					dir2 = dataTypeDist(datatype, "CTE");
					constante = ConstantRecord(dir2, datatype, op2);
					tablaConstantes[dir2] = constante
					Counts[CTESCOPE][scopeType(datatype)] = Counts[CTESCOPE][scopeType(datatype)] + 1;
				else:
					exit("too many constant variables!");

			tempVirtAddress = dataTypeDist(resType, "TEMP");
			pilaTipos.push(resType);
			pilaResultados.push(tempVirtAddress);
			#cuadruplo = Cuadruplo(p[2], p[1], p[3], tempVirtAddress);
			cuadruplo = Cuadruplo(opcode, dir1, dir2, tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
		else:
			sys.exit("Error, demasiadas variables temporales!")
		p[0] = resType;
	else:
		p[0] = p[1]

def p_Compara(p):
	'''Compara : 	  GT
					| LT
					| DIFERENTEDE
					| MAYORIGUALQUE
					| MENORIGUALQUE
					| IGUALQUE'''
	p[0] = p[1]

			
def p_Exp(p):
	'''Exp : Exp PLUS Termino
			| Exp MINUS Termino
			| Termino'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global tablaConstantes
	if len(p) == 4:
		# tipoOP1 = pilaTipos.pop()
		# tipoOP2 = pilaTipos.pop()
		# print "tipoOperador1: " + tipoOP1
		# print "tipoOperador2: " + tipoOP2
		oper1 = ""
		oper2 = ""
		if IDexist(p[1], localVars):
			oper1 = localVars[p[1]].tipo;
		elif IDexist(p[1], globalVars):
			oper1 = globalVars[p[1]].tipo;
		else:
			oper1 = p[1];

		if IDexist(p[3], localVars):
			oper2 = localVars[p[3]].tipo;
		elif IDexist(p[3], globalVars):
			oper2 = globalVars[p[3]].tipo;
		else:
			oper2 = p[3];

		resType = cubo(p[2], oper1, oper2)
		
		if resType == "x":
			exit("error: type mismatch! Invalid operation lineno : " + str(p.lexer.lineno));
		typep = scopeType(resType);	
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
		# varDeclSemValid(ID, datatype, dataTypeDist(datatype, "GLOBAL"), globalVars)
			opcode = opCode(p[2]);
			op1 = p[1];
			op2 = p[3];
			dir1 = ""
			dir2 = ""

			mutObj = [op1, ""] #0:ID 1:POS
			if IDexist(op1, localVars) or IDexist(op1, globalVars) or (funcName != "" and programName != funcName and findIDinParamList(mutObj)):
				dir1 = IDvirtAddr(op1);
			else:
				datatype = getType(op1);
				# print op1
				# print datatype
				if Counts[CTESCOPE][scopeType(datatype)] < MAXCTES:
					dir1 = dataTypeDist(datatype, "CTE");
					constante = ConstantRecord(dir1, datatype, op1);
					tablaConstantes[dir1] = constante
					Counts[CTESCOPE][scopeType(datatype)] = Counts[CTESCOPE][scopeType(datatype)] + 1;
				else:
					exit("too many constant variables!");

			if IDexist(op2, localVars) or IDexist(op2, globalVars):
				dir2 = IDvirtAddr(op2);
			else:
				datatype = getType(op2);
				if Counts[CTESCOPE][scopeType(datatype)] < MAXCTES:
					dir2 = dataTypeDist(datatype, "CTE");
					constante = ConstantRecord(dir2, datatype, op2);
					tablaConstantes[dir2] = constante
					Counts[CTESCOPE][scopeType(datatype)] = Counts[CTESCOPE][scopeType(datatype)] + 1;
				else:
					exit("too many constant variables!");

			tempVirtAddress = dataTypeDist(resType, "TEMP");
			#cuadruplo = Cuadruplo(p[2], p[1], p[3], tempVirtAddress);
			cuadruplo = Cuadruplo(opcode, dir1, dir2, tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
		else:
			sys.exit("Error, demasiadas variables temporales!")
		p[0] = resType;
	else:
		p[0] = p[1]

def p_Termino(p):
	'''Termino : Termino TIMES bitOp
			| Termino DIVIDE bitOp
			| bitOp'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global tablaConstantes
	if len(p) == 4:
		# tipoOP1 = pilaTipos.pop()
		# tipoOP2 = pilaTipos.pop()
		# print "tipoOperador1: " + tipoOP1
		# print "tipoOperador2: " + tipoOP2
		oper1 = ""
		oper2 = ""
		if IDexist(p[1], localVars) or IDexist(p[1], globalVars):
			oper1 = getIDtype(p[1]);
		else:
			oper1 = p[1];

		if IDexist(p[3], localVars) or IDexist(p[3], globalVars):
			oper2 = getIDtype(p[3]);
		else:
			oper2 = p[3];

		resType = cubo(p[2], oper1, oper2)
		
		if resType == "x":
			exit("error: type mismatch! Invalid operation lineno : " + str(p.lexer.lineno));
		typep = scopeType(resType);	
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
		# varDeclSemValid(ID, datatype, dataTypeDist(datatype, "GLOBAL"), globalVars)
			opcode = opCode(p[2]);
			op1 = p[1];
			op2 = p[3];
			dir1 = ""
			dir2 = ""
			if IDexist(op1, localVars) or IDexist(op1, globalVars):
				dir1 = IDvirtAddr(op1);
			else:
				datatype = getType(op1);
				if Counts[CTESCOPE][scopeType(datatype)] < MAXCTES:
					dir1 = dataTypeDist(datatype, "CTE");
					constante = ConstantRecord(dir1, datatype, op1);
					tablaConstantes[dir1] = constante
					Counts[CTESCOPE][scopeType(datatype)] = Counts[CTESCOPE][scopeType(datatype)] + 1;
				else:
					exit("too many constants variables!");

			if IDexist(op2, localVars) or IDexist(op2, globalVars):
				dir2 = IDvirtAddr(op2);
			else:
				datatype = getType(op2);
				if Counts[CTESCOPE][scopeType(datatype)] < MAXCTES:
					dir2 = dataTypeDist(datatype, "CTE");
					constante = ConstantRecord(dir2, datatype, op2);
					tablaConstantes[dir2] = constante
					Counts[CTESCOPE][scopeType(datatype)] = Counts[CTESCOPE][scopeType(datatype)] + 1;
				else:
					exit("too many constants variables!");

			tempVirtAddress = dataTypeDist(resType, "TEMP");
			#cuadruplo = Cuadruplo(p[2], p[1], p[3], tempVirtAddress);
			cuadruplo = Cuadruplo(opcode, dir1, dir2, tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
		else:
			sys.exit("Error, demasiadas variables temporales!")
		p[0] = resType;
	else:
		p[0] = p[1]
	

def p_bitOp(p):
	'''bitOp : bitOp ORBIT Factor
			| bitOp XORBIT Factor
			| bitOp ANDBIT Factor
			| Factor'''
	#global pilaTipos
	global cuadruplos
	global contCuadruplos
	global Counts
	global pilaResultados
	global pilaTipos
	global tablaConstantes
	if len(p) == 4:
		# tipoOP1 = pilaTipos.pop()
		# tipoOP2 = pilaTipos.pop()
		# print "tipoOperador1: " + tipoOP1
		# print "tipoOperador2: " + tipoOP2
		oper1 = ""
		oper2 = ""
		if IDexist(p[1], localVars):
			oper1 = localVars[p[1]].tipo;
		elif IDexist(p[1], globalVars):
			oper1 = globalVars[p[1]].tipo;
		else:
			oper1 = p[1];

		if IDexist(p[3], localVars):
			oper2 = localVars[p[3]].tipo;
		elif IDexist(p[3], globalVars):
			oper2 = globalVars[p[3]].tipo;
		else:
			oper2 = p[3];

		resType = cubo(p[2], oper1, oper2)
		
		if resType == "x":
			exit("error: type mismatch! Invalid operation lineno : " + str(p.lexer.lineno));
		typep = scopeType(resType);	
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
		# varDeclSemValid(ID, datatype, dataTypeDist(datatype, "GLOBAL"), globalVars)
			opcode = opCode(p[2]);
			op1 = p[1];
			op2 = p[3];
			dir1 = ""
			dir2 = ""

			if IDexist(op1, localVars) or IDexist(op1, globalVars):
				dir1 = IDvirtAddr(op1);
			else:
				datatype = getType(op1);
				if Counts[CTESCOPE][scopeType(datatype)] < MAXCTES:
					dir1 = dataTypeDist(datatype, "CTE");
					constante = ConstantRecord(dir1, datatype, op1);
					tablaConstantes[dir1] = constante;
					Counts[CTESCOPE][scopeType(datatype)] = Counts[CTESCOPE][scopeType(datatype)] + 1;
				else:
					exit("too many constant variables!");

			if IDexist(op2, localVars) or IDexist(op2, globalVars):
				dir2 = IDvirtAddr(op2);
			else:
				datatype = getType(op2);
				if Counts[CTESCOPE][scopeType(datatype)] < MAXCTES:
					dir2 = dataTypeDist(datatype, "CTE");
					constante = ConstantRecord(dir2, datatype, op2);
					tablaConstantes[dir2] = constante
					Counts[CTESCOPE][scopeType(datatype)] = Counts[CTESCOPE][scopeType(datatype)] + 1;
				else:
					exit("too many constant variables!");

			tempVirtAddress = dataTypeDist(resType, "TEMP");
			#cuadruplo = Cuadruplo(p[2], p[1], p[3], tempVirtAddress);
			cuadruplo = Cuadruplo(opcode, dir1, dir2, tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
		else:
			sys.exit("Error, demasiadas variables temporales!")
		p[0] = resType;
	else:
		p[0] = p[1]

def p_Factor(p):
	'''Factor : LPAREN Expresion RPAREN
			| ID LPAREN MULTIARG RPAREN
			| CTE
			| IDoperand'''
	if len(p) == 5:
		ID = p[1]
		if functionExist(ID):
			p[0] = processDir[ID].nombre;
		else:
			exit("error function " + str(ID) + " is not declared!");
	elif len(p) == 4:
		p[0] = p[2]
		pilaTipos.pop()
		pilaResultados.pop()
	elif len(p) == 2:
		p[0] = p[1]

def p_IDoperand(p):
	'''IDoperand : ID'''
	if not IDexist(p[1], localVars):
		if not IDexist(p[1], globalVars):
			mutObj = [p[1],""]; #LIST[0] = ID  LIST[1] = POS
			if funcName != "" and not (funcName != "" and programName != funcName and findIDinParamList(mutObj)):
				sys.exit("Error!, trying to operate with " + p[1] + " but it does note exist..")
			else:
				p[0] = listaParametrica[int(mutObj[1])].nombre;#list item 1 is position of ID found
	 	else:
	 		p[0] = globalVars[p[1]].nombre;

	else:
		p[0] = localVars[p[1]].nombre;
	#p[0] = p[1]
def p_CTE(p):
	'''CTE : Entero
				| CteFlotante
				| CteCadena
				| CteCaracter
				| CteByte
				| CteBooleano'''
	p[0] = p[1]

def p_CteByte(p):
	'''CteByte : ConstanteByte'''
	# p[0] = 'byte'
	p[0] = p[1]
def p_CteCaracter(p):
	'''CteCaracter : ConstanteCaracter'''
	# p[0] = 'caracter'
	p[0] = p[1]
def p_CteCadena(p):
	'''CteCadena : ConstanteCadena'''
	# p[0] = 'cadena'
	p[0] = p[1]
def p_CteFlotante(p):
	'''CteFlotante : ConstanteFlotante'''
	# p[0] = 'flotante'
	p[0] = p[1]
def p_CteBooleano(p):
	'''CteBooleano : ConstanteBooleano'''
	# p[0] = 'booleano'
	p[0] = p[1]
def p_Entero(p):
	'''Entero : EnteroDecimal
				| EnteroHexadecimal'''
	# p[0] = 'entero'
	p[0] = p[1]


def p_NULL(p):
	'''NULL : '''

def p_Contenido(p):
	'''Contenido : Estatuto Contenido
					| NULL'''

def p_Variables_Globales(p):
	'''Variables_Globales : R'''
	
def p_R(p):
	'''R : TIPO COLON ID seenIDglobVar SEMICOLON R
			| NULL'''

			
def p_seenIDglobVar(p):
	'''seenIDglobVar : '''
	global globalVars
	global Counts
	typep = 0
	datatype = p[-3]
	ID = p[-1]
	typep = scopeType(datatype);
	counts = Counts[GLOBALSCOPE][typep]
	if counts < MAXGLOBALS:
		# varDeclSemValid(ID, datatype, dataTypeDist(datatype, "GLOBAL"), globalVars)
		varRecord = VariableRecord(ID, datatype, dataTypeDist(datatype, "GLOBAL"));
		globalVars[ID] = varRecord;
		counts = counts + 1
		Counts[GLOBALSCOPE][typep] = counts
	else:
		sys.exit("Error, demasiadas variables globales!")

def p_TIPO(p):
	'''TIPO : ENTERO
			| FLOTANTE
			| CADENA
			| CARACTER
			| BYTE
			| BOOLEANO
			| SINTIPO'''
	p[0]=p[1];
	

			


###########################

def p_error(p):
	print("Syntax error at '%s' lineno: '%d' column: '%d'" %\
	(p.value, p.lineno, p.lexpos - offset))
	exit("Error aqui")

def compile():
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
	print "lista de constantes"
	cont = 0
	llavesConstantes = sorted(tablaConstantes.keys())
	for constante in llavesConstantes:
		print "constante " + str(cont+1) + ": " + str(tablaConstantes[constante].dirVirtual) + ", " + str(tablaConstantes[constante].tipo) + ", " +\
		str(tablaConstantes[constante].valor);
		cont = cont + 1
		
	print "lista de cuadruplos"
	cont = 0
	for cuadruplo in cuadruplos:
		print "cuadruplo " + str(cont) + ": " + str(cuadruplo.operacion) + ", " + str(cuadruplo.operando1) + ", " +\
		str(cuadruplo.operando2) + ", " + str(cuadruplo.resultado);
		cont = cont + 1

compile();
