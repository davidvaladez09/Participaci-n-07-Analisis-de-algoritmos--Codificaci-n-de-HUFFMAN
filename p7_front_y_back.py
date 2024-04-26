# BACKEND DAVID VALADEZ GUTIERREZ
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import heapq
import os
import time


# ---------------------------------------------------------- FUNCIONES BACKEND ------------------------------------------------------------------- 

# FUNCION BACKEND DAVID VALADEZ
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

# FUNCION BACKEND DAVID VALADEZ
# Función que cuenta los caracteres repetidos
def contar_caracteres(archivo, ventana_principal):
    # Parte BackEnd DAVID VALADEZ
    with open(archivo, 'r', encoding='utf-8') as file_open:
        contador_caracteres = 0

        # Contar todos los caracteres del archivo
        for linea in file_open:
            contador_caracteres += len(linea)
        
        print('Número de caracteres:', contador_caracteres)
        
        file_open.seek(0) # Reiniciar puntero en el archivo
        
        texto = file_open.read() # Abre el archivo de texto
        contador = {} # Diccionario para almacenar los caracteres repetidos

        # Contar los caracteres repetidos
        for caracter in texto:
            if caracter in contador:
                contador[caracter] += 1
            else:
                contador[caracter] = 1

        caracteres_ordenados = sorted(contador.items(),  key=lambda item: item[1], reverse=True)
        print(caracteres_ordenados)

        nombre_archivo_resultados = archivo + "_resultados.txt"

        # Escribir los resultados en un archivo de texto
        with open(nombre_archivo_resultados, 'w', encoding='utf-8') as resultado_file:
            resultado_file.write(f"Número de caracteres: {contador_caracteres}\n")
            resultado_file.write("Caracteres y su frecuencia:\n")
            for caracter, frecuencia in caracteres_ordenados:
                resultado_file.write(f"{caracter}: {frecuencia}\n")

        
        # Parte FrontEnd       
        # Muestra la frecuencia de los caracteres en la ventana
        textResultadoCaracteres = tk.Text(root, wrap="word", height=10, width=50)
        textResultadoCaracteres.insert(tk.END, f"Caracteres y su frecuencia:\n{contador}\n")
        textResultadoCaracteres.config(state="disabled")
        textResultadoCaracteres.pack(padx=10, pady=10)


        # Retorna el diccionario de caracteres repetidos
        return contador

# FUNCION BACKEND DAVID VALADEZ
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

# FUNCION BACKEND DAVID VALADEZ
# Función para genera la tabla de códigos
def crear_tabla_codigos(arbol_huffman, prefijo='', tabla_codigos={}):
    if arbol_huffman.caracter is not None:
        tabla_codigos[arbol_huffman.caracter] = prefijo
    else:
        crear_tabla_codigos(arbol_huffman.izquierda, prefijo + '0', tabla_codigos)
        crear_tabla_codigos(arbol_huffman.derecha, prefijo + '1', tabla_codigos)
    
    return tabla_codigos

# FUNCION BACKEND DAVID VALADEZ
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

# FUNCION BACKEND DAVID VALADEZ
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

# FUNCION BACKEND DAVID VALADEZ
# Funcion para seleccionar el archivo
def examinar(ventana_principal):
    archivo = filedialog.askopenfilename(filetypes=[("Solo archivos TXT", "*txt")])
    if archivo:
        messagebox.showinfo("Archivo seleccionado", f"Archivo seleccionado") # Mensaje de archivo seleccionado
        # Cuenta los caracteres
        inicio = time.time() # Comienza a medir el tiempo
        no_caracteres = contar_caracteres(archivo, ventana_principal)
        fin = time.time() # Termina de medir el tiempo
        tiempo_contar_caracteres = fin - inicio # Calcula el tiempo transcurrido

        # Crea el árbol de Huffman con los caracteres repetidos contados
        inicio = time.time() # Comienza a medir el tiempo
        arbol_huffman = crear_arbol_huffman(no_caracteres)
        fin = time.time() # Termina de medir el tiempo
        tiempo_crear_arbol = fin - inicio # Calcula el tiempo transcurrido

        # Genera tabla de códigos Huffman
        inicio = time.time() # Comienza a medir el tiempo
        tabla_codigos = crear_tabla_codigos(arbol_huffman)
        fin = time.time() # Termina de medir el tiempo
        tiempo_generar_tabla = fin - inicio # Calcula el tiempo transcurrido

        # Guarda la información necesaria para compresión/descompresión
        ventana_principal.archivo = archivo
        ventana_principal.arbol_huffman = arbol_huffman
        ventana_principal.tabla_codigos = tabla_codigos 

        tiempo_total_examinar = tiempo_contar_caracteres + tiempo_crear_arbol + tiempo_generar_tabla
        print(f"Tiempo total para procesar el archivo: {tiempo_total_examinar} segundos")

        # Implementacion Del front end
        archivo_entrada_entry.delete(0, tk.END)
        archivo_entrada_entry.insert(0, archivo)
        # Mostrar contenido del archivo en el widget Text
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            contenido_text.delete(1.0, tk.END)
            contenido_text.insert(tk.END, contenido)

        return tiempo_total_examinar

# FUNCION BACKEND DAVID VALADEZ
# Funcion para comprimir el archivo
def comprimir(ventana_principal):
    archivo = ventana_principal.archivo
    tabla_codigos = ventana_principal.tabla_codigos
    if archivo and tabla_codigos:
        inicio = time.time() # Comienza a medir el tiempo
        nombre_archivo_comprimido = comprimir_archivo(archivo, tabla_codigos)
        fin = time.time() # Termina de medir el tiempo
        tiempo_comprimir = fin - inicio # Calcula el tiempo transcurrido

        messagebox.showinfo("Compresión completada", f"ARCHIVO COMPRIMIDO") # Mensaje de archivo comprimido

        print(f"Tiempo total para comprimir el archivo: {tiempo_comprimir} segundos")

        return tiempo_comprimir

