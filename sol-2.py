import argparse
import subprocess
import re

def get_ints(linea: str):
    """Convierte una línea de texto con números separados por espacios en una lista de enteros."""
    return [int(x) for x in linea.strip().split()]

# ---------------- Funciones para gestionar el .in y crear el archivo .dat ----------------
def leer_in(archivo_in):
    """Lee y valida el fichero .in del problema 3D (Parte 2)."""
    with open(archivo_in, "r") as f:
        # Extraemos las dimensiones (L, H) y los vectores de datos de las cajas
        dimensiones = get_ints(f.readline())
        prioridades = get_ints(f.readline())
        pesos = get_ints(f.readline())
        capacidad = get_ints(f.readline())

    #cajas totales = L * L * H
    n_cajas = dimensiones[0] ** 2 * dimensiones[1]  
    
    #Validación
    if not (len(prioridades) == len(pesos) == len(capacidad) == n_cajas):
        raise ValueError("El número de cajas no coincide con L^2 * H")

    return dimensiones, prioridades, pesos, capacidad

def crear_archivo_data(archivo_in, nombre_archivo_dat):
    """Genera el fichero .dat con los parámetros en formato MathProg/GLPK."""
    dimensiones, prioridades, pesos, capacidad = leer_in(archivo_in)
    lado, niveles = dimensiones[0], dimensiones[1]

    with open(nombre_archivo_dat, "w", encoding="utf-8") as f:
        f.write("data;\n\n")
        # Parámetro L: lado del pallet cuadrado
        f.write(f"param L := {lado};\n")
        # Parámetro K: altura máxima del pallet (H)
        f.write(f"param K := {niveles};\n\n")

        # Volcado del vector de prioridades (1 valor, 2 valor...)
        f.write("param prioridad :=\n")
        for idx, valor in enumerate(prioridades, start=1):
            f.write(f"  {idx} {valor}\n")
        f.write(";\n\n")

        # Volcado del vector de pesos
        f.write("param peso :=\n")
        for idx, valor in enumerate(pesos, start=1):
            f.write(f"  {idx} {valor}\n")
        f.write(";\n\n")

        # Volcado del vector de capacidades (resistencia)
        f.write("param capacidad :=\n")
        for idx, valor in enumerate(capacidad, start=1):
            f.write(f"  {idx} {valor}\n")
        f.write(";\n\nend;\n")

    return nombre_archivo_dat

def crear_archivo_salida(dimensiones, prioridades, pesos, capacidad, nombre_output_glpk="resultado.txt", nombre_archivo_salida="output-2.txt"):
    """
    Lee el volcado de GLPK, filtra las asignaciones activas usando regex,
    y genera un mapa visual 3D separado por pisos.
    """
    
    
    L = dimensiones[0]
    H = dimensiones[1]
    
    # Inicialización de la matriz 3D con las dimensiones del pallet (H x L x L)
    matriz = [[[["-"] for _ in range(L)] for _ in range(L)] for _ in range(H)]
    
    # Regex para capturar los índices de la variable de decisión x[k, i, j, a] cuando vale 1
    patron = r"x\[(\d+),(\d+),(\d+),(\d+)\]\s+\*\s+1"
    
    with open(nombre_output_glpk, "r") as f:
        # leer datos relevantes del txt generado por glpk
        f.readline()
        rows = f.readline()
        columns = f.readline()
        f.readline()
        f.readline()
        f_objetivo = f.readline()

        for linea in f:
            coincidencia = re.search(patron, linea)
            if coincidencia:
                k = int(coincidencia.group(1))
                i = int(coincidencia.group(2))
                j = int(coincidencia.group(3))
                a = int(coincidencia.group(4))
                
                #Rellenamos la posición exacta con los atributos de la caja asignada
                matriz[a-1][i-1][j-1] = f"[P:{prioridades[k-1]}, W:{pesos[k-1]}, C:{capacidad[k-1]}]"

    #Generación del formato visual en texto
    resultado_visual = f"\n--- DISTRIBUCIÓN DEL PALLET 3D ({L}x{L}x{H}) ---\n\n"
    for a in range(H):
        resultado_visual += f"=== PISO {a+1} {'(Suelo)' if a == 0 else '(Superior)'} ===\n"
        for i in range(L):
            # Etiquetamos las filas para orientarnos sobre qué lado es el acceso
            if i == 0:
                etiqueta = f"FILA {i+1} (Fondo) :"
            elif i == L - 1:
                etiqueta = f"FILA {i+1} (Acceso):"
            else:
                etiqueta = f"FILA {i+1}          :"

            resultado_visual += f"{etiqueta} {matriz[a][i]}\n"
            resultado_visual += "\n"

    with open(nombre_archivo_salida, "w", encoding="utf-8") as f:
        f.write(f"(número de restricciones) {rows}\n") #Número restricciones
        f.write(f"(número de variables de decisión) {columns}\n") #Número de variables de decisión
        f.write(f"{f_objetivo}\n") #Función objetivo
        print(f"(número de restricciones) {rows}")
        print(f"(número de variables de decisión) {columns}")
        print(f"{f_objetivo}")
        f.write(resultado_visual)
        
    print(resultado_visual)

def main():
    #Captura de los argumentos obligatorios por línea de comandos
    parser = argparse.ArgumentParser()
    parser.add_argument("--nombre_fichero_in", type=str, required=True, help="Fichero .in de entrada")
    parser.add_argument("--nombre_fichero_dat", type=str, required=True, help="Fichero .dat a generar")
    args = parser.parse_args()

    #Generamos el archivo .dat a partir de los datos originales
    datos = crear_archivo_data(args.nombre_fichero_in, args.nombre_fichero_dat)
    modelo = "parte-2.mod"
    
    path = "glpsol" #r"C:\Users\Av1M1\Downloads\winglpk-4.65\glpk-4.65\w64\glpsol.exe" # 
    
    #Comando a ejecutar
    comando = [path, "--math", modelo, "--data", datos, "--name", "PARTE_2", "--output", "resultado.txt"]
    
    try:
        #capture_output=True mantiene la consola limpia
        subprocess.run(comando, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("\nError al ejecutar GLPK:\n", e.stderr)
        return

    #Extraemos los datos iniciales
    dimensiones, prioridades, pesos, capacidad = leer_in(args.nombre_fichero_in)
    
    #Parseamos el archivo de resultados de GLPK y generamos el output
    crear_archivo_salida(dimensiones, prioridades, pesos, capacidad, nombre_output_glpk="resultado.txt", nombre_archivo_salida="output-2.txt")


main()