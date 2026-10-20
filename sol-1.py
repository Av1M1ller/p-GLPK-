import argparse
import subprocess

def leer_in(archivo_in):
    """Lee el fichero .in y valida que el total de cajas sea L^2."""
    with open(archivo_in, "r") as f:
        # Dimensión L de la base del pallet
        n_lado_cajas = int(f.readline().strip())
        # Lista con las prioridades de cada caja
        prioridades = [int(x) for x in f.readline().split()]

    # Comprueba que el número de cajas coincida con el tamaño del pallet 2D
    if len(prioridades) != n_lado_cajas ** 2:
        raise ValueError("El número de prioridades no coincide con L^2")
        
    return n_lado_cajas, prioridades

def crear_archivo_data(archivo_in, nombre_archivo_dat):
    """Genera el fichero .dat con la sintaxis de MathProg/GLPK."""
    n_lado_cajas, prioridades = leer_in(archivo_in)
    
    with open(nombre_archivo_dat, "w", encoding="utf-8") as f:
        f.write("data;\n\n")
        # Parámetro del tamaño de la base (L)
        f.write(f"param l := {n_lado_cajas};\n\n")
        # Parámetro con la prioridad p[k] de cada caja k
        f.write("param p :=\n")
        for idx, valor in enumerate(prioridades, start=1):
            f.write(f"{idx} {valor}\n")
        f.write(";\n\nend;\n")

    return nombre_archivo_dat

def main():
    # Parámetros de entrada por línea de comandos
    parser = argparse.ArgumentParser() 
    parser.add_argument("--nombre_fichero_in", type=str, required=True, help="Fichero .in de entrada")
    parser.add_argument("--nombre_fichero_dat", type=str, required=True, help="Fichero .dat a generar")
    args = parser.parse_args()

    # Genera el fichero de datos para el solver
    datos = crear_archivo_data(args.nombre_fichero_in, args.nombre_fichero_dat)
    modelo = "part-1.mod"

    # Comando para ejecutar GLPK con el modelo, los datos y la salida
    comando = ["glpsol", "--math", modelo, "--data", datos, "--output", "resultado.txt"]
    subprocess.run(comando, check=True)

if __name__ == "__main__":
    main()