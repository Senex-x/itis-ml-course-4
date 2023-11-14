# Библиотека для рисования
import pygame
# Для вычисления расстояния между точками
from math import dist

pygame.init()
screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)

# Покрасим экран в белый
screen.fill('white')
pygame.display.update()

# Флаг для закрытия paint
is_paint_opened = True

# Радиус шаров для отрисовки
circle_radius = 5

mouse_button_down = False
points = []

# Количество соседей для того, чтобы считать точку зелёной
required_neighbor_amount = 3

# is_paint_opened = False
while is_paint_opened:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
            is_paint_opened = False

        # В консоли можно увидеть все действия, которые вызываются мышкой (либо клавиатурой)
        # print(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_button_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_down = False

        if event.type == pygame.WINDOWEXPOSED:
            screen.fill('white')
            for point in points:
                pygame.draw.circle(screen, color='black', center=point, radius=circle_radius)

        if mouse_button_down:
            new_circle_coordinates = event.pos

            if not len(points) or dist(new_circle_coordinates, points[-1]) > 5 * circle_radius:
                points.append(new_circle_coordinates)
                pygame.draw.circle(screen, color='black', center=new_circle_coordinates, radius=circle_radius)
                pygame.draw.circle(screen, color='black', center=new_circle_coordinates, radius=60, width=1)

        pygame.display.update()

        if event.type == pygame.KEYDOWN and event.unicode == '2':
            search_radius = 60

            for index, point in enumerate(points):
                neighbour_count = 0
                potential_neighbors = points.copy()
                potential_neighbors.pop(index)
                for potential_neighbor in potential_neighbors:
                    if dist(potential_neighbor, point) <= search_radius:
                        neighbour_count += 1

                if neighbour_count == 0:
                    color = 'red'
                elif neighbour_count < required_neighbor_amount:
                    color = 'yellow'
                else:
                    color = 'green'

                pygame.draw.circle(screen, color=color, center=points[index],
                                   radius=circle_radius)
                pygame.display.update()


        def find_neighbors(point, points, suitable_radius):
            """
            Метод ищет соседей для точки (point) в точках (points) в радиусе (suitable_radius)
            :param point: Точка для поиска соседей
            :param points: Массив точек среди которых ищем соседей
            :param suitable_radius: Радиус в пределах которого ищем соседей
            :return: neighbors: Массив индексов соседей
            """
            neighbors = []

            for potential_neighbor_index in range(len(points)):
                distance_point_to_point = dist(points[potential_neighbor_index], point)
                if suitable_radius >= distance_point_to_point > 0:
                    neighbors.append(potential_neighbor_index)

            return neighbors


        def is_points_have_clusters(points, clusters):
            """
            Метод проверяет, какому кластеру принадлежат точки и выдаёт номер кластера
            :param points: Массив индексов точек
            :param clusters: Массив кластеров (индекс - номер кластера, значение - массив номеров точек в кластере)
            :return: Номер кластера | Массив кластеров | False
            """
            exist_cluster = []
            for cluster_index, cluster in enumerate(clusters):
                if any(point in cluster for point in points):
                    exist_cluster.append(cluster_index)

            if len(exist_cluster) == 0:
                return False
            elif len(exist_cluster) == 1:
                return exist_cluster[0]
            return exist_cluster


        def merge_clusters(clusters_to_merge, clusters):
            """
            Метод объединяет кластеры clusters_to_merge в один кластер
            :param clusters_to_merge: Массив с индексами кластеров для объединения
            :param clusters: Массив всех кластеров
            """
            for index_old_point, old_cluster_point in enumerate(clusters[clusters_to_merge[1]]):
                clusters[clusters_to_merge[0]].append(old_cluster_point)
                del clusters[clusters_to_merge[1]][index_old_point]


        if event.type == pygame.KEYDOWN and event.unicode == '3':
            # Присвоим кластер каждой точке.
            # Кластеры храним в двумерном массиве, где индекс - номер кластера, значение -
            # массив номеров точек, которые в этом кластере
            clusters = [[]]
            # Массив крайних точек, которые могли не попасть никуда
            edges_point = []
            for current_point_enum in enumerate(points):

                current_neighbors = find_neighbors(current_point_enum[1], points, search_radius)
                # Если эти соседи уже в кластерах, добавляем к этому же кластеру
                exist_cluster = is_points_have_clusters(current_neighbors, clusters)
                if not isinstance(exist_cluster, list) and exist_cluster:
                    clusters[exist_cluster].append(current_point_enum[0])
                # Если соседи в разных кластерах, объединяем их в один кластер
                elif isinstance(exist_cluster, list) and exist_cluster:
                    merge_clusters(exist_cluster, clusters)
                # Если соседей нет, создаём новый кластер в clusters
                elif len(current_neighbors) >= required_neighbor_amount:
                    clusters.append([])
                    clusters[len(clusters) - 1].append(current_point_enum[0])
                else:
                    edges_point.append(current_point_enum[0])

            for edge_point in edges_point:
                current_neighbors = find_neighbors(points[edge_point], points, search_radius)
                exist_cluster = is_points_have_clusters(current_neighbors, clusters)
                if exist_cluster:
                    clusters[exist_cluster].append(edge_point)

            # Перекрасим разные кластеры
            color = ['olive', 'darkorange', 'lightcoral', 'teal', 'violet',
                     'skyblue', 'blue', 'cyan', 'meta', 'black', 'pink', 'gray', 'lawn green', 'gainsboro',
                     'steel blue',
                     'salmon', 'maroon']
            for cluster_index, cluster in enumerate(clusters):
                for point_in_cluster in cluster:
                    pygame.draw.circle(screen, color=color[cluster_index], center=points[point_in_cluster],
                                       radius=circle_radius)
                    pygame.display.update()
