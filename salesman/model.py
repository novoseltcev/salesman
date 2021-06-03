import numpy as np


class Matrix:
    def __init__(self, matrix):
        self.array = np.array(matrix)
        self._normalize()
        self.base = self.array.copy()

    def search_null(self):
        null_indexes = np.where(self.array == 0)
        return list(zip(null_indexes[0], null_indexes[1]))

    def _normalize(self):
        for i in range(len(self)):
            self.array[i][i] = np.inf

        for i, j in self.search_null():
            self.array[i][j] = np.inf

    def __len__(self):
        return len(self.array)

    def min_in_row(self, i, without_j=-1):
        row_without_i = (x for idx, x in enumerate(self.array[i], 0) if idx != without_j)
        return min(row_without_i)

    def min_in_col(self, j, without_i=-1):
        col_without_i = (x for idx, x in enumerate(self.array[:, j], 0) if idx != without_i)
        return min(col_without_i)

    def __repr__(self):
        return '\n'.join(
            '   '.join(str(x) for x in self.array[i]) for i in range(len(self))
        )

    def __str__(self):
        return self.__repr__()
