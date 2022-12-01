import math
from random import randint


# уравнение вида 1*x1+2*x2+3*x3+4*x4+5*x5=876

def get_new_mutation(populations, populations_count):
    new_populations = []
    for i in range(len(populations)):
        # возможность мутации определяю случайным образом
        random = randint(0, 300)
        if random < 50:
            index = int(math.floor(random / 100 * populations_count))
            populations[i][index] = randint(0, 100)
        new_populations.append(populations[i])
    return new_populations


# 1/(итоговый результат - предполагаемый результат) все это делю на сумму обратных коэффициентов
def get_reverse_coefficient(results):
    results = [1 / abs(EXPECTED_RESULT - result) for result in results]
    return [result / sum(results) for result in results]


# подсчет результата популяции
def calculate_populations_result(populations):
    results = []
    for x1, x2, x3, x4, x5 in populations:
        results.append(1 * x1 + 2 * x2 + 3 * x3 + 4 * x4 + 5 * x5)
    return results


# подсчет уравнения по возможным параметрам
def get_equation_result(populations):
    for x1, x2, x3, x4, x5 in populations:
        calculated = 1 * x1 + 2 * x2 + 3 * x3 + 4 * x4 + 5 * x5
        if calculated == EXPECTED_RESULT:
            return x1, x2, x3, x4, x5
    return False


# определение следующей популяции
def next_population(populations, populations_count):
    results = calculate_populations_result(populations)
    # получаю коэффициент выживаемости
    coefficient = get_reverse_coefficient(results)
    fitness = sum(coefficient)
    results = dict(zip(range(0, len(populations)), coefficient))
    results = [k for k, i in sorted(results.items(), key=lambda item: item[1], reverse=True)]
    new_populations = []
    # скрещивание хромосом (беру пары 1-2, 3-4, 5-6 и тд)
    for i in range(math.floor(len(populations) / 2)):
        population_1 = populations[results[2 * i]]
        population_2 = populations[results[2 * i + 1]]
        crossover_position = randint(1, len(population_1) - 2)
        # скрещиваю разные хромосомы родителей (вроде это называется кросс-овер)
        new_population = (
            population_1[:crossover_position] + population_2[crossover_position:],
            population_2[:crossover_position] + population_1[crossover_position:]
        )

        new_populations.extend(new_population)
    # если ответ равен финальному возвращаю популяцию
    if get_equation_result(new_populations):
        return new_populations
    new_fitness = sum(get_reverse_coefficient(calculate_populations_result(new_populations)))
    # если средняя приспособленность потомков меньше родителей прибегаю к новой мутации
    if fitness > new_fitness:
        populations = get_new_mutation(populations, populations_count)
    else:
        populations = new_populations
    return populations


if __name__ == '__main__':
    EXPECTED_RESULT = 876
    X_COUNT = 5

    populations = []
    populations_count = 10
    for i in range(populations_count):
        population_params = []
        for j in range(X_COUNT):
            population_params.append(randint(0, 300))
        populations.append(population_params)

    i = 1
    while not get_equation_result(populations):
        print('Популяция ', i)
        populations = next_population(populations, populations_count)
        calculated_populations = calculate_populations_result(populations)
        final_result = None
        for result in calculated_populations:
            if (final_result is None or abs(final_result - EXPECTED_RESULT) > abs(result - EXPECTED_RESULT)):
                final_result = result
        print('Лучший результат', final_result)
        i += 1
    x_values = get_equation_result(populations)
    print(x_values)
    print(
        f'1*{x_values[0]}+2*{x_values[1]}+3*{x_values[2]}+4*{x_values[3]}+5*{x_values[4]}={EXPECTED_RESULT}')
