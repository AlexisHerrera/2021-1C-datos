def iguales_anterior(anterior,posterior):
    iguales = 0
    for i in range(min(len(anterior),len(posterior))):
        if posterior[i] == anterior[i]:
            iguales +=1
        else: 
            break
    return iguales

def crear_lexico_concatenado(terminos):
    """
    Crear lexico recibe una lista de palabras y devuelve una tupla de listas.
    La primera es el índice de punteros a los terminos concatenados y la segunda son los términos concatenados.
    """
    return crear_indice_concatenado(terminos)

def crear_lexico_front_coding(terminos,n=None):
    if n ==None:
        n=len(terminos)
    ultima_palabra = None
    indice = [0]
    iguales = []
    distintos = []
    front_coding_terminos = []
    indice_actual = 0
    len_anterior = 0
    for termino in terminos:
        if not(indice_actual%n):
            iguales.append(0)
            distintos.append(len(termino))
            front_coding_terminos.append(termino)
        else:
            igual_anterior = iguales_anterior(ultima_palabra,termino)
            iguales.append(igual_anterior)
            distintos.append(len(termino)-igual_anterior)
            front_coding_terminos.append(termino[igual_anterior:])
        if indice_actual != 0:
            indice.append(indice[indice_actual-1]+distintos[indice_actual-1])
        indice_actual += 1
        len_anterior += len(termino)
        ultima_palabra = termino
    lexico = iguales,distintos,indice,front_coding_terminos
    return lexico

def crear_lexico(terminos,modo='c',n=None):
    """
    Crear lexico recibe una lista de palabras y devuelve una tupla de listas.
    La primera es el índice de punteros a los terminos concatenados y la segunda son los términos concatenados.
    """ 
    terminos.sort()
    indice = [0]
    len_anterior = 0
    if modo == 'c':
        return crear_lexico_concatenado(terminos)
    elif modo == 'fc':
        return crear_lexico_front_coding(terminos)
    elif modo == 'fcp':
        return crear_lexico_front_coding(terminos,n)

def print_lexico(lexico):
    print_indice(lexico)

def print_lexico_front_coding(lexico):
    iguales,distintos,indice,front_coding_terminos = lexico
    print("i|d|p")
    if not(len(iguales) == len(distintos) and len(distintos) == len(indice)):
        return
    for i in range(len(iguales)):
        print(f"{iguales[i]}|{distintos[i]}|{indice[i]}")
    print_lexico((indice,front_coding_terminos))

def crear_indice_concatenado(terminos):
    indice = [0]
    len_anterior = 0
    for termino in terminos:
        indice.append(len(termino)+len_anterior)
        len_anterior += len(termino)
    indice.pop()
    lexico = indice,terminos
    return lexico

def print_indice(lexico):
    """Dado una tupla de indice y terminos imprime el índice de léxicos de forma legible"""
    indice,terminos = lexico
    for termino in terminos:
        print(termino,end=" ")
    print()
    posicion = 0
    for i in range(len(indice)):
        largo_espacios = len(terminos[posicion])
        if len(str(indice[i]))>1: #solo funciona hasta indices <100 :sad:
            largo_espacios -= len(str(indice[i]))-1
        print(indice[i],end=" "*largo_espacios)
        posicion += 1
def crear_indice_distancias(documentos):
    documentos_en_distancia = []
    for lista_documento in documentos:
        distancia = ""
        num_doc_actual=0
        for i in range(len(lista_documento)):
            if i == 0:
                distancia += lista_documento[0]
            else:
                diferencia = int(lista_documento[i])-num_doc_actual
                distancia += str(diferencia)
            num_doc_actual += int(lista_documento[i])
        documentos_en_distancia.append(distancia)
    return crear_indice_concatenado(documentos_en_distancia)

def crear_indice_documentos(documentos,modo='c'):
    if modo =='c':
        indice_documentos = crear_indice_concatenado(documentos)
    elif modo == 'd':
        indice_documentos = crear_indice_distancias(documentos)
    return indice_documentos

def print_indice_documentos(indice_documento):
    print_indice(indice_documento)