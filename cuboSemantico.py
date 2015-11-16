import re

cuboSemantico = [ [ [ 'x' for i in range(15) ] for j in range(5) ] for k in range(5) ]

cuboSemantico[0][0][0] = 'entero'; #E + E = E
cuboSemantico[0][0][1] = 'entero'; #E - E = E
cuboSemantico[0][0][2] = 'entero'; #E * E = E  
cuboSemantico[0][0][3] = 'entero'; #//E / E = E
cuboSemantico[0][0][4] = 'booleano'; #//B < B = B
cuboSemantico[0][0][5] = 'booleano'; #//B > B = B

cuboSemantico[1][1][0] = 'flotante'; #//F + F = F
cuboSemantico[1][1][1] = 'flotante'; #//F - F = F
cuboSemantico[1][1][2] = 'flotante'; #//F * F = F
cuboSemantico[1][1][3] = 'flotante'; #//F / F = F
cuboSemantico[1][1][4] = 'booleano'; #//B < B = B
cuboSemantico[1][1][5] = 'booleano'; #//B > B = B

cuboSemantico[2][2][6] = 'booleano'; #//B igualque B = B
cuboSemantico[2][2][7] = 'booleano'; #//B diferentede B = B
cuboSemantico[2][2][8] = 'booleano'; #//B menorigualque B = B
cuboSemantico[2][2][9] = 'booleano'; #//B mayorigualque B = B
cuboSemantico[2][2][13] = 'booleano'; #//B and B = B
cuboSemantico[2][2][14] = 'booleano'; #//B or B = B

cuboSemantico[3][3][0] = 'byte'; #Byte + Byte = Byte
cuboSemantico[3][3][1] = 'byte'; #Byte - Byte = Byte
cuboSemantico[3][3][2] = 'byte'; #Byte * Byte = Byte
cuboSemantico[3][3][3] = 'byte'; #Byte / Byte = Byte
cuboSemantico[3][3][10] = 'byte'; #Byte orbit Byte = Byte
cuboSemantico[3][3][11] = 'byte'; #Byte xorbit Byte = Byte
cuboSemantico[3][3][12] = 'byte'; #Byte andbit Byte = Byte

cuboSemantico[4][4][0] = 'caracter'; #Cadena + Cadena = Cadena
cuboSemantico[4][4][1] = 'caracter'; #Cadena - Cadena = Cadena

# cuboSemantico[5][5][0] = 'cadena'; 
# cuboSemantico[5][5][1] = 'cadena'; 
# cuboSemantico[5][5][2] = 'cadena'; 
# cuboSemantico[5][5][3] = 'cadena'; 

def getType(dato):
    tipo = ""
    dato = str(dato)
    if re.search(r'[0-1]{8}B', dato):
        tipo = "byte"
    elif re.search(r'\'(\\?.)?\'', dato):
        tipo = "caracter"
    elif re.search(r'\"[^\"]*\"', dato):
        tipo = "cadena"
    elif re.search(r'[0-9]+\.[0-9]+', dato):
        tipo = "flotante"
    elif re.search(r'True|False', dato):
        tipo = "booleano"
    elif re.search('[0-9a-fA-F]+H', dato) or re.search('[0-9]+', dato):
        tipo = "entero"
    else:
        tipo = "ninguno"
    return tipo

def cubo(operador, operando1, operando2): #si regresa 'x' es error
#si no regresa e de entero
# f de flotante
# b de booleano
    indice1 = 0
    indice2 = 0
    indiceoper = 0
    operando1 = str(operando1)
    operando2 = str(operando2)
    
    if operando1 == "entero":
        indice1 = 0
    elif operando1 == "flotante":
        indice1 = 1
    elif operando1 == "booleano":
        indice1 = 2
    elif operando1 == "byte": #byte
        indice1 = 3
    elif operando1 == "caracter": #caracter
        indice1 = 4
    else:
        strOp1 = getType(operando1);  
        if strOp1 == "entero":
            indice1 = 0
        elif strOp1 == "flotante":
            indice1 = 1
        elif strOp1 == "booleano":
            indice1 = 2
        elif strOp1 == "byte": #byte
            indice1 = 3
        elif strOp1 == "caracter": #caracter
            indice1 = 4
    
    if operando2 == "entero":
        indice2 = 0
    elif operando2 == "flotante":
        indice2 = 1
    elif operando2 == "booleano":
        indice2 = 2
    elif operando2 == "byte": #byte
        indice2 = 3
    elif operando2 == "caracter": #caracter
        indice2 = 4
    else:
        strOp2 = getType(operando2);
        if operando2 == "entero":
            indice2 = 0
        elif operando2 == "flotante":
            indice2 = 1
        elif operando2 == "booleano":
            indice2 = 2
        elif operando2 == "byte": #byte
            indice2 = 3
        elif operando2 == "caracter": #caracter
            indice2 = 4
 
        
    if(operador == '+'):
        indiceoper = 0
    elif(operador == '-'):
        indiceoper = 1
    elif(operador == '*'):
        indiceoper = 2
    elif(operador == '/'):
        indiceoper = 3
    elif(operador == '<'):
        indiceoper = 4
    elif(operador == '>'):
        indiceoper = 5
    elif(operador == "igualque"):
        indiceoper = 6
    elif(operador == "diferentede"):
        indiceoper = 7
    elif(operador == "menorigualque"):
        indiceoper = 8
    elif(operador == "mayorigualque"):
        indiceoper = 9
    elif(operador == "orbit"):
        indiceoper = 10
    elif(operador == "xorbit"):
        indiceoper = 11
    elif(operador == "andbit"):
        indiceoper = 12
    elif(operador == "and"):
        indiceoper = 13
    elif(operador == "or"):
        indiceoper = 14
        
    return cuboSemantico[indice1][indice2][indiceoper];
    