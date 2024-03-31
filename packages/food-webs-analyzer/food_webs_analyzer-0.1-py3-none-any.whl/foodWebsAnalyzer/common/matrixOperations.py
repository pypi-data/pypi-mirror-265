# import common libraries
import sympy as sp

# import libraries
from ecosystems.data.foodWebData import FoodWebData
from ecosystems.data.symbolicData import SymbolicData

"""
check if the given matrix are equals

|1 2|        |1 2|
|3 4| equals |3 4| = True

|1 2|        |2 5|
|3 4| equals |3 6| = False

(note: reimplemented from sp + for visualising purposes)
"""
def equals(matrixA: sp.Matrix | sp.MatrixSymbol, matrixB: sp.Matrix | sp.MatrixSymbol, report: bool = True) -> bool:
    # check sizes
    if ((matrixA.cols != matrixB.cols) or (matrixA.rows != matrixB.rows)):
        if (report):
            sp.pprint("different sizes")
        return False
    # compare every cell
    for i in range(0, matrixA.rows):
        for j in range(0, matrixA.cols):
            if (matrixA[i, j] != matrixB[i, j]):
                if (report):
                    sp.pprint("MatrixA[" + str(i) + ", " + str(j) + "]:")
                    sp.pprint(matrixA[i, j])
                    sp.pprint("MatrixB[" + str(i) + ", " + str(j) + "]:")
                    sp.pprint(matrixB[i, j])
                    sp.pprint("Difference:")
                    sp.pprint(sp.simplify(matrixA[i, j] - matrixB[i, j]))
                return False
    # all equal, then return true
    return True

"""
sum the given nxn matrix with the given nxn matrix

|1 2|     |5 6|   |1+5 + 2+6|
|3 4| add |7 8| = |3+7 + 4+8|

(note: reimplemented from sp + for visualising purposes)
"""
def add(matrixA: sp.Matrix | sp.MatrixSymbol, matrixB: sp.Matrix | sp.MatrixSymbol) -> sp.Matrix:
    # check sizes
    if ((matrixA.cols != matrixB.cols) or (matrixA.rows != matrixB.rows)):
        raise Exception("sum only works for matrices with the same size. "
                        "Given " + str(matrixA.cols) + "x" + str(matrixA.rows) + " and " + str(matrixB.cols) + "x" + str(matrixB.rows))
    # reuse add from sympy
    return sp.Matrix(sp.MatAdd(matrixA, matrixB))

"""
rest the given nxn matrix by the given nxn matrix

|1 2|           |5 6|   |1-5 + 2-6|
|3 4| substract |7 8| = |3-7 + 4-8|

(note: reimplemented from sp - for visualising purposes)
"""
def substract(matrixA: sp.Matrix | sp.MatrixSymbol, matrixB: sp.Matrix | sp.MatrixSymbol) -> sp.Matrix:
    # check sizes
    if ((matrixA.cols != matrixB.cols) or (matrixA.rows != matrixB.rows)):
        raise Exception("substract only works for matrices with the same size. "
                        "Given " + str(matrixA.cols) + "x" + str(matrixA.rows) + " and " + str(matrixB.cols) + "x" + str(matrixB.rows))
    # reuse substract from sympy
    return sp.Matrix(matrixA - matrixB)

"""
multiply the given nxn matrix by the given nxn matrix

|1 2|         |5 6|   |1*5 + 2*6|
|3 4| product |7 8| = |3*7 + 4*8|

(note: reimplemented from sp * for visualising purposes)
"""
def product(matrixA: sp.Matrix | sp.MatrixSymbol, matrixB: sp.Matrix | sp.MatrixSymbol) -> sp.Matrix:
    # reuse product from sympy
    return sp.Matrix(sp.MatMul(matrixA, matrixB))

"""
multiply the given nxn matrix by the given nxn matrix

|1 2|                  |5 6|   |1*5 2*6|
|3 4| hadamard_product |7 8| = |3*7 4*8|

(note: reimplemented from sp.hadamard_product(...) for visualising purposes
"""
def hadamard_product(matrixA: sp.Matrix | sp.MatrixSymbol, matrixB: sp.Matrix | sp.MatrixSymbol) -> sp.Matrix:
    # check sizes
    if ((matrixA.cols != matrixB.cols) or (matrixA.rows != matrixB.rows)):
        raise Exception("hadamard_product only works for matrices with the same size. "
                        "Given " + str(matrixA.cols) + "x" + str(matrixA.rows) + " and " + str(matrixB.cols) + "x" + str(matrixB.rows))
    # reuse hadamard_product from sympy
    return sp.Matrix(sp.hadamard_product(matrixA, matrixB))

"""
multiply the given nxn matrix by the given n*1 vector

|1 2|            |5|   |1*5 2*6|
|3 4| mul_vector |6| = |3*5 2*6|
"""
def hadamard_product_vector(matrix: sp.Matrix | sp.MatrixSymbol, vector: sp.Matrix | sp.MatrixSymbol) -> sp.Matrix:
    # check sizes
    if ((matrix.cols != vector.rows) or (matrix.rows != vector.rows)):
        raise Exception("hadamard_product_vector only works for nxn matrix and n*1 vectors. "
                        "Given " + str(matrix.cols) + "x" + str(matrix.rows) + " and " + str(vector.cols) + "x" + str(vector.rows))
    # create a zero matrix as solution
    hadamardProductMatrix: sp.Matrix = sp.Matrix(sp.ZeroMatrix(matrix.cols, vector.rows))
    for i in range(0, hadamardProductMatrix.rows):
        for j in range(0, hadamardProductMatrix.cols):
            hadamardProductMatrix[i,j] = matrix[i, j] * vector[j, 0]
    return hadamardProductMatrix

