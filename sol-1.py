import argparse
import subprocess
import re

# ---------------- Funciones para gestionar el .in y crear el archivo .dat ----------------
def leer_in(archivo_in):
    """
    Lee el fichero .in para el modelo 2D (Parte 1).
    Extrae la dimensión L (lado del pallet) y el vector de prioridades.
    Valida que el total de cajas coincida exactamente con L^2.
    """
    with open(archivo_in, "r") as f:
        n_lado_cajas = int(f.readline().strip())
        prioridades = [int(x) for x in f.readline().split()]

    # Comprobación
    if len(prioridades) != n_lado_cajas ** 2:
        raise ValueError("El número de prioridades no coincide con L^2")
        
    return n_lado_cajas, prioridades

def crear_archivo_data(archivo_in, nombre_archivo_dat):
    """
    Genera el fichero .dat dinámicamente con la sintaxis exacta de MathProg (GLPK).
    """
    n_lado_cajas, prioridades = leer_in(archivo_in)
    
    with open(nombre_archivo_dat, "w", encoding="utf-8") as f:
        f.write("data;\n\n")
        # Parámetro l: longitud del lado del pallet
        f.write(f"param l := {n_lado_cajas};\n\n")
        
        # Volcado del vector de prioridades
        f.write("param p :=\n")
        for idx, valor in enumerate(prioridades, start=1):
            f.write(f"{idx} {valor}\n")
        f.write(";\n\nend;\n")

    return nombre_archivo_dat

def crear_archivo_salida(nombre_fichero_in, nombre_output_glpk="resultado.txt", nombre_archivo_salida="output-1.txt"):
    """
    Parsea el output bruto de GLPK, filtra las variables x activas con regex,
    y genera un mapa visual para entender la distribución fácilmente.
    """
    L, prioridades = leer_in(nombre_fichero_in)
    
    # Matriz 2D inicializada con ceros para la parte 1
    matriz = [[0 for _ in range(L)] for _ in range(L)]
    
    patron = r"x\[(\d+),(\d+),(\d+)\]\s+\*\s+1"
    
    with open(nombre_output_glpk, "r") as f:
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
                
                # Asignamos la prioridad de la caja a su posición en la matriz
                matriz[i-1][j-1] = prioridades[k-1]

    # Construimos el resultado visual limpio
    resultado_visual = f"\n--- DISTRIBUCIÓN DEL PALLET ({L}x{L}) ---\n"
    for i in range(L):
        if i == 0:
            etiqueta = f"FILA {i+1} (Fondo) :"
        elif i == L - 1:
            etiqueta = f"FILA {i+1} (Acceso):"
        else:
            etiqueta = f"FILA {i+1}          :"
            
        resultado_visual += f"{etiqueta} {matriz[i]}\n"
    
    #Lo guardamos en el txt y lo imprimimos en la terminal
    with open(nombre_archivo_salida, "w", encoding="utf-8") as f:
        f.write(f"(número de restricciones) {rows}\n") #Número restricciones
        f.write(f"(número de variables de decisión) {columns}\n") #Número de variables de decisión
        f.write(f"{f_objetivo}\n") #Función objetivo
        print(f"(número de restricciones) {rows}")
        print(f"(número de variables de decisión) {columns}")
        print(f"{f_objetivo}")
        f.write(resultado_visual)
        f.write(resultado_visual)
        
    print(resultado_visual)

def main():
    #Captura de los argumentos por línea de comandos
    parser = argparse.ArgumentParser() 
    parser.add_argument("--nombre_fichero_in", type=str, required=True, help="Fichero .in de entrada")
    parser.add_argument("--nombre_fichero_dat", type=str, required=True, help="Fichero .dat a generar")
    args = parser.parse_args()

    # 1. Generamos el archivo .dat a partir de los datos originales
    datos = crear_archivo_data(args.nombre_fichero_in, args.nombre_fichero_dat)
    modelo = "parte-1.mod"
    
    path_local_glpk = "glpsol" #r"C:\Users\Av1M1\Downloads\winglpk-4.65\glpk-4.65\w64\glpsol.exe" 
    
    #Configurar la llamada a GLPK
    comando = [path_local_glpk, "--math", modelo, "--data", datos, "--name", "PARTE_1", "--output", "resultado.txt"]
    
    try:
        # Se añade capture_output=True para mantener la consola limpia
        subprocess.run(comando, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("\nError al ejecutar GLPK:\n", e.stderr)
        return
    
    #Leer el resultado bruto y generar el mapa visual
    crear_archivo_salida(args.nombre_fichero_in, nombre_output_glpk="resultado.txt", nombre_archivo_salida="output-1.txt")

main()