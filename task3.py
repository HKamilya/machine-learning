from enum import Enum
import pygame
import numpy as np


class Color(Enum):
    BLACK = 'black'
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    WHITE = 'white'


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = Color.BLACK.value
        self.distances = {}

    def __eq__(self, other):
        if self.color == other.color and self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.x, self.y, self.color))

    def set_red(self):
        self.color = Color.RED.value

    def set_group_num(self, num):
        self.group_num = num

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)

    def add_distance(self, point):
        dist = np.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)
        self.distances[point] = dist
        self.distances = dict(sorted(self.distances.items(), key=lambda x: x[1]))

    def get_neighbours(self, dist):
        neighbours = []
        for k, v in self.distances.items():
            if v <= dist:
                neighbours.append(k)

        return neighbours


def clusterize(points, eps, min_pts, singles):
    groups = []
    for point1 in points:
        for point2 in points:
            # считаю расстояние от каждой до каждой точки
            if point1 != point2 and point2 not in point1.distances:
                point1.add_distance(point2)

            if point1 != point2 and point1 not in point2.distances:
                point2.add_distance(point1)

    while len(points) != 0:
        for point in points:
            # проверяю всех соседей, если соседей меньше чем min_pts, то это кучка ошельников
            # добавляю их в список одиночек, убираю из списка общих точек
            if len(point.get_neighbours(eps)) < min_pts - 1:
                singles.append(point)
                points.remove(point)
            else:
                # если точка относится к списку возможных участников группы, убираю из списка всех точек, устанавливаю зеленый цвет
                points.remove(point)
                group = [point]
                for n in point.get_neighbours(eps):
                    # проверяю каждую точку в списке соседей этой точки,
                    # если расстояние меньше eps и количество возможных соседей соответсвует,
                    # убираю из списка одиночек, устанавливаю желтый цвет
                    if n in singles or len(n.get_neighbours(eps)) < min_pts - 1:
                        if n in singles:
                            singles.remove(n)
                        group.append(n)
                        if n in points:
                            points.remove(n)
                    if len(n.get_neighbours(eps)) >= min_pts - 1:
                        group.append(n)
                        if n in points:
                            points.remove(n)

                groups.append(group)

    for single in singles:
        single.set_red()

    for group1 in groups:
        for group2 in groups:
            if group1 != group2:
                # так как собирала группы для каждой точки, определяю нет ли дублирования групп, и обединяю группы имеющие тех же соседей
                c = list(set(group1) & set(group2))
                if len(c) > 0:
                    group1 += group2
                    groups.remove(group2)

    colors = {
        0: 'purple',
        1: 'brown',
        2: 'violet',
        3: 'green',
        4: 'blue',
        5: 'cyan',
        6: 'olive',
        7: 'orange',
        8: 'pink',
        9: 'lightblue',
        10: 'tan',
        11: 'sienna',
        12: 'beige',
        13: 'darkgrey',
        14: 'lightred',
        15: 'lightgreen',
        16: 'lightcyan'

    }

    idx = 0
    for idx, group in enumerate(groups):
        color1 = group[0].color
        color2 = group[1].color
        color3 = group[2].color
        for point in group:
            if color1 == color2 and color1 != 'black' and color1 != 'red':
                point.color = color1
            elif color1 == color3 and color1 != 'black' and color1 != 'red':
                point.color = color1
            elif color2 == color3 and color2 != 'black' and color2 != 'red':
                point.color = color2
            else:
                point.color = colors[idx]


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption('DBSCAN')
    font = pygame.font.Font(None, 30)

    quit = False
    points = []
    singles = []
    eps = 100
    min_pts = 3
    points_count = 0

    while not quit:
        screen.fill((255, 255, 255))

        if len(points) == points_count:
            for point in points:
                point.draw(screen)
        else:
            for point in singles:
                point.draw(screen)

            for point in points:
                point.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                point = Point(event.pos[0], event.pos[1])
                points.append(point)
                point.draw(screen)
                points_count += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(points) == points_count:
                    clusterize(points.copy(), eps, min_pts, singles)
                    pygame.display.update()
