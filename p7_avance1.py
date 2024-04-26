# Desarrollado por David Valadez Gutierrez
import os
import tkinter 
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog

def contar_caracteres():
    archivo = filedialog.askopenfilename(filetypes=[("Solo archivos", "*.txt")])

    with open(archivo, 'r', encoding='utf-8') as file_open:
        contador_caracteres = 0

        # Contar todos los caracteres del archivo
        for linea in file_open:
            contador_caracteres += len(linea)
        
        print('Número de caracteres:', contador_caracteres)
        
        file_open.seek(0) # Reiniciar puntero en el archivo
        
        # CONTAR CARACTERES REPETIDOS

        texto = file_open.read() 
        
        conteo = {}
        
        # Contar los caracteres repetidos
        for caracter in texto:
            if caracter in conteo:
                conteo[caracter] += 1
            else:
                conteo[caracter] = 1

        caracteres_ordenados = sorted(conteo.items(),  key=lambda item: item[1], reverse=True)
    
        print(caracteres_ordenados)
        labelResultadoCaracteres = ttk.Label(text=f"Caracteres y su frecuencia:\n {caracteres_ordenados}\n", style="BW.TLabel").pack()


    nombre_archivo_resultados =  "C:/Users/usuario/Desktop/resultados.txt" # Generar archivos de resultados

    # Escribir los resultados en un archivo de texto
    with open(nombre_archivo_resultados, 'w', encoding='utf-8') as resultado_file:
        resultado_file.write(f"Número de caracteres: {contador_caracteres}\n")
        resultado_file.write("Caracteres y su frecuencia:\n")
        for caracter, frecuencia in caracteres_ordenados:
            resultado_file.write(f"{caracter}: {frecuencia}\n")
    
    labelNoCaracteres = ttk.Label(text=f"Número de caracteres: {contador_caracteres}\n", style="BW.TLabel").pack()


#archivo = "C:/Users/usuario/Desktop/Gullivers_Travels.txt"

#contar_caracteres(archivo)

root = tkinter.Tk()

style = ttk.Style()

l1 = ttk.Label(text="BUSCAR ARCHIVO", style="BW.TLabel").pack()
abrir_archivo = ttk.Button(text='Abrir archivo', command=contar_caracteres).pack()

root.mainloop()