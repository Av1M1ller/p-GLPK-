import argparse
import subprocess


def get_ints(lista_strings: list):
    lista_strings.split()
    lista_procesada = []             # para no tener que modificar la lista de entrada 
    for string in lista_strings:
        lista_procesada.append(int(string))
    return lista_procesada


# ---------------- funciones para gestionar el ejemplo.in y crear el archivo .dat ----------------
def leer_in(archivo_in):
    """
    formato de ejemplo.in:
    <longitud del lado del pallet, l> <n´ umero de niveles, h>, <coste del montaje de un pallet, P>
    <p1 p2 ... pn >
    <ω1 ω2 ... ωn >
    <γ1 γ2 ... γn >
    """

    try:
        # obtener los datos del .in y guardarlos en variables locales
        with open(archivo_in, "r") as f:
            n_cajas_niveles_costeMontaje = get_ints(f.readline())  # [2,3]
            prioridades = get_ints(f.readline()) # [1, 3, 349, 11, 7, 10, 3218]
            pesos = get_ints(f.readline()) # [3, 4, 9, 11, 13, 4, 15, 2817,10]
            capacidad = get_ints(f.readline()) #[0, 0, 0, 11, 3, 21, 14, 2, 19, 12, 14, 16]

            print(f"n_cajas_niveles: {n_cajas_niveles_costeMontaje}, prioridades: {prioridades}, pesos: {pesos}, capacidad: {capacidad}") #depurar 
            return  n_cajas_niveles_costeMontaje, prioridades, pesos, capacidad


    except: 
        raise TypeError("no se entró en el try de la función")

    # devolver los valores de las variables si el número de prioridades coincide con el cuadrado del numero de cajas
    # TODO: comprobaciones y raise error?


def crear_archivo_data(archivo_in, nombre_archivo_dat): #FIXME ruta dat o nombre del archivo (1)?
    n_cajas_niveles_costeMontaje, prioridades, pesos, capacidad = leer_in(archivo_in)

    n_cajas = n_cajas_niveles_costeMontaje[0]
    n_niveles = n_cajas_niveles_costeMontaje[1]
    coste_montaje = n_cajas_niveles_costeMontaje[2]

    with open(nombre_archivo_dat, "w", encoding="utf-8") as f:
        f.write("data;\n\n") #FIXME: doble salto de línea?
        f.write(f"param L := {n_cajas};\n\n")
        f.write(f"param K := {n_niveles};\n\n")
        f.write(f"param P := {coste_montaje};\n\n")

        f.write("param prioridad :=\n")
        # Escribimos cada par: posición valor
        for idx, valor in enumerate(prioridades, start=1):
            f.write(f"{idx} {valor}\n")

        f.write("param peso :=\n")
        for idx, peso in enumerate(pesos, start =1):
            f.write(f"{idx} {peso}\n")

        f.write("param capacidad :=\n")
        for idx, capacidad in enumerate(capacidad, start =1):
            f.write(f"{idx} {capacidad}\n")

        f.write(";\n\nend;\n")

    return nombre_archivo_dat

def main():
    
    #TODO: Estructurar mejor el código con diferentes funciones
    parser = argparse.ArgumentParser() 
    parser.add_argument("--nombre_fichero_in", type = str, required = True)
    parser.add_argument("--nombre_fichero_dat", type = str, required = True)
    args = parser.parse_args()

    path_local_glpk = r"C:\Users\Av1M1\Downloads\winglpk-4.65\glpk-4.65\w64\glpsol.exe # "glpsol" #r"C:\Users\cheve\Downloads\2_HEURÍSTICA\TrabajoGLPK\winglpk-4.65\glpk-4.65\w64\glpsol.exe" # PATH Ordenador Ángel r"C:\Users\Av1M1\Downloads\winglpk-4.65\glpk-4.65\w64\glpsol.exe"
    modelo = "part-4.mod"
    datos = crear_archivo_data(args.nombre_fichero_in, args.nombre_fichero_dat)


    comando = [path_local_glpk,"--math", modelo,"--data", datos,"--output", "resultado.txt"]
    subprocess.run(comando, check = True) #what is capture_output and text?

main() #esto hace que se ejecute la función main y por tanto el código que está dentro de él, creo que es mejor así para que esté más estructurado el código

