# Написать с нуля алгоритм k-means без использования библиотек (но можно пользоваться библиотеками,
# не связанными с самим алгоритмом - отрисовки, подсчетов и т.д.). Пошагово:
# 1. Найти оптимальное количество кластеров по формулам. И только для этого оптимального значения выводить рисунки.
# 2. Рисунки выводятся на каждый шаг – сдвиг центроидов. Сколько шагов, столько рисунков (можно в виде gif).
# Точки из разных кластеров разными цветами.
# 3. Точки задаются случайным образом на плоскости.
# 4. Центроиды образуют правильную вписанную в окружность фигуру.
# 5.  Каждый шаг алгоритма – вывод графически (см. п.2).

import sys
import matplotlib.pyplot as plt
import random
import numpy as np
import operator


def get_points(dots_amount=100):
    '''
    Метод создаёт рандомные точки в пределах от 0 до 100, возвращаемые в массиве
    :param dots_amount: Количество точек
    :return: Двумерный массив, где по первому индексу хранится точка,
    а по второму x или y соответствующей точки
    '''
    points = []
    for i in range(dots_amount):
        points.append([random.randint(0, 100), random.randint(0, 100)])
    return points


def visualize_points(points, centroids, clusters=None):
    '''
    Отображение точек на графике
    :param points: массив точек
    :param centroids: массив центроидов
    :param clusters: массив кластеров, если есть
    После вызова использовать plt.show() для отрисовки графика
    '''
    color = ['lightcoral', 'darkorange', 'olive', 'teal', 'violet',
             'skyblue', 'blue', 'cyan', 'meta', 'black', 'pink', 'gray']
    for number_point in range(len(points)):
        if clusters:
            plt.scatter(points[number_point][0], points[number_point][1], color=color[clusters[number_point]])
        else:
            plt.scatter(points[number_point][0], points[number_point][1], color='black')
    for centroid in centroids:
        plt.scatter(centroid[0], centroid[1], color='r')


def get_distance(point_first, point_second):
    return np.sqrt((point_first[0] - point_second[0]) ** 2 +
                   (point_first[1] - point_second[1]) ** 2)


def place_centroids(points, amount_of_centroids=4):
    '''
    Метод возвращает массив центроидов, удалённых максимально далеко друг от друга и
    расположенных равномерно по окружности от всех точек.
    '''
    center, circle_radius = set_boundary(points)
    centroids = []
    for i in range(amount_of_centroids):
        centroids.append([circle_radius * np.cos(2 * np.pi * i / amount_of_centroids) + center[0],
                          circle_radius * np.sin(2 * np.pi * i / amount_of_centroids) + center[1]])
    return centroids


def set_boundary(points):
    '''
    Метод возвращает центр окружности, центр которой лежит на среднем значении х и у точек,
    и радиус этой окружности, равный расстоянию от центра окружности до самой удалённой точки.
    '''
    circle_center = [0, 0]
    for point in points:
        circle_center[0] += point[0]
        circle_center[1] += point[1]
    circle_center[0] /= len(points)
    circle_center[1] /= len(points)
    # print(circle_center)
    circle_radius = 0
    for point in points:
        distance_to_point = get_distance(circle_center, point)
        if distance_to_point > circle_radius:
            circle_radius = distance_to_point
    return [circle_center, circle_radius]


def assign_clusters_to_points(points, centroids):
    '''
    Метод ищет ближайшие точки к центроидам и возвращает массив,
    индексы которого равны индексам точек, а значение - номеру центроида (кластера)
    :param points: массив точек
    :param centroids: массив центроидов
    :return: clusters: массив кластеров
    '''
    clusters = []
    for point in points:
        min_distance_to_centroid = sys.maxsize
        index = -1
        for centroid_number in range(len(centroids)):
            # print('i:', centroid_number)
            distance_from_centroid_to_point = get_distance(point, centroids[centroid_number])
            if min_distance_to_centroid > distance_from_centroid_to_point:
                min_distance_to_centroid = distance_from_centroid_to_point
                index = centroid_number
        # print(min_distance_to_centroid)
        # print(index)
        clusters.append(index)
    return clusters


