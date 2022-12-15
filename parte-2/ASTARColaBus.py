import manipular_txt
import sys
import time
from queue import Queue


PATH = sys.argv[1]
numeroHeuristica=sys.argv[2]
PATH_OUT_PROB: str = 'parte-2/ASTAR-tests-output/' + PATH[20:28] + '_' + str(numeroHeuristica) + '.output.prob'
PATH_OUT_STAT: str = 'parte-2/ASTAR-tests-output/' + PATH[20:28] + '_' + str(numeroHeuristica) + '.stat'
nodos_expandidos = 0

class Node():
    def __init__(self, parent=None, position=None):
        self.cola_inicial = []
        self.cola_final = Queue
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0


def expandirNodo(current: Node) -> list:
    """Esta funcion genera los nodos hijos dado un nodo padre"""
    list_children = []
    cola_inicial = current.cola_inicial
    cola_final = current.cola_final
    for i in cola_inicial:
        newNode = Node()
        newNode.parent = current
        for j in cola_inicial:
            newNode.cola_inicial.append(j)
        newNode.cola_inicial.remove(i) # eliminamos al alumno de la cola inicial
        newNode.cola_final = Queue()
        for e in cola_final.display():
            newNode.cola_final.enqueue(e)
        newNode.cola_final.enqueue(i)
        newNode.g = insertarAlumnoCola(newNode.cola_final)
        if numeroHeuristica == 1:
            newNode.h = heuristics1(newNode.cola_final)
        elif numeroHeuristica == 2:
            newNode.h = heuristics2(newNode.cola_final)
        list_children.append(newNode)
    return list_children



def insertarAlumnoCola(final_queue: Queue) -> int:
    """ Esta función inserta un alumno en la cola final y devuelve el coste g """
    coste_conflictivo = 1
    g = 0
    len_queue = final_queue.size()  # numero de alumnos en la cola inicialmente
    i: int = 0
    alumno_anterior = ""
    coste_anterior = 0
    while i < len_queue:
        alumno = final_queue.dequeue()
        if i == 0:
            if 'XX' in alumno:
                g += 1
            if 'XR' in alumno:
                g += 3
            if 'CX' in alumno:
                g += 1
        else:
            if 'XX' in alumno:
                if 'CX' in alumno_anterior:  # alumno conflictivo
                    g += 2
                    coste_anterior = 2
                if 'XR' in alumno_anterior:
                    g = g
                    coste_anterior = 3

                if 'XX' in alumno_anterior:
                    g += 1
                    coste_anterior = 1

            if 'XR' in alumno:
                if 'XX' in alumno_anterior:
                    g += 3
                    coste_anterior = 3

                if 'CX' in alumno_anterior:
                    g += 6
                    coste_anterior = 6

                if 'XR' in alumno_anterior:
                    g += 1111111111
                    coste_anterior = 1111111111

            if 'CX' in alumno:
                if 'XX' in alumno_anterior:
                    g = g + coste_anterior + coste_conflictivo
                    coste_anterior = 1
                if 'XR' in alumno_anterior:
                    g = g - coste_anterior + coste_anterior * 2 + coste_conflictivo
                    coste_anterior = 1
                if 'CX' in alumno:
                    g = g - coste_anterior + coste_anterior * 2 + coste_conflictivo
                    coste_anterior = 1
        final_queue.enqueue(alumno)
        i += 1
        alumno_anterior = alumno
    return g

def heuristics1(final_queue: Queue) -> int:
    """ Esta heurística depende del tipo de alumno que estemos insertando en la cola. """
    h, i = 0, 0
    len_queue = final_queue.size()  # numero de alumnos en la cola inicialmente
    while i < len_queue:
        alumno = final_queue.dequeue()
        if 'XX' in alumno:
            h += 1
        if 'XR' in alumno:
            h += 2
        if 'CX' in alumno:
            h += 2
        final_queue.enqueue(alumno)
        i += 1
    return h

def heuristics2(final_queue: Queue) -> int:
    """ Esta heurística relaja la restricción de que los alumnos conflictivos duplican el tiempo de los que van delante
    y de los que van detrás. """
    h, i, alumno_anterior = 0, 0, 0
    len_queue = final_queue.size()  # numero de alumnos en la cola inicialmente
    while i < len_queue:
        alumno = final_queue.dequeue()
        if i == 0:
            if 'XX' in alumno:
                h += 1
            if 'XR' in alumno:
                h += 3
            if 'CX' in alumno:
                h += 1
        else:
            if 'XX' in alumno:
                if 'CX' in alumno_anterior:  # alumno conflictivo
                    h += 1
                if 'XR' in alumno_anterior:
                    h = h
                if 'XX' in alumno_anterior:
                    h += 1
            if 'XR' in alumno:
                h += 3
            if 'CX' in alumno:
                h += 1
        final_queue.enqueue(alumno)
        i += 1
        alumno_anterior = alumno
    return h


def aStar(start, goal):
    """ Función que implementa el algoritmo A*. Dado un estado inicial, tenemos que conseguir llegar a un estado final.
    En esta función se definen 2 sets, uno de ABIERTO y otro de CERRADO. """
    global nodos_expandidos
    openset = set()
    closedset = set()
    current = start
    openset.add(current)
    #While the open set is not empty
    while openset:
       # for element in openset:
        current = min(openset, key=lambda o:o.g + o.h)  # luego sumar o.h
        if current.cola_inicial == goal.cola_inicial:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        openset.remove(current)
        for nodoExpandido in expandirNodo(current):
            nodoExpandido.parent = current
            openset.add(nodoExpandido)
            nodos_expandidos += 1

    #Throw an exception if there is no path
    raise ValueError('No Path Found')



#  Definimos los estados iniciales y finales
if __name__ == "__main__":
    initial_node = Node()  # estado incial
    final_node = Node()   # estado final
    initial_node.cola_inicial = manipular_txt.extract_cola_inicial_astar(PATH)[1]
    initial_node.cola_final = Queue()
    final_node.cola_inicial = []
    final_node.cola_final = Queue()
    inicio = time.time()
    value = aStar(initial_node, final_node)
    for i in value:
        final_sol_aux = i.cola_final.display()
        coste = i.g
    sol = []
    for i in range(0, len(final_sol_aux)):
        sol.append(final_sol_aux.pop())
    fin = time.time()
    tiempo_total = (fin - inicio) * 1000
    longitud_plan = len(sol)
    output = manipular_txt.output_astar_prob(PATH, PATH_OUT_PROB, sol)
    output_stat = manipular_txt.generar_fichero_stat(int(tiempo_total), coste, longitud_plan, nodos_expandidos, PATH_OUT_STAT)