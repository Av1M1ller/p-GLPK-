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

            n_lado_cajas = int(f.readline())
            print(n_lado_cajas) # depurar

            prioridades = f.readline().split()
            print(prioridades) # depurar

            for i in prioridades:
                entero = int(i)
                prioridades.pop(0)
                prioridades.append(entero)
    except: 
        raise TypeError("no se entró en el try de la función")

    # devolver los valores de las variables si el número de prioridades coincide con el cuadrado del numero de cajas
    if len(prioridades) == n_lado_cajas **2:
        return n_lado_cajas, prioridades
    else:
        raise ValueError("l**2 no coincide con el número de prioridades")
def crear_archivo_data(archivo_in):  # archivo_in = ejemplo.in
    n_lado_cajas, prioridades = leer_in(archivo_in)
    prioridades_formateadas = enumerate(prioridades, start = 1)
    with open("part-1.dat", "w") as f:
        f.write("data; \n")
        f.write(f"param l := {n_lado_cajas}")
        f.write(f"param p := {prioridades_formateadas}")
# ---------------------------------------------------------------------


datos = crear_archivo_data("ejemplo.in") # crear el .dat a partir de la entra .in si su formato es correcto

path_local_glpk = r"C:\Users\Av1M1\Downloads\winglpk-4.65\glpk-4.65\w64\glpsol.exe"
modelo = "part-1.mod"
# datos = "datos-1.dat"

subprocess.run([path_local_glpk,"--math", modelo, "--data", datos, "--output", "resultado.txt" ], 
               check= True)


