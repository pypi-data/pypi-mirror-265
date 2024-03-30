import numpy as np

def mean_absolute_percentage_error(actual, predicted):
    return np.mean(np.abs((actual - predicted) / actual)) * 100

def mean_absolute_error(actual, predicted):
    return np.mean(np.abs(actual - predicted))

def mean_squared_error(actual, predicted):
    return np.mean((actual - predicted) ** 2)

def root_mean_squared_error(actual, predicted):
    return np.sqrt(mean_squared_error(actual, predicted))

def binary_cross_entropy(actual, predicted):
    return -np.mean(actual * np.log(predicted) + (1 - actual) * np.log(1 - predicted))

def categorical_correntropy(actual, predicted):
    return -np.mean(np.sum(actual * np.log(predicted), axis=1))

def sparse_categorical_crossentropy(actual, predicted):
    return -np.mean(np.log(predicted)[np.arange(len(actual)), actual])
