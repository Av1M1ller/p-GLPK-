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
    Lee el fichero .in del problema con múltiples pallets:
    """
    try:
        with open(archivo_in, "r", encoding="utf-8") as f:
            n_cajas_niveles_costeMontaje = get_ints(f.readline())  # [l, h, P]
            prioridades = get_ints(f.readline())                  # lista de prioridades
            pesos = get_ints(f.readline())                        # lista de pesos
            capacidad = get_ints(f.readline())                    # lista de capacidades

            return n_cajas_niveles_costeMontaje, prioridades, pesos, capacidad

    except Exception as e:
        raise Exception(f"Error al leer el archivo de entrada '{archivo_in}': {e}")


def crear_archivo_data(archivo_in, nombre_archivo_dat):
    """
    Genera el archivo .dat en formato MathProg con los parámetros para GLPK:
    dimensiones (L, K), coste por pallet (P), total de cajas (n), prioridades, pesos y capacidades.
    """
    n_cajas_niveles_costeMontaje, prioridades, pesos, capacidad = leer_in(archivo_in)

    n_cajas = n_cajas_niveles_costeMontaje[0]
    n_niveles = n_cajas_niveles_costeMontaje[1]
    coste_montaje = n_cajas_niveles_costeMontaje[2]
    
    m = len(prioridades) # El número máximo de pallets es el total de cajas (por si va una por pallet)

    with open(nombre_archivo_dat, "w", encoding="utf-8") as f:
        f.write("data;\n\n")
        # Parámetro L: lado de la base del pallet
        f.write(f"param L := {n_cajas};\n\n")
        # Parámetro K: niveles máximos de altura (H)
        f.write(f"param H := {n_niveles};\n\n")
        # Parámetro P: coste fijo de activación/montaje de un pallet
        f.write(f"param P := {coste_montaje};\n\n")
        # Parámetro n: número total de cajas a distribuir
        f.write(f"param n := {len(prioridades)};\n\n")
        # Parámetro m: número de pallets utilizables
        f.write(f"param m := {m};\n\n")

        # Parámetro prioridad: vector con las prioridades
        f.write("param prioridad :=\n")
        for idx, valor in enumerate(prioridades, start=1):
            f.write(f"{idx} {valor}\n")
        f.write(";\n\n")

        # Parámetro peso: vector con el peso en gramos
        f.write("param peso :=\n")
        for idx, peso in enumerate(pesos, start=1):
            f.write(f"{idx} {peso}\n")
        f.write(";\n\n")

        # Parámetro capacidad
        f.write("param capacidad :=\n")
        for idx, cap in enumerate(capacidad, start=1):
            f.write(f"{idx} {cap}\n")
        f.write(";\n\nend;\n")

    return nombre_archivo_dat


def crear_archivo_salida(nombre_fichero_in, nombre_archivo_glpk="resultado.txt", nombre_archivo_salida="output-4.txt"):
    """
         3 x[1,1,3,1,1]     *              0             0             1 
    """
    # print("SE HA ENTRADO A LA FUNCION CREAR ARCHIVO SALIDA")
    n_cajas_niveles_costeMontaje, prioridades, pesos, capacidad = leer_in(nombre_fichero_in) 
    L = n_cajas_niveles_costeMontaje[0]
    H = n_cajas_niveles_costeMontaje[1]
    m = len(prioridades)
    
    #Matriz inicializada con huecos vacíos 
    matriz = [[[[["-"] for _ in range(L)] for _ in range(L)] for _ in range(H)] for _ in range(m)]
    pallets_usados = set()
    
    #Expresión regular para capturar la línea de resultado.txt generado por glpsol que indique que la caja se ha colocado
    patron = r"^\s*\d+\s+x\[(\d+),(\d+),(\d+),(\d+),(\d+)\]\s*\*\s+1\s+0\s+1" 

    n_coincidencias = 0
    with open(nombre_archivo_glpk, "r") as f:
        # print(f"SE HA ABIERTO EL ARCHIVO CORRECTAMENTE")
        f.readline()
        rows = f.readline()
        columns = f.readline()
        f.readline()
        f.readline()
        f_objetivo = f.readline()


        for linea in f:
            coincidencia = re.search(patron, linea)
            # if coincidencia:
                # n_coincidencias += 1
            # print(f"COINCIDENCIA: {coincidencia}")
            # print(f"NUMERO: {n_coincidencias}")
            if coincidencia:
                k = int(coincidencia.group(1))
                i = int(coincidencia.group(2))
                j = int(coincidencia.group(3))
                a = int(coincidencia.group(4))
                q = int(coincidencia.group(5))
                
                matriz[q-1][a-1][i-1][j-1] = f"[P:{prioridades[k-1]}, W:{pesos[k-1]}, C:{capacidad[k-1]}]"
                pallets_usados.add(q-1)

    #Generamos el texto visual 
    resultado_visual = f"\n--- DISTRIBUCIÓN MULTIPALLET ({L}x{L}x{H}) ---\n"
    
    if not pallets_usados:
        resultado_visual += "No se ha encontrado ninguna solución válida.\n"
    else:
        for q in sorted(list(pallets_usados)):
            resultado_visual += f"\n-------------- PALLET {q+1} --------------n"
            for a in range(H):
                resultado_visual += f"\n----- PISO {a+1} {'(Suelo)' if a == 0 else '(Superior)'} -----\n" #expresión ternaria para poner el condicional en una sola línea 
                for i in range(L):
                    etiqueta = f"FILA {i+1} (Fondo) :" if i == 0 else (f"FILA {i+1} (Acceso):" if i == L - 1 else f"FILA {i+1}          :")
                    resultado_visual += f"{etiqueta} {matriz[q][a][i]}\n"
    
    with open(nombre_archivo_salida, "w", encoding="utf-8") as f:
        f.write(f"(número de restricciones) {rows}\n") #Número restricciones
        f.write(f"(número de variables de decisión) {columns}\n") #Número de variables de decisión
        f.write(f"{f_objetivo}\n") #Función objetivo
        f.write(resultado_visual)
        
    print(resultado_visual)


def main():
    #Argumentos de entrada por consola
    parser = argparse.ArgumentParser() 
    parser.add_argument("--nombre_fichero_in", type=str, required=True)
    parser.add_argument("--nombre_fichero_dat", type=str, required=True)
    args = parser.parse_args()

    path_local_glpk = "glpsol" #r"C:\Users\Av1M1\Downloads\winglpk-4.65\glpk-4.65\w64\glpsol.exe" #
    modelo = "parte-4.mod"
    datos = crear_archivo_data(args.nombre_fichero_in, args.nombre_fichero_dat)

    # Invocación de glpsol 
    comando = [path_local_glpk, "--math", modelo, "--data", datos, "--name", "PARTE_4", "--output", "resultado.txt"]

    # print("ANTES DE LLAMAR A subprocess")
    subprocess.run(comando, check=True, capture_output=True, text=True) 

    # print("ANTES LLAMAR A LA FUNCIÓN DE CREAR ARCHIVO") 
    crear_archivo_salida(args.nombre_fichero_in, nombre_archivo_glpk="resultado.txt", nombre_archivo_salida="output-4.txt")
    # print("DESPUES DE LLAMAS A LA FUNCION DE CREAR ARCHIVO")

    # esto hace que se ejecute la función main y por tanto el código que está dentro de él, creo que es mejor así para que esté más estructurado el código

main()