############ ESTO ES UNA PRUEBA DEL SEÑOR
from constraint import *
from itertools import combinations
from random import randint
import os
problem = Problem()

def rellenar_alumnos():
    matrix=[]
    f = open('CSP-tests/alumnos6.txt')
    linea = f.readline()
    while linea:
        alumno = []
        linea = f.readline()
        al = linea.split(sep=', ')
        for i in al:
            if i.isdigit():
                alumno.append(int(i))
            if not i.isdigit() and i != ',' and i != ' ':
                if '\n' in i:
                    i = int(i[0])
                alumno.append(i)

        matrix.append(alumno)
    f.close()
    matrix.pop()
    return matrix


#Obtenemos los alumnos contenidos en el fichero input
alumnos = rellenar_alumnos()

autobus = [[1, 2, -1, 3, 4],
           [5, 6, -1, 7, 8],
           [-1, -1, -1, -1, -1],
           [9, 10, -1, 11, 12],
           [13, 14, -1, 15, 16]]




dom_red_c1, dom_red_c2, dom_c1, dom_c2, asientos, autobus_num = [], [], [], [], [], []
dict_alumnos = {}

def reducir_bus(autobus):
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
    #dom_red_c1.remove(-1)
    asientos = dom_c1 + dom_c2


reducir_bus(autobus)

def get_caracteristicas(index):
    return alumnos[index][0], alumnos[index][1], alumnos[index][2], alumnos[index][3], alumnos[index][4]

def assign_domain(alumnos):
    for i in range(0, len(alumnos)):
        id, ciclo, movilidad, conflictivo, hermano = get_caracteristicas(i)
        id_alumno = str(id) + str(movilidad) + str(conflictivo)
        if id not in dict_alumnos.keys():
            if hermano == 0 and ciclo == 1:
                asignar_dom_c1(id_alumno)
            if hermano == 0 and ciclo == 2:
                asignar_dom_c2(id_alumno)
            if hermano != 0:
                asignar_dom_hermanos(id_alumno, hermano-1, ciclo)
        problem.addVariable(id_alumno, dict_alumnos[id_alumno])


def asignar_dom_c2(id_alumno):
    if 'R' in id_alumno:
        dict_alumnos[id_alumno] = dom_red_c2
    else:
        dict_alumnos[id_alumno] = dom_c2

def asignar_dom_c1(id_alumno):
    if 'R' in id_alumno:
        dict_alumnos[id_alumno] = dom_red_c1
    else:
        dict_alumnos[id_alumno] = dom_c1

def asignar_dom_hermanos(id_alumno, hermano, ciclo):
    id_hermano, ciclo_hermano, movilidad_hermano, conflictivo_hermano = alumnos[hermano][0], alumnos[hermano][1], alumnos[hermano][2], alumnos[hermano][3]
    id_h = str(id_hermano) + str(movilidad_hermano) + str(conflictivo_hermano)
    if ('R' in id_h and ciclo_hermano == 2) or ('R' in id_alumno and ciclo == 2):
        asignar_dom_c2(id_alumno)
        asignar_dom_c2(id_h)
    else:
        asignar_dom_c1(id_alumno)
        asignar_dom_c1(id_h)

assign_domain(alumnos)

# Primera restricción: Todos los alumnos tienen que tener asignado un asiento
def todosAlumnosConAsiento(*args: list) -> bool:
    #return all(alumno in list(args) for alumno in [1, 2, 3])
    for alumno in list(args):
        if alumno not in asientos:
            return False
    return True

problem.addConstraint(todosAlumnosConAsiento, dict_alumnos.keys())

# Segunda restricción: impide que un mismo asiento se le asigne a 2 alumnos
def not_encima(alumno_1: int, alumno_2: int) -> bool:
    if alumno_1 != alumno_2:
        return True

for alumno in combinations(dict_alumnos.keys(), 2):
    problem.addConstraint(not_encima, (alumno[0], alumno[1]))

# Tercera restricción: Los alumnos de mov reducida deben dejar el asiendo de al lado libre

def no_al_lado(alumno_red: int, alumno_normie: int) -> bool:
    if alumno_red % 2 == 0 and alumno_normie != alumno_red - 1:
        return True
    if alumno_red % 2 != 0 and alumno_normie != alumno_red + 1:
        return True

for alumno_conflictivo in dict_alumnos.keys():
    if 'R' in alumno_conflictivo:
        for alumno in dict_alumnos.keys():
            if alumno != alumno_conflictivo:
                problem.addConstraint(no_al_lado, (alumno_conflictivo, alumno))


# Cuarta restricción: Si un asiento para una persona de movilidad reducida no está asignado, cualquier otro alumno
# se puede sentar en ese asiento: viene implícito en la forma en la que se ha modelado el problema

