/* PARTE 3 */

/* Parámetros del problema */
# Longitud del lado del pallet
param longitud_pallet;
# Número de niveles
param niveles;
# Número total de posiciones para las cajas
param num_cajas := niveles * longitud_pallet**2;

/* Conjuntos (sets) */
# Índices de las filas del pallet (1 = fila delantera)
set FILA := 1..longitud_pallet;
# Índices de las columnas del pallet 
set COLUMNA := 1..longitud_pallet;
# Índices de los diferentes niveles de altura
set NIVEL := 1..niveles;

# Identificadores de las cajas
set CAJA := 1..num_cajas;


param valor_prioridades{CAJA};
param valor_costes{CAJA};
param valor_aguantes{CAJA};
param valor_pesos{CAJA};

/* Variables de decisión */
# Para cada posición en el pallet (FILAxCOLUMNAxALTURA),
# se indica mediante variables booleanas si una caja (representada por su valor de PRIORIDAD)
# se encuentra en esa posición

var cajas {p in CAJA, f in FILA, c in COLUMNA, n in NIVEL} binary;
var coste {f in FILA, c in COLUMNA, n in NIVEL} >= 0;

/* Función objetivo */
#minimize Coste_Medio: sum{p in CAJA, f in FILA, c in COLUMNA, n in NIVEL} (valor_costes[p] * (f - 1) * cajas[p, f, c, n]) / num_cajas;
minimize Coste_Medio:
    sum{f in FILA, c in COLUMNA, n in NIVEL} coste[f,c,n]
    / (sum{p in CAJA: valor_costes[p] > 0} 1);
/* Restricciones */
# Cada caja solo se puede colocar una vez


s.t. Una_posicion_por_caja {p in CAJA}: sum{f in FILA, c in COLUMNA, n in NIVEL} cajas[p, f, c, n] = 1; 

# Tiene que haber una caja en cada hueco
s.t. Una_caja_por_hueco {f in FILA, c in COLUMNA, n in NIVEL}: sum{p in CAJA} cajas[p, f, c, n] = 1;




# Las cajas de mayor prioridad deben estar delante de las de menor prioridad
s.t. Mayor_prioridad_delante {f in FILA, col1 in COLUMNA, col2 in COLUMNA, n in NIVEL: f < longitud_pallet}: sum{p in CAJA} valor_prioridades[p] * cajas[p, f+1, col1, n] <= sum{p in CAJA} valor_prioridades[p] * cajas[p, f, col2, n];

# Las cajas no pueden soportar mas peso del que indican
# PARA CADA CAJA, QUE LA SUMA DE LOS PESOS DE LAS CAJAS SUPERIORES SEA MENOR QUE SU AGUANTE
s.t. Capacidad_maxima {f in FILA, c in COLUMNA, n1 in NIVEL: n1 < niveles}: sum{p in CAJA, n2 in NIVEL: n2 > n1} valor_pesos[p] * cajas[p, f, c, n2] <= sum{p in CAJA} valor_aguantes[p] * cajas[p, f, c, n1];

s.t. Calcular_coste {f in FILA, c in COLUMNA, n in NIVEL}:
    coste[f,c,n] >=
        sum{p in CAJA, f2 in FILA: f2 > f}
            valor_costes[p] * cajas[p,f2,c,n]
        - (sum{p in CAJA} valor_costes[p])
        * (sum{p in CAJA: valor_costes[p] = 0} cajas[p,f,c,n]);

end;
