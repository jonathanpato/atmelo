cuboSemantico = [ [ [ 'x' for i in range(8) ] for j in range(5) ] for k in range(5) ]

cuboSemantico[0][0][0] = 'int'; #E + E = E
cuboSemantico[0][0][1] = 'int'; #E - E = E
cuboSemantico[0][0][2] = 'int'; #E * E = E  
cuboSemantico[0][0][3] = 'int'; #//E / E = E
    
cuboSemantico[0][1][0] = 'float'; #//E + F = F
cuboSemantico[1][0][0] = 'float'; #//F + E = F
cuboSemantico[1][1][0] = 'float'; #//F + F = F

cuboSemantico[0][1][1] = 'float'; #//E - F = F
cuboSemantico[1][0][1] = 'float'; #//F - E = F
cuboSemantico[1][1][1] = 'float'; #//F - F = F

cuboSemantico[0][1][2] = 'float'; #//E * F = F
cuboSemantico[1][0][2] = 'float'; #//F * E = F
cuboSemantico[1][1][2] = 'float'; #//F * F = F

cuboSemantico[0][1][3] = 'float'; #//E / F = F
cuboSemantico[1][0][3] = 'float'; #//F / E = F
cuboSemantico[1][1][3] = 'float'; #//F / F = F

cuboSemantico[2][2][4] = 'bool'; #//B < B = B
cuboSemantico[2][2][5] = 'bool'; #//B > B = B
cuboSemantico[2][2][6] = 'bool'; #//B equal B = B
cuboSemantico[2][2][7] = 'bool'; #//B not B = B

def cubo(operando1, operando2, operador): #si regresa 'x' es error
#si no regresa e de entero
# f de flotante
# b de booleano
    indice1 = 0
    indice2 = 0
    indiceoper = 0
    if(type(operando1) is int):
        indice1 = 0
    elif(type(operando1) is float):
        indice1 = 1
    elif(type(operando1) is bool):
        indice1 = 2
    
    if(type(operando2) is int):
        indice2 = 0
    elif(type(operando2) is float):
        indice2 = 1
    elif(type(operando2) is bool):
        indice2 = 2
        
 
        
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
        
    return cuboSemantico[indice1][indice2][indiceoper];
    