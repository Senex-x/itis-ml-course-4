import pygame
from math import dist
import random
import numpy as np
from sklearn.cluster import DBSCAN


def scatter(point):
    R = 5
    n = random.randint(3, 5)
    points = []
    for i in range(n):
        radius = random.randint(R, 3 * R)
        angle = random.randint(0, 360)
        x = radius * np.cos(2 * np.pi * angle / 360) + point[0]
        y = radius * np.sin(2 * np.pi * angle / 360) + point[1]
        points.append((x, y))
    return points


def dbscan(points):
    minPts = 5
    radius = 15
    db = DBSCAN(eps=radius, min_samples=minPts)
    db.fit(points)
    return db.labels_


if name == 'main':
    pygame.init()
    r = 3
    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    screen.fill('white')
    pygame.display.update()
    points = []
    flag = True
    mouse_button_down = False
    while (flag):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            if event.type == pygame.WINDOWEXPOSED:
                screen.fill('white')
                for point in points:
                    pygame.draw.circle(screen,
                                       color='black', center=point,
                                       radius=r)
            if event.type == pygame.KEYDOWN:
                if event.unicode == '\r':
                    screen.fill('white')
                    points = []
                if event.key == pygame.K_r:
                    clusters = dbscan(points)
                    clusters_number = max(clusters) + 1
                    colors = []
                    for i in range(clusters_number):
                        colors.append((random.randint(0, 255),
                                       random.randint(0, 255),
                                       random.randint(0, 255)))
                    colors.append('#000000')
                    for index, point in enumerate(points):
                        pygame.draw.circle(screen,
                                           color=colors[clusters[index]],
                                           center=point, radius=r)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_button_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_button_down = False
            if mouse_button_down:
                coord = event.pos

                points_new = scatter(coord)

                if len(points):
                    if dist(coord, points[-1]) > 5 * r:
                        points.append(coord)

                        points.extend(points_new)
                        for point in points_new:
                            pygame.draw.circle(screen,
                                               color='black', center=point,
                                               radius=r)

                        pygame.draw.circle(screen,
                                           color='black', center=coord,
                                           radius=r)
                else:
                    points.append(coord)
                    pygame.draw.circle(screen,
                                       color='black', center=coord,
                                       radius=r)
            pygame.display.update()