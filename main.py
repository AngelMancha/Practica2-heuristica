from constraint import *

problem = Problem()


#Variables
#1 movilidad reducida
#2 conflictivo
#3 normie (que no salga de aquí guarrona)
#4 conflictivo
#5 con

domain =[1,2,3]
problem.addVariable('alumno_1', [1, 2])
problem.addVariable('alumno_2', [1, 2, 3, 4])
problem.addVariable('alumno_3', [1, 2, 3, 4])

# Primera restricción: Todos los alumnos tienen que tener asignado un asiento

def todosAlumnosConAsiento(*args: list) -> bool:
    #return all(alumno in list(args) for alumno in [1, 2, 3])
    for alumno in list(args):
        if alumno not in domain :
            return True


problem.addConstraint(todosAlumnosConAsiento, (['alumno_1', 'alumno_2', 'alumno_3']))

# Segunda restricción: Los alumnos de mov reducida deben dejar el asiendo de al lado libre

def no_al_lado(alumno_red: int, alumno_normie: int) -> bool:
    if alumno_red % 2 == 0 and alumno_normie != alumno_red - 1:
        return True
    if alumno_red % 2 != 0 and alumno_normie != alumno_red + 1:
        return True


problem.addConstraint(no_al_lado, ('alumno_1', 'alumno_2'))
problem.addConstraint(no_al_lado, ('alumno_1', 'alumno_3'))

# Tercera restricción: impide que un mismo asiento se le asigne a 2 alumnos
def not_encima(alumno_1: int, alumno_2: int) -> bool:
    if alumno_1 != alumno_2:
        return True

problem.addConstraint(not_encima, ('alumno_1', 'alumno_2'))
problem.addConstraint(not_encima, ('alumno_1', 'alumno_3'))
problem.addConstraint(not_encima, ('alumno_2', 'alumno_3'))

# Cuarta restricción: Si un asiento para una persona de movilidad reducida no está asignado, cualquier otro alumno
# se puede sentar en ese asiento: viene implícito en la forma en la que se ha modelado el problema


# Quinta restricción: No puede haber 2 alumnos conflictivos juntos en los asientos adyacentes
def comprobar_asientos_adyacentes(alumno_conflictivo1: int, alumno_conflictivo2: int) -> bool:
    for asiento in domain:
        if alumno_conflictivo1 == asiento:
            # comprobar asientos contiguos
            if alumno_conflictivo2 == asiento + 1 or alumno_conflictivo2 == asiento - 1:
                return False

            if alumno_conflictivo2 == asiento + 2 or alumno_conflictivo2 == asiento + 2:
                return False

            if alumno_conflictivo2 == asiento + 3 or alumno_conflictivo2 == asiento -3:
                return False


print(problem.getSolutions())