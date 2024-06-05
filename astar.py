# a-star.py
from queue import PriorityQueue
from geopy.distance import geodesic

class AStar:
    def __init__(self, graph, cities):
        """
        初始化A*算法实例。
        
        :param graph: NetworkX图对象。
        :param cities: 城市及其坐标的字典。
        """
        self.graph = graph
        self.cities = cities

    def heuristic(self, a, b):
        """
        使用地理距离作为启发式函数
        :param a: 城市a
        :param b: 城市b
        :return: a和b之间的地理距离
        """
        pos_a = self.cities[a]
        pos_b = self.cities[b]
        return geodesic(pos_a, pos_b).kilometers

    def search(self, start, goal):
        """
        执行A*算法搜索从起点到目标点的最短路径。

        :param start: 起点节点。
        :param goal: 目标节点。
        :return: 一个包含最短路径和路径成本的元组 (path, cost)。
        """
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            _, current = frontier.get()

            if current == goal:
                break

            for next in self.graph.neighbors(current):
                new_cost = cost_so_far[current] + self.graph[current][next]['weight']
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put((priority, next))
                    came_from[next] = current

        return self.reconstruct_path(came_from, start, goal), cost_so_far.get(goal)

    def reconstruct_path(self, came_from, start, goal):
        """
        重建从起点到目标点的路径。

        :param came_from: 记录每个节点前驱节点的字典。
        :param start: 起点节点。
        :param goal: 目标节点。
        :return: 从起点到目标点的路径（列表）。
        """
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
