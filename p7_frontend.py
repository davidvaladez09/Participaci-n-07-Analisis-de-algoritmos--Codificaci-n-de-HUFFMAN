import tkinter as tk
from tkinter import filedialog, messagebox
import heapq
import os

# Clase para crear los nodos del árbol de Huffman
class NodoHuffman:
    # Constructor para definir los nodos
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# Función que cuenta los caracteres repetidos
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
        
        # labelResultadoCaracteres = tk.Label(text=f"Caracteres y su frecuencia:\n {contador}\n").pack()

        # Muestra la frecuencia de los caracteres en la ventana
        textResultadoCaracteres = tk.Text(ventana_principal, wrap="word", height=10, width=50)
        textResultadoCaracteres.insert(tk.END, f"Caracteres y su frecuencia:\n{contador}\n")
        textResultadoCaracteres.config(state="disabled")
        textResultadoCaracteres.pack(padx=10, pady=10)

        # Retorna el diccionario de caracteres repetidos
        return contador

# Función para generar el árbol de Huffman
def crear_arbol_huffman(contador): # Recibe como parámetro el diccionario de caracteres repetidos
    heap = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in contador.items()] # Se identifica el caracter que más se repite
    heapq.heapify(heap) # Se coloca el caracter que más se repite al inicio del árbol
    
    # Crea el árbol comparando la cabeza del árbol
    while len(heap) > 1:
        nodo_izquierda = heapq.heappop(heap)
        nodo_derecha = heapq.heappop(heap)

        nodo_combinado = NodoHuffman(None, nodo_izquierda.frecuencia + nodo_derecha.frecuencia)
        nodo_combinado.izquierda = nodo_izquierda
        nodo_combinado.derecha = nodo_derecha

        heapq.heappush(heap, nodo_combinado)
    
    return heap[0]

# Función para genera la tabla de códigos
def crear_tabla_codigos(arbol_huffman, prefijo='', tabla_codigos={}):
    if arbol_huffman.caracter is not None:
        tabla_codigos[arbol_huffman.caracter] = prefijo
    else:
        crear_tabla_codigos(arbol_huffman.izquierda, prefijo + '0', tabla_codigos)
        crear_tabla_codigos(arbol_huffman.derecha, prefijo + '1', tabla_codigos)
    
    return tabla_codigos

# Función para comprimir el archivo
def comprimir_archivo(archivo, tabla_codigos):
    nombre_archivo_comprimido = archivo + '.bin' # Crea el nombre del archivo
    
    with open(archivo, 'r', encoding='utf-8') as entrada, open(nombre_archivo_comprimido, 'wb') as salida:
        bit_acumulado = ''
        while True:
            caracter = entrada.read(1)
            if not caracter:
                break

            # Busca su código Huffman correspondiente en la tabla de códigos
            bit_acumulado += tabla_codigos[caracter]
            while len(bit_acumulado) >= 8: # Comprueba si hay al menos 8 bits 
                # Convierte los primeros 8 bits a un entero y escribe ese byte en el archivo de salida
                byte = int(bit_acumulado[:8], 2)
                salida.write(bytes([byte]))
                bit_acumulado = bit_acumulado[8:]
        
        # Repite este proceso hasta que se haya leído todo el archivo de entrada
        if bit_acumulado:
            byte = int(bit_acumulado + '0' * (8 - len(bit_acumulado)), 2)
            salida.write(bytes([byte]))

    return nombre_archivo_comprimido

# Función para descomprimir el archivo con extensión .huffman
def descomprimir_archivo(archivo_comprimido, arbol_huffman):
    nombre_archivo_descomprimido = archivo_comprimido[:-8] + "_descomprimido.txt"  # Modificar el nombre del archivo descomprimido

    with open(archivo_comprimido, 'rb') as entrada, open(nombre_archivo_descomprimido, 'w', encoding='utf-8') as salida:
        bit_acumulado = ''
        byte = entrada.read(1)
        # Leer el archivo byte por byte
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')  # Convertir el byte a una cadena de bits de longitud fija
            bit_acumulado += bits
            byte = entrada.read(1)
        
        # Se toma el árbol de Huffman creado
        nodo_actual = arbol_huffman
        # Recorre los nodos del árbol de acuerdo con los bits en bit_acumulado
        for bit in bit_acumulado:
            if bit == '0':
                nodo_actual = nodo_actual.izquierda
            else:
                nodo_actual = nodo_actual.derecha

            if nodo_actual.caracter is not None:
                salida.write(nodo_actual.caracter)
                nodo_actual = arbol_huffman

    return nombre_archivo_descomprimido 


# Función para manejar la selección de archivo
def examinar():
    archivo = filedialog.askopenfilename(filetypes=[("Solo archivos TXT", "*txt")])
    if archivo:
        messagebox.showinfo("Archivo seleccionado", f"Archivo seleccionado")
        # Cuenta los caracteres
        no_caracteres = contar_caracteres(archivo)
        # Crea el árbol de Huffman con los caracteres repetidos contados
        arbol_huffman = crear_arbol_huffman(no_caracteres)
        # Genera tabla de códigos Huffman
        tabla_codigos = crear_tabla_codigos(arbol_huffman)
        # Guarda la información necesaria para compresión/descompresión
        ventana_principal.archivo = archivo
        ventana_principal.arbol_huffman = arbol_huffman
        ventana_principal.tabla_codigos = tabla_codigos 

# Función para manejar la compresión del archivo
def comprimir():
    archivo = ventana_principal.archivo
    tabla_codigos = ventana_principal.tabla_codigos
    if archivo and tabla_codigos:
        nombre_archivo_comprimido = comprimir_archivo(archivo, tabla_codigos)
        messagebox.showinfo("Compresión completada", f"ARCHIVO COMPRIMIDO")


# Función para manejar la descompresión del archivo
def descomprimir():
    archivo_comprimido = filedialog.askopenfilename(filetypes=[("Archivos BIN", "*.bin")])
    if archivo_comprimido:
        # Se carga el árbol de Huffman previamente creado
        arbol_huffman = ventana_principal.arbol_huffman
        # Descomprimir el archivo
        archivo_descomprimido = descomprimir_archivo(archivo_comprimido, arbol_huffman)
        messagebox.showinfo("Descompresión completada", f"ARCHIVO DESCOMPRIMIDO")

# Crear la ventan principal GUI
class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compresión y Descompresión Huffman")
        self.archivo = None
        self.arbol_huffman = None
        self.tabla_codigos = None

ventana_principal = VentanaPrincipal()

# Botones para la ventana
boton_examinar = tk.Button(ventana_principal, text="Examinar", command=examinar)
boton_examinar.pack(pady=10)

boton_comprimir = tk.Button(ventana_principal, text="Comprimir", command=comprimir)
boton_comprimir.pack(pady=5)

boton_descomprimir = tk.Button(ventana_principal, text="Descomprimir", command=descomprimir)
boton_descomprimir.pack(pady=5)

ventana_principal.mainloop()
