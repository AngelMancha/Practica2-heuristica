from constraint import *

problem = Problem()


#Variables
#1 movilidad reducida
#2 conflictivo
#3 normie (que no salga de aquí guarrona)

domain =[1,2,3]
problem.addVariable('alumno_1', [1, 2])
problem.addVariable('alumno_2', [1, 2, 3, 4])
problem.addVariable('alumno_3', [1, 2, 3, 4])

# Primera restricción: Todos los alumnos tienen que tener asignado un asiento

def todosAlumnosConAsiento(*args):
    #return all(alumno in list(args) for alumno in [1, 2, 3])
    for alumno in list(args):
        if alumno not in domain :
            return True


problem.addConstraint(todosAlumnosConAsiento, (['alumno_1', 'alumno_2', 'alumno_3']))

# Segunda restricción: Los alumnos de mov reducida deben dejar el asiendo de al lado libre

def no_al_lado(alumno_red, alumno_normie):
    if alumno_red % 2 == 0 and alumno_normie != alumno_red - 1:
        return True
    if alumno_red % 2 != 0 and alumno_normie != alumno_red + 1:
        return True


problem.addConstraint(no_al_lado, ('alumno_1', 'alumno_2'))
problem.addConstraint(no_al_lado, ('alumno_1', 'alumno_3'))


def not_encima(alumno_1, alumno_2):
    if alumno_1 != alumno_2:
        return True


problem.addConstraint(not_encima, ('alumno_1', 'alumno_2'))
problem.addConstraint(not_encima, ('alumno_1', 'alumno_3'))
problem.addConstraint(not_encima, ('alumno_2', 'alumno_3'))
print(problem.getSolutions())