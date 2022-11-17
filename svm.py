import numpy as np
import pygame
from sklearn.svm import SVC


def get_line_points(svc):
    w = svc.coef_[0]
    a = -w[0] / w[1]
    xx = np.array([0, width])
    yy = a * xx - (svc.intercept_[0]) / w[1]
    return np.array(list(zip(xx, yy)))


def draw_circle(points, event, current_class, screen):
    color = GREEN
    if current_class == 1:
        color = RED
    pygame.draw.circle(screen, color, event.pos, radius)
    points.append([[event.pos[0], event.pos[1]], current_class, None])


def draw_pygame():
    line_printed = False
    coordinates = []
    screen = pygame.display.set_mode((width, height))
    screen.fill(WHITE)
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and line_printed is False:
                    draw_circle(coordinates, event, 0, screen)
                if event.button == 3 and line_printed is False:
                    draw_circle(coordinates, event, 1, screen)
                if line_printed is True:
                    pos = list(event.pos)
                    cls = svc.predict([pos])[0]
                    points.append([pos, cls, None])
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and line_printed is False:
                line_printed = True
                x_coords = np.array(list(map(lambda p: p[0], coordinates)))
                y_coords = np.array(list(map(lambda p: p[1], coordinates)))
                svc = SVC(kernel='linear')
                svc.fit(x_coords, y_coords)
                line_points = get_line_points(svc)
                p1, p2 = line_points[0], line_points[-1]
                pygame.draw.line(screen, 'black', p1, p2, 2)

        count_sim = 0
        count_diff = 0
        for point in points:
            is_above = lambda point, p1, p2: np.cross(point - p1, p2 - p1) < 0
            if is_above(point[0], p1, p2):
                point[2] = 0
            else:
                point[2] = 1
            if point[1] == point[2]:
                count_sim = count_sim + 1
            else:
                count_diff = count_diff + 1
            if count_sim > count_diff:
                pygame.draw.circle(screen, colors[point[2]], point[0], radius)
            else:
                pygame.draw.circle(screen, colors[point[1]], point[0], radius)

        pygame.display.update()


if __name__ == '__main__':
    width, height = 600, 400
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    radius = 5
    points = []
    colors = {0: GREEN, 1: RED}
    draw_pygame()
