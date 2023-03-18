import queue


class problem:
    def __init__(self) -> None:
        self.initial_state = None
        self.goal_state = []
        self.current_node = None

    def is_goal(self, val_node_state) -> bool:
        pass

    def bfs(self):
        print('Breath first search')
        counter = 0
        if self.is_goal(self.current_node.state):
            return True
        frontier = queue.Queue()
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

    def dfs(self):
        print('Depth first search')
        counter = 0
        if self.is_goal(self.current_node.state):
            return True
        frontier = queue.LifoQueue()
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


