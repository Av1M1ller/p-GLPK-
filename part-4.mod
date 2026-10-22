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

# Orden de prioridad (solo si la celda delantera está ocupada)
s.t. orden_prioridad{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS: i < L}: 
    sum{k in CAJAS} prioridad[k] * x[k,i+1,j,a,q] <= 
    sum{k in CAJAS} prioridad[k] * x[k,i,j,a,q] + M * (1 - u[i+1,j,a,q]);

# Resistencia vertical
s.t. resistencia{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS: a < H}:
    sum{k in CAJAS} capacidad[k] * x[k,i,j,a,q] >= sum{ap in ALTURAS, k in CAJAS: ap > a} peso[k] * x[k,i,j,ap,q];

# Gravedad vertical (no flotar)
s.t. gravedad_vertical{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS: a < H}:
    u[i,j,a+1,q] <= u[i,j,a,q];

# Gravedad horizontal (empujar al fondo para evitar huecos)
s.t. gravedad_horizontal{i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS: i < L}:
    u[i+1,j,a,q] <= u[i,j,a,q];

# Cálculo exacto del coste de extracción
s.t. calculo_coste{k in CAJAS, i in FILAS, j in COLUMNAS, a in ALTURAS, q in PALLETS}:
    c[k] >= prioridad[k] * (sum{ip in FILAS: ip > i} u[ip,j,a,q]) - (prioridad[k] * L) * (1 - x[k,i,j,a,q]);

end;