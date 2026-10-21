import argparse
import subprocess
import re

def get_ints(linea: str):
    """Convierte una línea de texto con números separados por espacios en una lista de enteros."""
    return [int(x) for x in linea.strip().split()]

def leer_in(archivo_in):
    """
    Lee y valida el fichero .in del problema 3D:

    """
    with open(archivo_in, "r") as f:
        # Lado del pallet (L) y altura máxima (H)
        dimensiones = get_ints(f.readline())
        prioridades = get_ints(f.readline())
        pesos = get_ints(f.readline())
        capacidad = get_ints(f.readline())

    n_cajas = dimensiones[0] ** 2 * dimensiones[1]  # L^2 * H
    # Comprueba que la cantidad de datos coincida con el número total de cajas del pallet 3D
    if not (len(prioridades) == len(pesos) == len(capacidad) == n_cajas):
        raise ValueError("El número de cajas no coincide con L^2 * H")

    return dimensiones, prioridades, pesos, capacidad

def crear_archivo_data(archivo_in, nombre_archivo_dat):
    """Genera el fichero .dat con los parámetros en formato MathProg/GLPK."""
    dimensiones, prioridades, pesos, capacidad = leer_in(archivo_in)
    lado, niveles = dimensiones[0], dimensiones[1]

    with open(nombre_archivo_dat, "w", encoding="utf-8") as f:
        f.write("data;\n\n")
        # Dimensiones del pallet
        f.write(f"param L := {lado};\n")
        f.write(f"param K := {niveles};\n\n")

        # Prioridad de cada caja
        f.write("param prioridad :=\n")
        for idx, valor in enumerate(prioridades, start=1):
            f.write(f"  {idx} {valor}\n")
        f.write(";\n\n")

        # Peso en gramos de cada caja
        f.write("param peso :=\n")
        for idx, valor in enumerate(pesos, start=1):
            f.write(f"  {idx} {valor}\n")
        f.write(";\n\n")

        # Capacidad de soporte de cada caja
        f.write("param capacidad :=\n")
        for idx, valor in enumerate(capacidad, start=1):
            f.write(f"  {idx} {valor}\n")
        f.write(";\n\nend;\n")

    return nombre_archivo_dat

def crear_archivo_salida(dimensiones, prioridades, expresion_regular, pesos = None, capacidad = None, nombre_fichero_in = "ejemplo.txt", nombre_output_glpk= "resultado.txt", nombre_archivo_salida = "salida.txt"):
    resultado = []
    n_filas = dimensiones
    # patron = r"\s*\d+\s+x\[\d+,\d+,\d+,\d+\]\s+\*\s+1\s+0\s+1"

    patron = expresion_regular
    with open(nombre_output_glpk, "r") as f: # sirve para cualquier caso
        for linea in f:
            coincidencia = re.search(patron, linea)
            if coincidencia:
                linea = linea.split()
                resultado.append(linea)

    print(resultado)

    filas = []
    filas.append([]*n_filas)
    

        

    
    # filas = [0,0,0,0,0,0,0,0,0]
    # output_xs = []
    # # dimensiones , prioridades, pesos, capacidad  = leer_in(nombre_fichero_in) #TODO: Añadir pesos y capacidad?

    # for element in resultado:
    #     output_xs.append(element[1])

    # for element in output_xs: # x[1,2,1,3] x[k,i,j,a] 
    #     for i in range(1,4): 
    #         print(f"element[4]:  {element[4]}, i: {i}")
    #         if int(element[4]) == i: # # x[1,2,2] x[k,i,j] , element[4] = 2, que es = fila
    #             posicion = (i - 1) * 3 + int(element[6]) - 1  # x[1,2,2] x[k,i,j] , element[6] = 2, que es = columna. Se multiplica x3 a razón de i-1 porque representamos una matriz en un vector
    #             filas[posicion] = [prioridades[int(element[2])-1], pesos[int(element[2])-1], capacidad[int(element[2])-1]]

    # with open(nombre_archivo_salida, "w") as f:
    #     for i in range(0,3):
    #         f.write(f"FILA {i+1}: ")
    #         f.write(f"{filas[0+3*i:3+3*i]}\n")
    # # x[1,2,1,3]

def main():
    # Argumentos por línea de comandos
    parser = argparse.ArgumentParser()
    parser.add_argument("--nombre_fichero_in", type=str, required=True, help="Fichero .in de entrada")
    parser.add_argument("--nombre_fichero_dat", type=str, required=True, help="Fichero .dat a generar")
    args = parser.parse_args()

    # Genera el fichero de datos intermedio
    datos = crear_archivo_data(args.nombre_fichero_in, args.nombre_fichero_dat)
    modelo = "part-2.mod"
    path = r"C:\Users\Av1M1\Downloads\winglpk-4.65\glpk-4.65\w64\glpsol.exe"
    comando = [path,"--math", modelo,"--data", datos,"--output", "resultado.txt"]
    subprocess.run(comando, check = True) #what is capture_output and text?

    dimensiones, prioridades, pesos, capacidad = leer_in(args.nombre_fichero_in)
    expresion_regular = r"\s*\d+\s+x\[\d+,\d+,\d+,\d+\]\s+\*\s+1\s+0\s+1"

    crear_archivo_salida(dimensiones = dimensiones, prioridades=prioridades, expresion_regular = expresion_regular, pesos=pesos, capacidad = capacidad, nombre_fichero_in = args.nombre_fichero_in, nombre_output_glpk="resultado.txt", nombre_archivo_salida="output-2.txt")

main() #esto hace que se ejecute la función main y por tanto el código que está dentro de él, creo que es mejor así para que esté más estructurado el código

# prioridades, expresion_regular, n_pallets = 1, n_alturas= 1,pesos = None, capacidad = None, nombre_fichero_in = "ejemplo.txt", nombre_output_glpk= "resultado.txt", nombre_archivo_salida = "salida.txt"