# Quinta restricción: No puede haber 2 alumnos conflictivos juntos en los asientos adyacentes
def comprobar_asientos_adyacentes(alumno_conflictivo: int, alumno: int) -> bool:
    count_fila, count_col = 0, 0
    fila_conflictivo, columna_conflictivo = 0, 0
    for fila in autobus_num:
        for asiento in fila:
            if alumno_conflictivo == asiento:
                fila_conflictivo = count_fila
                columna_conflictivo = count_col
            if alumno == asiento:
                fila_otro = count_fila
                columna_otro = count_col
            count_col += 1
        count_fila += 1
        count_col = 0
    if abs(fila_conflictivo-fila_otro) <= 1 and abs(columna_conflictivo-columna_otro) <= 1:
        return False
    return True


def comprobar_hermanos(alumno_1: str, alumno_2: str):
    cond1, cond2 = False, False
    for al in alumnos:
        if al[0] == int(alumno_1[0]):
            if al[4] == int(alumno_2[0]):  # el alumno1 es hermano del alumno2
                cond1 = True

    for al in alumnos:
        if al[0] == int(alumno_2[0]):
            if al[4] == int(alumno_1[0]):  # el alumno2 es hermano del alumno1
                cond2 = True
    if cond1 and cond2:
        return True

    else:
        return False


for alumno_conflictivo in dict_alumnos.keys():
    if 'C' in alumno_conflictivo:
        for alumno in dict_alumnos.keys():
            #print('alumno1: ', alumno_conflictivo, ' alumno2: ', alumno)
            son_hermanos = comprobar_hermanos(alumno_conflictivo, alumno)
            #print('¿Son hermanos?', son_hermanos)
            if not son_hermanos:
                #print('no somos hermanos')
                if alumno != alumno_conflictivo and ('R' in alumno or 'C' in alumno):
                    problem.addConstraint(comprobar_asientos_adyacentes, (alumno_conflictivo, alumno))


def get_asiento(alumno: int) -> tuple:
    count_fila = 0
    for fila in autobus_num:
        count_col = 0
        for asiento in fila:
            if alumno == asiento:
                return count_fila, count_col
            count_col +=1
        count_fila +=1


def get_ciclo(alumno)-> int:
    for al in alumnos:
        if al[0] == int(alumno[0]):
            return al[1]

def get_movilidad(alumno)-> int:
    if alumno[1] == 'R':
        return True

def al_lado(alumno1, alumno2):
    if (alumno1 % 2 == 0) and (alumno2 == alumno1 - 1):

        return True
    if (alumno1 % 2 != 0) and (alumno2 == alumno1 + 1):

        return True

def hermanos_ciclo1_ciclo2(hermano_c1: int, hermano_c2: int) -> bool:
    f_c2 = get_asiento(hermano_c2)
    f_h2, c_h2 = f_c2[0], f_c2[1]
    if c_h2 == 1:
        if (hermano_c2 % 2 == 0) and (hermano_c1 == hermano_c2 - 1):
            return True
    if c_h2 == 2:
        if (hermano_c2 % 2 != 0) and (hermano_c1 == hermano_c2 + 1):
            return True


for alumno in combinations(dict_alumnos.keys(), 2):
    son_hermanos = False
    son_hermanos = comprobar_hermanos(alumno[0], alumno[1])
    if son_hermanos:
        hermano1 = alumno[0]
        hermano2 = alumno[1]
        ciclo_hermano1 = get_ciclo(hermano1)
        ciclo_hermano2 = get_ciclo(hermano2)
        movilidad_hermano1 = get_movilidad(hermano1)
        movilidad_hermano2 = get_movilidad(hermano2)

        if not movilidad_hermano2 and not movilidad_hermano1:
            if ciclo_hermano1 == ciclo_hermano2:
                problem.addConstraint(al_lado, (hermano1, hermano2))
            if ciclo_hermano1 != ciclo_hermano2:
                if ciclo_hermano1 == 1:
                    problem.addConstraint(hermanos_ciclo1_ciclo2, (hermano1, hermano2))
                else:
                    problem.addConstraint(hermanos_ciclo1_ciclo2, (hermano2, hermano1))

        son_hermanos = False


num_sol = len(problem.getSolutions())

solutions = problem.getSolutions()

#print("El número de soluciones es", num_sol)
sol1 = problem.getSolution()

sorted_sol = dict(sorted(sol1.items(), key=lambda item:item[1]))


file = open('CSP-tests-output/alumnos6.output.txt', 'w')
file.write('Numero soluciones: ' + str(num_sol) + os.linesep)
file.write('Una posible solucion es: ' + str(sorted_sol))
counter = 0
print('Generando soluciones...')
random1 = randint(0, num_sol-1)
random2 = randint(0, num_sol-1)
random3 = randint(0, num_sol-1)
random4 = randint(0, num_sol-1)

file.write(os.linesep + str(solutions[random1]))
file.write(os.linesep + str(solutions[random2]))
file.write(os.linesep + str(solutions[random3]))
