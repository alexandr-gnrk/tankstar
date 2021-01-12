import copy
from queue import PriorityQueue
from operator import add

FIELD_TEMPLATE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

FIELD_TEMPLATE = [
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
 [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
 [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
 [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
 [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
class AStar():
    DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def __init__(self, start_pos, end_pos, matrix):
        self.start_pos = tuple(start_pos)
        self.end_pos = tuple(end_pos)
        self.matrix = copy.deepcopy(matrix)
        # self.firing_positions = self.get_firing_positions(self.start_pos)

    def solve(self, full_path=False):
        queue = PriorityQueue()
        queue.put(self.start_pos, 0)
        from_map = dict()
        dist_map = dict()

        from_map[self.start_pos] = None
        dist_map[self.start_pos] = 0

        while not queue.empty():
            curr_pos = queue.get()

            if curr_pos == self.end_pos:
                break

            for next_pos in self.get_neighbor_cells(curr_pos):
                dist = dist_map[curr_pos] + 1

                if next_pos not in dist_map or dist < dist_map[next_pos]:
                    dist_map[next_pos] = dist
                    priority = dist + self.manhattan_distance(next_pos, self.end_pos)
                    queue.put(next_pos, priority)
                    from_map[next_pos] = curr_pos

        return self.get_traversal(from_map)

    def get_traversal(self, from_map):
        traversal = list()
        traversal.append(self.end_pos)
        previous_pos = from_map.get(self.end_pos, None)
        if previous_pos is None:
            return None

        while previous_pos != self.start_pos:
            traversal.insert(0, previous_pos)
            previous_pos = from_map[traversal[0]]

        return traversal

    # @classmethod
    # def heuristic(cls, pos1, pos2):
        

    @classmethod
    def manhattan_distance(cls, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_neighbor_cells(self, pos):
        neighbors = list()
        for diff in self.DIRECTIONS:
            neighbor = tuple(map(add, pos, diff))
            if self.matrix[neighbor[0]][neighbor[1]] == 0:
                neighbors.append(neighbor)

        return neighbors

    # @classmethod
    # def get_firing_positions(cls, pos):
    #     positions = list()
    #     for diff in cls.DIRECTIONS:
    #         next_pos = tuple(map(add, pos, diff))

    #         while self.matrix[next_pos[0]][next_pos[1]] == 0:
    #             positions.append(next_pos)
    #             next_pos = tuple(map(add, pos, diff))

    #     return positions
