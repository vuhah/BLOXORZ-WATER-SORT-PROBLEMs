from problem_fomulation import *
import numpy as np
import random


class node_bloxorz:
    def __init__(self, state, parent_node=None, level=0):
        self.state = state
        self.parent_node = parent_node
        self.level = level

    def expand(self, move_direction=('LEFT', 'RIGHT', 'UP', 'DOWN')):
        expanded_node = []

        direction = self.state.get('current_position').get('direction')
        x = self.state.get('current_position').get('coordinate_x')
        y = self.state.get('current_position').get('coordinate_y')

        if direction == 'vertical':
            for move in move_direction:
                flag = False
                rolled_node = self.state.get('current_position').copy()
                rolled_node.update({'direction': 'horizontal'})

                if move == 'RIGHT':
                    rolled_node.update({'coordinate_x': [x[0] + 1, x[0] + 2]})
                if move == 'LEFT':
                    rolled_node.update({'coordinate_x': [x[0] - 2, x[0] - 1]})
                if move == 'UP':
                    rolled_node.update({'coordinate_y': [y[0] - 2, y[0] - 1]})
                if move == 'DOWN':
                    rolled_node.update({'coordinate_y': [y[0] + 1, y[0] + 2]})

                for i in rolled_node.get('coordinate_x'):
                    for j in rolled_node.get('coordinate_y'):
                        if (j, i) in self.state.get('empty_cell'):
                            flag = True
                            break
                    if flag:
                        break

                if not flag:
                    expanded_node.append(node_bloxorz({
                        'current_position': rolled_node,
                        'empty_cell': self.state.get('empty_cell'),
                    }, self, self.level + 1))

        if direction == 'horizontal' and len(x) == 2:
            for move in move_direction:
                flag = False
                rolled_node = self.state.get('current_position').copy()
                rolled_node.update({'direction': 'horizontal'})

                if move == 'LEFT':
                    rolled_node.update({'direction': 'vertical'})
                    rolled_node.update({'coordinate_x': [x[0] - 1]})
                if move == 'RIGHT':
                    rolled_node.update({'direction': 'vertical'})
                    rolled_node.update({'coordinate_x': [x[1] + 1]})
                if move == 'UP':
                    rolled_node.update({'coordinate_y': [y[0] - 1]})
                if move == 'DOWN':
                    rolled_node.update({'coordinate_y': [y[0] + 1]})

                for i in rolled_node.get('coordinate_x'):
                    for j in rolled_node.get('coordinate_y'):
                        if (j, i) in self.state.get('empty_cell'):
                            flag = True
                            break
                    if flag:
                        break

                if not flag:
                    expanded_node.append(node_bloxorz({
                        'current_position': rolled_node,
                        'empty_cell': self.state.get('empty_cell'),
                    }, self, self.level + 1))

        if direction == 'horizontal' and len(y) == 2:
            for move in move_direction:
                flag = False
                rolled_node = self.state.get('current_position').copy()
                rolled_node.update({'direction': 'horizontal'})

                if move == 'LEFT':
                    rolled_node.update({'coordinate_x': [x[0] + 1]})
                if move == 'RIGHT':
                    rolled_node.update({'coordinate_x': [x[0] - 1]})
                if move == 'UP':
                    rolled_node.update({'direction': 'vertical'})
                    rolled_node.update({'coordinate_y': [y[0] - 1]})
                if move == 'DOWN':
                    rolled_node.update({'direction': 'vertical'})
                    rolled_node.update({'coordinate_y': [y[0] + 1]})

                for i in rolled_node.get('coordinate_x'):
                    for j in rolled_node.get('coordinate_y'):
                        if (j, i) in self.state.get('empty_cell'):
                            flag = True
                            break
                    if flag:
                        break

                if not flag:
                    expanded_node.append(node_bloxorz({
                        'current_position': rolled_node,
                        'empty_cell': self.state.get('empty_cell'),
                    }, self, self.level + 1))

        return expanded_node

    def print_path(self):
        coordinate_x = self.state.get('current_position').get('coordinate_x')
        coordinate_y = self.state.get('current_position').get('coordinate_y')
        print(f'({coordinate_y},{coordinate_x})---{self.level}')
        a = self
        while a.parent_node is not None:
            a = a.parent_node
            coordinate_x = a.state.get('current_position').get('coordinate_x')
            coordinate_y = a.state.get('current_position').get('coordinate_y')
            print(f'(x,y) = ({coordinate_y},{coordinate_x})     Level:{a.level}')


