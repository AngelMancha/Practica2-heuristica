from queue import Queue

class Node():
    def __init__(self, parent=None, position=None):
        self.cola_inicial = []
        self.cola_final = Queue
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def children(self, current):
        list_children = []
        cola_inicial=current.cola_inicial
        cola_final=current.cola_final
        ultimo_alumno_cola_final = cola_final.pop()
        for i in current.cola_inicial:
            newNode = Node()
            newNode.parent = current
            newNode.cola_inicial=cola_inicial
            newNode.cola_inicial.remove(i)
            newNode.cola_inicial=cola_final
            newNode.cola_final.enqueue(i)
            newNode.g = self.checkCoste(newNode, i, ultimo_alumno_cola_final)
            list_children.append(newNode)

        return list_children


    def checkCoste(self, newNode, alumno, ultimo_alumno):
        g = 0

        if newNode.cola_final.size() > 1:
            # normal
            if alumno[1]=='X' and alumno[2] == 'X':
                #normal después de normal
                if ultimo_alumno[1]=='X' and ultimo_alumno[2] == 'X':
                    g = 1
                    return g
                #normal después de reducido
                if ultimo_alumno[1]=='R' and ultimo_alumno[2] == 'X':
                    g = 0

                if ultimo_alumno[1] == 'R' and ultimo_alumno[2] == 'R':
                    g = 000




    def moverAlumno(self, alumno):
        if len(self.cola_inicial) == 0:
            return False
        self.cola_inicial.remove(alumno)
        self.cola_final.enqueue(alumno)
        self.g = 1


    def moverAlumnoReducido(self, alumno):
        if len(self.cola_inicial) == 0:
            self.g=00

