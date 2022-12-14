# En este fichero tenemos las funciones basicas para trabajar con el fichero txt
import os
from random import randint


def rellenar_alumnos(path: str) -> list[list]:
    """En esta función devuelve una matriz a partir de los datos que haya en el fichero"""
    print('Abriendo fichero ' + path)
    matrix = []
    f = open(path)
    linea = f.readline()
    while linea:
        alumno = []
        linea = f.readline()
        al = linea.split(sep=', ')
        for i in al:
            if i.isdigit():
                alumno.append(int(i))
            if not i.isdigit() and i != ',' and i != ' ':
                if '\n' in i:
                    i = int(i[0])
                alumno.append(i)

        matrix.append(alumno)
    f.close()
    matrix.pop()
    print('Generando soluciones...\n')
    return matrix


def output(path: str, num_sol: int, random_sol: list, solution: dict) -> None:
    """Esta funcion genera un archivo con la solucion"""
    print('Generando fichero con soluciones...')
    file = open(path, 'w')
    file.write('Número de soluciones: ' + str(num_sol) + os.linesep)
    sorted_sol = sort_dict(sol_dict=solution)
    file.write(str(sorted_sol))
    file.write(os.linesep + 'Otras posibles soluciones')
    for i in range(0, 5):
        random_number = randint(0, num_sol-1)
        sorted_rand_sol = sort_dict(random_sol[random_number])
        file.write(os.linesep + str(sorted_rand_sol))
    print('Fichero', path, 'generado con éxito')


def sort_dict(sol_dict: dict) -> dict:
    """Esta funcion ordena el diccionario por valor"""
    return dict(sorted(sol_dict.items(), key=lambda item: item[1]))


def extract_cola_inicial_astar(path: str) -> list[list]:
    f = open(path)
    linea = f.readline()
    alumno = ""
    lista_ordenada = []
    cola_inical = []
    for character in linea:
        if character == " ":
            lista_ordenada.append(alumno)
            alumno = ""
            continue
        if character != "{" and character != "}" and character != "'" and character != "," and character != ":":
            alumno = alumno + character
    f.close()

    for item in lista_ordenada:
        if 'C' in item or 'X' in item or 'R' in item:
            cola_inical.append(item)

    return cola_inical
