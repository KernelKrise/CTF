import os
import logging
from copy import deepcopy
from z3 import *


logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='[%(levelname)s]: %(message)s',
)
logger = logging.getLogger()

CURRENT_ITERATION = 1


def read_matrix():
    logger.info(f"CWD -> {os.getcwd()}")
    filename = ""
    for i in os.listdir(os.getcwd()):
        if f"lvl_{CURRENT_ITERATION}.txt" == i:
            logger.info(f'Find .txt file {i}')
            filename = i
            break

    with open(filename, 'r') as f:
        text = f.read()

    rows_raw = text.split('\n')
    matrix_raw = rows_raw[:rows_raw.index('')]

    logger.debug(f'Extracted {len(matrix_raw)}x{len(matrix_raw)} matrix')

    matrix = list()
    for i in matrix_raw:
        matrix.append(i.split(' '))

    contraints_raw = rows_raw[rows_raw.index('')+1:-1]
    constraints = list()
    for i in contraints_raw:
        constraints.append(i.split(' '))

    return matrix, constraints


def solve_matrix(matrix, constraints):
    s = Solver()

    # create array with z3 variables
    variables = dict()
    variables_z3 = list()
    for row in matrix:
        for element in row:
            if element not in variables:
                variables[element] = 1
            else:
                variables[element] +=1
            variables_z3.append(Int(f"{element}_{variables[element]}"))
    
    logger.debug(f"z3 variables -> {variables_z3}")
    
    # all variables in rows are not equal
    for i in range(0, len(variables_z3), len(matrix)):
        logger.debug(f"all variables in rows are not equal -> {variables_z3[i:i+len(matrix)]}")
        s.add(Distinct(variables_z3[i:i+len(matrix)]))
    
    # all variables in columns are not equal
    for i in range(len(matrix)):
        column = [variables_z3[i + j * len(matrix)] for j in range(len(matrix))]
        logger.debug(f"all variables in columns are not equal -> {column}")
        s.add(Distinct(column))

    # all variables > 0
    for i in variables_z3:
        logger.debug(f"all variables > 0 -> {i}")
        s.add(i > 0)

    # add group constraints
    for i, constraint in zip(sorted(variables.keys()), constraints):
        common_vars = list()
        for j in variables_z3:
            if i in str(j):
                common_vars.append(j)
        logger.debug(f"common variables -> {common_vars}")
        if constraint[2] == '+':
            logger.debug(f"sum of {common_vars} == {int(constraint[1])}")
            s.add(Sum(common_vars) == int(constraint[1]))
        elif constraint[2] == '-':
            logger.debug(f"diff of {common_vars} == {int(constraint[1])}")
            s.add(Or(
                common_vars[0] - common_vars[1] == int(constraint[1]),
                common_vars[1] - common_vars[0] == int(constraint[1])
                ))
        elif constraint[2] == '/':
            logger.debug(f"dev of {common_vars} == {int(constraint[1])}")
            s.add(Or(
                common_vars[0] / common_vars[1] == int(constraint[1]),
                common_vars[1] / common_vars[0] == int(constraint[1])
                ))
        elif constraint[2] == '*':
            logger.debug(f"mul of {common_vars} == {int(constraint[1])}")
            product = 1
            for var in common_vars:
                product *= var
            s.add(product == int(constraint[1]))        

    # all variables <= len(matrix)
    # print(len(matrix))
    for i in variables_z3:
        s.add(i <= len(matrix))
    
    # solve
    if s.check() == sat:
        model = s.model()

        print('Model:')
        delimiter = 0
        for i in variables_z3:
            print(model[i], end=' ')
            delimiter += 1
            if delimiter == len(matrix):
                print()
                delimiter = 0
        
        password = ""
        for i in variables_z3:
            password += str(model[i])
        logger.info(f"Password: {password}")
    else:
        raise Exception("Not satisfiable")
    
    return password

def extract_archive(password):
    filename = ""
    for i in os.listdir(os.getcwd()):
        if f"lvl_{CURRENT_ITERATION}.zip" == i:
            logger.info(f'Find .zip file {i}')
            filename = i
            break

    os.system(f"7z x -p{password} -o. {filename}")

    logger.info(f'{filename} extracted to CWD')
    logger.info(f'chdir to {os.getcwd()}')

def main():
    work = True
    flag = ""
    global CURRENT_ITERATION
    while work:
        matrix, constraints = read_matrix()
        password = solve_matrix(matrix, constraints)
        extract_archive(password)

        CURRENT_ITERATION += 1

        for i in os.listdir(os.getcwd()):
            if 'flag' in i:
                work = False
                flag = i
                break
    with open(flag, 'r') as f:
        print(f.read())
    

if __name__ == "__main__":
    main()
