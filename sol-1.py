import argparse
import subprocess
import re

def leer_in(archivo_in):
    """Lee el fichero .in y valida que el total de cajas sea L^2."""
    with open(archivo_in, "r") as f:
        # Dimensión L de la base del pallet
        n_lado_cajas = int(f.readline().strip())
        # Lista con las prioridades de cada caja
        prioridades = [int(x) for x in f.readline().split()]

    # Comprueba que el número de cajas coincida con el tamaño del pallet 2D
    if len(prioridades) != n_lado_cajas ** 2:
        raise ValueError("El número de prioridades no coincide con L^2")
        
    return n_lado_cajas, prioridades

def crear_archivo_data(archivo_in, nombre_archivo_dat):
    """Genera el fichero .dat con la sintaxis de MathProg/GLPK."""
    n_lado_cajas, prioridades = leer_in(archivo_in)
    
    with open(nombre_archivo_dat, "w", encoding="utf-8") as f:
        f.write("data;\n\n")
        # Parámetro del tamaño de la base (L)
        f.write(f"param l := {n_lado_cajas};\n\n")
        # Parámetro con la prioridad p[k] de cada caja k
        f.write("param p :=\n")
        for idx, valor in enumerate(prioridades, start=1):
            f.write(f"{idx} {valor}\n")
        f.write(";\n\nend;\n")

    return nombre_archivo_dat

def crear_archivo_salida(nombre_fichero_in, nombre_output_glpk= "resultado.txt", nombre_archivo_salida = "salida.txt"):
    resultado = []
    patron = r"\s*\d\s+x\[\d+,\d+,\d+\]\s+\*\s+1\s+0\s+1"
    with open(nombre_output_glpk, "r") as f:
        for linea in f:
            coincidencia = re.search(patron, linea)
            if coincidencia:
                linea = linea.split()#.strip()
                # print(f"linea[1]!!!!!!!!!!!!!!!!!!!!!!!!!!!!1: {linea[1]}")
                # linea[1] = linea[1].split()
                resultado.append(linea)

    
    filas = [0,0,0,0,0,0,0,0,0]
    output_xs = []
    _ , prioridades = leer_in(nombre_fichero_in)

    for element in resultado:
        output_xs.append(element[1])

    for element in output_xs: # x[1,2,2] x[k,i,j] 
        for i in range(1,4): 
            print(f"element[4]:  {element[4]}, i: {i}")
            if int(element[4]) == i: # # x[1,2,2] x[k,i,j] , element[4] = 2, que es = fila
                posicion = (i - 1) * 3 + int(element[6]) - 1  # x[1,2,2] x[k,i,j] , element[6] = 2, que es = columna. Se multiplica x3 a razón de i-1 porque representamos una matriz en un vector
                filas[posicion] = prioridades[int(element[2])-1]

    with open(nombre_archivo_salida, "w") as f:
        for i in range(0,3):
            f.write(f"FILA {i+1}: ")
            f.write(f"{filas[0+3*i:3+3*i]}\n")

def main():
    # Parámetros de entrada por línea de comandos
    parser = argparse.ArgumentParser() 
    parser.add_argument("--nombre_fichero_in", type=str, required=True, help="Fichero .in de entrada")
    parser.add_argument("--nombre_fichero_dat", type=str, required=True, help="Fichero .dat a generar")
    args = parser.parse_args()

    # Genera el fichero de datos para el solver
    datos = crear_archivo_data(args.nombre_fichero_in, args.nombre_fichero_dat)
    modelo = "part-1.mod"
    path_local_glpk = "glpsol" #r"C:\Users\Av1M1\Downloads\winglpk-4.65\glpk-4.65\w64\glpsol.exe"
    # Comando para ejecutar GLPK con el modelo, los datos y la salida
    comando = [path_local_glpk,"--math", modelo,"--data", datos,"--output", "resultado.txt"]
    subprocess.run(comando, check = True) #what is capture_output and text?
    crear_archivo_salida(args.nombre_fichero_in, nombre_output_glpk="resultado.txt", nombre_archivo_salida="output-1.txt")

main() #esto hace que se ejecute la función main y por tanto el código que está dentro de él, creo que es mejor así para que esté más estructurado el código