class bloxorz(problem):
    def __init__(self):
        super().__init__()

    def set_initial_state(self, worldmap) -> None:
        current_position = {}
        empty_cell = []
        destination_cell = []

        current_position.update({'direction': 'vertical'})
        for i in range(15):
            for j in range(15):
                if worldmap[i][j] == 'C':
                    current_position.update({'coordinate_y': [i]})
                    current_position.update({'coordinate_x': [j]})
                elif worldmap[i][j] == 'E':
                    empty_cell.append((i, j))
                elif worldmap[i][j] == 'D':
                    destination_cell.append((i, j))

        self.initial_state = {
            'current_position': current_position,
            'empty_cell': empty_cell
        }
        self.set_goal_state(destination_cell)
        self.current_node = node_bloxorz(self.initial_state, None, 0)

    def set_goal_state(self, destination_cell):
        self.goal_state = destination_cell

    def is_goal(self, val_node_state) -> bool:
        return val_node_state.get('current_position').get('direction') == 'vertical' \
               and (val_node_state.get('current_position').get('coordinate_y')[0],
                    val_node_state.get('current_position').get('coordinate_x')[0]) in self.goal_state

    def get_distance(self):
        distance_x = np.abs(
            self.current_node.state.get('current_position').get('coordinate_x')[0] - self.goal_state[0][1])
        distance_y = np.abs(
            self.current_node.state.get('current_position').get('coordinate_y')[0] - self.goal_state[0][0])
        return distance_x + distance_y

    def fitness_function(self, gen):
        node_run = self.current_node
        for i in range(len(gen)):
            node_run_tmp = node_run.expand((gen[i],))
            if len(node_run_tmp) == 0:
                return 100*(len(gen)-i)
            else:
                node_run = node_run_tmp[0]

        distance_x = np.abs(node_run.state.get('current_position').get('coordinate_x')[0] - self.goal_state[0][1])
        distance_y = np.abs(node_run.state.get('current_position').get('coordinate_y')[0] - self.goal_state[0][0])
        distance = distance_x + distance_y
        if distance_x == 0 or distance_y == 0:
            if node_run.state.get('current_position').get('direction') != 'vertical':
                result = 0.5
            else:
                result = 0
            return result
        else:
            return distance

    def genetic(self):
        length_of_DNA = int(self.get_distance())
        original_element = ['LEFT', 'RIGHT', 'UP', 'DOWN']

        """Initialization ---------------------------------------"""
        population = []
        for i in range(6):
            population.append(random.choices(original_element, k=length_of_DNA))

        flag = False
        result = None
        count = 0

        while not flag:
            count += 1
            """Evaluation -------------------------------------------"""
            value = list(map(self.fitness_function, population))
            """Selection --------------------------------------------"""
            fitness_value = list(map(lambda x: 1 / (1 + x), value))

            total = sum(fitness_value)

            probability = list(map(lambda x: x / total, fitness_value))

            cumulative_probability = []
            for i in range(6):
                if i == 0:
                    cumulative_probability.append(probability[i])
                else:
                    cumulative_probability.append(probability[i] + cumulative_probability[i - 1])

            roulette_wheel = []
            for i in range(6):
                roulette_wheel.append(random.random())

            new_population = []
            for i in range(6):
                if roulette_wheel[i] < cumulative_probability[0]:
                    new_population.append(population[0])
                else:
                    for j in range(6):
                        if roulette_wheel[i] > cumulative_probability[j]:
                            new_population.append(population[j + 1])
                            break

            """Cross-over ------------------------------------"""
            parent_index = random.sample(range(0, 5), 3)
            position_interchange = random.sample(range(0, length_of_DNA - 1), 3)
            for i in range(3):
                if i == 0:
                    new_population[parent_index[0]] = new_population[parent_index[0]][:position_interchange[0]] + \
                                                      new_population[parent_index[1]][position_interchange[0]:]
                if i == 1:
                    new_population[parent_index[1]] = new_population[parent_index[1]][:position_interchange[1]] + \
                                                      new_population[parent_index[2]][position_interchange[1]:]
                if i == 2:
                    new_population[parent_index[2]] = new_population[parent_index[2]][:position_interchange[2]] + \
                                                      new_population[parent_index[0]][position_interchange[2]:]

            """Mutation ---------------------------------------"""
            mutation_rate = 0.1
            total_gen = 6 * length_of_DNA
            num_gen_exchange = round(mutation_rate * total_gen)
            mutation_gen = random.sample(range(0, 6 * length_of_DNA - 1), num_gen_exchange)

            for i in mutation_gen:
                n = int(i / length_of_DNA)
                m = i - n * length_of_DNA
                new_population[n][m] = random.choice(original_element)

            """Reevaluate new population -------------------------------------------"""
            new_value = list(map(self.fitness_function, new_population))
            for i in range(6):
                if new_value[i] == 0:
                    result = new_population[i]
                    flag = True

        print(f'Number of generations: {count}')
        print(f'PATH: {result}')
        return
