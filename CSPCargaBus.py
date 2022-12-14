import sys
import manipular_txt
from constraint import *
from itertools import combinations


PATH: str = sys.argv[1]
PATH_OUT: str = 'CSP-tests-output/' + PATH[10:18] + '.output.txt'

#  Rellenamos la matriz de alumnos obtenida del fichero input
alumnos = manipular_txt.rellenar_alumnos(PATH)

#  Creamos la matriz que representa los asientos del autobús. El pasillo y
#  y la separación entre ciclo 1 y ciclo 2 queda representado por -1
AUTOBUS = [[1, 2, -1, 3, 4],
           [5, 6, -1, 7, 8],
           [9, 10, -1, 11, 12],
           [13, 14, -1, 15, 16],
           [-1, -1, -1, -1, -1],
           [17, 18, -1, 19, 20],
           [21, 22, -1, 23, 24],
           [25, 26, -1, 27, 28],
           [29, 30, -1, 31, 32]]

#  Inicializamos los dominios
dom_red_c1, dom_red_c2, dom_c1, dom_c2, asientos, autobus_num = [], [], [], [], [], []
dict_alumnos = {}

problem = Problem()


#  Primero definimos funciones auxiliares que va a utilizar nuestro
#  programa antes de comenzar con el problema

def reducir_bus(autobus: list[list]) -> None:
    """Esta función se encarga de dar valor a los dominios a partir del bus"""
    global dom_red_c1, dom_c1, dom_c2, asientos, dom_red_c2
    counter = 0
    dom_red_c1 = autobus[0]
    for fila in autobus:
        if fila != [-1, -1, -1, -1, -1]:
            fila.remove(-1)
            dom_c1 = fila + dom_c1
            autobus_num.append(fila)
        if fila == [-1, -1, -1, -1, -1]:
            dom_red_c1 += autobus[counter - 1]
            break
        counter = counter + 1
    dom_red_c2 = autobus[counter+1]
    for i in range(counter + 1, len(autobus)):
        fila = autobus[i]
        fila.remove(-1)
        dom_c2 = fila + dom_c2
        autobus_num.append(fila)
    dom_c1.sort()
    dom_c2.sort()
    dom_red_c1.sort()
    dom_red_c2.sort()
    asientos = dom_c1 + dom_c2


#  ----  Funciones para asignar los dominios correspondientes a los alumnos ----
def assign_domain() -> None:
    """Esta función se encarga de asignar dominios a cada alumno dadas unas características. Recibe como argumento
    una matriz 'alumnos' y va añadiendo cada alumno con su respectivo dominio al diccionario dict_alumnos.
    Una vez hecho esto añade las variables al problema"""
    for i in range(0, len(alumnos)):
        id_alumno, ciclo, conflictivo, movilidad,  hermano = get_caracteristicas(i)
        id_alumno = str(id_alumno) + str(conflictivo) + str(movilidad)
        if id_alumno not in dict_alumnos.keys():
            if hermano == 0 and ciclo == 1:
                asignar_dom_c1(id_alumno)
            if hermano == 0 and ciclo == 2:
                asignar_dom_c2(id_alumno)
            if hermano != 0:
                asignar_dom_hermanos(id_alumno, hermano-1, ciclo)
        problem.addVariable(id_alumno, dict_alumnos[id_alumno])


def asignar_dom_c2(id_alumno: str) -> None:
    """Esta función asigna el dominio de ciclo 2 a los alumnos correspondientes"""
    if 'R' in id_alumno:
        dict_alumnos[id_alumno] = dom_red_c2
    else:
        dict_alumnos[id_alumno] = dom_c2


def asignar_dom_c1(id_alumno: str) -> None:
    """Esta función asigna el dominio de ciclo 1 a los alumnos correspondientes"""
    if 'R' in id_alumno:
        dict_alumnos[id_alumno] = dom_red_c1
    else:
        dict_alumnos[id_alumno] = dom_c1