"""
divide the given nxn matrix by the given nxn matrix

|1 2|                   |5 6|   |1/5 2/6|
|3 4| hadamard_division |7 8| = |3/7 2/8|
"""
def hadamard_division(matrixA: sp.Matrix | sp.MatrixSymbol, matrixB: sp.Matrix | sp.MatrixSymbol, zeroAlternative: float = 0) -> sp.Matrix:
    # check sizes
    if ((matrixA.cols != matrixB.cols) or (matrixA.rows != matrixB.rows)):
        raise Exception("hadamard_division only works for matrices with the same size. "
                        "Given " + str(matrixA.cols) + "x" + str(matrixA.rows) + " and " + str(matrixB.cols) + "x" + str(matrixB.rows))
    # create a zero matrix as solutions
    hadamardDivisionMatrix: sp.Matrix = sp.Matrix(sp.ZeroMatrix(matrixA.rows, matrixA.cols))
    for i in range(0, hadamardDivisionMatrix.rows):
        for j in range(0, hadamardDivisionMatrix.cols):
            # check if in matrixB[i, j] is zero
            if (matrixB[i, j] == 0):
                # check if we're provided a alternative for zero
                if (zeroAlternative != 0):
                    print("division by 0 in hadamard_division. Using zero alternative '" + str(zeroAlternative) + "'")
                    hadamardDivisionMatrix[i,j] = matrixA[i, j] / zeroAlternative
                else:
                    raise Exception("division by 0 in hadamard_division. stop.")
            else:
                hadamardDivisionMatrix[i,j] = matrixA[i, j] / matrixB[i, j]
    return hadamardDivisionMatrix

"""
divide the given nxn matrix by the given n*1 vector

|1 2|                          |5|   |1/5 2/6|
|3 4| hadamard_division_vector |6| = |3/5 2/6|
"""
def hadamard_division_vector(matrix: sp.Matrix | sp.MatrixSymbol, vector: sp.Matrix | sp.MatrixSymbol, zeroAlternative: float = 0) -> sp.Matrix:
    # check sizes
    if ((matrix.cols != vector.rows) or (matrix.rows != vector.rows)):
        raise Exception("hadamard_division_vector only works for nxn matrix and n*1 vectors. "
                        "Given " + str(matrix.cols) + "x" + str(matrix.rows) + " and " + str(vector.cols) + "x" + str(vector.rows))
    # create a zero matrix as solution
    hadamardDivisionMatrix: sp.Matrix = sp.Matrix(sp.ZeroMatrix(matrix.cols, vector.rows))
    for i in range(0, hadamardDivisionMatrix.rows):
        for j in range(0, hadamardDivisionMatrix.cols):
            # check if in vector[j, 0] is zero
            if (vector[j, 0] == 0):
                # check if we're provided a alternative for zero
                if (zeroAlternative != 0):
                    print("division by 0 in hadamard_division_vector. Using zero alternative '" + str(zeroAlternative) + "'")
                    hadamardDivisionMatrix[i,j] = matrix[i, j] / zeroAlternative
                else:
                    raise Exception("division by 0 in hadamard_division_vector. stop.")
            else:
                hadamardDivisionMatrix[i,j] = matrix[i, j] / vector[j, 0]
    return hadamardDivisionMatrix

"""
calculate the sumatorial of the given matrix using criterium x dot

|1 2|                   |1+2|
|3 4| sumatorial_dotx = |3+4|
"""
def sumatorial_xdot(matrix: sp.Matrix | sp.MatrixSymbol) -> sp.Matrix:
    # create solution matrix
    sumatorialMatrix: sp.Matrix = sp.Matrix(sp.ZeroMatrix(matrix.rows, 1))
    # from top to bot, iterate over all values and sum elements
    for i in range(0, matrix.rows):
        for j in range(0, matrix.cols):
            sumatorialMatrix[i, 0] += matrix[i, j]
    return sumatorialMatrix

"""
calculate the sumatorial of the given matrix using criterium dot x

|1 2|                   |1+3|
|3 4| sumatorial_dotx = |2+4|
"""
def sumatorial_dotx(matrix: sp.Matrix | sp.MatrixSymbol) -> sp.Matrix:
   # simply traspose matrix and apply sumatorial xdot
   return sumatorial_xdot(matrix.transpose())

"""
calculate the diagonal of the given matrix
"""
def diagonal(matrix: sp.Matrix | sp.MatrixSymbol) -> sp.Matrix:
    if (matrix.cols == 1):
        # create diagonal solution
        diagonalRowMatrix: sp.Matrix = sp.Matrix(sp.ZeroMatrix(matrix.rows, matrix.rows))
        # iterate over matrix
        for i in range(0, matrix.rows):
            diagonalRowMatrix[i, i] = matrix[i, 0]
        return diagonalRowMatrix
    elif (matrix.rows == 1):
        # create diagonal solution
        diagonalColMatrix: sp.Matrix = sp.Matrix(sp.ZeroMatrix(matrix.cols, matrix.cols))
        # iterate over matrix
        for i in range(0, matrix.cols):
            diagonalColMatrix[i, i] = matrix[0, i]
        return diagonalColMatrix
    else:
        raise Exception("this method only works for vector matrix (1xn) or (nx1). Given " + str(matrix.cols) + "x" + str(matrix.rows))