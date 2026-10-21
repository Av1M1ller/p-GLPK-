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


# --------------- VARIABLES DE DECISIÓN -Y- FUNCION OBJETIVO----------------------------------------------------------------

var x{CAJAS, FILAS, COLUMNAS, ALTURAS}, binary;
var c{CAJAS} >= 0;

minimize coste_medio: (1/n) * sum{ca in CAJAS} c[ca];

#---------------------------------------------------------------------------------------------------------

#-----------------------------RESTRICCIONES ---------------------------------------------

s.t. una_posicion_por_caja {ca in CAJAS}: sum{i in FILAS, j in COLUMNAS, k in ALTURAS} x[ca,i,j,k] = 1;

s.t. una_caja_por_posicion {i in FILAS, j in COLUMNAS, k in ALTURAS}: sum {ca in CAJAS} x[ca,i,j,k] <= 1;

# Soporte físico (no cajas flotantes)
s.t. gravedad {i in FILAS, j in COLUMNAS, k in ALTURAS: k > 1}:
    sum{ca in CAJAS} x[ca, i, j, k] <= sum{cp in CAJAS} x[cp, i, j, k-1];

s.t. orden_prioridad {i in FILAS, j in COLUMNAS, k in ALTURAS: i < L}:
    sum{ca in CAJAS} prioridad[ca] * x[ca,i+1,j,k] + M * (1 - sum{ca in CAJAS} x[ca,i+1,j,k]) <= 
    sum{ca in CAJAS} prioridad[ca] * x[ca,i,j,k] + M * (1 - sum{ca in CAJAS} x[ca,i,j,k]);

s.t. Resistencia {i in FILAS, j in COLUMNAS, k in ALTURAS: k < K}:
    sum{ca in CAJAS} capacidad[ca] * x[ca,i,j,k] >= sum{kp in ALTURAS, ca in CAJAS: kp > k} peso[ca] * x[ca,i,j,kp];

# Calculo exacto del coste sin sobreestimar huecos
s.t. calculo_coste {ca in CAJAS, i in FILAS, j in COLUMNAS, k in ALTURAS}:
    c[ca] >= prioridad[ca] * (sum{ip in FILAS, cp in CAJAS: ip < i} x[cp, ip, j, k]) 
             - (prioridad[ca] * (i - 1)) * (1 - x[ca, i, j, k]);

end;