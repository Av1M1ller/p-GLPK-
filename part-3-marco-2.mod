/* PARTE 3 - Modelo compatible con sol-3.py */

/* Parámetros: estos nombres coinciden con los que escribe sol-3.py */
param L, integer, > 0;                 # lado de la base del pallet
param K, integer, > 0;                 # número de niveles
param n, integer, > 0, <= L * L * K;   # número real de cajas

/* Conjuntos */
set FILA    := 1..L;
set COLUMNA := 1..L;
set NIVEL   := 1..K;
set CAJA    := 1..n;

/* Datos: nombres coincidentes con sol-3.py */
param prioridad{CAJA};
param peso{CAJA};
param capacidad{CAJA};

/* sol-3.py no proporciona un vector independiente de costes.
   Se conserva el parámetro de costes del modelo y se toma prioridad
   como su valor, que es el único vector disponible en el .dat. */
param valor_costes{p in CAJA} := prioridad[p];

/* Variables de decisión.
   El orden de índices de x coincide con el parser de sol-3.py:
   x[caja, fila, columna, altura]. */
var x{p in CAJA, f in FILA, c in COLUMNA, a in NIVEL} binary;
var coste{f in FILA, c in COLUMNA, a in NIVEL} >= 0;

/* Función objetivo: misma expresión que en parte-marco.mod */
minimize Coste_Medio:
    sum{f in FILA, c in COLUMNA, a in NIVEL} coste[f,c,a]
    / (sum{p in CAJA: valor_costes[p] > 0} 1);

/* Restricciones */

# Cada caja se coloca exactamente una vez.
s.t. Una_posicion_por_caja {p in CAJA}:
    sum{f in FILA, c in COLUMNA, a in NIVEL} x[p,f,c,a] = 1;

# Un hueco puede contener como máximo una caja.
# Se usa <= 1 para permitir los huecos vacíos que representa sol-3.py.
s.t. Una_caja_por_hueco {f in FILA, c in COLUMNA, a in NIVEL}:
    sum{p in CAJA} x[p,f,c,a] <= 1;

# Las cajas de mayor prioridad deben quedar delante de las de menor prioridad.
s.t. Mayor_prioridad_delante
    {f in FILA, col1 in COLUMNA, col2 in COLUMNA, a in NIVEL: f < L}:
    sum{p in CAJA} prioridad[p] * x[p,f+1,col1,a]
    <= sum{p in CAJA} prioridad[p] * x[p,f,col2,a];

# El peso situado por encima de una caja no puede superar su capacidad.
s.t. Capacidad_maxima {f in FILA, c in COLUMNA, a1 in NIVEL: a1 < K}:
    sum{p in CAJA, a2 in NIVEL: a2 > a1} peso[p] * x[p,f,c,a2]
    <= sum{p in CAJA} capacidad[p] * x[p,f,c,a1];

# Cálculo del coste: se conserva la expresión del modelo original.
s.t. Calcular_coste {f in FILA, c in COLUMNA, a in NIVEL}:
    coste[f,c,a] >=
        sum{p in CAJA, f2 in FILA: f2 > f}
            valor_costes[p] * x[p,f2,c,a]
        - (sum{p in CAJA} valor_costes[p])
          * (sum{p in CAJA: valor_costes[p] = 0} x[p,f,c,a]);

end;
