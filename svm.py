import pygame
from sklearn import svm

RADIUS = 5


def add_new_point(screen, color, position, points, classes, class_number=0):
    pygame.draw.circle(screen, color=color, center=position, radius=RADIUS)
    pygame.display.update()
    points.append(list(position))
    classes.append(class_number)


def add_new_point_with_class_predict(model, position, screen, colors):
    class_predicted = model.predict([position])
    pygame.draw.circle(screen, color=colors[class_predicted[0]], center=position, radius=RADIUS)
    pygame.display.update()


def add_grade_separation_line(points, classes, model, screen):
    model.fit(points, classes)
    coef = model.coef_[0]
    start_pos = [0, model.intercept_[0] / -coef[1]]
    end_pos = [800, coef[0] / -coef[1] * 800 + model.intercept_[0] / -coef[1]]
    pygame.draw.line(screen, color='black', start_pos=start_pos, end_pos=end_pos)
    pygame.display.update()


def start_svm_algorithm():
    model = svm.SVC(kernel='linear')

    points = []
    classes = []
    play = True
    learning_mode = True
    colors = ['red', 'blue', 'black', 'yellow']

    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    screen.fill(color='white')
    pygame.display.update()

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if learning_mode:
                    add_new_point(screen, colors[0], event.pos, points, classes)
                else:
                    add_new_point_with_class_predict(model, event.pos, screen, colors)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if learning_mode:
                    add_new_point(screen, colors[1], event.pos, points, classes, class_number=1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                learning_mode = False
                add_grade_separation_line(points, classes, model, screen)


start_svm_algorithm()
