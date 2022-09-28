import numpy as np
from matplotlib import pyplot as plt


# генерация случайных точек
def random_point(n):
    points = []
    for _ in range(n):
        points.append(np.random.randint(1, 100, 2))
    return points


# определение начального положения центроидов
def init_centroids(points, k):
    x_c = 0
    y_c = 0
    for i in range(len(points)):
        x_c += points[i][0]
        y_c += points[i][1]
    x_c /= len(points)
    y_c /= len(points)
    R = 0
    for i in range(len(points)):
        if R < dist([x_c, y_c], points[i]):
            R = dist([x_c, y_c], points[i])
    centroids = []
    for i in range(k):
        x_cntr = R * (np.cos(2 * np.pi * i / k)) + x_c
        y_cntr = R * (np.sin(2 * np.pi * i / k)) + y_c
        centroids.append([x_cntr, y_cntr])
    return centroids


# поиск оптимальной точки центра внутри кластера
def find_cluster_mean(points, clusters, k, centroids):
    for i in range(0, k):
        x_sum = 0
        y_sum = 0
        size = 0
        for j in range(0, len(clusters)):
            if clusters[j] == i:
                x_sum += points[j][0]
                y_sum += points[j][1]
                size = size + 1
        centroids[i][0] = x_sum / size
        centroids[i][1] = y_sum / size
    return centroids


# определение расстояния между точками
def dist(p_i, p_j):
    return np.sqrt((p_i[0] - p_j[0]) ** 2 + (p_i[1] - p_j[1]) ** 2)

def count_j_c(j_c):
    c_k = len(j_c) - 2
    return (j_c[c_k] - j_c[c_k + 1]) / (j_c[c_k - 1] - j_c[c_k])


def check(points, centroids, cluster, k):
    global j_c
    x_old = []
    y_old = []
    for i in range(0, len(centroids)):
        x_old.append(centroids[i][0])
        y_old.append(centroids[i][1])

    new_cluster = find_nearest(points, centroids)
    new_centroids = find_cluster_mean(points, new_cluster, k, centroids)
    plot(points, new_centroids, cluster)
    count = 0
    for i in range(0, k):
        cluster_sum = 0
        for j in range(0, len(new_cluster)):
            if new_cluster[j] == i:
                # сумма квадратов расстояний от точек до центроидов
                cluster_sum += dist(points[j], new_centroids[i]) ** 2
        count += cluster_sum
    j_c.append(count)
    global k_min
    global optimal_found
    global k_optimal
    # поиск D(k) (оптимального числа кластеров) по формуле из учебника
    if len(j_c) > 2:
        j_c_val = count_j_c(j_c)
        if j_c_val > k_min:
            k_optimal = k
            optimal_found = True
        else:
            k_min = j_c_val
    return True


def plot(points, centroids, clusters):
    clr = np.array(
        ["green", "blue", "yellow", "olive", "pink", "black", "orange", "purple", "beige", "brown", "gray", "cyan",
         "magenta"])
    colors = []
    points_x = []
    points_y = []
    for i in range(len(points)):
        points_x.append(points[i][0])
        points_y.append(points[i][1])
        colors.append(clr[int(clusters[i])])

    centroids_x = []
    centroids_y = []
    for i in range(len(centroids)):
        centroids_x.append(centroids[i][0])
        centroids_y.append(centroids[i][1])

    plt.scatter(points_x, points_y, c=colors)
    plt.scatter(centroids_x, centroids_y, c='red')
    plt.show()


def find_nearest(points, centroids):
    cluster = np.zeros(len(points))
    for i in range(len(points)):
        min_dist = np.infty
        for j in range(len(centroids)):
            if min_dist > dist(points[i], centroids[j]):
                min_dist = dist(points[i], centroids[j])
                cluster[i] = j
    return cluster


def kmeans(k, points):
    centroids = init_centroids(points, k)

    cluster = find_nearest(points, centroids)
    plot(points, centroids, cluster)

    while not check(points, centroids, cluster, k):
        check(points, centroids, cluster, k)


if __name__ == '__main__':
    k_optimal = 0
    j_c = []
    k_min = 1
    optimal_found = False
    n = 100
    points = random_point(n)
    # расчет к средних до нахождения оптимального числа кластеров
    for i in range(1, 10):
        if optimal_found:
            break
        else:
            kmeans(i, points)
    plt.plot(range(1, k_optimal + 1), j_c, marker='o')
    plt.xlabel('Cluster number')
    plt.ylabel('J(C)')
    plt.show()