def find_new_centroids_point(points, clusters):
    '''
    Метод возвращает новые координаты центроидов для заданных кластеров
    :param points: Массив точек
    :param clusters: Массив кластеров, где индекс элемента - номер точки, а значение - номер кластера
    :return: Новые координаты центроидов для кластеров
    '''

    def divide_by_third_element(array):
        return list(map(lambda sum_of_points: round(sum_of_points / array[2], 1), array[:2]))

    count_of_clusters = len(set(clusters))
    sum_of_coordinates = []
    for number_of_cluster in range(count_of_clusters):
        sum_of_coordinates.append([0, 0, 0])
    for number_point in range(len(points)):
        sum_of_coordinates[clusters[number_point]][0] += points[number_point][0]
        sum_of_coordinates[clusters[number_point]][1] += points[number_point][1]
        sum_of_coordinates[clusters[number_point]][2] += 1
    new_centroids = list(map(divide_by_third_element, sum_of_coordinates))
    return new_centroids


def get_max_difference_between_arrays(first_array, second_array):
    max_difference = 0
    for index in range(len(first_array)):
        for inner_index in range(len(first_array[index])):
            difference = operator.abs(first_array[index][inner_index] - second_array[index][inner_index])
            if difference > max_difference:
                max_difference = difference
    return max_difference


def get_sum_of_squares_of_distances(points, centroids, clusters):
    '''
    Метод считает сумму квадратов расстояний для заданных точек и центроидов
    :param points: Массив точек
    :param centroids: Массив центроидов
    :param clusters: Массив кластеров, где индекс - номер точки, значение - номер кластера
    :return: Сумма квадратов расстояний (int)
    '''
    sums_of_squares_of_distances = [0] * len(centroids)
    sum_of_squares_of_distances = 0

    for point_index in range(len(points)):
        sums_of_squares_of_distances[clusters[point_index]] = get_distance(
            points[point_index],
            centroids[clusters[point_index]]
        )
    for index in range(len(sums_of_squares_of_distances)):
        sum_of_squares_of_distances += sums_of_squares_of_distances[index]
    return sum_of_squares_of_distances


points = get_points()
sums_of_square_distances = [0] * 8
for centroids_amount in range(len(sums_of_square_distances)):
    delta = sys.maxsize
    centroids_amount += 2
    centroids = place_centroids(points, centroids_amount)
    clusters = []
    # visualize_points(points, centroids)
    while True:
        new_clusters = assign_clusters_to_points(points, centroids)
        if np.array_equiv(clusters, new_clusters):
            break
        clusters = new_clusters
        new_centroids = find_new_centroids_point(points, clusters)
        centroids = new_centroids
    sums_of_square_distances[centroids_amount - 2] = get_sum_of_squares_of_distances(points, centroids, clusters) # J(C)
# sums_of_squares_of_distances - [0] - два центроида, [1] - три, ... .
# print(sums_of_squares_of_distances)

# Теперь надо найти оптимальное число кластеров D(k)
fall_rates_measures = [0] * 8
for k_index, sum_of_squares_of_distances in enumerate(sums_of_square_distances[1:-1], start=1):
    # print(cluster_amount, sum_of_squares_of_distances)
    fall_rates_measures[k_index] = operator.abs(
        sum_of_squares_of_distances - sums_of_square_distances[k_index + 1]) / operator.abs(
        sums_of_square_distances[k_index - 1] - sum_of_squares_of_distances)

optimal_k = -1
min_value = sys.maxsize
for k_index in range(len(fall_rates_measures)):
    current_distance = fall_rates_measures[k_index]
    if (current_distance < min_value) & (current_distance != 0):
        min_value = current_distance
        optimal_k = k_index

# centroids = set_centroids(points, optimal_clusters_amount)
# clusters = find_nearby_point(points, centroids)
print('Optimal clusters amount: ', optimal_k)

delta = sys.maxsize
centroids = place_centroids(points, optimal_k)
clusters = []
while True:
    new_clusters = assign_clusters_to_points(points, centroids)
    visualize_points(points, centroids, clusters)
    plt.show()
    if np.array_equiv(clusters, new_clusters):
        break
    clusters = new_clusters
    new_centroids = find_new_centroids_point(points, clusters)
    centroids = new_centroids