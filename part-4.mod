# ----------------------- PARÁMETROS GENERALES -----------------------

param L, integer, > 0;
param H, integer, > 0;
param n, integer, > 0;
param m, integer, > 0, <= n;
param P, integer, > 0;

# --------------------------------------------------------------------

set FILAS := 1..L;
set COLUMNAS := 1..L;
set ALTURAS := 1..H;
set CAJAS := 1..n;
set PALLETS := 1..m;

# -------------- PARÁMETROS ASOCIADOS A "LA CAJA" -------------------

param prioridad{CAJAS}, > 0;
param peso{CAJAS}, > 0;
param capacidad{CAJAS}, >= 0;

param max_p := max{k in CAJAS} prioridad[k];
param M := 1 + max_p;

# --------------------------------------------------------------------

var x{CAJAS, FILAS, COLUMNAS, ALTURAS, PALLETS}, binary;
var u{FILAS, COLUMNAS, ALTURAS, PALLETS}, binary;
var y{PALLETS}, binary;
var c{CAJAS} >= 0;

minimize coste_total: sum{q in PALLETS} P * y[q] + (1/n) * sum{k in CAJAS} c[k];

# Cada caja va a una única posición y pallet
s.t. una_posicion_por_caja{k in CAJAS}: 
    sum{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS} x[k,i,j,a,q] = 1;

# Ocupación de celda ligada a la activación del pallet
s.t. def_ocupacion{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS}: 
    sum{k in CAJAS} x[k,i,j,a,q] = u[i,j,a,q];

s.t. uso_pallet{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS}:
    u[i,j,a,q] <= y[q];

# Ruptura de simetría: usar pallets en orden correlativo (1, 2, ...)
s.t. orden_pallets{q in PALLETS: q < m}:
    y[q+1] <= y[q];

# Orden de prioridad con M ajustada
s.t. orden_prioridad{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS: i < L}: 
    sum{k in CAJAS} prioridad[k] * x[k,i+1,j,a,q] + M * (1 - u[i+1,j,a,q]) <= 
    sum{k in CAJAS} prioridad[k] * x[k,i,j,a,q]   + M * (1 - u[i,j,a,q]);

# Resistencia vertical