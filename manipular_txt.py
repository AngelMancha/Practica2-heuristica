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


def output_astar(dict_alumno: str, path_out: str, cola_inicial: list, cola_final: list):
    """Esta función genera 2 ficheros: 'alumnosXH.output.prob  y 'alumnosXH.stat', donde X es el número
    del test y H es la heurística que utiliza."""
    value = extract_cola_inicial_astar('ASTAR-tests/alumnos1.prob')
    lista_inicial_asientos = value[0]
    dict_final= {}
    f = open(dict_alumno)
    linea = f.readline()
    len_cola = len(cola_final)
    counter = 0
    for alumno in cola_final:
        for item in lista_inicial_asientos:
            if item == alumno and counter < len_cola*2:
                asiento = lista_inicial_asientos[counter + 1]
                dict_final[alumno] = asiento
                counter += 2
                break
    return dict_final


hola = output_astar('ASTAR-tests/alumnos1.prob', None, None, ['4XX', '3CX', '1XX', '2XX', '6CX', '5XX'])

print(hola)
