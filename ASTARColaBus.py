from queue import Queue

class Node():
    def __init__(self, parent=None, position=None):
        self.cola_inicial = []
        self.cola_final = Queue
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0


def expandirNodo(current: Node) -> list:
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
        """if numeroHeuristica == 1:
            newNode.h = heuristics1(newNode.cola_final)
        elif numeroHeuristica == 2:
            newNode.h = heuristics2(newNode.cola_final)"""
        list_children.append(newNode)

    return list_children



def insertarAlumnoCola(final_queue: Queue) -> int:
    coste_conflictivo = 1
    g = 0
    len_queue = final_queue.size()  # numero de alumnos en la cola inicialmente
    i: int = 0
    alumno_anterior = None
    coste_anterior = 0
    while i < len_queue:
        alumno = final_queue.dequeue()
        print('Soy el alumno ', alumno)
        if i == 0:
            print('Soy el primer alumno', alumno)
            if 'XX' in alumno:
                g += 1
                print('El coste que genero es ', g)
            if 'XR' in alumno:
                g += 3
                print('El coste que genero es ', g)

            if 'CX' in alumno:
                g += 1
                print('El coste que genero es ', g)

        else:
            if 'XX' in alumno:
                if 'CX' in alumno_anterior:  # alumno conflictivo
                    g += 2
                    coste_anterior = 2
                    print('El coste que genero es ', g)

                if 'XR' in alumno_anterior:
                    g = g
                    coste_anterior = 3
                    print('El coste que genero es ', g)

                if 'XX' in alumno_anterior:
                    g += 1
                    coste_anterior = 1
                    print('El coste que genero es ', g)

            if 'XR' in alumno:
                if 'XX' in alumno_anterior:
                    g += 3
                    coste_anterior = 3
                    print('El coste que genero es ', g)

                if 'CX' in alumno_anterior:
                    g += 6
                    coste_anterior = 6
                    print('El coste que genero es ', g)

            if 'CX' in alumno:
                if 'XX' in alumno_anterior:
                    g = g + coste_anterior + coste_conflictivo
                    coste_anterior = 1
                    print('El coste que genero es ', g)

                if 'XR' in alumno_anterior:
                    g = g - coste_anterior + coste_anterior * 2 + coste_conflictivo
                    coste_anterior = 1
                    print('El coste que genero es ', g)

                if 'XC' in alumno:
                    g = g - coste_anterior + coste_anterior * 2 + coste_conflictivo
                    coste_anterior = 1
                    print('El coste que genero es ', g)

        final_queue.enqueue(alumno)
        i += 1
        alumno_anterior = alumno
    print('El coste total de esta cola es ', g)
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
    openset = set()
    closedset = set()
    current = start
    openset.add(current)


    #While the open set is not empty
    while openset:
       # for element in openset:
             #print('Openset cola final ', element.cola_final.display())
           # print('Openset cola inicial ', element.cola_inicial)
        current = min(openset, key=lambda o:o.g + o.h)  # luego sumar o.h

        if current.cola_inicial == goal.cola_inicial:
            #print("La cola final es: ", current.cola_final.display())
            #print("El coste de g es: ", current.g)
            print("COSTE FINAL", insertarAlumnoCola(current.cola_final))
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        openset.remove(current)

        for nodoExpandido in expandirNodo(current):
           # print("EXPANDES", nodoExpandido.cola_final.display())
            print('\nCola inicial nodo nodoExpandido: ', nodoExpandido.cola_inicial)
            print('Cola final nodo nodoExpandido: ', nodoExpandido.cola_final.display())
            #print('Coste parcial g del nodo nodoExpandido', nodoExpandido.g)
            #print('Coste heurística h del nodo nodoExpandido', nodoExpandido.h)
            #print('Función de evaluación nodo nodoExpandido', nodoExpandido.g + nodoExpandido.h)
            nodoExpandido.parent = current
            openset.add(nodoExpandido)

    #Throw an exception if there is no path
    raise ValueError('No Path Found')


initial_node=Node()
final_node=Node()
initial_node.cola_inicial = ['3XX', '5XR', '4CX']
#initial_node.cola_inicial = ['3XX', '4CX', '5XR']
initial_node.cola_final = Queue()

final_node.cola_inicial = []
final_node.cola_final = Queue()




queue =  Queue()
queue.enqueue('5CX')
queue.enqueue('3XR')
queue.enqueue('4XX')

value=insertarAlumnoCola(queue)
print("HOLAPUTAAAAAAAAAAAAAAAAAAAAA", value)


