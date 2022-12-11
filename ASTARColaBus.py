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


def children(current: Node) -> list:
        list_children = []
        cola_inicial=current.cola_inicial
        cola_final=current.cola_final
        ultimo_alumno_cola_final = cola_final.pop()
        for i in current.cola_inicial:
            newNode = Node()
            newNode.parent = current
            for j in cola_inicial:
                newNode.cola_inicial.append(j)
            newNode.cola_inicial.remove(i) # eliminamos al alumno de la cola inicial

            newNode.cola_final = Queue()
            for e in cola_final.display():
                newNode.cola_final.enqueue(e)

            newNode.cola_final.enqueue(i)
            newNode.g = moverAlumno(newNode.cola_final)
            list_children.append(newNode)

        return list_children




def moverAlumno(final_queue: Queue) -> int:
    coste_normal = 1
    coste_conflictivo = 1
    g = 0
    len_queue = final_queue.size()  # numero de alumnos en la cola inicialmente
    i: int = 0
    alumno_anterior = None
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
                    coste_anterior = 0
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
            if 'CX' in alumno:
                if 'XX' in alumno_anterior:
                    g = g - coste_anterior + coste_anterior * 2 + coste_conflictivo
                    coste_anterior = 1
                if 'XR' in alumno_anterior:
                    g = g - coste_anterior + coste_anterior * 2 + coste_conflictivo
                    coste_anterior = 1
                if 'XC' in alumno:
                    g = g - coste_anterior + coste_anterior * 2 + coste_conflictivo
                    coste_anterior = 1

        final_queue.enqueue(alumno)
        i += 1
        alumno_anterior = alumno
    return g

def heuristics():
    pass

def aStar(start, goal):
    # The open and closed sets
    openset = set()
    closedset = set()
    # Current point is the starting point
    current = start
    # Add the starting point to the open set
    openset.add(current)
    # While the open set is not empty
    while openset:
        print('Open set not empty', openset)
        #Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o:o.g)  # luego sumar o.h
        #print("CURRENT", current.cola_final)
        print('Current node initial: ', current.cola_inicial)
        print('Current node final queue: ', current.cola_final.display())
        #If it is the item we want, retrace the path and return it
        if current.cola_inicial == goal.cola_inicial:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent

            path.append(current)
            print("COSTEEEE", current.g)
            return path[::-1]
        #Remove the item from the open set
        openset.remove(current)
        #Add it to the closed set
        closedset.add(current)
        #Loop through the node's children/siblings
        for node in children(current):
            #If it is already in the closed set, skip it
            if node in closedset:
                continue
            #Otherwise if it is already in the open set
            if node in openset:
                #Check if we beat the G score
                new_g = current.g
                if node.g > new_g:
                    #If so, update the node to have a new parent
                    node.g = new_g
                    node.parent = current
            else:
                #If it isn't in the open set, calculate the G and H score for the node
                node.g = current.g
                node.h = heuristics()
                #Set the parent to our current item
                node.parent = current
                #Add it to the set
                openset.add(node)
            print('Closed set', closedset)
    #Throw an exception if there is no path
    raise ValueError('No Path Found')


initial_node=Node()
final_node=Node()

initial_node.cola_inicial = ['3XX', '4CX', '5XR']
initial_node.cola_final = Queue()

final_node.cola_inicial = []
final_node.cola_final = Queue()


"""
value=children(initial_node)
for i in value:
    print("CHILDREN", i.cola_final.display())
"""

value = aStar(initial_node, final_node)
for i in value:
    print(i.cola_final.display())
