PATH: str = 'CSP-tests/'


with open('CSP-tests/alumnos1.txt') as file:
    alumnos = []
    alum, al = [], []
    for linea in file:
        al.clear()
        alum.clear()
        print(alum)
        print(alumnos)
        al = linea.split(sep=', ')
        for element in al:
            if element.isdigit():
                alum.append(int(element))
            if not element.isdigit():
                if '\n' in element:
                    element = int(element[0])
                alum.append(element)
        alumnos.append(alum)
        print(alum)
        print(alumnos)



#print(alumnos)