def asignar_dom_hermanos(id_alumno: str, hermano: int, ciclo: int) -> None:
    """Esta función le asigna el dominio correspondiente a un par de hermanos"""
    id_hermano, ciclo_hermano, conflictivo_hermano, movilidad_hermano = alumnos[hermano][0], alumnos[hermano][1], \
        alumnos[hermano][2], alumnos[hermano][3]
    id_h = str(id_hermano) + str(movilidad_hermano) + str(conflictivo_hermano)
    if ('R' in id_h and ciclo_hermano == 2) or ('R' in id_alumno and ciclo == 2):
        asignar_dom_c2(id_alumno)
        asignar_dom_c2(id_h)
    else:
        asignar_dom_c1(id_alumno)
        asignar_dom_c1(id_h)


#  ----  Funciones para obtener información de los alumnos ----

def get_asiento(asiento_alumno: int) -> tuple:
    """Esta función obtiene el asiento del alumno"""
    count_fila = 0
    for fila in autobus_num:
        count_col = 0
        for asiento in fila:
            if asiento_alumno == asiento:
                return count_fila, count_col
            count_col += 1
        count_fila += 1


def get_ciclo(datos_alumno) -> int:
    """Esta función obtiene el ciclo de un alumno"""
    for al in alumnos:
        if al[0] == int(datos_alumno[0]):
            return al[1]


def get_movilidad(datos_alumno) -> int:
    """Esta función obtiene la movilidad de un alumno"""
    if datos_alumno[1] == 'R':
        return True
    return False


def get_caracteristicas(index: int) -> tuple:
    """Esta función devuelve una tuple con las características de los alumnos dado un índice"""
    return alumnos[index][0], alumnos[index][1], alumnos[index][2], alumnos[index][3], alumnos[index][4]


def comprobar_hermanos(alumno_1: str, alumno_2: str) -> bool:
    """Esta función comprueba si un par de alumnos son hermanos. Si lo son devuelve True, en otro caso False"""
    cond1, cond2 = False, False
    for al in alumnos:
        if (al[0] == int(alumno_1[0])) and al[4] == int(alumno_2[0]):  # el alumno1 es hermano del alumno2
            cond1 = True
        if (al[0] == int(alumno_2[0])) and al[4] == int(alumno_1[0]):  # el alumno2 es hermano del alumno1
            cond2 = True
    if cond1 and cond2:
        return True
    return False


# ---- Funciones que representan las restricciones del problema ----

def todos_alumnos_con_asiento(*args: list) -> bool:
    """Esta función obliga a todos los alumnos a tener un asiento asignado"""
    for al in list(args):
        if al not in asientos:
            return False
    return True


def not_encima(alumno_1: int, alumno_2: int) -> bool:
    """Esta función hace que 2 alumnos no tengan asignado el mismo asiento"""
    if alumno_1 != alumno_2:
        return True


def no_al_lado(alumno_red: int, alumno_normie: int) -> bool:
    """Esta función hace que al lado de un alumno reducido no se siente nadie"""
    if alumno_red % 2 == 0 and alumno_normie != alumno_red - 1:
        return True
    if alumno_red % 2 != 0 and alumno_normie != alumno_red + 1:
        return True


def comprobar_asientos_adyacentes(alumno_conf: int, alumno_normal: int) -> bool:
    """Esta función hace que un alumno conflictivo no se siente al lado de otro alumno conflictivo
    o un alumno con movilidad reducida en los asientos adyacentes"""
    count_fila, count_col, fila_otro, columna_otro = 0, 0, 0, 0
    fila_conflictivo, columna_conflictivo = 0, 0
    for fila in autobus_num:
        for asiento in fila:
            if alumno_conf == asiento:
                fila_conflictivo = count_fila
                columna_conflictivo = count_col
            if alumno_normal == asiento:
                fila_otro = count_fila
                columna_otro = count_col
            count_col += 1
        count_fila += 1
        count_col = 0
    if abs(fila_conflictivo-fila_otro) <= 1 and abs(columna_conflictivo-columna_otro) <= 1:
        return False
    return True


