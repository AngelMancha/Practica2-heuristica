from constraint import *
from itertools import combinations
problem = Problem()


#Variables
#1 movilidad reducida
#2 conflictivo
#3 normie (que no salga de aquí guarrona)
#4 conflictivo
#5 con

dominio_reducido = [1, 2]
domain_ciclo1 = [1, 2, 3, 4, 5 ,6 ,7 ,8]
domain_ciclo2 = [9, 10, 11, 12]
asientos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

problem.addVariable('alumno_1', dominio_reducido)
problem.addVariable('alumno_2', domain_ciclo1)
problem.addVariable('alumno_3', domain_ciclo1)
problem.addVariable('alumno_conflictivo4', domain_ciclo2)
problem.addVariable('alumno_conflictivo5', domain_ciclo2)
problem.addVariable('alumno_ciclo1', domain_ciclo1 )
problem.addVariable('alumno_ciclo2', domain_ciclo1)

lista_alumnos = ['alumno_1', 'alumno_2','alumno_3','alumno_conflictivo4','alumno_conflictivo5','alumno_ciclo1','alumno_ciclo2']
lista_alumnos_red = ['alumno_1']
lista_alumnos_con = ['alumno_2','alumno_conflictivo4', 'alumno_conflictivo5' ]

# Primera restricción: Todos los alumnos tienen que tener asignado un asiento

def todosAlumnosConAsiento(*args: list) -> bool:
    #return all(alumno in list(args) for alumno in [1, 2, 3])
    for alumno in list(args):
        if alumno not in asientos:
            return False
    return True

problem.addConstraint(todosAlumnosConAsiento, (['alumno_1', 'alumno_2', 'alumno_3', 'alumno_conflictivo4', 'alumno_conflictivo5']))

# Segunda restricción: Los alumnos de mov reducida deben dejar el asiendo de al lado libre

def no_al_lado(alumno_red: int, alumno_normie: int) -> bool:
    if alumno_red % 2 == 0 and alumno_normie != alumno_red - 1:
        return True
    if alumno_red % 2 != 0 and alumno_normie != alumno_red + 1:
        return True


problem.addConstraint(no_al_lado, ('alumno_1', 'alumno_2'))
problem.addConstraint(no_al_lado, ('alumno_1', 'alumno_3'))
problem.addConstraint(no_al_lado, ('alumno_1', 'alumno_conflictivo4'))
problem.addConstraint(no_al_lado, ('alumno_1', 'alumno_conflictivo5'))
problem.addConstraint(no_al_lado, ('alumno_1', 'alumno_ciclo1'))
problem.addConstraint(no_al_lado, ('alumno_1', 'alumno_ciclo2'))

# Tercera restricción: impide que un mismo asiento se le asigne a 2 alumnos
def not_encima(alumno_1: int, alumno_2: int) -> bool:
    if alumno_1 != alumno_2:
        return True


for alumno in combinations(lista_alumnos, 2):
    problem.addConstraint(not_encima, (alumno[0], alumno[1]))


# Cuarta restricción: Si un asiento para una persona de movilidad reducida no está asignado, cualquier otro alumno
# se puede sentar en ese asiento: viene implícito en la forma en la que se ha modelado el problema

primera_fila = [1, 2, 3, 4]
ultima_fila = [9, 10, 11, 12]

