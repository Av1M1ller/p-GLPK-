
# -----------------------parametros generales -----------------------

param L, integer, > 0;
param K, integer, > 0;

param n, integer, >0, <= L * L * K;

# ---------------------------------------------------------------------

set FILAS := 1..L;
set COLUMNAS := 1..L;
set ALTURAS := 1..K;
set CAJAS  := 1..n;

# -------------- PARÁMETROS ASOCIADOS A "LA CAJA" ---------------------
param prioridad{CAJAS}, >= 0;
param peso{CAJAS}, >0;
param capacidad{CAJAS} >= 0;
param M := 1 + sum{c in CAJAS} prioridad[c];
# ---------------------------------------------------------------------


# --------------- VARIABLE DE DECISIÓN -Y- FUNCION OBJETIVO----------------------------------------------------------------

var x{CAJAS, FILAS, COLUMNAS, ALTURAS}, binary;

minimize coste_medio: 1/n * sum{c in CAJAS, i in FILAS, j in COLUMNAS, k in ALTURAS} (i-1) * prioridad[c] * x[c,i,j,k];

#---------------------------------------------------------------------------------------------------------

#-----------------------------RESTRICCIONES ---------------------------------------------

s.t. una_posicion_por_caja {c in CAJAS}: sum{i in FILAS, j in COLUMNAS, k in ALTURAS} x[c,i,j,k] = 1;

s.t. una_caja_por_posicion {i in FILAS, j in COLUMNAS, k in ALTURAS}: sum {c in CAJAS} x[c,i,j,k] <= 1;

s.t. orden_prioridad {i in FILAS, j in COLUMNAS, k in ALTURAS: i < L}:
    sum{c in CAJAS} prioridad[c] * x[c,i+1,j,k] <= sum{c in CAJAS} prioridad[c] * x[c,i,j,k]; #TODO: MenorOigual o menor estrictor?

s.t. Resistencia {i in FILAS, j in COLUMNAS, k in ALTURAS: k < K}:
    sum{c in CAJAS} capacidad[c] * x[c,i,j,k] >= sum{kp in ALTURAS, c in CAJAS: kp > k} peso[c] * x[c,i,j,kp];

end;
