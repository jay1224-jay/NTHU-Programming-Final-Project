"""

Use BFS to find the shortest path between 2 points

"""
from src.utils import Position

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

class PathFinder:
    def __init__(self):
        self.maze = None
        self.start = None
        self.end = None
        self.visited = None
        self.maze_w = None
        self.maze_h = None

    def get_parent(self, pos, dir):

        if dir == UP:
            return (pos[0], pos[1]+1)
        if dir == DOWN:
            return (pos[0], pos[1]-1)
        if dir == LEFT:
            return (pos[0]+1, pos[1])

        return (pos[0]-1, pos[1])

    def backtracking(self):
        ret = []
        cur = self.end
        _c = 0
        while cur != self.start and _c < 20:
            ret.append((cur[0], cur[1], self.maze[cur[1]][cur[0]]))
            cur = self.get_parent(cur, self.maze[cur[1]][cur[0]])
        return ret


    def bfs(self):
        visited = [[0 for _ in range(self.maze_w)] for __ in range(self.maze_h)]
        reach = 0
        q = list()
        q.append((self.start, 1))

        while len(q) > 0:
            node = q[0][0]
            length = q[0][1]
            q.pop(0)
            # print(node)
            try:
                if visited[node[1]][node[0]]:
                    continue
            except IndexError:
                return None
            visited[node[1]][node[0]] = length
            if node == self.end:
                reach = 1
                break

            x = node[0]
            y = node[1]
            # Left
            if x > 0:
                neighbor = (x-1, y)
                if self.maze[neighbor[1]][neighbor[0]] == 0 and not visited[neighbor[1]][neighbor[0]]:
                    q.append((neighbor, LEFT))

            # right
            if x < self.maze_w - 1:
                neighbor = (x + 1, y)
                if self.maze[neighbor[1]][neighbor[0]] == 0 and not visited[neighbor[1]][neighbor[0]]:
                    q.append((neighbor, RIGHT))

            # Up
            if y > 0:
                neighbor = (x, y-1)
                if self.maze[neighbor[1]][neighbor[0]] == 0 and not visited[neighbor[1]][neighbor[0]]:
                    q.append((neighbor, UP))

            # down
            if y < self.maze_h - 1:
                neighbor = (x, y+1)
                if self.maze[neighbor[1]][neighbor[0]] == 0 and not visited[neighbor[1]][neighbor[0]]:
                    q.append((neighbor, DOWN))


        if reach:
            print("Found path")
            self.maze = visited
            return 1
        else:
            print("No path")
            self.maze = None
        return 0

    def search_path(self, maze, start, end) -> None:
        self.maze = maze
        self.start = start
        self.end = end
        self.maze_w = len(self.maze[0])
        self.maze_h = len(self.maze)
        print("search: from {} to {}".format(self.start, self.end))
        if self.bfs():
            return self.backtracking()
