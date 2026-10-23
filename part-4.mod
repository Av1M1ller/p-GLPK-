/* PARTE 4: modelo multipallet adaptado a sol-4.py */

# -----------------------------------------------------------------------------
# Parámetros generales
# -----------------------------------------------------------------------------

# sol-4.py escribe en el .dat los parámetros L, H, P, n y m.
param L, integer, > 0;
param H, integer, > 0;
param P, >= 0;
param n, integer, > 0;

# sol-4.py también escribe m (número máximo de pallets disponibles).
# Se declara para que el parámetro del archivo .dat sea reconocido. Se conserva
# el límite de pallets del modelo original: ceil(n / L).
param m, integer, > 0;

# -----------------------------------------------------------------------------
# Conjuntos
# -----------------------------------------------------------------------------

set FILA    := 1..L;
set COLUMNA := 1..L;
set NIVEL   := 1..H;
set PALLET  := 1..ceil(n / L);
set CAJA    := 1..n;

# -----------------------------------------------------------------------------
# Datos de las cajas
# Los nombres coinciden con los que escribe sol-4.py en el .dat.
# -----------------------------------------------------------------------------

param prioridad{CAJA};
param peso{CAJA};
param capacidad{CAJA};

# sol-4.py no proporciona un vector de costes por caja. Para que el modelo
# pueda ejecutarse con sus datos actuales, se toma el coste de cada caja igual
# a su prioridad. Si los costes deben ser distintos de las prioridades, habrá
# que añadir valor_costes al .dat en sol-4.py.
param valor_costes{p in CAJA} := prioridad[p];

# Cota usada para representar el efecto de las posiciones vacías en la
# restricción de prioridades, conservando la formulación original.
param prioridad_vacia := (max{p in CAJA} prioridad[p]) + 1;

# -----------------------------------------------------------------------------
# Variables de decisión
# -----------------------------------------------------------------------------

# x[caja, fila, columna, altura, pallet], como espera sol-4.py al leer el
# archivo de salida de GLPK.
var x{p in CAJA, f in FILA, c in COLUMNA, a in NIVEL, q in PALLET} binary;

# Coste asociado a cada posición.
var coste{f in FILA, c in COLUMNA, a in NIVEL, q in PALLET} >= 0;

# Indica si un pallet se utiliza.
var pallet_usado{q in PALLET} binary;

# -----------------------------------------------------------------------------
# Función objetivo (misma estructura que el modelo original)
# -----------------------------------------------------------------------------

minimize Coste_Total:
    sum{f in FILA, c in COLUMNA, a in NIVEL, q in PALLET}
        coste[f, c, a, q]
    + P * sum{q in PALLET} pallet_usado[q];

# -----------------------------------------------------------------------------
# Restricciones
# -----------------------------------------------------------------------------

# Cada caja se coloca exactamente una vez.
s.t. Una_posicion_por_caja {p in CAJA}:
    sum{f in FILA, c in COLUMNA, a in NIVEL, q in PALLET}
        x[p, f, c, a, q] = 1;

# Como máximo una caja por hueco; un pallet no utilizado no admite cajas.
s.t. Una_caja_por_hueco {f in FILA, c in COLUMNA, a in NIVEL, q in PALLET}:
    sum{p in CAJA} x[p, f, c, a, q] <= pallet_usado[q];

# Las cajas de mayor prioridad deben estar delante de las de menor prioridad.
s.t. Mayor_prioridad_delante {
    f in FILA, col1 in COLUMNA, col2 in COLUMNA, a in NIVEL, q in PALLET
    : f < L
}:
    sum{p in CAJA}
        (prioridad_vacia - prioridad[p]) * x[p, f + 1, col1, a, q]
    >=
    sum{p in CAJA}
        (prioridad_vacia - prioridad[p]) * x[p, f, col2, a, q];

# Las cajas no pueden soportar más peso del que indica su capacidad.
s.t. Capacidad_maxima {f in FILA, c in COLUMNA, a1 in NIVEL, q in PALLET
                        : a1 < H}:
    sum{p in CAJA, a2 in NIVEL : a2 > a1}
        peso[p] * x[p, f, c, a2, q]
    <=
    sum{p in CAJA} capacidad[p] * x[p, f, c, a1, q];

# No puede haber cajas sobre un hueco, incluso si una caja pesa cero.
s.t. Sin_cajas_sobre_huecos {f in FILA, c in COLUMNA, a in NIVEL, q in PALLET
                              : a < H}:
    sum{p in CAJA} x[p, f, c, a + 1, q]
    <=
    sum{p in CAJA} x[p, f, c, a, q];

# Calcula el coste de una posición a partir de las cajas situadas detrás,
# conservando la expresión del modelo original.
s.t. Calcular_coste {f in FILA, c in COLUMNA, a in NIVEL, q in PALLET}:
    coste[f, c, a, q] >=
        sum{p in CAJA, f2 in FILA : f2 > f}
            valor_costes[p] * x[p, f2, c, a, q]
        - (sum{p in CAJA} valor_costes[p])
            * (1 - sum{p in CAJA} x[p, f, c, a, q]);

# Todo pallet marcado como utilizado debe contener alguna caja real.
s.t. Pallet_no_vacio {q in PALLET}:
    pallet_usado[q] <=
        sum{p in CAJA, f in FILA, c in COLUMNA, a in NIVEL}
            x[p, f, c, a, q];

end;
