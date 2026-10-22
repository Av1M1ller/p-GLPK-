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
    Extrae las dimensiones (L, H) y los vectores de prioridades, pesos y capacidades.
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
        # Parámetro n: cantidad real de cajas existentes
        f.write(f"param n := {len(prioridades)};\n\n")

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

def crear_archivo_salida(nombre_fichero_in, nombre_output_glpk= "resultado.txt", nombre_archivo_salida = "salida.txt"):
    """
    Parsea el output bruto de GLPK, filtra las variables x activas (valor 1)
    y genera un mapa visual 3D por pisos para entender la distribución.
    """
    n_cajas_niveles, prioridades, pesos, capacidad  = leer_in(nombre_fichero_in) 
    L = n_cajas_niveles[0]
    H = n_cajas_niveles[1]
    
    # Matriz inicializada con huecos vacíos ("-")
    matriz = [[[["-"] for _ in range(L)] for _ in range(L)] for _ in range(H)]
    
    # Expresión para capturar x[caja, fila, columna, altura]
    patron = r"x\[(\d+),(\d+),(\d+),(\d+)\]\s+\*\s+1"
    
    with open(nombre_output_glpk, "r") as f:
        for linea in f:
            coincidencia = re.search(patron, linea)
            if coincidencia:
                k = int(coincidencia.group(1))
                i = int(coincidencia.group(2))
                j = int(coincidencia.group(3))
                a = int(coincidencia.group(4))
                
                # Asignamos los datos de la caja a su hueco
                matriz[a-1][i-1][j-1] = f"[P:{prioridades[k-1]}, W:{pesos[k-1]}, C:{capacidad[k-1]}]"

    # Generamos el texto visual
    resultado_visual = f"\n--- DISTRIBUCIÓN DEL PALLET (HUECOS PERMITIDOS) ({L}x{L}x{H}) ---\n\n"
    for a in range(H):
        resultado_visual += f"=== PISO {a+1} {'(Suelo)' if a == 0 else '(Superior)'} ===\n"
        for i in range(L):
            etiqueta = f"FILA {i+1} (Fondo) :" if i == 0 else (f"FILA {i+1} (Acceso):" if i == L - 1 else f"FILA {i+1}          :")
            resultado_visual += f"{etiqueta} {matriz[a][i]}\n"
        resultado_visual += "\n"

    with open(nombre_archivo_salida, "w", encoding="utf-8") as f:
        f.write(resultado_visual)
        
    print(resultado_visual)


def main():
    #Argumentos de entrada por línea de comandos
    parser = argparse.ArgumentParser()
    parser.add_argument("--nombre_fichero_in", type=str, required=True)
    parser.add_argument("--nombre_fichero_dat", type=str, required=True)
    args = parser.parse_args()

    #Rutas locales del solver GLPK y del modelo 3D con espacios vacíos
    path_local_glpk = "glpsol" 
    modelo = "part-3.mod"
    datos = crear_archivo_data(args.nombre_fichero_in, args.nombre_fichero_dat)

    #Invocación de glpsol
    comando = [path_local_glpk, "--math", modelo, "--data", datos, "--tmlim", "10", "--name", "PARTE_3", "--output", "resultado.txt"]
    
    print("Ejecutando, 10S...")
    try:
        #capture_output=True para ocultar el bloque que ensucia
        subprocess.run(comando, check=True, capture_output=True, text=True)
        print("Optimización completada con éxito!")
    except subprocess.CalledProcessError as e:
        print("\nError al ejecutar GLPK:\n", e.stderr)
        return

    crear_archivo_salida(args.nombre_fichero_in, nombre_output_glpk="resultado.txt", nombre_archivo_salida="output-3.txt")

if __name__ == "__main__":
    # esto hace que se ejecute la función main y por tanto el código que está dentro de él, creo que es mejor así para que esté más estructurado el código
    main()