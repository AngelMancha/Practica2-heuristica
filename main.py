
PATH: str = 'CSP-tests/'
alumnos = []

with open('CSP-tests/alumnos1.txt') as file:

    alum, al = [], []
    for linea in file:
        al.clear()
        al = linea.split(sep=', ')
        for element in al:
            if element.isdigit():
                alum.append(int(element))
            if not element.isdigit():
                if '\n' in element:
                    element = element[0]
                alum.append(element)
       # print(alum)
        alumnos.append(alum)


print(alumnos)
""" 
if i != ',' and  not in i and i !=' ':
     if i.isdigit():
         alumno.append(int(i))
     if not i.isdigit():
         alumno.append(i)"""