# Quinta restricción: No puede haber 2 alumnos conflictivos juntos en los asientos adyacentes
def comprobar_asientos_adyacentes(alumno_conflictivo1: int, alumno_conflictivo2: int) -> bool:
    for asiento in asientos:
        if alumno_conflictivo1 == asiento:
            #ASIENTOS PARES
            if alumno_conflictivo1 % 2 == 0:
                #asientos está en la primera fila
                if asiento in primera_fila:
                    # comprobamos el caso que el asiento sea 2
                    if asiento == 2 and (alumno_conflictivo2 == 5 or alumno_conflictivo2 == 6 or alumno_conflictivo2 == 7 or \
                            alumno_conflictivo2 == 3 or alumno_conflictivo2 == 1) :
                        return False
                    # en otro caso estoy en el asiento 4
                    if asiento == 4 and (alumno_conflictivo2 == 7 or alumno_conflictivo2 == 3 or alumno_conflictivo2 == 8) :
                        return False

                #asiento está en la última fila
                if asiento in ultima_fila:
                    #alumno en ventana inferior
                    if (asiento)%4 == 0 and (alumno_conflictivo2 == asiento - 1 or alumno_conflictivo2 == asiento -5 or alumno_conflictivo2 == asiento -4):
                        return False
                    #no está en ventana inferior
                    else:
                        if alumno_conflictivo2 == asiento -1 or alumno_conflictivo2 == asiento +1 or \
                                alumno_conflictivo2 == asiento -5 or alumno_conflictivo2 == asiento -4 or \
                                alumno_conflictivo2 == asiento -3:
                            return False

                #asientos que no están en la última fila ni en la primera
                else:
                        #si no estoy en ventana inferior
                        if asiento % 4 != 0:
                               if alumno_conflictivo2 == alumno_conflictivo1 + 1 or \
                                       alumno_conflictivo2 == alumno_conflictivo1 -1 or \
                                       alumno_conflictivo2 == alumno_conflictivo1 -3 or \
                                       alumno_conflictivo2 == alumno_conflictivo1 -4 or \
                                       alumno_conflictivo2 == alumno_conflictivo1 -5 or \
                                       alumno_conflictivo2 == alumno_conflictivo1 +3 or \
                                       alumno_conflictivo2 == alumno_conflictivo1 +4 or \
                                       alumno_conflictivo2 == alumno_conflictivo1+5:
                                   return False

                        #si estoy en ventana inferior
                        else:

                            if alumno_conflictivo2 == alumno_conflictivo1 - 1 or \
                                    alumno_conflictivo2 == alumno_conflictivo1 - 4 or \
                                    alumno_conflictivo2 == alumno_conflictivo1 - 5 or \
                                    alumno_conflictivo2 == alumno_conflictivo1 + 3 or \
                                    alumno_conflictivo2 == alumno_conflictivo1 + 4:
                                return False

            if alumno_conflictivo1 % 2 != 0:
                if asiento in primera_fila:
                    # comprobamos el caso que el asiento sea 1
                    if asiento == 1 and (alumno_conflictivo2 == 2 or alumno_conflictivo2 == 4 or alumno_conflictivo2 == 5 or \
                            alumno_conflictivo2 == 6):
                        return False
                    # en otro caso estoy en el asiento 3
                    if alumno_conflictivo2 == 2 or alumno_conflictivo2 == 4 or alumno_conflictivo2 == 6 or \
                            alumno_conflictivo2 == 7 or alumno_conflictivo2 == 8:
                        return False

                if asiento in ultima_fila:
                    #asiento está en la ventana superior
                    if (asiento-1)%4 == 0 and (alumno_conflictivo2 == asiento + 1 or
                                               alumno_conflictivo2 == asiento -4 or alumno_conflictivo2 == asiento -3):
                        return False
                    #asiento no está en la ventana superior
                    else:
                        if alumno_conflictivo2 == asiento -1 or alumno_conflictivo2 == asiento +1 or \
                                alumno_conflictivo2 == asiento -5 or alumno_conflictivo2 == asiento -4 or \
                                alumno_conflictivo2 == asiento -3:
                            return False
                # no estamos en la primera fila ni en la última fila
                else:
                    #si estamos en la ventana superior
                    if (asiento-1)%4 == 0:
                        if alumno_conflictivo2 == asiento - 3 or alumno_conflictivo2 == asiento - 4 or \
                                alumno_conflictivo2 == asiento + 1 or alumno_conflictivo2 == asiento + 4 or \
                                alumno_conflictivo2 == asiento + 5:
                            return False
                    else:
                        if alumno_conflictivo2 == asiento -5 or alumno_conflictivo2 == asiento - 4 \
                                or alumno_conflictivo2 == asiento - 3 \
                                or alumno_conflictivo2 == asiento - 1 or alumno_conflictivo2 == asiento + 1 \
                                or alumno_conflictivo2 == asiento + 3 or alumno_conflictivo2 == asiento + 4 \
                                or alumno_conflictivo2 == asiento +5:
                            return False

    return True

#for x in combinations(lista_alumnos_red + lista_alumnos_con, 2):
    #problem.addConstraint(comprobar_asientos_adyacentes, (x[0], x[1]))

problem.addConstraint(comprobar_asientos_adyacentes, ('alumno_conflictivo4', 'alumno_conflictivo5'))
problem.addConstraint(comprobar_asientos_adyacentes, ('alumno_conflictivo4', 'alumno_1'))
problem.addConstraint(comprobar_asientos_adyacentes, ('alumno_conflictivo5', 'alumno_1'))
problem.addConstraint(comprobar_asientos_adyacentes, ('alumno_2', 'alumno_1'))
problem.addConstraint(comprobar_asientos_adyacentes, ('alumno_2', 'alumno_conflictivo4'))
problem.addConstraint(comprobar_asientos_adyacentes, ('alumno_2', 'alumno_conflictivo5'))

# Sexta restricción: alumnos de 1er ciclo alante, los tontitos viejos atras


print(problem.getSolutions())