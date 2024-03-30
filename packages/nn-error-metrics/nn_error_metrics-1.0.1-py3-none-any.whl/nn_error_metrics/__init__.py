from .nn_error_metrics import (
    mean_absolute_percentage_error,
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    binary_cross_entropy,
    categorical_correntropy,
    sparse_categorical_crossentropy,
)

def mape(actual, predicted):
    mean_absolute_percentage_error(actual, predicted)

def mae(actual, predicted):
    mean_absolute_error(actual, predicted)

def mse(actual, predicted):
    mean_squared_error(actual, predicted)

def rmse(actual, predicted):
    root_mean_squared_error(actual, predicted)

def bce(actual, predicted):
    binary_cross_entropy(actual, predicted)

def cc(actual, predicted):
    categorical_correntropy(actual, predicted)

def scc(actual, predicted):
    sparse_categorical_crossentropy(actual, predicted)