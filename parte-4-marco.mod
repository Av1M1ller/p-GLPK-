/* PARTE 4 */

# ----------------------------------------------------------------------------------------------
/* Parámetros del problema */
# ----------------------------------------------------------------------------------------------

# Longitud del lado del pallet
param longitud_pallet;

# Número de cajas reales
param num_cajas_reales;

# Número de niveles
param niveles;

# Coste por pallet
param coste_pallet >= 0;


# ----------------------------------------------------------------------------------------------
/* Conjuntos (sets) */
# ----------------------------------------------------------------------------------------------

# Índices de las filas del pallet (longitud_pallet = fila delantera)
set FILA := 1..longitud_pallet;

# Índices de las columnas del pallet
set COLUMNA := 1..longitud_pallet;

# Índices de los diferentes niveles de altura
set NIVEL := 1..niveles;

# Índices de los diferentes pallets
# El número de pallets es el mínimo necesario para almacenar todas las cajas reales, redondeando
# hacia arriba
set PALLET := 1..ceil(num_cajas_reales / longitud_pallet);

# Identificadores de las cajas reales
set CAJA := 1..num_cajas_reales;

# Valor de la prioridad de cada caja
param valor_prioridades{CAJA};

# Cota mayor que todas las prioridades reales para representar los huecos
param prioridad_vacia := (max{p in CAJA} valor_prioridades[p]) + 1;

# Valor del coste de cada caja
param valor_costes{CAJA};

# Valor de la capacidad de carga
param valor_aguantes{CAJA};

# Valor del peso de cada caja
param valor_pesos{CAJA};


# ----------------------------------------------------------------------------------------------
/* Variables de decisión */
# ----------------------------------------------------------------------------------------------

# Para cada posición en el pallet (FILAxCOLUMNAxALTURA),
# se indica mediante variables booleanas si una caja (representada por su valor de PRIORIDAD)
# se encuentra en esa posición
var cajas {p in CAJA, f in FILA, c in COLUMNA, n in NIVEL, k in PALLET} binary;

# Coste de cada posición en el pallet
var coste {f in FILA, c in COLUMNA, n in NIVEL, k in PALLET} >= 0;

# Variable que indica si un pallet está siendo utilizado
var pallet_usado {k in PALLET} binary;


# ----------------------------------------------------------------------------------------------
/* Función objetivo */
# ----------------------------------------------------------------------------------------------

# minimize Coste_Medio:
#     sum{p in CAJA, f in FILA, c in COLUMNA, n in NIVEL}
#         (valor_costes[p] * (f - 1) * cajas[p, f, c, n]) / num_cajas;
minimize Coste_Total:
    sum{f in FILA, c in COLUMNA, n in NIVEL, k in PALLET} coste[f, c, n, k]
    + coste_pallet * sum{k in PALLET} pallet_usado[k];


# ----------------------------------------------------------------------------------------------
/* Restricciones */
# ----------------------------------------------------------------------------------------------

# Cada caja solo se puede colocar una vez
s.t. Una_posicion_por_caja {p in CAJA}:
    sum{f in FILA, c in COLUMNA, n in NIVEL, k in PALLET} cajas[p, f, c, n, k] = 1;

# Como máximo una caja por hueco; si el pallet no se utiliza, no admite cajas
s.t. Una_caja_por_hueco {f in FILA, c in COLUMNA, n in NIVEL, k in PALLET}:
    sum{p in CAJA} cajas[p, f, c, n, k] <= pallet_usado[k];

# Las cajas de mayor prioridad deben estar delante de las de menor prioridad
s.t. Mayor_prioridad_delante {
    f in FILA, col1 in COLUMNA, col2 in COLUMNA, n in NIVEL, k in PALLET : f < longitud_pallet
}:
    sum{p in CAJA} (prioridad_vacia - valor_prioridades[p]) * cajas[p, f + 1, col1, n, k]
    >= sum{p in CAJA} (prioridad_vacia - valor_prioridades[p]) * cajas[p, f, col2, n, k];

# Las cajas no pueden soportar mas peso del que indican
# PARA CADA CAJA, QUE LA SUMA DE LOS PESOS DE LAS CAJAS SUPERIORES SEA MENOR QUE SU AGUANTE
s.t. Capacidad_maxima {f in FILA, c in COLUMNA, n1 in NIVEL, k in PALLET : n1 < niveles}:
    sum{p in CAJA, n2 in NIVEL : n2 > n1} valor_pesos[p] * cajas[p, f, c, n2, k]
    <= sum{p in CAJA} valor_aguantes[p] * cajas[p, f, c, n1, k];

# No puede haber cajas sobre un hueco, incluso si alguna tiene peso cero
s.t. Sin_cajas_sobre_huecos {f in FILA, c in COLUMNA, n in NIVEL, k in PALLET : n < niveles}:
    sum{p in CAJA} cajas[p, f, c, n + 1, k]
    <= sum{p in CAJA} cajas[p, f, c, n, k];

s.t. Calcular_coste {f in FILA, c in COLUMNA, n in NIVEL, k in PALLET}:
    coste[f, c, n, k] >=
        sum{p in CAJA, f2 in FILA : f2 > f} valor_costes[p] * cajas[p, f2, c, n, k]
        - (sum{p in CAJA} valor_costes[p]) * (1 - sum{p in CAJA} cajas[p, f, c, n, k]);

# Un pallet marcado como utilizado debe contener al menos una caja real
s.t. Pallet_no_vacio {k in PALLET}:
    pallet_usado[k] <=
        sum{p in CAJA, f in FILA, c in COLUMNA, n in NIVEL} cajas[p, f, c, n, k];

end;
