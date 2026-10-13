import sys
import argparse
import subprocess


# ---------------- funciones para gestionar el ejemplo.in y crear el archivo .dat ----------------
def leer_in(archivo_in):
    """
    formato de ejemplo.in:
    3
    4 11 13 8 5 4 1 3 9  
    """
    try:
        # obtener los datos del .in y guardarlos en variables locales
        with open(archivo_in, "r") as f: 
            # print(f"readline: {f.readline().strip()}")
            n_lado_cajas = int(f.readline())
            print(n_lado_cajas) # depurar

            prioridades = f.readline().split()
            prioridades.replace(" ","") #TODO: enrique quiere cambiarlo
            print(prioridades) # depurar

            # for i in prioridades:
            #     entero = int(i)
            #     prioridades.pop(0)
            #     prioridades.append(entero)

            prioridades_enteros = []
            for i in prioridades:
                prioridades_enteros.append(int(i))
            prioridades = prioridades_enteros

            print(prioridades) #depurar 
    except: 
        raise TypeError("no se entró en el try de la función")

    # devolver los valores de las variables si el número de prioridades coincide con el cuadrado del numero de cajas
    if len(prioridades) == n_lado_cajas **2:
        return n_lado_cajas, prioridades
    else:
        raise ValueError("l**2 no coincide con el número de prioridades")
    
# def crear_archivo_data(archivo_in):  # archivo_in = ejemplo.in
#     n_lado_cajas, prioridades = leer_in(archivo_in)
#     prioridades_formateadas = enumerate(prioridades, start = 1)
#     with open("parte-1.dat", "w") as f:
#         f.write("data; \n")
#         f.write(f"param l := {n_lado_cajas}")
#         f.write(f"param p := {prioridades_formateadas}")
#         f.write("end;")


def crear_archivo_data(archivo_in, ruta_dat):
    n_lado_cajas, prioridades = leer_in(archivo_in)
    
    with open(ruta_dat, "w", encoding="utf-8") as f:
        f.write("data;\n\n")
        f.write(f"param l := {n_lado_cajas};\n\n")
        f.write("param p :=\n")
        
        # Escribimos cada par: posición valor
        for idx, valor in enumerate(prioridades, start=1):
            f.write(f"  {idx} {valor}\n")
            
        f.write(";\n\nend;\n")
        
    return ruta_dat
# ---------------------------------------------------------------------
if __name__ == "__main__": #NUEVO DE ENRIQUE
    # Comprobar que nos pasan los dos argumentos obligatorios
    if len(sys.argv) < 3:
        print("Uso: python sol-1.py <fichero_entrada> <fichero_dat>")
        sys.exit(1)
    fichero_in = sys.argv[1]
    fichero_dat = sys.argv[2]
    fichero_sol = "resultado.sol"

    # 1. Creamos el archivo .dat usando la ruta recibida
    crear_archivo_data(fichero_in, fichero_dat)

    # 2. Rutas del ejecutable y del modelo
    path_local_glpk = r"C:\Users\cheve\Downloads\2_HEURÍSTICA\TrabajoGLPK\winglpk-4.65\glpk-4.65\w64\glpsol.exe"
    modelo = "parte-1.mod"

    # 3. Ejecución de GLPK
    comando = [
        path_local_glpk,
        "--math", modelo,
        "--data", fichero_dat,
        "--output", fichero_sol

    ]

    proceso = subprocess.run(comando, capture_output=True, text=True)

    if proceso.returncode != 0:
        print("Error en GLPK:")
        print(proceso.stderr)
        sys.exit(1)

    #ERA EL ERROR 4
    # 4. Procesar el archivo resultado.sol
    cols, rows, coste, contenido_sol = parsear_solucion(fichero_sol)

    # Imprimir en pantalla exactamente en el formato exigido:
    # <variables> <restricciones> <coste_medio>
    print(f"{cols} {rows} {coste:.2f}")

    # 5. Generar la salida gráfica (por ejemplo con extension .out)
    n_lado_cajas, prioridades = leer_in(fichero_in)
    ruta_grafica = fichero_dat.replace(".dat", ".out")
    generar_salida_grafica(contenido_sol, n_lado_cajas, prioridades, ruta_grafica)

#datos = crear_archivo_data("ejemplo.in") # crear el .dat a partir de la entrada .in si su formato es correcto

# path_local_glpk = r"C:\Users\Av1M1\Downloads\winglpk-4.65\glpk-4.65\w64\glpsol.exe"
# modelo = "parte-1.mod"
# # datos = "datos-1.dat"

# subprocess.run([path_local_glpk,"--math", modelo, "--data", datos, "--output", "resultado.txt" ], 
#                check= True) 

