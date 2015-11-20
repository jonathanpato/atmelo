
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
 	def __init__(self, IDnumber, nombre, tipoRetorno, tablaVars, paramList, numberOfVars, numberOfParams, beginningCuad, returnGlobalVar):
 		self.nombre = nombre
 		self.tipoRetorno = tipoRetorno
 		self.tablaVars = tablaVars
 		self.paramList = paramList
 		self.numberOfVars = numberOfVars
 		self.numberOfParams = numberOfParams
 		self.beginningCuad = beginningCuad
 		self.returnGlobalVar = returnGlobalVar

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
numberOfVars = {}
numberOfParams = 0
cuadruplos = []
contCuadruplos = 0;
pilaSaltos = Stack();
pilaTipos = Stack();
pilaResultados = Stack();
pilaResultadosTemp = Stack();
pilamultiarg = Stack();
MemoriaEjecucion = {}
pilaEjecucion = Stack();
pilaO = Stack();
FunctionCount = 0
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
LOCALBEGIN = 23800
TEMPBEGIN = 47800
CTEBEGIN = 71800

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

def funcionSinParametros(ID):
	global Counts
	global cuadruplos
	global contCuadruplos
	global processDir
	global pilaResultados
	global pilaTipos
	global pilamultiarg
	global argCont
	ID = ID
	if functionExist(ID):
		sizeERA = 0
		sizeDef = processDir[ID].numberOfParams;
		for i in range(sizeDef):
			sizeERA = sizeERA + typeSize(processDir[ID].paramList[i]);
			sizeERA = sizeERA + processDir[ID].numberOfVars["entero"]*typeSize("entero");
			sizeERA = sizeERA + processDir[ID].numberOfVars["flotante"]*typeSize("flotante");
			sizeERA = sizeERA + processDir[ID].numberOfVars["caracter"]*typeSize("caracter");
			sizeERA = sizeERA + processDir[ID].numberOfVars["cadena"]*typeSize("cadena");
			sizeERA = sizeERA + processDir[ID].numberOfVars["booleano"]*typeSize("booleano");
			cuadruplo = Cuadruplo(opCode("ERA"), sizeERA, "", "");
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			
		beginningDir = processDir[ID].beginningCuad;
		cuadruplo = Cuadruplo(opCode("GOSUB"), ID, "", beginningDir);
		cuadruplos.append(cuadruplo);
		contCuadruplos = contCuadruplos + 1;
		datatype = processDir[ID].tipoRetorno;
		typep = scopeType(datatype)
		counts = Counts[GLOBALSCOPE][typep];
		if counts < MAXGLOBALS:
			tempVirtAddress = dataTypeDist(datatype, "GLOBAL");
			variableGlobal = VariableRecord(ID, datatype, tempVirtAddress);
			processDir[ID].returnGlobalVar = variableGlobal;
			counts = counts + 1;
			Counts[GLOBALSCOPE][typep] = counts;
			pilaTipos.push(datatype)
			pilaResultados.push(tempVirtAddress)
		else:
			exit("too many globals!");
	else:
		exit("error function " + str(ID) + " is not declared!");

def typeSize(aType):
	size = 0;
	if aType == "entero":
		size = 4;
	elif aType == "flotante":
		size = 8;
	elif aType == "caracter":
		size = 1;
	elif aType == "cadena":
		size = 30;
	elif aType == "booleano":
		size = 1;
	return size;

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

def isVirtDir(obj):
	flag = False;
	if type(obj) == int:
		if obj >= 1000 and obj < 120000:
			flag = True;
	return flag;

def isType(dato):
	flag = False;
	if dato == "entero" or dato == "flotante" or dato == "booleano" or dato == "cadena" or dato == "caracter" or dato == "byte":
		flag = True;
	return flag

