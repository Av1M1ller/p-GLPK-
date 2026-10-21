import argparse
import subprocess
import re

def get_ints(linea_texto: str):
    # Divide la cadena por espacios y convierte cada valor a entero
    lista_strings = linea_texto.strip().split()
    lista_procesada = []
    for string in lista_strings:
        lista_procesada.append(int(string))
    return lista_procesada


# ---------------- funciones para gestionar el ejemplo.in y crear el archivo .dat ----------------
def leer_in(archivo_in):
    """
    Lee el fichero .in para el modelo con espacios vacíos:
    """
    try:
        # Obtener los datos del .in y guardarlos en variables locales
        with open(archivo_in, "r", encoding="utf-8") as f:
            n_cajas_niveles = get_ints(f.readline())  # [l, h]
            prioridades = get_ints(f.readline())      # lista de prioridades
            pesos = get_ints(f.readline())            # lista de pesos
            capacidad = get_ints(f.readline())        # lista de capacidades

            return n_cajas_niveles, prioridades, pesos, capacidad

    except Exception as e:
        raise IOError(f"Error al leer el archivo de entrada '{archivo_in}': {e}")


def crear_archivo_data(archivo_in, nombre_archivo_dat):
    """
    Genera el archivo .dat en formato MathProg:
    Escribe dimensiones (L, K), total de cajas reales (n), prioridades, pesos y capacidades.
    """
    n_cajas_niveles, prioridades, pesos, capacidad = leer_in(archivo_in)

    n_cajas = n_cajas_niveles[0]
    n_niveles = n_cajas_niveles[1]

    with open(nombre_archivo_dat, "w", encoding="utf-8") as f:
        f.write("data;\n\n")
        # Parámetro L: lado de la base cuadrada del pallet
        f.write(f"param L := {n_cajas};\n\n")
        # Parámetro K: número máximo de niveles de altura (H)
        f.write(f"param K := {n_niveles};\n\n")
        # Parámetro n: cantidad real de cajas existentes (n <= L * L * H)
        f.write(f"param n := {len(prioridades)};\n\n")

        # Parámetro prioridad: vector con la prioridad de cada caja
        f.write("param prioridad :=\n")
        for idx, valor in enumerate(prioridades, start=1):
            f.write(f"{idx} {valor}\n")
        f.write(";\n\n")

        # Parámetro peso: vector con el peso en gramos de cada caja
        f.write("param peso :=\n")
        for idx, peso in enumerate(pesos, start=1):
            f.write(f"{idx} {peso}\n")
        f.write(";\n\n")

        # Parámetro capacidad: peso máximo que cada caja puede aguantar encima
        f.write("param capacidad :=\n")
        for idx, cap in enumerate(capacidad, start=1):
            f.write(f"{idx} {cap}\n")
        f.write(";\n\nend;\n")

    return nombre_archivo_dat

def crear_archivo_salida(nombre_fichero_in, nombre_output_glpk= "resultado.txt", nombre_archivo_salida = "salida.txt"):
    resultado = []
    # patron = r"\s*\d\s+x\[\d+,\d+,\d+\]\s+\*\s+1\s+0\s+1"
    patron = r"\s*\d+\s+x\[\d+,\d+,\d+,\d+\]\s+\*\s+1\s+0\s+1"
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
    _ , prioridades, pesos, capacidad  = leer_in(nombre_fichero_in) #TODO: Añadir pesos y capacidad?

    for element in resultado:
        output_xs.append(element[1])

    for element in output_xs: # x[1,2,1,3] x[k,i,j,a] 
        for i in range(1,4): 
            print(f"element[4]:  {element[4]}, i: {i}")
            if int(element[4]) == i: # # x[1,2,2] x[k,i,j] , element[4] = 2, que es = fila
                posicion = (i - 1) * 3 + int(element[6]) - 1  # x[1,2,2] x[k,i,j] , element[6] = 2, que es = columna. Se multiplica x3 a razón de i-1 porque representamos una matriz en un vector
                filas[posicion] = [prioridades[int(element[2])-1], pesos[int(element[2])-1], capacidad[int(element[2])-1]]

    with open(nombre_archivo_salida, "w") as f:
        for i in range(0,3):
            f.write(f"FILA {i+1}: ")
            f.write(f"{filas[0+3*i:3+3*i]}\n")
    # x[1,2,1,3]


def main():
    # Argumentos de entrada por línea de comandos
    parser = argparse.ArgumentParser()
    parser.add_argument("--nombre_fichero_in", type=str, required=True)
    parser.add_argument("--nombre_fichero_dat", type=str, required=True)
    args = parser.parse_args()

    # Rutas locales del solver GLPK y del modelo 3D con espacios vacíos
    path_local_glpk = r"C:\Users\Av1M1\Downloads\winglpk-4.65\glpk-4.65\w64\glpsol.exe"
    modelo = "part-3.mod"
    datos = crear_archivo_data(args.nombre_fichero_in, args.nombre_fichero_dat)

    # Invocación de glpsol para resolver el modelo MathProg
    comando = [path_local_glpk, "--math", modelo, "--data", datos, "--output", "resultado.txt"]
    subprocess.run(comando, check=True)

    comando = [path_local_glpk,"--math", modelo,"--data", datos,"--output", "resultado.txt"]
    subprocess.run(comando, check = True) #what is capture_output and text?
    crear_archivo_salida(args.nombre_fichero_in, nombre_archivo_glpk="resultado.txt", nombre_archivo_salida="output-3.txt")

main() #esto hace que se ejecute la función main y por tanto el código que está dentro de él, creo que es mejor así para que esté más estructurado el código