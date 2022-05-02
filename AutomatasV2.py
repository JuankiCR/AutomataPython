from os import listdir
from os.path import isfile, join
import os
RCF = ['','','']
sigma = []
finales = []
filePath = "./files"
estadoAC = ['0']
estadoN = []
inicialDel = True
def loadFiles():
    dirList =  [f for f in listdir(filePath) if isfile(join(filePath, f))]
    return dirList
def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list
def stringValidate(chain, sigma):
    status = True
    if chain == '':
        return False
    for car in chain:
        if (status):
            existe = sigma.count(car)
            if (existe < 1):
                status = False
            else:
                status = True
        else:
            return status
    return status
def fileExtractData(fileName):
    fileDir = filePath+'/'+fileName
    txt = open(fileDir, 'r')
    contenido = txt.read();
    txt.close
    saltos = 0
    FILA = -1
    COLUMNA = 0
    captura = 0
    for i, caracter in enumerate(contenido):
        #Condiciones para primeros 3 renglones
        if (saltos <= 2 and caracter.isnumeric()):
            RCF[saltos] += caracter
        if (saltos <= 2 and (caracter == '\n')):
            saltos += 1
        #Crear matriz
        if (saltos == 3):
            X = int(RCF[1])
            Y = int(RCF[0])
            tablaTran = []
            for i in range(Y):
                a = ['']*X
                tablaTran.append(a)
        #Condiciones Sig
        if (saltos == 3 and caracter == 'S'):
            saltos += 1
        if (saltos == 4 and caracter == '{'):
            saltos += 1
        if (saltos == 5 and caracter != '}'):
            if (caracter != ' ' and caracter != ',' and caracter != '{' and caracter != '\n'):
                sigma.append(caracter)
        if (saltos == 5 and caracter == '}'):
            saltos += 1    
        #Condiciones F
        if (saltos == 6 and caracter == 'F'):
            saltos += 1
        if (saltos == 7 and caracter == '{'):
            saltos += 1
        if (saltos == 8 and caracter != '}'):
            if (caracter.isnumeric()):
                finales.append(caracter)
        if (saltos == 8 and caracter == '}'):
            saltos += 1
        #Condiciones tabla de transiciones
        if (saltos == 9):
            if (caracter == '>'):
                captura = 1
                FILA += 1
                COLUMNA = 0
            if (caracter == '|'):
                COLUMNA += 1
            if (caracter == ','):
                captura = 0
            if (captura == 1 and caracter != '>' and caracter != ' ' and caracter != '|' and caracter != ',' and caracter != '}' and caracter != '\n'):
                tablaTran[FILA][COLUMNA] = tablaTran[FILA][COLUMNA]+caracter 
            if (captura == 1 and (caracter == 'N' or caracter == 'U' or caracter == 'L')):
                tablaTran[FILA][COLUMNA] = ''
    return tablaTran
def evTransicion(posSigma, estadosEntrada, inicialDel):
    estadosResultado = []
    estadosPosibles = []
    Del = inicialDel
    for estado in estadoAC:
        estadosPosibles = Union(estadosPosibles, tablaTran[int(estado)][posSigma])
    if Del:
        for estado in estadosEntrada:
            estadoAC.remove(estado)
        Del = False
    for c in estadosPosibles:
        estadosResultado.append(c)
        estadosResultado = Union(estadoAC, estadosResultado)
    return estadosResultado
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
programState = True
files = loadFiles()
cfiles = len(files)
while programState != False:
    clearConsole()
    fileNum = 0
    fileCol = {}
    cadena = ''
    print("Archivos encontrados:")
    for fileItem in files:
        fileNum += 1
        print(f"{fileNum}.- {fileItem}") 
        fileCol[fileNum] = fileItem
    print("0.- Salir")
    fileSelected = int(input("Seleccione un archivo: "))
    if fileSelected == 0:
        programState = False
        print('Saliendo del programa :v/')
    elif fileSelected <= cfiles and fileSelected > 0:
        print('Archivo seleccionado: ',fileCol[fileSelected])
        tablaTran = fileExtractData(fileCol[fileSelected])
        print("Sigma =", sigma)
        cadena = input('Ingrese la cadena a evaluar: ')
        if (stringValidate(cadena,sigma)):
            print('Cadena valido')
            for c in cadena:
                inicialDel = True
                estadoAC = evTransicion(sigma.index(c), estadoAC, inicialDel)
                print('lengtEsta =',estadoAC)
            strEstados = ''
            for elemento in estadoAC:
                strEstados += elemento
            print('estados finales: ',strEstados,'varFinales',finales)
            cadenaValida = False
            for c in strEstados:
                if (finales.count(c) > 0):
                    cadenaValida = True
                    break
                else :
                    cadenaValida = False
            if (cadenaValida):
                print('Cadena aceptada')
            else:
                print('Cadena no aceptada')
        else:
            print('Cadena no valida')

        # print("RCF", RCF)
        # print("Sigma", sigma)
        # print("Finales", finales)
        # print("Tabla", tablaTran)
            
        RCF = ['','','']
        estadoAC = ['0']
        estadoN = []
        sigma = []
        finales = []
        tablaTran = []
        inicialDel = True
        input("Presione enter para continuar...")
    else:
        print('Opción no valida :c')
        input("Presione enter para continuar...")