import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn import datasets

from collections import Counter

iris = datasets.load_iris()
iris_df = pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                       columns=iris['feature_names'] + ['target'])
iris_df.head()


def normalize(a):
    row_sums = a.sum(axis=1)
    new_matrix = a
    for i, (row, row_sum) in enumerate(zip(a, row_sums)):
        new_matrix[i, :] = row / row_sum
    return new_matrix


x = iris_df.iloc[:, :-1]
y = iris_df.iloc[:, -1]

x_train = x.sample(frac=0.8, random_state=0)
y_train = y.sample(frac=0.8, random_state=0)
x_test = x.drop(x_train.index)
y_test = y.drop(y_train.index)

x_train = np.asarray(x_train)
y_train = np.asarray(y_train)

x_test = np.asarray(x_test)
y_test = np.asarray(y_test)

current_palette = sns.color_palette()
print('x train до нормализации')
print(x_train[0:5])
di = {0.0: 'Setosa', 1.0: 'Versicolor', 2.0: 'Virginica'}

before = sns.pairplot(iris_df.replace({'target': di}), hue='target', corner=True)
before.fig.suptitle('До нормализации', y=1.08)

normalized_x_train = normalize(x_train)
normalized_x_test = normalize(x_test)

print('x train после нормализации')
print(normalized_x_train[0:5])

iris_df_2 = pd.DataFrame(data=np.c_[normalized_x_train, y_train],
                         columns=iris['feature_names'] + ['target'])
di = {0.0: 'Setosa', 1.0: 'Versicolor', 2.0: 'Virginica'}
after = sns.pairplot(iris_df_2.replace({'target': di}), hue='target', corner=True)
after.fig.suptitle('После нормализации', y=1.08)


def distance_euclidean(x_train, x_test_point):
    distances = []
    # рассчитываю расстояния до каждой точки в наборе обучающих данных
    for row in range(len(x_train)):
        current_train_point = x_train[row]
        current_distance = 0

        for col in range(len(current_train_point)):
            current_distance += (current_train_point[col] - x_test_point[col]) ** 2
        current_distance = np.sqrt(current_distance)
        distances.append(current_distance)

    distances = pd.DataFrame(data=distances, columns=['dist'])
    return distances


def nearest_neighbors(distance_point, k):
    # сортировка расстояний всех точек
    knearests = distance_point.sort_values(by=['dist'], axis=0)

    # беру ближайщих k соседей
    knearests = knearests[:k]
    return knearests


def most_common(k_nearest, y_train):
    # получаю индексы видов соседей c их повторениями
    common_types = Counter(y_train[k_nearest.index])
    # определяю самый популярный вид среди соседей
    prediction = common_types.most_common()[0][0]
    return prediction


def knn(x_train, y_train, x_test, k):
    prediction = []

    for x_test_point in x_test:
        # получаю все расстояния от точек до точек
        distance_point = distance_euclidean(x_train, x_test_point)
        # определяю ближайшие точки
        nearest_point = nearest_neighbors(distance_point, k)
        # ближайшие популярные точки
        pred_point = most_common(nearest_point, y_train)
        prediction.append(pred_point)

    return prediction


# функция для подсчета точности вычислений
def calculate_accuracy(y_test, y_pred):
    correct_count = 0
    for i in range(len(y_test)):
        if y_test[i] == y_pred[i]:
            correct_count = correct_count + 1
    accuracy = correct_count / len(y_test)
    return accuracy


accuracies = []
ks = range(1, 30)
for k in ks:
    y_pred = knn(normalized_x_train, y_train, normalized_x_test, k)
    accuracy = calculate_accuracy(y_test, y_pred)
    accuracies.append(accuracy)
fig, ax = plt.subplots()
ax.plot(ks, accuracies)
ax.set(xlabel="k",
       ylabel="Accuracy",
       title="Performance of knn")
plt.show()

sepal_length = np.random.uniform(iris_df.min(axis=0)['sepal length (cm)'], iris_df.max(axis=0)['sepal length (cm)'])
sepal_width = np.random.uniform(iris_df.min(axis=0)['sepal width (cm)'], iris_df.max(axis=0)['sepal width (cm)'])
petal_length = np.random.uniform(iris_df.min(axis=0)['petal length (cm)'], iris_df.max(axis=0)['petal length (cm)'])
petal_width = np.random.uniform(iris_df.min(axis=0)['petal width (cm)'], iris_df.max(axis=0)['petal width (cm)'])

testSet = [[sepal_length, sepal_width, petal_length, petal_width]]
# testSet = [[5.6,2.5,3.9,1.1]] # цветок из класса 1
# testSet = [[6.2	,2.8,	4.8,	1.8]] #цветок из класса 2
test = pd.DataFrame(testSet)
test = np.asarray(test)
test_array = normalize(test)

di = {0.0: 'Setosa', 1.0: 'Versicolor', 2.0: 'Virginica'}
max_value = max(accuracies)
k = accuracies.index(max_value) + 1
predictions = knn(normalized_x_train, y_train, test_array, k)
for i in predictions:
    print(di[i])