# FUNCION BACKEND DAVID VALADEZ
# Funcion para descomprimir el archivo
def descomprimir(ventana_principal):
    archivo_comprimido = filedialog.askopenfilename(filetypes=[("Archivos BIN", "*.bin")])
    if archivo_comprimido:
        # Se carga el árbol de Huffman previamente creado
        arbol_huffman = ventana_principal.arbol_huffman
        inicio = time.time() # Comienza a medir el tiempo
        archivo_descomprimido = descomprimir_archivo(archivo_comprimido, arbol_huffman)
        fin = time.time() # Termina de medir el tiempo
        tiempo_descomprimir = fin - inicio # Calcula el tiempo transcurrido

        messagebox.showinfo("Descompresión completada", f"ARCHIVO DESCOMPRIMIDO") # Mensaje de archivo descomprimido

        print(f"Tiempo total para descomprimir el archivo: {tiempo_descomprimir} segundos")

        return tiempo_descomprimir
    
# ---------------------------------------------------------- FUNCIONES FRONTEND ------------------------------------------------------------------- 
# Estas funciones solo son utilzadas con los botones 'Seleccionar Archivo de Salida' Y 'Mostrar Resultados'

#Esta funcion es la que utilice la anterior clase para contar los caracteres
def contar_caracteres_lineas(archivo_entrada, archivo_salida):
    try: 
        with open(archivo_entrada, 'r', encoding='utf-8') as f_in: 
            contenido = f_in.readlines()  
            num_lineas = len(contenido)  
            contenido = ''.join(contenido)  
            frecuencia_caracteres = Counter(contenido)
            caracteres_ordenados = sorted(frecuencia_caracteres.items(), key=lambda x: x[1], reverse=True)  
            with open(archivo_salida, 'w', encoding='utf-8') as f_out:
                f_out.write("Caracteres ordenados por frecuencia:\n")
                print("Caracteres ordenados por frecuencia: ")
                for caracter, frecuencia in caracteres_ordenados:
                    print(f"{caracter}: {frecuencia}")
                    f_out.write(f"{caracter}: {frecuencia}\n")
                f_out.write(f"Número total de líneas: {num_lineas}\n")
                print(f"Numero total de lineas: {num_lineas}")  
            print(f"Resultados guardados en '{archivo_salida}'")
    except FileNotFoundError:
        print(f"El archivo '{archivo_entrada}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

#Aqui esta funcion la cree para que pueda yo seleccionar el archivo txt que quiero que leea el codigo
def seleccionar_archivo(entrada=True):
    filename = filedialog.askopenfilename() if entrada else filedialog.asksaveasfilename()
    if filename:
        if entrada:
            archivo_entrada_entry.delete(0, tk.END)
            archivo_entrada_entry.insert(0, filename)
            # Mostrar contenido del archivo en el widget Text
            with open(filename, 'r', encoding='utf-8') as f:
                contenido = f.read()
                contenido_text.delete(1.0, tk.END)
                contenido_text.insert(tk.END, contenido)
        else:
            archivo_salida_entry.delete(0, tk.END)
            archivo_salida_entry.insert(0, filename)

def mostrar_resultados():
    archivo_entrada = archivo_entrada_entry.get()
    archivo_salida = archivo_salida_entry.get()
    contar_caracteres_lineas(archivo_entrada, archivo_salida)
    with open(archivo_salida, 'r', encoding='utf-8') as f:
        resultados = f.read()
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, resultados)




# ----------------------------------------------------------- GUI -------------------------------------------------

#Aqui cree la ventana principal
root = tk.Tk()
root.title("Contador de Caracteres y Líneas")

root.archivo = None
root.arbol_huffman = None
root.tabla_codigos = None

#Cree el widget
tk.Label(root, text="Archivo de Entrada:").pack()
archivo_entrada_entry = tk.Entry(root, width=50)
archivo_entrada_entry.pack()

# Botones FrontEnd
#botones de Comprimir y Descomprimir (sin funciones por ahora)
#tk.Button(root, text="Seleccionar Archivo de Entrada", command=lambda: examinar(ventana_principal)).pack()
#tk.Button(root, text="Comprimir").pack()
#tk.Button(root, text="Descomprimir").pack()

# Botones con funciones BackEnd
tk.Button(root, text="Seleccionar Archivo de Entrada", command=lambda: examinar(root)).pack() # Correcciones BackEnd
boton_comprimir = tk.Button(root, text="Comprimir", command=lambda: comprimir(root)).pack() # Correcciones BackEnd
boton_descomprimir = tk.Button(root, text="Descomprimir", command=lambda: descomprimir(root)).pack() # Correcciones BackEnd

tk.Label(root, text="Contenido del Archivo de Entrada:").pack()
contenido_text = tk.Text(root, height=10, width=80)
contenido_text.pack()

tk.Label(root, text="Archivo de Salida:").pack()
archivo_salida_entry = tk.Entry(root, width=50)
archivo_salida_entry.pack()
tk.Button(root, text="Seleccionar Archivo de Salida", command=lambda: seleccionar_archivo(entrada=False)).pack()

tk.Button(root, text="Mostrar Resultados", command=mostrar_resultados).pack()
resultado_text = tk.Text(root, height=10, width=80)
resultado_text.pack()

root.mainloop()