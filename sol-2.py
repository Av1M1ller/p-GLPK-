import argparse
import subprocess

def get_ints(linea: str):
    """Convierte una línea de texto con números separados por espacios en una lista de enteros."""
    return [int(x) for x in linea.strip().split()]

def leer_in(archivo_in):
    """
    Lee y valida el fichero .in del problema 3D:

    """
    with open(archivo_in, "r") as f:
        # Lado del pallet (L) y altura máxima (H)
        dimensiones = get_ints(f.readline())
        prioridades = get_ints(f.readline())
        pesos = get_ints(f.readline())
        capacidad = get_ints(f.readline())

    n_cajas = dimensiones[0] ** 2 * dimensiones[1]  # L^2 * H
    # Comprueba que la cantidad de datos coincida con el número total de cajas del pallet 3D
    if not (len(prioridades) == len(pesos) == len(capacidad) == n_cajas):
        raise ValueError("El número de cajas no coincide con L^2 * H")

    return dimensiones, prioridades, pesos, capacidad

def crear_archivo_data(archivo_in, nombre_archivo_dat):
    """Genera el fichero .dat con los parámetros en formato MathProg/GLPK."""
    dimensiones, prioridades, pesos, capacidad = leer_in(archivo_in)
    lado, niveles = dimensiones[0], dimensiones[1]

    with open(nombre_archivo_dat, "w", encoding="utf-8") as f:
        f.write("data;\n\n")
        # Dimensiones del pallet
        f.write(f"param L := {lado};\n")
        f.write(f"param H := {niveles};\n\n")

        # Prioridad de cada caja
        f.write("param prioridad :=\n")
        for idx, valor in enumerate(prioridades, start=1):
            f.write(f"  {idx} {valor}\n")
        f.write(";\n\n")

        # Peso en gramos de cada caja
        f.write("param peso :=\n")
        for idx, valor in enumerate(pesos, start=1):
            f.write(f"  {idx} {valor}\n")
        f.write(";\n\n")

        # Capacidad de soporte de cada caja
        f.write("param capacidad :=\n")
        for idx, valor in enumerate(capacidad, start=1):
            f.write(f"  {idx} {valor}\n")
        f.write(";\n\nend;\n")

    return nombre_archivo_dat

def main():
    # Argumentos por línea de comandos
    parser = argparse.ArgumentParser()
    parser.add_argument("--nombre_fichero_in", type=str, required=True, help="Fichero .in de entrada")
    parser.add_argument("--nombre_fichero_dat", type=str, required=True, help="Fichero .dat a generar")
    args = parser.parse_args()

    # Genera el fichero de datos intermedio
    datos = crear_archivo_data(args.nombre_fichero_in, args.nombre_fichero_dat)
    modelo = "part-2.mod"

    # Ejecuta el solver glpsol con el modelo y los datos generados
    comando = ["glpsol", "--math", modelo, "--data", datos, "--output", "resultado.txt"]
    subprocess.run(comando, check=True)

if __name__ == "__main__":
    main()