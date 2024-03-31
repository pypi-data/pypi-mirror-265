import sympy as sp
import typing as tp

# transform the given sp matrix to vector
def matrixFloatToList(matrixVector: sp.Matrix) -> list[tp.Any]:
    solution: list[tp.Any] = []
    for i in range (0, matrixVector.rows):
        solution.append(matrixVector[i, 0])
    return solution

# transform the given sp matrix to string vector
def matrixFloatToListStr(matrixVector: sp.Matrix) -> list[str]:
    solution: list[str] = []
    for i in range (0, matrixVector.rows):
        solution.append(str(matrixVector[i, 0]))
    return solution