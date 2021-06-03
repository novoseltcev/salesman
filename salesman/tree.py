import numpy as np


class Node:
    def __init__(self, weight, cond=None, prev=None, status=None):
        self.weight = weight
        self.cond = cond
        self.prev = prev
        self.status = status
        if self.prev is not None:
            self.weight += self.prev.weight

    def __ge__(self, other):
        return self.weight >= other.weight

    def __lt__(self, other):
        return not self.__ge__(other)

    def __eq__(self, other):
        return self.status == other.status and self.prev == other.prev

    def __repr__(self):
        return ' - '.join([str(self.cond[:2]), str(self.status), str(self.weight)])


class DecisionTree:
    def __init__(self, weight):
        self.basis = Node(weight=weight)
        self.nodes = [self.basis]
        self.actives = [self.basis]
        self.route = []

    def add_depth_for_node(self, node, cond, weight0, weight1):
        self.actives.remove(node)
        l_node = Node(prev=node, cond=cond, status=False, weight=weight0)
        r_node = Node(prev=node, cond=cond, status=True, weight=weight1)
        self.actives.append(l_node)
        self.actives.append(r_node)

    def get_route(self, node, init=False):
        if init:
            self.route.clear()

        if node.status is None:
            return self.route

        self.route.append(
            (node.cond[:2], node.status, node.weight)
        )
        return self.get_route(node.prev)

    def cur_node(self):
        min_node = Node(weight=np.inf)
        for node in self.actives:
            if node < min_node:
                min_node = node
        return min_node
