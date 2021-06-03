from salesman import SalesMan

matrix = [
    [ 0., 20, 18, 12,  8],
    [ 5,  0, 14,  7, 11],
    [12, 18,  0,  6, 11],
    [11, 17, 11,  0, 12],
    [ 5,  5,  5,  5,  0],
]

print(SalesMan(matrix).solve())

matrix = [
    [0., 7, 12, 25, 10],
    [10, 0, 9,  5, 11],
    [13,  8, 0, 6,  4],
    [6, 11, 15, 0, 15],
    [0,  9, 12, 17, 0]
]

print()
print(SalesMan(matrix).solve())

matrix = [
    [0., 68, 73, 24, 70,  9],
    [58, 0, 16, 44, 11, 92],
    [63, 9, 0, 86,  13, 18],
    [17, 34, 76, 0, 52, 70],
    [60, 18,  3, 45, 0, 58],
    [16, 82, 11, 60, 48, 0]
]

print()
print(SalesMan(matrix).solve())

# Task: V 12 -> v 4

matrix = [
    [0., 6, 0, 15, 27,  19],
    [58, 0, 16, 44, 11, 9],
    [2, 9, 0, 86,  0, 36],
    [17, 69, 56, 0, 52, 12],
    [6, 18,  31, 45, 0, 48],
    [16, 12, 0, 60, 48, 0]
]

salesman = SalesMan(matrix)
# print(salesman.base)
print(salesman.solve(tracing=True))
