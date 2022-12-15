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


def extract_cola_inicial_astar(path_in: str):
    f = open(path_in)
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
    asiento_ultimo = linea[len(linea)-3] + linea[len(linea)-2]
    lista_ordenada.append(asiento_ultimo)
    f.close()
    for item in lista_ordenada:
        if 'C' in item or 'X' in item or 'R' in item:
            cola_inical.append(item)
    return lista_ordenada, cola_inical


def output_astar_prob(path_in: str, path_out: str, cola_final: list) -> None:
    """Esta función genera 2 ficheros: 'alumnosXH.output.prob donde X es el número
    del test y H es la heurística que utiliza."""
    f = open(path_in)
    fichero_original = f.readline()
    value = extract_cola_inicial_astar(path_in)
    lista_inicial_asientos = value[0]
    dict_final = convertir_diccionario(lista_inicial_asientos, cola_final)
    print('Generando fichero', path_out)
    file = open(path_out, 'w')
    file.write('INCIAL: ' + fichero_original + os.linesep)
    file.write('FINAL:  ' + str(dict_final))
    print('Solución generada')


def generar_fichero_stat(tiempo: int, coste: int, longitud: int, nodos_exp: int, path_out: str):
    """Esta funcion genera un fichero con la extensión 'alumnosXH.stat', donde X es el número
    del test y H es la heurística que utiliza."""
    print('Generando fichero', path_out)
    file = open(path_out, 'w')
    file.write('Tiempo total: ' + str(tiempo) + os.linesep)
    file.write('Coste total:  ' + str(coste) + os.linesep)
    file.write('Longitud del plan:  ' + str(longitud) + os.linesep)
    file.write('Nodos expandidos:  ' + str(nodos_exp) + os.linesep)
    print('Solución generada')


def convertir_diccionario(lista_inicial_asientos: list, cola_final: list) -> dict:
    """Esta función devuelve un diccionario con los asientos correspondientes a los alumnos"""
    dict_final = {}
    len_cola = len(cola_final)
    counter = 0
    for alumno in cola_final:
        for item in lista_inicial_asientos:
            if item == alumno and counter < len_cola * 2:
                asiento = lista_inicial_asientos[counter + 1]
                dict_final[alumno] = int(asiento)
                break
            counter += 1
        counter = 0
    return dict_final
