# ----------------------- PARAMETROS GENERALES -----------------------


param L, integer, > 0;                 
param K, integer, > 0;                 
param n, integer, > 0, <= L * L * K;   


set FILA    := 1..L;
set COLUMNA := 1..L;
set NIVEL   := 1..K;
set CAJA    := 1..n;

# ----------------------- PARÁMETROS ASOCIADOS A "LA CAJA" -----------------------
param prioridad{CAJA};
param peso{CAJA};
param capacidad{CAJA};
param valor_costes{p in CAJA} := prioridad[p];

# ----------------------- VARIABLES DE DECISIÓN -----------------------
var x{p in CAJA, f in FILA, c in COLUMNA, a in NIVEL} binary;
var coste{f in FILA, c in COLUMNA, a in NIVEL} >= 0;

# ----------------------- FUNCION OBJETIVO -----------------------
minimize Coste_Medio:
    sum{f in FILA, c in COLUMNA, a in NIVEL} coste[f,c,a]
    / (sum{p in CAJA: valor_costes[p] > 0} 1);


# ----------------------- RESTRICCIONES ---------------------------------------------------------------------

# Cada caja se coloca exactamente una vez
s.t. Una_posicion_por_caja {p in CAJA}:
    sum{f in FILA, c in COLUMNA, a in NIVEL} x[p,f,c,a] = 1;

# Un hueco puede contener como máximo una caja. Se usa <= 1 para permitir los huecos vacíos
s.t. Una_caja_por_hueco {f in FILA, c in COLUMNA, a in NIVEL}:
    sum{p in CAJA} x[p,f,c,a] <= 1;

# Las cajas de mayor prioridad deben quedar delante de las de menor prioridad
s.t. Mayor_prioridad_delante
    {f in FILA, col1 in COLUMNA, col2 in COLUMNA, a in NIVEL: f < L}:
    sum{p in CAJA} prioridad[p] * x[p,f+1,col1,a]
    <= sum{p in CAJA} prioridad[p] * x[p,f,col2,a];

# El peso situado por encima de una caja no puede superar su capacidad
s.t. Capacidad_maxima {f in FILA, c in COLUMNA, a1 in NIVEL: a1 < K}:
    sum{p in CAJA, a2 in NIVEL: a2 > a1} peso[p] * x[p,f,c,a2]
    <= sum{p in CAJA} capacidad[p] * x[p,f,c,a1];


s.t. Calcular_coste {f in FILA, c in COLUMNA, a in NIVEL}:
    coste[f,c,a] >=
        sum{p in CAJA, f2 in FILA: f2 > f}
            valor_costes[p] * x[p,f2,c,a]
        - (sum{p in CAJA} valor_costes[p])
          * (sum{p in CAJA: valor_costes[p] = 0} x[p,f,c,a]);

end;
