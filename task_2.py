import pygame

from math import dist


class Point:
    position: tuple
    flag_color = None
    in_cluster: bool = False

    def __init__(self, position: tuple):
        self.position = position

    def __repr__(self):
        return f"{self.position} {self.flag_color}"


def draw_points(points, screen, radius, color=None):
    for point in points:
        pygame.draw.circle(screen, color if color else point.flag_color, point.position, radius=radius)
    pygame.display.update()


def clear_cluster_flags(cluster, softly: bool = False):
    for point in cluster:
        point.in_cluster = False
        if softly and point.flag_color == "black":
            continue
        point.flag_color = None


def color_clusters(clusters, screen, radius):
    colors = ["purple", "blue", "orange", "gray", "brown", "aqua"]
    for color_index, cluster in enumerate(clusters):
        draw_points(cluster, screen, radius, color=colors[color_index])
        clear_cluster_flags(cluster)


def color_group(group, group_threshold, original_point):
    if len(group) > group_threshold:
        original_point.flag_color = "green"
        for point in group:
            if point.flag_color == "black":
                point.flag_color = "yellow"
            else:
                point.flag_color = "green"
    else:
        original_point.flag_color = "black"
        for point in group:
            point.flag_color = "black"
            point.in_cluster = False


def find_and_mark_neighbours(point, points, search_radius):
    neighbours = []
    for neighbour in points:
        if neighbour != point \
                and not neighbour.in_cluster \
                and dist(neighbour.position, point.position) <= search_radius:
            neighbours.append(neighbour)
            neighbour.in_cluster = True
    return neighbours


def find_group(initial_point, points, search_radius):
    initial_point.in_cluster = True
    group = [initial_point]

    for point in group:
        neighbours = find_and_mark_neighbours(point, points, search_radius)
        group.extend(neighbours)
    return group


def find_clusters(points, screen, radius):
    group_threshold = 3
    search_radius = 30
    clusters = []

    clear_cluster_flags(points, softly=True)
    for point in points:
        if point.in_cluster:
            continue
        group = find_group(point, points, search_radius)
        color_group(group, group_threshold, point)
        if len(group) > group_threshold:
            clusters.append(group)
    draw_points(points, screen, radius)
    return clusters


def main():
    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    screen.fill("white")

    radius = 3
    should_continue = True
    mouse_pressed = False
    points = []
    clusters = []

    pygame.display.update()

    while should_continue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_continue = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    clusters = find_clusters(points, screen, radius)
                elif event.key == pygame.K_SPACE:
                    color_clusters(clusters, screen, radius)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False

            if mouse_pressed and event.dict.get("pos"):
                pos = event.pos

                if not len(points) or dist(pos, points[-1].position) > 10 * radius:
                    pygame.draw.circle(screen, "red", pos, radius=radius)
                    points.append(Point(pos))

            pygame.display.update()
    return points


if __name__ == '__main__':
    main()
