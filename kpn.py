import numpy as np
from matplotlib import pyplot as plt
import math
import sys


def generate_points(count):
    x = np.random.randint(0, 1000, count)
    y = np.random.randint(0, 1000, count)
    return np.array(list(zip(x, y)))


def dist(a, b, axis=1):
    return np.linalg.norm(a - b, axis=axis)


def point_dist(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


if __name__ == '__main__':
    k = 4
    points_count = 10
    plt.ion()
    # генерация вершин
    points = generate_points(points_count)
    # центр масс
    center = np.mean(points, axis=0)
    # yаходим радиус вписанной окружности
    radius = np.nanmax(dist(points, center))
    # находим дальние точки
    x_boundary, y_boundary = points.max(axis=0)

    plt.xlim([-radius, x_boundary + radius])
    plt.ylim([-radius, y_boundary + radius])

    # отрисовываю точки
    for point in enumerate(points):
        (index, [x, y]) = point
        plt.scatter(x, y, s=30, c='r')
    plt.draw()

    # нулевая матрица для хранения расстояний
    min_distances = np.zeros(points_count, dtype=[('x', 'i4'), ('y', 'i4'), ('z', 'f4')])

    # ищем ближайшие друг к другу точки
    for i in range(points_count):
        point = points[i]
        other_points_indexes = list(range(points_count))
        # вычисляю евлидово расстояние между точками и заполняю нулевую матрицу
        d = np.array([point_dist(point, points[j]) for j in other_points_indexes])
        np.put(d, i, sys.maxsize)
        min_distances.put(i, (i, np.nanargmin(d), np.nanmin(d)))

    # несоединенные точки
    single_points = list(range(points_count))
    # соединенные точки
    connected_points = []
    # список ребер
    edges = []
    # список прямых
    lines = []
    # самая первая пара точек
    min_distances_list = min_distances.tolist()
    # нахожу расстония для отрисовки прямых
    min_dist = min(min_distances_list, key=lambda t: t[2])
    first_index = min_dist[0]
    second_index = min_dist[1]
    [first_x, first_y] = points[first_index]
    [second_x, second_y] = points[second_index]

    # отрисовка прямой
    lines.append(plt.plot([first_x, second_x], [first_y, second_y]))
    plt.draw()
    plt.pause(1)
    edges.append((first_index, second_index, min_dist[2]))
    single_points.remove(first_index)
    single_points.remove(second_index)
    connected_points.append(first_index)
    connected_points.append(second_index)

    print(single_points)
    print(connected_points)

    while len(single_points) > 0:
        min_distances = np.zeros(len(single_points), dtype=[('x', 'i4'), ('y', 'i4'), ('z', 'f4')])
        for index, point_index in enumerate(single_points):
            point = points[point_index]
            d = np.array([point_dist(point, points[j]) for j in connected_points])
            min_distances.put(index, (point_index, connected_points[np.nanargmin(d)], np.nanmin(d)))
        min_distances_list = min_distances.tolist()
        min_dist = min(min_distances_list, key=lambda t: t[2])
        first_index = min_dist[0]
        second_index = min_dist[1]
        [first_x, first_y] = points[first_index]
        [second_x, second_y] = points[second_index]

        lines.append(plt.plot([first_x, second_x], [first_y, second_y]))
        plt.draw()
        plt.pause(1)
        edges.append((first_index, second_index, min_dist[2]))
        single_points.remove(first_index)
        connected_points.append(first_index)
    print(edges)

    # удаляю k-1 ребер
    for i in list(range(k - 1)):
        max_edge = max(edges, key=lambda t: t[2])
        max_index = edges.index(max_edge)
        edges.remove(max_edge)
        print(max_index)
        [first_x, first_y] = points[max_edge[0]]
        [second_x, second_y] = points[max_edge[1]]
        plt.plot([first_x, second_x], [first_y, second_y], linestyle='None', )
        lines[max_index][0].remove()
        plt.draw()
        plt.pause(1)
    plt.draw()
    plt.pause(60)
