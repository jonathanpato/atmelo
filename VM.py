#13 "escribepuerto"
#14  "leepuerto"
#15 "printf"
#16 "return"
#17 "GOTO"
#18 "GOTOF"
#19 "GOTOT"
#23
#24 " "

import atmelo
atmelo.compile()
class Instruction:
    def __init__(self,operacion, operando1, operando2, resultado):
        self.operacion = operacion
        self.operando1 = operando1
        self.operando2 = operando2
        self.resultado = resultado

#variables
diccionarioVariables={}
operacionC = 0
cuadruplos = atmelo.cuadruplos
contVariablesT = 0
contVariablesA = 0

print ("#include <avr/io.h>")
print ("#include <util/delay.h>")
for i in range(len(atmelo.cuadruplos)):
    operacionC = atmelo.getopCode(atmelo.cuadruplos[i].operacion)
    
    if (atmelo.cuadruplos[i].operacion == 1 or atmelo.cuadruplos[i].operacion == 2 or atmelo.cuadruplos[i].operacion == 3 or\
    atmelo.cuadruplos[i].operacion == 4 or atmelo.cuadruplos[i].operacion == 5 or atmelo.cuadruplos[i].operacion == 6 or\
    atmelo.cuadruplos[i].operacion == 7 or atmelo.cuadruplos[i].operacion == 8 or atmelo.cuadruplos[i].operacion == 9 or\
    atmelo.cuadruplos[i].operacion == 10 or atmelo.cuadruplos[i].operacion == 11 or atmelo.cuadruplos[i].operacion == 12 or\
    atmelo.cuadruplos[i].operacion == 21 or atmelo.cuadruplos[i].operacion == 22):
        if (atmelo.cuadruplos[i].resultado >= 47800 and atmelo.cuadruplos[i].resultado < 71800):
            if (not(atmelo.cuadruplos[i].resultado in diccionarioVariables.keys())):
                diccionarioVariables[atmelo.cuadruplos[i].resultado] = "T_"+str(contVariablesT)
                if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="entero"):
                    print ("int " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
                if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="flotante"):
                    print ("double " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
                if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="cadena"):
                    print ("String " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
                if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="caracter"):
                    print ("char " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
                if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="byte"):
                    print ("unsigned char " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
                if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="booleano"):
                    print ("unsigned char " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
                contVariablesT += 1
                
        print diccionarioVariables[atmelo.cuadruplos[i].resultado] + " = " ,
        if(atmelo.cuadruplos[i].operando1>=71800):
            print str(atmelo.tablaConstantes[atmelo.cuadruplos[i].operando1].valor),
        else: 
            print diccionarioVariables[atmelo.cuadruplos[i].operando1],
            
        print operacionC + " ",   

        if(atmelo.cuadruplos[i].operando2>=71800):
            print(str(atmelo.tablaConstantes[atmelo.cuadruplos[i].operando2].valor) + ";")
        else: 
            print(diccionarioVariables[cuadruplos[i].operando2] + ";")
            



         
            
    elif atmelo.cuadruplos[i].operacion == 15:
        print "printf(\"",
        
        if ((atmelo.cuadruplos[i].operando1>=1000 and atmelo.cuadruplos[i].operando1<4800) or\
        (atmelo.cuadruplos[i].operando1>=23800 and atmelo.cuadruplos[i].operando1<27800) or\
        (atmelo.cuadruplos[i].operando1>=47800 and atmelo.cuadruplos[i].operando1<51800) or\
        (atmelo.cuadruplos[i].operando1>=71800 and atmelo.cuadruplos[i].operando1<75800)):
            print "%i\",",
            
        if ((atmelo.cuadruplos[i].operando1>=4800 and atmelo.cuadruplos[i].operando1<8600) or\
        (atmelo.cuadruplos[i].operando1>=27800 and atmelo.cuadruplos[i].operando1<31800) or\
        (atmelo.cuadruplos[i].operando1>=51800 and atmelo.cuadruplos[i].operando1<55800) or\
        (atmelo.cuadruplos[i].operando1>=75800 and atmelo.cuadruplos[i].operando1<79800)):
            print "%f\",",
        if ((atmelo.cuadruplos[i].operando1>=8600 and atmelo.cuadruplos[i].operando1<12400) or\
        (atmelo.cuadruplos[i].operando1>=31800 and atmelo.cuadruplos[i].operando1<35800) or\
        (atmelo.cuadruplos[i].operando1>=55800 and atmelo.cuadruplos[i].operando1<59800) or\
        (atmelo.cuadruplos[i].operando1>=79800 and atmelo.cuadruplos[i].operando1<83800)):
            print "%s\",",
        if ((atmelo.cuadruplos[i].operando1>=12400 and atmelo.cuadruplos[i].operando1<16200) or\
        (atmelo.cuadruplos[i].operando1>=23800 and atmelo.cuadruplos[i].operando1<27800) or\
        (atmelo.cuadruplos[i].operando1>=47800 and atmelo.cuadruplos[i].operando1<51800) or\
        (atmelo.cuadruplos[i].operando1>=71800 and atmelo.cuadruplos[i].operando1<75800)):
            print "%c\",",
        
        if ((atmelo.cuadruplos[i].operando1>=71800 and atmelo.cuadruplos[i].operando1<75800) or\
        (atmelo.cuadruplos[i].operando1>=75800 and atmelo.cuadruplos[i].operando1<79800) or\
        (atmelo.cuadruplos[i].operando1>=79800 and atmelo.cuadruplos[i].operando1<83800) or\
        (atmelo.cuadruplos[i].operando1>=83800 and atmelo.cuadruplos[i].operando1<87800)):    
            print str(atmelo.tablaConstantes[atmelo.cuadruplos[i].operando1].valor) + ");",
        else:
            print  diccionarioVariables[atmelo.cuadruplos[i].operando1] + ");",
            
   
   
   
    elif atmelo.cuadruplos[i].operacion == 20:
        
        if (not(atmelo.cuadruplos[i].resultado in diccionarioVariables.keys())):
            diccionarioVariables[atmelo.cuadruplos[i].resultado] = "A_"+str(contVariablesA)
            
            if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="entero"):
                print ("int " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
            if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="flotante"):
                print ("double " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
            if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="cadena"):
                print ("String " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
            if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="caracter"):
                print ("char " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
            if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="byte"):
                print ("unsigned char " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
            if(atmelo.getTypeFromDir(atmelo.cuadruplos[i].resultado)=="booleano"):
                print ("unsigned char " + diccionarioVariables[atmelo.cuadruplos[i].resultado] + ";")
            contVariablesA += 1
            
        print diccionarioVariables[atmelo.cuadruplos[i].resultado] + " = ",
        
        if(atmelo.cuadruplos[i].operando1>=71800):
            print(str(atmelo.tablaConstantes[atmelo.cuadruplos[i].operando1].valor) + ";")
        else:
            print(diccionarioVariables[atmelo.cuadruplos[i].operando1] + ";")


