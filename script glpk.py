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

def crear_archivo_data(archivo_in, nombre_archivo_dat): #FIXME ruta dat o nombre del archivo (1)?
    n_lado_cajas, prioridades = leer_in(archivo_in)
    
    with open(nombre_archivo_dat, "w", encoding="utf-8") as f:
        f.write("data;\n\n") #FIXME: doble salto de línea?
        f.write(f"param l := {n_lado_cajas};\n\n")
        f.write("param p :=\n")
        
        # Escribimos cada par: posición valor
        for idx, valor in enumerate(prioridades, start=1):
            f.write(f"{idx} {valor}\n")

        f.write(";\n\nend;\n")

    return nombre_archivo_dat

def main():
    #TODO: Estructurar mejor el código con diferentes funciones
    parser = argparse.ArgumentParser() 
    parser.add_argument("--nombre_fichero_in", type = str, required = True)
    parser.add_argument("--nombre_fichero_dat", type = str, required = True)
    args = parser.parse_args()


    #FIXME: No usar path local, sino global 
    path_local_glpk = r"C:\Users\cheve\Downloads\2_HEURÍSTICA\TrabajoGLPK\winglpk-4.65\glpk-4.65\w64\glpsol.exe" # PATH Ordenador Ángel r"C:\Users\Av1M1\Downloads\winglpk-4.65\glpk-4.65\w64\glpsol.exe"
    modelo = "parte-1.mod"
    datos = crear_archivo_data(args.nombre_fichero_in, args.nombre_fichero_dat) #FIXME ruta dat o nombre del archivo (2)?


    comando = [path_local_glpk,"--math", modelo,"--data", datos,"--output", "resultado.txt"]


    
    
    subprocess.run(comando, capture_output=True, text=True, check = True) #what is capture_output and text?



    # cols, rows, coste, contenido_sol = parsear_solucion(fichero_sol) #FIXME: I dont Understand mr Echeverria
    # print(f"{cols} {rows} {coste:.2f}")

    # n_lado_cajas, prioridades = leer_in(fichero_in)
    # ruta_grafica = fichero_dat.replace(".dat", ".out")
    # generar_salida_grafica(contenido_sol, n_lado_cajas, prioridades, ruta_grafica)



main() #esto hace que se ejecute la función main y por tanto el código que está dentro de él, creo que es mejor así para que esté más estructurado el código

