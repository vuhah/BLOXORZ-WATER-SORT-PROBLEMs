from problem_fomulation import *
from itertools import permutations
from copy import deepcopy


class node_water_sort:
    def __init__(self, state, parent_node=None, level=0):
        self.state = state
        self.parent_node = parent_node
        self.level = level

    def __lt__(self, other):
        comparator = False
        if (self.heuristic_function() + self.level) < (self.heuristic_function() + self.level):
            comparator = True
        elif (self.heuristic_function() + self.level) == (
                self.heuristic_function() + self.level) and self.level > other.level:
            comparator = True
        return comparator

    def __str__(self):
        return f'{self.state}, {self.level} + {self.heuristic_function()}'

    def expand(self):
        expended_node = []
        not_empty_column = []
        not_full_column = []
        for i in range(len(self.state)):
            if len(self.state[i]) < 4:
                not_full_column.append(i)
            if len(self.state[i]) > 0:
                not_empty_column.append(i)

        for index1 in not_empty_column:
            for index2 in not_full_column:
                if index1 == index2:
                    continue
                if len(self.state[index2]) == 0 or self.state[index1][-1] == self.state[index2][-1]:
                    data_temporary = deepcopy(self.state)
                    data_temporary[index2].append(data_temporary[index1].pop(-1))
                    while len(data_temporary[index1]) > 0 and len(data_temporary[index2]) < 4 and \
                            data_temporary[index1][-1] == data_temporary[index2][-1]:
                        data_temporary[index2].append(data_temporary[index1].pop(-1))
                    expended_node.append(node_water_sort(data_temporary, self, self.level + 2))
        return expended_node

    def heuristic_function(self):
        evaluation = 0
        for i in range(len(self.state)):
            if len(self.state[i]) < 2:
                continue
            for j in range(len(self.state[i]) - 1):
                if self.state[i][j] != self.state[i][j + 1]:
                    evaluation += 1
        return evaluation

    def print_path(self):
        print(self.state)
        a = self
        while a.parent_node is not None:
            a = a.parent_node
            print(f'{a.state},{a.level}, {a.heuristic_function()}')


class water_sort(problem):
    def __init__(self):
        super().__init__()

    def set_initial_state(self, initial_state: []) -> None:
        num_of_color = len(initial_state)

        self.initial_state = initial_state
        self.initial_state.append([])
        if num_of_color > 2:
            self.initial_state.append([])

        self.set_goal_state(num_of_color)
        self.current_node = node_water_sort(self.initial_state, None, 0)

    def set_goal_state(self, num_of_color: int) -> []:
        goal = []
        for i in range(num_of_color):
            goal.append([i + 1] * 4)
        goal.append([])
        if num_of_color > 2:
            goal.append([])
        goal = list(permutations(goal))
        for i in range(len(goal)):
            goal[i] = list(goal[i])
        self.goal_state = goal

    def is_goal(self, val_node_state) -> bool:
        return val_node_state in self.goal_state

    def astar(self):
        print('A* Search')
        if self.is_goal(self.current_node.state):
            return True
        counter = 0
        frontier = queue.PriorityQueue()
        frontier.put(self.current_node)
        reached = [self.current_node.state]
        while not frontier.empty():
            self.current_node = frontier.get()
            for child in self.current_node.expand():
                counter += 1
                if self.is_goal(child.state):
                    child.print_path()
                    print(f'Number of node traversals {counter}')
                    return True
                if child.state not in reached:
                    reached.append(child.state)
                    frontier.put(child)
        return False
