from salesman.tree import DecisionTree, np
from salesman.model import Matrix


class SalesMan(Matrix):
    def __init__(self, matrix):
        super(SalesMan, self).__init__(matrix)
        self.numbers_rows = list(range(len(self)))
        self.numbers_cols = list(range(len(self)))

    def get_old_edge(self, i, j):
        return self.numbers_rows[i], self.numbers_cols[j]

    def get_new_edge(self, i, j):
        return self.numbers_rows.index(i), self.numbers_cols.index(j)

    def minimize_rows(self):
        result = 0
        for i in range(len(self)):
            tmp_min = self.min_in_row(i)
            result += tmp_min
            self.array[i] -= tmp_min
        return result

    def minimize_cols(self):
        result = 0
        for j in range(len(self)):
            tmp_min = self.min_in_col(j)
            result += tmp_min
            self.array[:, j] -= tmp_min
        return result

    def minimize(self):
        return self.minimize_rows() + self.minimize_cols()

    def error(self):
        max_value = self.minimize()
        h, k = 0, 0
        null_indexes = self.search_null()
        for index in null_indexes:
            i, j = index
            tmp = self.min_in_row(i, j) + self.min_in_col(j, i)
            if tmp >= max_value:
                h, k = i, j
                max_value = tmp
        return h, k, max_value

    def reduce(self, i, j):
        try:
            i2, j2 = self.get_old_edge(i, j)
            i2, j2 = self.get_new_edge(j2, i2)
            self.array[i2][j2] = np.inf
        except IndexError:
            pass
        except ValueError:
            pass

        del self.numbers_rows[i]
        del self.numbers_cols[j]
        self.array = np.delete(self.array, i, axis=0)
        self.array = np.delete(self.array, j, axis=1)

    def add_last_edges(self, raw_way):
        last_null = set(self.search_null())
        l_null = {x for x in last_null if sum(x) == 0 or sum(x) == 2}
        if len(l_null) == 2:
            last_null = l_null
        else:
            last_null -= l_null

        res = [((self.numbers_rows[i] + 1, self.numbers_cols[j] + 1), True, 0) for i, j in last_null]
        raw_way.append(res[0])
        raw_way.append(res[1])
        return raw_way

    def get_condition(self):
        selected_matrix = self.array.copy()

        i, j, error_weight = self.error()
        self.array[i][j] = np.inf
        error_cond = (self.array.copy(), self.numbers_rows.copy(), self.numbers_cols.copy())

        self.array = selected_matrix
        self.reduce(i, j)
        selected_weight = self.minimize()
        selected_cond = (self.array, self.numbers_rows, self.numbers_cols)

        i, j = error_cond[1][i] + 1, error_cond[2][j] + 1
        cond = (i, j, error_cond, selected_cond)
        return cond, error_weight, selected_weight

    def get_way(self, tree, tracing):
        raw_way = self.add_last_edges(tree.get_route(tree.cur_node(), init=True))
        if tracing:
            print()
            print(raw_way)

        pre_way = [x[0] for x in raw_way if x[1]]
        result = [pre_way[0]]
        for _ in range(len(self.base) - 1):
            for obj in pre_way:
                if obj[0] == result[-1][1]:
                    result.append(obj)
                    break

        weight = raw_way[0][2]
        way = ' -> '.join(str(obj[0]) for obj in result) + ' -> ' + str(result[-1][-1])
        return weight, way

    def solve(self, tracing=False):
        tree = DecisionTree(self.minimize())
        node = tree.cur_node()
        while True:
            cond, error_weight, selected_weight = self.get_condition()
            tree.add_depth_for_node(node, cond=cond, weight0=error_weight, weight1=selected_weight)
            node = tree.cur_node()
            self.array        = node.cond[2 + node.status][0].copy()
            self.numbers_rows = node.cond[2 + node.status][1].copy()
            self.numbers_cols = node.cond[2 + node.status][2].copy()
            if len(self) <= 2:
                break

        return self.get_way(tree, tracing)
