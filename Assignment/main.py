from watersort import *
from bloxorz import *
from testcase.bloxorz.testcase import maps
from testcase.watersort.testcase import initial_states

initialization_watersort = initial_states[1]
initialization_bloxorz = maps[1]

game1 = water_sort()
game1.set_initial_state(initialization_watersort)

game2 = bloxorz()
game2.set_initial_state(initialization_bloxorz)

# game1.dfs()
# game1.bfs()
game1.astar()


# game2.dfs()
# game2.bfs()
# game2.genetic()
