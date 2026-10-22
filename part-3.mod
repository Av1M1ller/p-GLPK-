# ----------------------- PARÁMETROS GENERALES -----------------------

param L, integer, > 0;
param K, integer, > 0;
param n, integer, > 0, <= L * L * K;

# ---------------------------------------------------------------------

set FILAS := 1..L;
set COLUMNAS := 1..L;
set ALTURAS := 1..K;
set CAJAS  := 1..n;

# -------------- PARÁMETROS ASOCIADOS A "LA CAJA" ---------------------

param prioridad{CAJAS};
param coste_caja{CAJAS};
param capacidad{CAJAS};
param peso{CAJAS};

param max_p := max{c in CAJAS} prioridad[c];
param M := 1 + max_p;

# ---------------- VARIABLES DE DECISIÓN Y FO -----------------------

var x{p in CAJAS, f in FILAS, c in COLUMNAS, k in ALTURAS}, binary;
# x = cajas

var coste_pos{FILAS, COLUMNAS, ALTURAS};

# var u{FILAS, COLUMNAS, ALTURAS}, binary;
# var c{CAJAS} >= 0;

minimize coste_medio:
    sum{f in FILAS, c in COLUMNAS, k in ALTURAS}
        coste_pos[f,c,k]
    / (sum{p in CAJAS: coste_caja[p] > 0} 1);

# Se divide por el número de cajas reales:
# sum{p in CAJAS: coste_caja[p] > 0} 1

# -------------------------- RESTRICCIONES ---------------------------

s.t. una_posicion_por_caja {p in CAJAS}:
    sum{f in FILAS, c in COLUMNAS, k in ALTURAS}
        x[p,f,c,k] = 1;

s.t. una_caja_por_posicion {f in FILAS, c in COLUMNAS, k in ALTURAS}:
    sum{p in CAJAS}
        x[p,f,c,k] = 1;

s.t. Mayor_prioridad_delante
    {f in FILAS, c1 in COLUMNAS, c2 in COLUMNAS,
     k in ALTURAS: f < L}:

    sum{p in CAJAS}
        prioridad[p] * x[p,f+1,c1,k]
    <=
    sum{p in CAJAS}
        prioridad[p] * x[p,f,c2,k];

s.t. Capacidad_maxima
    {f in FILAS, c in COLUMNAS, k1 in ALTURAS: k1 < K}:

    sum{p in CAJAS, k2 in ALTURAS: k2 > k1}
        peso[p] * x[p,f,c,k2]
    <=
    sum{p in CAJAS}
        capacidad[p] * x[p,f,c,k1];

s.t. Calcular_coste
    {f in FILAS, c in COLUMNAS, k in ALTURAS}:

    coste_pos[f,c,k] >=
        sum{p in CAJAS, f2 in FILAS: f2 > f}
            coste_caja[p] * x[p,f2,c,k]
        -
        (sum{p in CAJAS} coste_caja[p])
        *
        (sum{p in CAJAS: coste_caja[p] = 0}
            x[p,f,c,k]);

end;

















#s.t. def_ocupacion {i in FILAS, j in COLUMNAS, k in ALTURAS}: 
 #   sum{ca in CAJAS} x[ca,i,j,k] = u[i,j,k];

# s.t. gravedad {i in FILAS, j in COLUMNAS, k in ALTURAS: k > 1}:
  #  u[i,j,k] <= u[i,j,k-1];

# Empuja las cajas hacia el fondo para que no queden huecos muertos en medio
# s.t. gravedad_filas {i in FILAS, j in COLUMNAS, k in ALTURAS: i < L}:
  #  u[i+1,j,k] <= u[i,j,k];

# Solo exige el orden de prioridad si la posición de delante (i+1) está ocupada
# s.t. orden_prioridad {i in FILAS, j in COLUMNAS, k in ALTURAS: i < L}:
  #  sum{ca in CAJAS} prioridad[ca] * x[ca,i+1,j,k] <= 
   # sum{ca in CAJAS} prioridad[ca] * x[ca,i,j,k] + M * (1 - u[i+1,j,k]);

# s.t. Resistencia {i in FILAS, j in COLUMNAS, k in ALTURAS: k < K}:
  #  sum{ca in CAJAS} capacidad[ca] * x[ca,i,j,k] >= sum{kp in ALTURAS, ca in CAJAS: kp > k} peso[ca] * x[ca,i,j,kp];

# s.t. calculo_coste {ca in CAJAS, i in FILAS, j in COLUMNAS, k in ALTURAS}:
  #  c[ca] >= prioridad[ca] * (sum{ip in FILAS: ip > i} u[ip,j,k]) 
   #          - (prioridad[ca] * L) * (1 - x[ca,i,j,k]);


# end; 