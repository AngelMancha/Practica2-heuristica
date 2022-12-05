############ ESTO ES UNA PRUEBA DEL SEÑOR
from constraint import *
from itertools import combinations
problem = Problem()

alumnos = [[1, 1, 'X', 'X', 0],
           [2, 1, 'X', 'X', 0],
           [3, 1, 'X', 'X', 4],
           [4, 2, 'X', 'X', 3],
           [5, 2, 'X', 'X', 0],
           [6, 2, 'X', 'X', 0]]


autobus = [[1, 2, -1, 3, 4],
           [5, 6, -1, 7, 8],
           [-1, -1, -1, -1, -1],
           [9, 10, -1, 11, 12],
           [13, 14, -1, 15, 16]
           ]

dom_red_c1, dom_red_c2, dom_c1, dom_c2, asientos, autobus_num, dom_hermanos = [], [], [], [], [], [], []
dict_alumnos = {}

def reducir_bus(autobus):
    global dom_red_c1, dom_c1, dom_c2, asientos, dom_red_c2, dom_hermanos
    counter = 0
    dom_red_c1 = autobus[0]
    for fila in autobus:
        if fila != [-1, -1, -1, -1, -1]:
            fila.remove(-1)
            dom_c1 = fila + dom_c1
            autobus_num.append(fila)
        if fila == [-1, -1, -1, -1, -1]:
            #dom_red_c1 += autobus[counter - 1]
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
    dom_hermanos = asientos

reducir_bus(autobus)


#Crear diccionario de alumnos que asigna domino a los alumnos
def assign_dom(alumnos):
    for i in range(0, len(alumnos)):
        id = str(alumnos[i][0]) + str(alumnos[i][2]) + str(alumnos[i][3])
        ciclo = alumnos[i][1]
        movilidad = alumnos[i][3]
        hermano = alumnos[i][4]
        if ciclo == 1 and movilidad != 'R' and hermano == 0: #alumno ciclo 1 no reducidol
            dict_alumnos[id] = dom_c1
            problem.addVariable(id, dom_c1)
        if ciclo == 1 and movilidad == 'R'and hermano == 0: #alumno ciclo 1 reducidol
            dict_alumnos[id] = dom_red_c1
            problem.addVariable(id, dom_red_c1)
        if ciclo == 2 and movilidad != 'R'and hermano == 0: #alumnos ciclo 2 no reducido
            dict_alumnos[id] = dom_c2
            problem.addVariable(id, dom_c2)
        if ciclo == 2 and movilidad == 'R'and hermano == 0: #alumno ciclo 2 reducidol
            dict_alumnos[id] = dom_red_c1
            problem.addVariable(id, dom_red_c1)

        if hermano != 0:
            for j in range(0, len(alumnos)):
                id_hermano = alumnos[j][0]
                id_her = str(alumnos[j][0]) + str(alumnos[j][2]) + str(alumnos[j][3])
                ciclo_her = alumnos[j][1]
                movilidad_her = alumnos[j][3]
                hermano_her = alumnos[j][4]
                if hermano == id_hermano:

                    if ciclo != ciclo_her and movilidad != 'R' and movilidad_her != 'R':
                        if id not in dict_alumnos.keys() and id_her not in dict_alumnos.keys():
                            dict_alumnos[id] = dom_c1
                            dict_alumnos[id_her] = dom_c1

assign_dom(alumnos)

print(dict_alumnos)
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
    count_fila = 0
    count_col = 0
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


for alumno_conflictivo in dict_alumnos.keys():
    if 'C' in alumno_conflictivo:
        for alumno in dict_alumnos.keys():
            if alumno != alumno_conflictivo and ('R' in alumno or 'C' in alumno):
                problem.addConstraint(comprobar_asientos_adyacentes, (alumno_conflictivo, alumno))



def hermanos(hermano1: int, hermano2: int) -> bool:
    f_c1 = get_asiento(hermano1)
    f_h1, c_h1 = f_c1[0], f_c1[1]

    f_c2 = get_asiento(hermano2)
    f_h2, c_h2 = f_c2[0], f_c2[1]

    if dict_alumnos.get(hermano1) == dom_c1 and dict_alumnos.get(hermano2) == dom_c2:
        if autobus[f_h2][c_h2-1] == -1 or autobus[f_h2][c_h2+1] == -1:
            if (hermano2 % 2 == 0) and (hermano1 == hermano2 - 1):
                print("\n\nEl hermano2 es el grande y su asiento es", hermano2)
                print("El hermano1 es el pequeño y su asiento es", hermano1)
                return True
            if (hermano2 % 2 != 0) and (hermano1 == hermano2 + 1):
                print("\n\nEl hermano2 es el grande y su asiento es", hermano2)
                print("El hermano1 es el pequeño y su asiento es", hermano1)
                return True

    if dict_alumnos.get(hermano1) == dom_c2 and dict_alumnos.get(hermano2) == dom_c1:
        if autobus[f_h1][c_h1-1] == -1 or autobus[f_h1][c_h1+1] == -1:
            if (hermano1 % 2 == 0) and (hermano2 == hermano1 - 1):
                print("\n\nEl hermano1 es el grande y su asiento es", hermano1)
                print("El hermano2 es el pequeño y su asiento es", hermano2)
                return True
            if (hermano1 % 2 != 0) and (hermano2 == hermano1 + 1):
                print("\n\nEl hermano1 es el grande y su asiento es", hermano1)
                print("El hermano2 es el pequeño y su asiento es", hermano2)
                return True
    # si los hermanos pertenecen al mismo ciclo

    if (hermano1 % 2 == 0) and (hermano2 == hermano1 - 1):
        return True
    if (hermano1 % 2 != 0) and (hermano2 == hermano1 + 1):
        return True
    return False


def get_asiento(alumno: int) -> tuple:
    count_fila = 0
    count_col = 0
    for fila in autobus_num:
        for asiento in fila:
            if alumno == asiento:
                return count_fila, count_col

def al_lado(alumno1, alumno2):
    if (alumno1 % 2 == 0) and (alumno2 == alumno1 - 1):
        return True
    if (alumno1 % 2 != 0) and (alumno2 == alumno1 + 1):
        return True


problem.addConstraint(hermanos, ('4XX', '3XX'))

#num_sol = len(problem.getSolutions())

#print(problem.getSolutions())
#print("El número de soluciones es", num_sol)
#print(problem.getSolution())