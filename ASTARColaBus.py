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
    lista_final = []
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
        newNode.h = heuristics1(newNode.cola_final)
        list_children.append(newNode)

    return list_children



def insertarAlumnoCola(final_queue: Queue) -> int:
    coste_normal = 1
    coste_conflictivo = 1
    g = 0
    len_queue = final_queue.size()  # numero de alumnos en la cola inicialmente
    i: int = 0
    alumno_anterior = None
    coste_anterior = 0
    while i < len_queue:
        alumno = final_queue.dequeue()
        print("\nEl alumno es: ", alumno)
        if i == 0:
            if 'XX' in alumno:
                g += 1
                print("Coste del alumno: ", g)
            if 'XR' in alumno:
                g += 3
                print("Coste del alumno: ", g)
            if 'CX' in alumno:
                g += 1
                print("Coste del alumno: ", g)
        else:
            if 'XX' in alumno:
                if 'CX' in alumno_anterior:  # alumno conflictivo
                    g += 2
                    coste_anterior = 2
                    print("Coste del alumno: ", g)
                    print("Coste del alumno anterior: ", coste_anterior)

                if 'XR' in alumno_anterior:

                    print("El alumno anterior es un red, su coste es", coste_anterior)
                    g = g
                    print("Coste del alumno: ", g)
                    coste_anterior = 3
                    print("Coste del alumno anterior: ", coste_anterior)

                if 'XX' in alumno_anterior:
                    g += 1
                    coste_anterior = 1
                    print("Coste del alumno: ", g)
                    print("Coste del alumno anterior: ", coste_anterior)

            if 'XR' in alumno:
                if 'XX' in alumno_anterior:
                    g += 3
                    coste_anterior = 3
                    print("Coste del alumno: ", g)
                    print("Coste del alumno anterior: ", coste_anterior)

                if 'CX' in alumno_anterior:
                    g += 6
                    coste_anterior = 6
                    print("Coste del alumno: ", g)
                    print("Coste del alumno anterior: ", coste_anterior)

            if 'CX' in alumno:
                if 'XX' in alumno_anterior:
                    print("Coste del alumno anterior antes op: ", coste_anterior)
                    g = g + coste_anterior + coste_conflictivo
                    coste_anterior = 1
                    print("Coste del alumno: ", g)
                    print("Coste del alumno anterior: ", coste_anterior)

                if 'XR' in alumno_anterior:
                    g = g - coste_anterior + coste_anterior * 2 + coste_conflictivo
                    coste_anterior = 1
                    print("Coste del alumno: ", g)
                    print("Coste del alumno anterior: ", coste_anterior)

                if 'XC' in alumno:
                    g = g - coste_anterior + coste_anterior * 2 + coste_conflictivo
                    coste_anterior = 1
                    print("Coste del alumno: ", g)
                    print("Coste del alumno anterior: ", coste_anterior)
        print("\n Valor actual de g: ", g)
        #coste_anterior = g
        print("actualizacion del coste anterior:", coste_anterior, "\n")

        final_queue.enqueue(alumno)
        i += 1
        alumno_anterior = alumno
    return g

def heuristics1(final_queue: Queue) -> int:
    h: int = 0
    i: int = 0
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
    return 0

def heuristics2(final_queue: Queue) -> int:
    h: int = 0
    i: int = 0
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

def aStar(start, goal):
    openset = set()
    closedset = set()
    current = start
    openset.add(current)


    #While the open set is not empty
    while openset:

        current = min(openset, key=lambda o:o.g + o.h)  # luego sumar o.h

        if current.cola_inicial == goal.cola_inicial:
            #print("La cola final es: ", current.cola_final.display())
            #print("El coste de g es: ", current.g)
            #print("COSTE FINAL", insertarAlumnoCola(current.cola_final))
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        openset.remove(current)

        for nodoExpandido in expandirNodo(current):
           # print("EXPANDES", nodoExpandido.cola_final.display())
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


"""
value = aStar(initial_node, final_node)
for i in value:
    print(i.cola_final.display())
"""