def getTypeFromDir(aDir):
	datatype = ""
	maxLimit = 0
	begin = 0
	if aDir >= GLOBALBEGIN and aDir < LOCALBEGIN:
		maxLimit = MAXGLOBALS;
		begin = GLOBALBEGIN;
	elif aDir >= LOCALBEGIN and aDir < TEMPBEGIN:
		maxLimit = MAXLOCALS;
		begin = LOCALBEGIN;
	elif aDir >= TEMPBEGIN and aDir < CTEBEGIN:
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
	elif operation == "cast":
		opcode = 25
	elif operation == "ERA":
		opcode = 26
	elif operation == "GOSUB":
		opcode = 27
	elif operation == "PARAM":
		opcode = 28
	return opcode

def potNumber(port):
	number = 0
	if port == "B":
		number = 81;
	elif port == "C":
		number = 82;
	elif port == "D":
		number = 83;
	return number;

def getopCode(opVM):
	operVM = -1
	if opVM == 1:
		operVM = "|"
	elif opVM == 2:
		operVM = "^"
	elif opVM == 3:
		operVM = "&"
	elif opVM == 4:
		operVM = "*"
	elif opVM == 5:
		operVM = "/"
	elif opVM == 6:
		operVM = "+"
	elif opVM == 7:
		operVM = "-"
	elif opVM == 8:
		operVM = ">"
	elif opVM == 9:
		operVM = "<"
	elif opVM ==  10:
		operVM = "!="
	elif opVM == 11:
		operVM = ">="
	elif opVM == 12:
		operVM = "<="
	elif opVM == 13:
		operVM = "escribepuerto"
	elif opVM == 14:
		operVM = "leepuerto"
	elif opVM == 15:
		operVM = "printf"
	elif opVM == 16:
		operVM = "return"
	elif opVM == 17:
		operVM = "GOTO"
	elif opVM == 18:
		operVM = "GOTOF"
	elif opVM == 19:
		operVM = "GOTOT"
	elif opVM == 20:
		operVM = "="
	elif opVM == 21:
		operVM = "&&"
	elif opVM == 22:
		operVM = "||"
	elif opVM == 23:
		operVM = "!"
	elif opVM == 24:
		operVM = " "
	return operVM

##this function returns the vars virtual Address
def IDvirtAddr(varID):
	addr = -1
	if not IDexist(varID, localVars):
		mutObj = [varID, ""]; #0:ID 1:POS
		if not (funcName != "" and programName != funcName and findIDinParamList(mutObj)):
			if not IDexist(varID, globalVars):
				addr = -1
			else:
				addr = globalVars[varID].dirVirtual;
		else:
			addr = listaParametrica[int(mutObj[1])].dirVirtual;
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
	# print begin
	# print typeIndex*typeSectionSize
	# print count
	# print memDir
	return memDir


#list of tokens
tokens = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'COLON', 
'COMMA', 'SEMICOLON', 'GT', 'LT', 'LCBRACE', 'RCBRACE', 
	'LPAREN', 'RPAREN', 'ID', 'EnteroDecimal', 
	'EnteroHexadecimal', 
	'ConstanteFlotante', 'ConstanteCadena', 
	'ConstanteCaracter', 'ConstanteByte', 'ConstanteBooleano', 'DOBLEPOINT', 'LBRACKET', 'RBRACKET'
	
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
	'array' : 'ARRAY',

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
t_DOBLEPOINT = r'\.\.'
t_LBRACKET = r'\]'
t_RBRACKET = r'\['
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
	numberOfVars["entero"] = Counts[LOCALSCOPE][scopeType("entero")];
	numberOfVars["flotante"] = Counts[LOCALSCOPE][scopeType("flotante")];
	numberOfVars["caracter"] = Counts[LOCALSCOPE][scopeType("caracter")];
	numberOfVars["cadena"] = Counts[LOCALSCOPE][scopeType("cadena")];
	numberOfVars["booleano"] = Counts[LOCALSCOPE][scopeType("booleano")];

def p_beginningOfFunc(p):
	'''beginningOfFunc : '''
	global processDir
	global localVars
	global listaParametrica
	beginningCuad = contCuadruplos
	processRecord = ProcessRecord("", funcName, funcRetType, localVars, listaParametrica, numberOfVars, numberOfParams, beginningCuad, "");
	# print funcName
	processDir[funcName] = processRecord;
	# print processDir[funcName].beginningCuad;
