#!/usr/bin/env python3

def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    for row in matrix:
        row.reverse()
    return matrix

matrix_1 = [[3,2,1],[6,5,4]]
print("before: ", matrix_1)
print("after: ", mirror_matrix(matrix_1))

matrix_2 = [[42]]
print("before: ", matrix_2)
print("after: ", mirror_matrix(matrix_2))

matrix_3 = [[1,2,3,4,5]]
print("before: ", matrix_3)
print("after: ", mirror_matrix(matrix_3))

matrix_4 = [[-1,-2],[-3,-4]]
print("before: ", matrix_4)
print("after: ", mirror_matrix(matrix_4))