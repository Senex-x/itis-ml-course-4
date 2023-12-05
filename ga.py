import random
import numpy as np


def crossover(parents, offspring_size):
    """
    Метод производит кроссовер между родителями.
     Первый родитель (parent1) предоставляет первую часть своих генов, а второй родитель (parent2) - вторую часть.
     Кроссоверная точка (crossover_point) определяет, где происходит обмен генами.
     Этот процесс повторяется для каждого потомка (offspring).

    Например, если у нас есть два родителя с генами [1, 2, 3, 4, 5] и [6, 7, 8, 9, 10],
     и кроссоверная точка установлена на середине (по индексу 2), потомок может получить гены [1, 2, 8, 9, 10].
    :param parents:
    :param offspring_size:
    :return:
    """
    offspring = np.empty(offspring_size)
    crossover_point = np.uint8(offspring_size[1] / 2)

    for k in range(offspring_size[0]):
        parent1_idx = k % len(parents)
        parent2_idx = (k + 1) % len(parents)

        for i in range(crossover_point):
            offspring[k][i] = parents[parent1_idx][i]
            # print(i)

        for i in range(crossover_point, offspring_size[1]):
            offspring[k][i] = parents[parent2_idx][i]
            # print(i)
    return offspring


def fitness_assessment(population, y):
    """
    Метод вычисляет оценки приспособленности (fitness) для каждой хромосомы в популяции.
     Оценка приспособленности определяется насколько хорошо каждая хромосома соответствует желаемому результату
    :param population:
    :param y:
    :return:
    """
    assessment = []
    for population_index in range(len(population)):
        result = 0
        for diofantov_expr_index in range(len(diofantov_expr)):
            result += population[population_index][diofantov_expr_index] * diofantov_expr[diofantov_expr_index]
        # ошибка между текущим ответом и тем, что мы стремимся достичь
        difference = np.abs(y - result) + 1
        # чем меньше ошибка (r), тем выше оценка приспособленности.
        assessment.append(1 / difference)
    return assessment


def mutation_test(pop_after_cross, mutation_rate):
    """
    Метод отвечает за мутацию генов у потомков.
     Для каждого гена в каждой хромосоме проверяется, произойдет ли мутация с заданной вероятностью (mutation_rate).
     Если да, то к гену прибавляется случайное значение от -1.0 до 1.0.

    Например, если mutation_rate равна 0.1, ген [3] может стать [3.5] или [2.2] с некоторой вероятностью.
    :param pop_after_cross:
    :param mutation_rate:
    :return:
    """
    population_nextgen = []
    for i in range(0, len(pop_after_cross)):
        chromosome = pop_after_cross[i]
        for j in range(len(chromosome)):
            if random.random() < mutation_rate:
                random_value = np.random.randint(-1.0, 1.0, 1)
                chromosome[j] = chromosome[j] + random_value
        population_nextgen.append(chromosome)
    return population_nextgen


def parents_selection(population, parents_num, fitness_assessment):
    choose_parents = []
    for i in range(parents_num):
        max_ind = [j for j in range(len(fitness_assessment)) if fitness_assessment[j] == max(fitness_assessment)][0]
        choose_parents.append(population[max_ind])
        fitness_assessment.remove(max(fitness_assessment))
    return choose_parents


if __name__ == '__main__':
    diofantov_expr = [7, -3, 2, -1, 10, -2]
    y = 125

    diofantov_weights = len(diofantov_expr)

    count_chromosome = 12

    # Определение численности населения.
    population_size = (count_chromosome, diofantov_weights)
    # У популяции будет хромосома sol_per_pop, где каждая хромосома имеет num_weights генов.

    # Создание начальной популяции.
    new_population = np.random.randint(low=-len(diofantov_expr) * 3, high=len(diofantov_expr) * 3, size=population_size)
    # print(new_population)

    count_iteration = 1000
    for iteration in range(count_iteration):
        # Оценка приспособленности
        fitness = fitness_assessment(new_population, y)

        # 6 лучших родителей из популяции
        new_parents = parents_selection(new_population, 6, fitness)

        # создание потомков обменом генами
        new_offspring_cross = crossover(parents=new_parents,
                                        offspring_size=(population_size[0] - len(new_parents), diofantov_weights))

        # мутация потомков, изменяем случайные гены с заданной вероятностью
        new_offspring_mut = mutation_test(new_offspring_cross, 0.1)

        # Обновление популяции
        for i in range(len(new_parents)):
            new_population[i] = new_parents[i]

        current_count = 0

        for i in range(len(new_parents), len(new_parents) + len(new_offspring_mut)):
            new_population[i] = new_offspring_mut[current_count]
            current_count += 1

    # Оценка результатов
    # Вычисление оценок приспособленности для конечной популяции и поиск наилучшей хромосомы (с самой высокой оценкой)
    fitness = fitness_assessment(new_population, y)
    max_fitness = max(fitness)
    need_index = fitness.index(max_fitness)

    print("Лучшая хромосома (подборка весов): ", new_population[need_index])
    best_match_id = np.where(fitness == np.max(fitness))
    print(" (" + str(diofantov_expr[0]) + "*" + str(new_population[need_index][0]) + ") + (" +
          str(diofantov_expr[1]) + "*" + str(new_population[need_index][1]) + ") + (" +
          str(diofantov_expr[2]) + "*" + str(new_population[need_index][2]) + ") + (" +
          str(diofantov_expr[3]) + "*" + str(new_population[need_index][3]) + ") + (" +
          str(diofantov_expr[4]) + "*" + str(new_population[need_index][4]) + ") + (" +
          str(diofantov_expr[5]) + "*" + str(new_population[need_index][5]) + ") = " + str(y))

    # print(fitness)
    # print(best_match_id)
    #
    # print(new_population)
    # print(new_population[best_match_id, :])