def p_seenIDfunc(p):
	'''seenIDfunc : '''
	global localVars
	global funcName
	global processDir
	global FunctionCount
	funcName = p[-1]
	localVars = {}

def p_funcExit(p):
	'''funcExit : '''
	global funcName
	global localVars
	global listaParametrica
	global processDir
	global Counts
	global FunctionCount
	del localVars
	del listaParametrica
	del processDir[funcName].tablaVars
	processDir[funcName].IDnumber = FunctionCount;
	FunctionCount = FunctionCount + 1;
	funcName = ""
	# length = len(Counts[LOCALSCOPE])
	# for i in range(length):
	# 	Counts[LOCALSCOPE][i] = 0;

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


def p_Estatuto(p):
	'''Estatuto :  Estatuto_Asignacion
				| Estatuto_Condicion
				| Estatuto_Escritura_de_puerto
				| Estatuto_Lectura_de_puerto
				| Estatuto_Ciclo 
				| Imprimir
				| LlamadaFuncion'''


def p_LlamadaFuncion(p):
	'''LlamadaFuncion : ID LPAREN MULTIARG afterMultiArg afterMultiArgFUNC RPAREN SEMICOLON
						| ID LPAREN RPAREN SEMICOLON'''
	if len(p) == 5:
		ID = p[1];
		funcionSinParametros(ID);
	
def p_EstatutoAsignacion(p):
	'''Estatuto_Asignacion : ID EQUALS AssignOption'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global pilaResultados
	global pilaTipos

	ID = p[1];
	IDVAddr = IDvirtAddr(ID);
	if IDVAddr == -1:
		exit("trying to assign a value to a non declared variable!");
	dir1 = pilaResultados.pop()
	
	tipo = pilaTipos.pop()
	tipoID = getTypeFromDir(IDVAddr);
	
	if tipoID != tipo:
		exit("type mismatch during assignment!");
	cuadruplo = Cuadruplo(opCode("="), dir1, "", IDVAddr);
	cuadruplos.append(cuadruplo);
	contCuadruplos = contCuadruplos + 1;


def p_AssignOption(p):
	'''AssignOption : Expresion SEMICOLON
					| TIPO LPAREN Expresion RPAREN SEMICOLON''' #castingf
	global cuadruplos
	global contCuadruplos
	global pilaResultados
	global pilaTipos
	if len(p) == 6:
		p[0] = p[3]
		tipoAnterior = pilaTipos.pop()
		nuevoTipo = p[1]
		dir1 = pilaResultados.pop();
		typep = scopeType(nuevoTipo);
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
			opcode = opCode("cast");
			tempVirtAddress = dataTypeDist(nuevoTipo, "TEMP");
			cuadruplo = Cuadruplo(opcode, dir1, scopeType(nuevoTipo), tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
			p[0] = tempVirtAddress;
			pilaTipos.push(nuevoTipo);
			pilaResultados.push(tempVirtAddress);
	else:
		p[0] = p[1]
		
	# print "AssignOption: " + str(p[0])
	

def p_DeclaracionDeVariables(p):
	'''Declaracion_de_variables : formatoDeclarar Declaracion_de_variables
									| TIPO COLON ID COLON ARRAY LBRACKET CTE DOBLEPOINT CTE COMMA ARR RBRACKET Declaracion_de_variables
									| NULL''' #Arreglo en declaracion de variables

def p_formatoDeclarar(p):
	'''formatoDeclarar : TIPO COLON ID seenIDdeclVar declOptionAssign SEMICOLON'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global pilaResultados
	global pilaTipos
	global localVars

	ID = p[3];
	tipo = p[1]
	dirVirtual = ""
	hasExp = p[5]
	
	if hasExp:
		oper = "="
		opcode = opCode(oper);
		dir1 = pilaResultados.pop();
		tipoExp = pilaTipos.pop();
		if tipoExp != tipo:
			exit("type mismatch during declaration with assignment!");
		IDvirDir = IDvirtAddr(ID);
		cuadruplo = Cuadruplo(opcode, dir1, "", IDvirDir);
		cuadruplos.append(cuadruplo);
		contCuadruplos = contCuadruplos + 1;
	
	
