import math
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

def crear_indice_concatenado(terminos,codificacion=None):
    #Ver para codificaciones
    if codificacion == 'u':
        terminos = list(map(doc_num_to_unary,terminos))
    elif codificacion == 'g':
        terminos = list(map(doc_num_to_gamma,terminos))
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

def num_to_unary(num):
    return "0"*(int(num)-1)+"1"

def doc_num_to_unary(documentos):
    """123->101001"""
    doc_in_unary = ""
    for doc_numbers in documentos:
        doc_in_unary += num_to_unary(doc_numbers)
    return doc_in_unary

def doc_num_to_gamma(documentos):
    doc_in_gamma = ""
    for doc_numbers in documentos:
        floor_log_2_n = math.floor(math.log2(int(doc_numbers)))
        doc_in_gamma += num_to_unary(str(floor_log_2_n+1))
        if int(doc_numbers)>1:
            extend_binary = "0"*floor_log_2_n + "{0:b}".format(int(doc_numbers)-2**floor_log_2_n)
            doc_in_gamma += extend_binary[-floor_log_2_n:]
    return doc_in_gamma

def distancias_documentos(lista_documento):
    distancia = ""
    num_doc_actual=0
    for i in range(len(lista_documento)):
        if i == 0:
            distancia += lista_documento[0]
        else:
            diferencia = int(lista_documento[i])-num_doc_actual
            distancia += str(diferencia)
        num_doc_actual = int(lista_documento[i])
    return distancia    

def crear_indice_distancias(documentos,codificacion):
    documentos_en_distancia = []
    for lista_documento in documentos:
        documentos_en_distancia.append(distancias_documentos(lista_documento))
    return crear_indice_concatenado(documentos_en_distancia,codificacion)

def crear_indice_documentos(documentos,modo='c',codificacion=None):
    if modo =='c':
        indice_documentos = crear_indice_concatenado(documentos,codificacion)
    elif modo == 'd':
        indice_documentos = crear_indice_distancias(documentos,codificacion)
    return indice_documentos

def print_indice_documentos(indice_documento):
    print_indice(indice_documento)

def generar_indice_invertido(palabras_documentos,modo_lexico='c',codificacion=None,distancia_docs=False):
    terminos = list(palabras_documentos.keys())
    documentos = list(palabras_documentos.values())
    lexico = crear_lexico(terminos,modo_lexico)
    modo_docs = 'c'
    if distancia_docs == True:
        modo_docs = 'd' 
    indice_doc = crear_indice_documentos(documentos,modo_docs,codificacion)
    
    print("Lexico")
    if modo_lexico in ['fc','fcp']:
        print_lexico_front_coding(lexico)
    elif modo_lexico == 'c':
        print_lexico(lexico)
    print("\nDocumentos")
    print_indice_documentos(indice_doc)    

"""Markdown"""
def print_markdown_lexico_front_coding(lexico):
    iguales,distintos,indice,front_coding_terminos = lexico
    print("| iguales | distintos | punteros terminos |")
    print("| -------- | -------- | -------- |")
    if not(len(iguales) == len(distintos) and len(distintos) == len(indice)):
        return
    for i in range(len(iguales)):
        print(f"| {iguales[i]} | {distintos[i]} | {indice[i]} |")
    print()
    print_indice_markdown((indice,front_coding_terminos))

def print_indice_markdown(lexico):
    """Dado una tupla de indice y terminos imprime el índice de léxicos de forma legible"""
    indice,terminos = lexico
    #cabecera
    print("|",end="")
    for termino in terminos:
        print(f" {termino} ",end="|")
    print()
    #entrecabecera
    print("|",end="")
    for termino in terminos:
        print(f" {'-'*len(termino)} ",end="|")
    posicion = 0
    print()
    #Contenido

    print("|",end="")
    for i in range(len(indice)):
        print(f" {indice[i]} ",end="|")

def print_markdown_documentos(documentos):
    print_indice_markdown(documentos)

def print_markdown_indice_invertido(lexico,documentos):
    if len(lexico)==4:
        iguales,distintos,indice,front_coding_terminos = lexico
        indice_documentos,num_documentos = documentos
        print("| iguales | distintos | punteros terminos | punteros documentos |")
        print("| -------- | -------- | -------- | -------- |")
        if not(len(iguales) == len(distintos) and len(distintos) == len(indice)):
            return
        for i in range(len(iguales)):
            print(f"| {iguales[i]} | {distintos[i]} | {indice[i]} | {indice_documentos[i]} |")
        print()
        print_indice_markdown((indice,front_coding_terminos))
        print()
        print()
        print_indice_markdown(documentos)
    if len(lexico)==2:
        indice,terminos = lexico
        indice_documentos,num_documentos = documentos
        print("| punteros terminos | punteros documentos |")
        print("| -------- | -------- |")
        if not(len(indice) == len(indice_documentos)):
            return
        for i in range(len(indice)):
            print(f"| {indice[i]} | {indice_documentos[i]} |")
        print()
        print_indice_markdown((indice,terminos))
        print()
        print()
        print_indice_markdown(documentos)

