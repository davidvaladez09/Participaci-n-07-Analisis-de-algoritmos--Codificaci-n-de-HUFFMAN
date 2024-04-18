import heapq
import os

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def contar_caracteres(archivo):
    with open(archivo, 'r', encoding='utf-8') as file_open:
        texto = file_open.read()
        contador = {}

        # Contar los caracteres repetidos
        for caracter in texto:
            if caracter in contador:
                contador[caracter] += 1
            else:
                contador[caracter] = 1

        return contador

def construir_arbol_huffman(conteo):
    heap = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in conteo.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        nodo_izquierda = heapq.heappop(heap)
        nodo_derecha = heapq.heappop(heap)

        nodo_combinado = NodoHuffman(None, nodo_izquierda.frecuencia + nodo_derecha.frecuencia)
        nodo_combinado.izquierda = nodo_izquierda
        nodo_combinado.derecha = nodo_derecha

        heapq.heappush(heap, nodo_combinado)
    
    return heap[0]

def generar_tabla_codigos(arbol_huffman, prefijo='', tabla_codigos={}):
    if arbol_huffman.caracter is not None:
        tabla_codigos[arbol_huffman.caracter] = prefijo
    else:
        generar_tabla_codigos(arbol_huffman.izquierda, prefijo + '0', tabla_codigos)
        generar_tabla_codigos(arbol_huffman.derecha, prefijo + '1', tabla_codigos)
    return tabla_codigos

def comprimir_archivo(archivo, tabla_codigos):
    nombre_archivo_comprimido = archivo + '.huffman'
    
    with open(archivo, 'r', encoding='utf-8') as entrada, open(nombre_archivo_comprimido, 'wb') as salida:
        bit_acumulado = ''
        while True:
            caracter = entrada.read(1)
            if not caracter:
                break
            bit_acumulado += tabla_codigos[caracter]
            while len(bit_acumulado) >= 8:
                byte = int(bit_acumulado[:8], 2)
                salida.write(bytes([byte]))
                bit_acumulado = bit_acumulado[8:]
        
        # Escribir los bits restantes
        if bit_acumulado:
            byte = int(bit_acumulado + '0' * (8 - len(bit_acumulado)), 2)
            salida.write(bytes([byte]))

    return nombre_archivo_comprimido


def descomprimir_archivo(archivo_comprimido, arbol_huffman):
    nombre_archivo_descomprimido = "D:/Documentos/8vo/Analisis de Algoritmos/Actividades/practica7/Participaci-n-07-Analisis-de-algoritmos--Codificaci-n-de-HUFFMAN/descomprimido.txt"

    with open(archivo_comprimido, 'rb') as entrada, open(nombre_archivo_descomprimido, 'w', encoding='utf-8') as salida:
        bit_acumulado = ''
        byte = entrada.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')  # Convertir el byte a una cadena de bits de longitud fija
            bit_acumulado += bits
            byte = entrada.read(1)
        
        nodo_actual = arbol_huffman
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

# Contar los caracteres y construir el árbol de Huffman
conteo = contar_caracteres(archivo)
arbol_huffman = construir_arbol_huffman(conteo)

# Generar tabla de códigos Huffman
tabla_codigos = generar_tabla_codigos(arbol_huffman)

# Comprimir el archivo
nombre_archivo_comprimido = comprimir_archivo(archivo, tabla_codigos)

print("Archivo comprimido como:", nombre_archivo_comprimido)

# Descomprimir el archivo
archivo_descomprimido = descomprimir_archivo(nombre_archivo_comprimido, arbol_huffman)

print("Archivo descomprimido como:", archivo_descomprimido)