def p_declOptionAssign(p):
	'''declOptionAssign : EQUALS Expresion
						| NULL'''
	if len(p) == 3:
		p[0] = True;
	else:
		p[0] = False;

def p_ARR(p):
	'''ARR : SEMICOLON CTE DOBLEPOINT CTE ARR
				| NULL'''
				
def p_seenIDdeclVar(p):
	'''seenIDdeclVar : '''
	global localVars
	global Counts
	datatype = p[-3]
	ID = p[-1]
	typep = scopeType(datatype);
	counts = Counts[LOCALSCOPE][typep]
	if counts < MAXLOCALS:
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
	'''Imprimir : IMPRIMECONSOLA MULTIARG afterMultiArg SEMICOLON'''
	global cuadruplos
	global contCuadruplos
	global pilamultiarg
	global pilaTipos
	global argCont
	# print argCont
	while not pilamultiarg.isEmpty():
	 	cuadruplo = Cuadruplo(opCode("imprimeconsola"), pilamultiarg.pop(), "", "");
		cuadruplos.append(cuadruplo);
		contCuadruplos = contCuadruplos + 1;
		pilaTipos.pop()
	
argCont = 1;	
	
def p_MULTIARG(p):
	'''MULTIARG : Expresion afterExpresionMult COMMA MULTIARG 
				| Expresion'''
	

def p_afterExpresionMult(p):
	'''afterExpresionMult : '''
	global argCont
	argCont = argCont + 1;
	

def p_afterMultiArg(p):
	'''afterMultiArg : '''
	global pilamultiarg
	global pilaTipos
	global pilaResultados
	global argCont
	# print argCont
	# print pilaResultados.items
	# print pilaTipos.items
	# print "from aftermultiarg"
	# print str(argCont)
	for i in range(argCont):
		tempDir = pilaResultados.pop();
		datatype = pilaTipos.pop()
		pilamultiarg.push(tempDir);
		pilaTipos.push(datatype);
	argCont = 1
	# print "after modifying in aftermultiarg"
	# print pilaResultados.items
	# print pilamultiarg.items

