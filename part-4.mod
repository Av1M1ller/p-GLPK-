
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

param M := 1 + sum{k in CAJAS} prioridad[k];

# --------------------------------------------------------------------

var x{CAJAS, FILAS, COLUMNAS, ALTURAS, PALLETS}, binary;

var y{PALLETS}, binary;

minimize coste_total: sum{q in PALLETS} (P * y[q] + sum{k in CAJAS, i in FILAS, j in COLUMNAS, a in ALTURAS} (i - 1) * prioridad[k] * x[k,i,j,a,q]);

s.t. una_posicion_por_caja{k in CAJAS}: sum{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS} x[k,i,j,a,q] = 1;

s.t. una_caja_por_posicion{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS}: sum{k in CAJAS} x[k,i,j,a,q] <= y[q];

s.t. orden_prioridad{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS: i < L}: sum{k in CAJAS} prioridad[k] * x[k,i+1,j,a,q] <= sum{k in CAJAS} prioridad[k] * x[k,i,j,a,q];

s.t. Resistencia{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS: a < H}: sum{k in CAJAS} capacidad[k] * x[k,i,j,a,q]>=sum{ap in ALTURAS, k in CAJAS: ap > a}peso[k] * x[k,i,j,ap,q];

s.t. sin_huecos{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS: a < H}: sum{k in CAJAS} x[k,i,j,a+1,q]<= sum{k in CAJAS} x[k,i,j,a,q];