def print_markdown_indice_invertido_indexado(lexico,documentos):
    if len(lexico)==4:
        iguales,distintos,indice,front_coding_terminos = lexico
        indice_documentos,num_documentos = documentos
        print("| posicion | iguales | distintos | punteros terminos | punteros documentos |")
        print("| -------- | -------- | -------- | -------- | -------- |")
        if not(len(iguales) == len(distintos) and len(distintos) == len(indice)):
            return
        for i in range(len(iguales)):
            print(f"| {i } | {iguales[i]} | {distintos[i]} | {indice[i]} | {indice_documentos[i]} |")
        print()
        print_indice_markdown((indice,front_coding_terminos))
        print()
        print()
        print_indice_markdown(documentos)
    if len(lexico)==2:
        indice,terminos = lexico
        indice_documentos,num_documentos = documentos
        print("| posicion | punteros terminos | punteros documentos |")
        print("| -------- | -------- | -------- |")
        if not(len(indice) == len(indice_documentos)):
            return
        for i in range(len(indice)):
            print(f"| {i}|{indice[i]} | {indice_documentos[i]} |")
        print()
        print_indice_markdown((indice,terminos))
        print()
        print()
        print_indice_markdown(documentos)
def separar_segun_indice_markdown(texto,indice):
    texto_separado_markdown = ""
    posicion_indice = 0
    for i in range(len(texto)):
        if posicion_indice < len(indice) and i == indice[posicion_indice]:
            texto_separado_markdown += " | "
            posicion_indice += 1
        texto_separado_markdown += texto[i]
    texto_separado_markdown += " | "
    return texto_separado_markdown

def funcion_tf_idf(termino,numero_doc,documentos_contenido,b):
    tfi = 0
    palabras_documento_i = documentos_contenido.get(numero_doc,"")
    for palabra_doc_i in palabras_documento_i.split(" "):
        if termino == palabra_doc_i:
            tfi += 1
    if b:
        largo_doc_j = len(documentos_contenido.get(numero_doc,"").split(" "))
        largos_documentos = [len(contenido_documento.split(" ")) for contenido_documento in documentos_contenido.values()]
        avdl = sum(largos_documentos)/len(documentos_contenido)
        normalizacion = (1-b+b*((largo_doc_j)/avdl))
        #print(f"Largo doc {numero_doc}: {largo_doc_j}")
        return round(tfi/normalizacion,2)
    return tfi

def funcion_bm25(termino,numero_doc,documentos_contenido,k,b):
    if k is None:
        return -1
    tfi = funcion_tf_idf(termino,numero_doc,documentos_contenido,None)
    if b:
        largo_doc_j = len(documentos_contenido.get(numero_doc,"").split(" "))
        largos_documentos = [len(contenido_documento.split(" ")) for contenido_documento in documentos_contenido.values()]
        avdl = sum(largos_documentos)/len(documentos_contenido)
        normalizacion = (1-b+b*((largo_doc_j)/avdl))
        return round((k+1)*tfi/(tfi+k*normalizacion),2)
    return (k+1)*tfi/(tfi+k)


def print_markdown_tabla_tf_idf(palabras_documentos,documentos_contenido,modo="tf-idf",k=None,b=None):
    print(f"| terminos |",end="")
    existing_docs = []
    for documents in palabras_documentos.values():
        for num_doc in documents:
            if int(num_doc) not in existing_docs:
                existing_docs.append(int(num_doc))
    existing_docs.sort()
    for num_doc in existing_docs:
        print(f" {num_doc} |",end="")
    print(f"  Log((N+1)/fti)|")
    print("|",end="")
    for i in range(len(existing_docs)+2):
        print(" --- |",end="")
    print()
    big_n = len(existing_docs)
    for word,documents in palabras_documentos.items():
        print(f"| {word} |",end="")
        tf_terminos = 0
        for doc_record in existing_docs:
            if modo == "tf-idf":
                tfi = funcion_tf_idf(word,str(doc_record),documentos_contenido,b)
            elif modo == "bm25":
                tfi = funcion_bm25(word,str(doc_record),documentos_contenido,k,b)
            print(f" {tfi} |",end="")
            if tfi >0:
                tf_terminos += 1
        if tf_terminos >0: print(f"Log({big_n+1}/{tf_terminos}):{round(math.log10((big_n+1)/tf_terminos),2)} |")
        else : print(0)