def p_EstatutoEscrituraDePuerto(p):
	'''Estatuto_Escritura_de_puerto : ESCRIBEPUERTO PUERTO Expresion SEMICOLON'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global pilaTipos
	global pilaResultados
	datatype = pilaTipos.pop()
	puerto = p[2];
	if datatype != "byte":
		exit("type mismatch.. trying to write a non byte value to port: " + str(puerto));
	dir1 = pilaResultados.pop()
	
	cuadruplo = Cuadruplo(opCode("escribepuerto"), dir1, "", puerto);
	cuadruplos.append(cuadruplo);
	contCuadruplos = contCuadruplos + 1;
	

def p_EstatutoLecturaDePuerto(p):
	'''Estatuto_Lectura_de_puerto : LEEPUERTO PUERTO ID SEMICOLON'''
	global cuadruplos
	global contCuadruplos
	global Counts
	ID = p[3];
	dirVirtual = IDvirtAddr(ID);
	if dirVirtual == -1:
		exit("trying to assign to a non declared variable from read port");
	datatype = getTypeFromDir(dirVirtual);
	if datatype != "byte":
		exit("error, variable must be byte type to assign a value from read port");
	typep = scopeType(datatype);	
	counts = Counts[TEMPSCOPE][typep]
	puerto = p[2]
	cuadruplo = Cuadruplo("leepuerto", puerto, "", dirVirtual);	
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
	if len(p) == 3:
		op1 = pilaResultados.pop()
		tipo = pilaTipos.pop()
		operacion = "not"
		if tipo != "booleano":
			exit("error type mismatch!");
		typep = scopeType("booleano");
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
			opcode = opCode(operacion);
			tempVirtAddress = dataTypeDist(tipo, "TEMP");
			cuadruplo = Cuadruplo(opcode, op1, "", tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
			p[0] = tempVirtAddress;
			pilaTipos.push(tipo);
			pilaResultados.push(tempVirtAddress);
		else:
			sys.exit("Error, demasiadas variables temporales!")
		p[0] = p[2]
	else:
		p[0] = p[1]
	# print "Expresion: " + str(p[0])

def p_superExp(p):
	'''superExp : EX logica EX
				| EX'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global pilaResultados
	global pilaTipos
	if len(p) == 4:
		op1 = p[1];
		op2 = p[3];
		tipo1 = pilaTipos.pop()
		tipo2 = pilaTipos.pop()
		dir1 = pilaResultados.pop()
		dir2 = pilaResultados.pop()
		operacion = p[2]
		resType = cubo(operacion, tipo1, tipo2)
		if resType == "x":
			exit("error: type mismatch! Invalid operation lineno : " + str(p.lexer.lineno));
		typep = scopeType(resType);	
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
			opcode = opCode(operacion);
			tempVirtAddress = dataTypeDist(resType, "TEMP");
			cuadruplo = Cuadruplo(opcode, dir1, dir2, tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
			p[0] = tempVirtAddress;
			pilaTipos.push(resType);
			pilaResultados.push(tempVirtAddress);
		else:
			sys.exit("Error, demasiadas variables temporales!")
		
	else:
		p[0] = p[1]
	# print "SuperExp: " + str(p[0])

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
	global pilaResultados
	global pilaTipos
	if len(p) == 4:
		op1 = p[1];
		op2 = p[3];
		tipo1 = pilaTipos.pop()
		tipo2 = pilaTipos.pop()
		dir1 = pilaResultados.pop()
		dir2 = pilaResultados.pop()
		operacion = p[2]
		resType = cubo(operacion, tipo1, tipo2)
		if resType == "x":
			exit("error: type mismatch! Invalid operation lineno : " + str(p.lexer.lineno));
		typep = scopeType(resType);	
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
			opcode = opCode(operacion);
			tempVirtAddress = dataTypeDist(resType, "TEMP");
			cuadruplo = Cuadruplo(opcode, dir1, dir2, tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
			p[0] = tempVirtAddress;
			pilaTipos.push(resType);
			pilaResultados.push(tempVirtAddress);
		else:
			sys.exit("Error, demasiadas variables temporales!")
		
	else:
		p[0] = p[1]
	# print "EX" + str(p[0])

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
	global pilaResultados
	global pilaTipos
	if len(p) == 4:
		op1 = p[1];
		op2 = p[3];
		tipo1 = pilaTipos.pop()
		tipo2 = pilaTipos.pop()
		dir1 = pilaResultados.pop()
		dir2 = pilaResultados.pop()
		operacion = p[2]
		resType = cubo(operacion, tipo1, tipo2)
		if resType == "x":
			exit("error: type mismatch! Invalid operation lineno : " + str(p.lexer.lineno));
		typep = scopeType(resType);	
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
			opcode = opCode(operacion);
			tempVirtAddress = dataTypeDist(resType, "TEMP");
			cuadruplo = Cuadruplo(opcode, dir1, dir2, tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
			p[0] = tempVirtAddress;
			pilaTipos.push(resType);
			pilaResultados.push(tempVirtAddress);
		else:
			sys.exit("Error, demasiadas variables temporales!")
		
	else:
		p[0] = p[1]
	# print "Exp: " + str(p[0])

def p_Termino(p):
	'''Termino : Termino TIMES bitOp
			| Termino DIVIDE bitOp
			| bitOp'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global pilaResultados
	global pilaTipos
	if len(p) == 4:
		op1 = p[1];
		op2 = p[3];
		tipo1 = pilaTipos.pop()
		tipo2 = pilaTipos.pop()
		dir1 = pilaResultados.pop()
		dir2 = pilaResultados.pop()
		operacion = p[2]
		resType = cubo(operacion, tipo1, tipo2)
		if resType == "x":
			exit("error: type mismatch! Invalid operation lineno : " + str(p.lexer.lineno));
		typep = scopeType(resType);	
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
			opcode = opCode(operacion);
			tempVirtAddress = dataTypeDist(resType, "TEMP");
			cuadruplo = Cuadruplo(opcode, dir1, dir2, tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
			p[0] = tempVirtAddress;
			pilaTipos.push(resType);
			pilaResultados.push(tempVirtAddress);
		else:
			sys.exit("Error, demasiadas variables temporales!")
		
	else:
		p[0] = p[1]
	# print "Termino: " + str(p[0])

def p_bitOp(p):
	'''bitOp : bitOp ORBIT Factor
			| bitOp XORBIT Factor
			| bitOp ANDBIT Factor
			| Factor'''
	global cuadruplos
	global contCuadruplos
	global Counts
	global pilaResultados
	global pilaTipos
	if len(p) == 4:
		op1 = p[1];
		op2 = p[3];
		tipo1 = pilaTipos.pop()
		tipo2 = pilaTipos.pop()
		dir1 = pilaResultados.pop()
		dir2 = pilaResultados.pop()
		operacion = p[2]
		resType = cubo(operacion, tipo1, tipo2)
		if resType == "x":
			exit("error: type mismatch! Invalid operation lineno : " + str(p.lexer.lineno));
		typep = scopeType(resType);	
		counts = Counts[TEMPSCOPE][typep]
		if counts < MAXTEMPS:
			opcode = opCode(operacion);
			tempVirtAddress = dataTypeDist(resType, "TEMP");
			cuadruplo = Cuadruplo(opcode, dir1, dir2, tempVirtAddress);	
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			counts = counts + 1
			Counts[TEMPSCOPE][typep] = counts
			p[0] = tempVirtAddress;
			pilaTipos.push(resType);
			pilaResultados.push(tempVirtAddress);
		else:
			sys.exit("Error, demasiadas variables temporales!")
		
	else:
		p[0] = p[1]
	# print "bitOp: " + str(p[0])

def p_afterMultiArgFUNC(p):
	'''afterMultiArgFUNC : '''
	global Counts
	global cuadruplos
	global contCuadruplos
	global processDir
	global pilaResultados
	global pilaTipos
	global pilamultiarg
	global argCont
	ID = p[-4]
	if functionExist(ID):
		size = pilamultiarg.size()
		# print "multiarg values"
		# for i in range(size):
		# 	print pilamultiarg.items[i]
		sizeDef = len(processDir[ID].paramList)
		if size != sizeDef:
			exit("function received: " + str(size) + " arguments but was expecting: " + str(sizeDef));
		sizeERA = 0
		for i in range(sizeDef):
			sizeERA = sizeERA + typeSize(processDir[ID].paramList[i]);
		sizeERA = sizeERA + processDir[ID].numberOfVars["entero"]*typeSize("entero");
		sizeERA = sizeERA + processDir[ID].numberOfVars["flotante"]*typeSize("flotante");
		sizeERA = sizeERA + processDir[ID].numberOfVars["caracter"]*typeSize("caracter");
		sizeERA = sizeERA + processDir[ID].numberOfVars["cadena"]*typeSize("cadena");
		sizeERA = sizeERA + processDir[ID].numberOfVars["booleano"]*typeSize("booleano");
		cuadruplo = Cuadruplo(opCode("ERA"), sizeERA, "", "");
		cuadruplos.append(cuadruplo);
		contCuadruplos = contCuadruplos + 1;

		cont = -1;
		while not pilamultiarg.isEmpty():
			ResolvedParam = pilamultiarg.pop();
			tipo = pilaTipos.pop()
			tipoDef = processDir[ID].paramList[cont].tipo;
			if tipo != tipoDef:
				exit("param: " + str(size+cont+1) + "was expecting: " + str(tipoDef) + " but argument is: " + str(tipo));
			cont = cont -1;	
			cuadruplo = Cuadruplo(opCode("PARAM"), ResolvedParam, "", size+cont+1);
			cuadruplos.append(cuadruplo);
			contCuadruplos = contCuadruplos + 1;
			beginningDir = processDir[ID].beginningCuad;
		cuadruplo = Cuadruplo(opCode("GOSUB"), ID, "", beginningDir);
		cuadruplos.append(cuadruplo);
		contCuadruplos = contCuadruplos + 1;

		p[0] = processDir[ID].nombre;
		datatype = processDir[ID].tipoRetorno;
		typep = scopeType(datatype)
		counts = Counts[GLOBALSCOPE][typep];
		if counts < MAXGLOBALS:
			tempVirtAddress = dataTypeDist(datatype, "GLOBAL");
			variableGlobal = VariableRecord(ID, datatype, tempVirtAddress);
			processDir[ID].returnGlobalVar = variableGlobal;
			counts = counts + 1;
			Counts[GLOBALSCOPE][typep] = counts;
			pilaTipos.push(datatype)
			pilaResultados.push(tempVirtAddress)
		else:
			exit("too many globals!");
	else:
		exit("error function " + str(ID) + " is not declared!");

def p_Factor(p):
	'''Factor : LPAREN Expresion RPAREN
			| ID LPAREN MULTIARG afterMultiArg afterMultiArgFUNC RPAREN
			| CTE
			| IDoperand'''
	
	if len(p) == 4:
		p[0] = p[2]
		
	elif len(p) == 2:
		p[0] = p[1]

	# print "factor: " + str(p[0])
def p_IDoperand(p):
	'''IDoperand : ID'''
	global pilaTipos
	global pilaResultados
	res = ""
	tipo = ""
	if not IDexist(p[1], localVars):
		mutObj = [p[1],""]; #LIST[0] = ID  LIST[1] = POS
		if not (funcName != "" and programName != funcName and findIDinParamList(mutObj)):
			if not IDexist(p[1], globalVars):
				sys.exit("Error!, trying to operate with " + p[1] + " but it does note exist..")
			else:
				p[0] = globalVars[p[1]].nombre;
				res = globalVars[p[1]].dirVirtual;
				tipo = globalVars[p[1]].tipo;
	 	else:
	 		p[0] = listaParametrica[int(mutObj[1])].nombre;#list item 1 is position of ID found
			res = listaParametrica[int(mutObj[1])].dirVirtual;
			tipo =  listaParametrica[int(mutObj[1])].tipo;
	else:
		p[0] = localVars[p[1]].nombre;
		res = localVars[p[1]].dirVirtual;
		tipo = localVars[p[1]].tipo;

	pilaResultados.push(res);
	pilaTipos.push(tipo);
	#p[0] = p[1]
def p_CTE(p):
	'''CTE : Entero
				| CteFlotante
				| CteCadena
				| CteCaracter
				| CteByte
				| CteBooleano'''
	global Counts
	global pilaResultados
	global pilaTipos
	global tablaConstantes
	op1 = p[1]
	datatype = getType(op1);
	typep = scopeType(datatype);
	counts = Counts[CTESCOPE][typep];
	dir1 = ""
	if counts < MAXCTES:
		dir1 = dataTypeDist(datatype, "CTE");
		constante = ConstantRecord(dir1, datatype, op1);
		tablaConstantes[dir1] = constante;
		counts = counts + 1;
		Counts[CTESCOPE][typep] = counts;
		pilaResultados.push(dir1)
		pilaTipos.push(datatype)
	else:
		exit("too many constant variables!");
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
	# print "variables globales"
	# for ID in globalVars.keys():
	# 	variable = globalVars[ID];
	# 	print "nombre: " + str(variable.nombre) + " tipo: " + str(variable.tipo) + " dirVirtual: " + str(variable.dirVirtual);
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

#Build the parser
import ply.yacc as yacc
def compile():

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
	for dirVirtual in llavesConstantes:
		print "constante " + str(cont+1) + ": " + str(dirVirtual) + ", " + str(tablaConstantes[dirVirtual].tipo) + ", " +\
		str(tablaConstantes[dirVirtual].valor);
		cont = cont + 1
		
	print "lista de cuadruplos"
	cont = 0
	for cuadruplo in cuadruplos:
		print "cuadruplo " + str(cont) + ": " + str(cuadruplo.operacion) + ", " + str(cuadruplo.operando1) + ", " +\
		str(cuadruplo.operando2) + ", " + str(cuadruplo.resultado);
		cont = cont + 1

compile()