def al_lado(alumno1: int, alumno2: int) -> bool:
    """Esta funcion hace que dos hermanos se sienten juntos siempre si ninguno
    de los dos es de mov. reducida"""
    if (alumno1 % 2 == 0) and (alumno2 == alumno1 - 1):
        return True
    if (alumno1 % 2 != 0) and (alumno2 == alumno1 + 1):
        return True
    return False


def hermanos_ciclo1_ciclo2(hermano_c1: int, hermano_c2: int) -> bool:
    """Esta funcion asegura que cuando haya dos hermanos de diferentes ciclos,
    el mayor siempres se siente en la parte más cercana al pasillo"""
    f_c2 = get_asiento(hermano_c2)
    f_h2, c_h2 = f_c2[0], f_c2[1]
    if c_h2 == 1:
        if (hermano_c2 % 2 == 0) and (hermano_c1 == hermano_c2 - 1):
            return True
    if c_h2 == 2:
        if (hermano_c2 % 2 != 0) and (hermano_c1 == hermano_c2 + 1):
            return True
    return False


# ---- FUNCIÓN QUE EJECUTA LA SOLUCIÓN LLAMANDO A TODAS LAS RESTRICCIONES DEL PROBLEMA ----
def ejecutar_solucion():
    # Primera restricción: Todos los alumnos tienen que tener asignado un asiento
    problem.addConstraint(todos_alumnos_con_asiento, dict_alumnos.keys())

    for alumno_conflictivo in dict_alumnos.keys():
        # Segunda restricción: Los alumnos comflictivos no se pueden sentar cerca de ningún otro conflictivo ni reducido
        if 'C' in alumno_conflictivo:
            for alumno in dict_alumnos.keys():
                son_hermanos = comprobar_hermanos(alumno_conflictivo, alumno)
                if not son_hermanos:
                    if alumno != alumno_conflictivo and ('R' in alumno or 'C' in alumno):
                        problem.addConstraint(comprobar_asientos_adyacentes, (alumno_conflictivo, alumno))

        # Tercera restricción: al lado de cada alumno con mov. reducida no se sienta nadie
        if 'R' in alumno_conflictivo:
            for alumno in dict_alumnos.keys():
                if alumno != alumno_conflictivo:
                    problem.addConstraint(no_al_lado, (alumno_conflictivo, alumno))

    for alumno in combinations(dict_alumnos.keys(), 2):
        # Cuarta restricción: impide que un mismo asiento se le asigne a 2 alumnos
        problem.addConstraint(not_encima, (alumno[0], alumno[1]))

        # Quinta restricción: Hermanos
        son_hermanos = comprobar_hermanos(alumno[0], alumno[1])
        if son_hermanos:
            hermano1, hermano2 = alumno[0], alumno[1]
            ciclo_hermano1, ciclo_hermano2 = get_ciclo(hermano1), get_ciclo(hermano2)
            movilidad_hermano1, movilidad_hermano2 = get_movilidad(hermano1), get_movilidad(hermano2)
            # Si ninguno de los dos es de movilidad reducida:
            if not movilidad_hermano2 and not movilidad_hermano1:

                # Si ambos pertenecen al mismo ciclo, se sentarán al lado
                if ciclo_hermano1 == ciclo_hermano2:
                    problem.addConstraint(al_lado, (hermano1, hermano2))

                # Si pertenecen a ciclos diferentes, el mayor se sienta en ventana
                if ciclo_hermano1 != ciclo_hermano2:
                    if ciclo_hermano1 == 1:
                        problem.addConstraint(hermanos_ciclo1_ciclo2, (hermano1, hermano2))
                    else:
                        problem.addConstraint(hermanos_ciclo1_ciclo2, (hermano2, hermano1))
            son_hermanos = False


reducir_bus(AUTOBUS)

#  Ejecutamos función que asigna los dominos a las variables
assign_domain()

#  Ejecutamos función que calcula la solución final
ejecutar_solucion()

#  Guardamos en los ficheros output la solución obtenida
manipular_txt.output(PATH_OUT, len(problem.getSolutions()), problem.getSolutions(), problem.getSolution())
