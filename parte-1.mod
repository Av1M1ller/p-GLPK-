
param l, integer, > 0;               # Lado del pallet
param n := l * l;                   # N?mero total de cajas


# --- CONJUNTOS ---
set FILAS := 1..l;                  # i: Fila 1 (fondo) a Fila l (acceso)
set COLUMNAS := 1..l;               # j: Columnas 1 a l
set CAJAS := 1..n;                  # k: Identificador de cada caja


# Prioridad de cada caja
param p{CAJAS}, integer, >= 0;     # prioridad de cada caja en el set de cajas


# --- VARIABLES DE DECISI?N 




var x{CAJAS, FILAS, COLUMNAS}, binary; 
# x[k, i, j] = 1 si la caja k se sit?a en la fila i, columna j; 0 si no




# --- FUNCI?N OBJETIVO ---
# Minimizar el coste medio de disposici?n de las cajas sobre el pallet
minimize coste_medio:
    (1 / n) * sum{k in CAJAS, i in FILAS, j in COLUMNAS} (i - 1) * p[k] * x[k, i, j];




# --- RESTRICCIONES ---


#1. Todas las cajas deben tener UNA posici?n
s.t. AsignarCaja{k in CAJAS}:
    sum{i in FILAS, j in COLUMNAS} x[k, i, j] = 1;


# 2. Todas las posiciones deben tener UNA caja
s.t. OcuparPosicion{i in FILAS, j in COLUMNAS}:
    sum{k in CAJAS} x[k, i, j] = 1;


# 3. Restricci?n de orden y prioridad por columna:
# La caja m?s cercana al acceso (fila i+1) debe tener mayor o igual prioridad
# (menor o igual valor num?rico p) que la que tiene detr?s (fila i).


s.t. OrdenPrioridad{i in 1..(l - 1), j in COLUMNAS}:
    sum{k in CAJAS} p[k] * x[k, i + 1, j] <= sum{k in CAJAS} p[k] * x[k, i, j];




end;
