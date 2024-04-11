import os

def contar_caracteres(archivo):
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

    nombre_archivo_resultados =  "C:/Users/usuario/Desktop/resultados.txt" # Generar archivos de resultados

    # Escribir los resultados en un archivo de texto
    with open(nombre_archivo_resultados, 'w', encoding='utf-8') as resultado_file:
        resultado_file.write(f"Número de caracteres: {contador_caracteres}\n")
        resultado_file.write("Caracteres y su frecuencia:\n")
        for caracter, frecuencia in caracteres_ordenados:
            resultado_file.write(f"{caracter}: {frecuencia}\n")

archivo = "C:/Users/usuario/Desktop/Gullivers_Travels.txt"

contar_caracteres(archivo)
