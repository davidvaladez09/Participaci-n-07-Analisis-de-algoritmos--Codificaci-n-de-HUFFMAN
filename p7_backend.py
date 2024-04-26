# Desarrollado por David Valadez Gutierrez
import heapq
import os

# Clase para crear los nodos del arbol de huffman
class NodoHuffman:
    # Constructor para definir los nodos
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# Funcion que cuenta los caracteres repetidos
def contar_caracteres(archivo):
    with open(archivo, 'r', encoding='utf-8') as file_open:
        texto = file_open.read() # Abre el archivo de texto
        contador = {} # Diccionario para almacenar los caracteres repetidos

        # Contar los caracteres repetidos
        for caracter in texto:
            if caracter in contador:
                contador[caracter] += 1
            else:
                contador[caracter] = 1
        # Retorna el diccionario de caracteres repetidos
        return contador

# Funcion para generar el arbol de huffman
def crear_arbol_huffman(contador): # Recibe como parametro el dicionario de caracteres repetidos
    heap = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in contador.items()] # Se identifica el caracter que mas se repite
    heapq.heapify(heap) # Se coloca el caracter que mas se repite al inicio del arbol
    
    # Crea el arbol comparando la cabeza del arbol
    while len(heap) > 1:
        nodo_izquierda = heapq.heappop(heap)
        nodo_derecha = heapq.heappop(heap)

        nodo_combinado = NodoHuffman(None, nodo_izquierda.frecuencia + nodo_derecha.frecuencia)
        nodo_combinado.izquierda = nodo_izquierda
        nodo_combinado.derecha = nodo_derecha

        heapq.heappush(heap, nodo_combinado)
    
    return heap[0]

# Funcion para genera la tabla de codigos
def crear_tabla_codigos(arbol_huffman, prefijo='', tabla_codigos={}):
    if arbol_huffman.caracter is not None:
        tabla_codigos[arbol_huffman.caracter] = prefijo
    else:
        crear_tabla_codigos(arbol_huffman.izquierda, prefijo + '0', tabla_codigos)
        crear_tabla_codigos(arbol_huffman.derecha, prefijo + '1', tabla_codigos)
    
    return tabla_codigos

# Funcion para comprimir el archivo
def comprimir_archivo(archivo, tabla_codigos):
    nombre_archivo_comprimido = archivo + '.bin' # Crea el nombre del archivo
    
    with open(archivo, 'r', encoding='utf-8') as entrada, open(nombre_archivo_comprimido, 'wb') as salida:
        bit_acumulado = ''
        while True:
            caracter = entrada.read(1)
            if not caracter:
                break

            # Busca su codigo Huffman correspondiente en la tabla de codigos
            bit_acumulado += tabla_codigos[caracter]
            while len(bit_acumulado) >= 8: # comprueba si hay al menos 8 bits 
                # Convierte los primeros 8 bits a un entero y escribe ese byte en el archivo de salida
                byte = int(bit_acumulado[:8], 2)
                salida.write(bytes([byte]))
                bit_acumulado = bit_acumulado[8:]
        
        # Repite este proceso hasta que se haya leido todo el archivo de entrada
        if bit_acumulado:
            byte = int(bit_acumulado + '0' * (8 - len(bit_acumulado)), 2)
            salida.write(bytes([byte]))

    return nombre_archivo_comprimido

# Funcion para descomprimir el archivo con extension .bin
def descomprimir_archivo(archivo_comprimido, arbol_huffman):
    nombre_archivo_descomprimido = "D:/Documentos/8vo/Analisis de Algoritmos/Actividades/practica7/Participaci-n-07-Analisis-de-algoritmos--Codificaci-n-de-HUFFMAN/descomprimido.txt"

    with open(archivo_comprimido, 'rb') as entrada, open(nombre_archivo_descomprimido, 'w', encoding='utf-8') as salida:
        bit_acumulado = ''
        byte = entrada.read(1)
        # Leer el archivo byte por byte
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')  # Convertir el byte a una cadena de bits de longitud fija
            bit_acumulado += bits
            byte = entrada.read(1)
        
        # Se toma el arbol de Huffman creado
        nodo_actual = arbol_huffman
        # Recorre los nodos del arbol de acuerdo con los bits en bit_acumulado
        for bit in bit_acumulado:
            if bit == '0':
                nodo_actual = nodo_actual.izquierda
            else:
                nodo_actual = nodo_actual.derecha

            if nodo_actual.caracter is not None:
                salida.write(nodo_actual.caracter)
                nodo_actual = arbol_huffman

    return nombre_archivo_descomprimido


# Archivo de entrada
archivo = "D:/Documentos/8vo/Analisis de Algoritmos/Actividades/practica7/Participaci-n-07-Analisis-de-algoritmos--Codificaci-n-de-HUFFMAN/Gullivers_Travels.txt"

# Cuenta los caracteres
no_caracteres = contar_caracteres(archivo)
# Crea el arbol de huffman con los caracteres repetidos contados
arbol_huffman = crear_arbol_huffman(no_caracteres)
# Generar tabla de códigos Huffman
tabla_codigos = crear_tabla_codigos(arbol_huffman)
# Comprimir el archivo
nombre_archivo_comprimido = comprimir_archivo(archivo, tabla_codigos)

print("Archivo comprimido como:", nombre_archivo_comprimido)

# Descomprimir el archivo
archivo_descomprimido = descomprimir_archivo(nombre_archivo_comprimido, arbol_huffman)

print("Archivo descomprimido como:", archivo_descomprimido)
