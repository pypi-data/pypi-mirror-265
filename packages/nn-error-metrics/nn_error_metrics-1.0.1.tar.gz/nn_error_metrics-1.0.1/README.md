# Example Usage
```
import numpy as np
from nn_error_metrics import (
    mean_absolute_percentage_error,
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    binary_cross_entropy,
    categorical_correntropy,
    sparse_categorical_crossentropy
)

actual = np.array([10, 20, 30, 40, 50])
predicted = np.array([12, 18, 28, 41, 48])

print("Mean Absolute Percentage Error (MAPE):", mean_absolute_percentage_error(actual, predicted))
print("Mean Absolute Error (MAE):", mean_absolute_error(actual, predicted))
print("Mean Squared Error (MSE):", mean_squared_error(actual, predicted))
print("Root Mean Squared Error (RMSE):", root_mean_squared_error(actual, predicted))

actual = np.array([1, 0, 1, 1, 0])
predicted = np.array([0.9, 0.2, 0.8, 0.6, 0.3])
print("Binary Cross Entropy (BCE):", binary_cross_entropy(actual, predicted))

actual = np.array([[0, 1], [1, 0], [0, 1], [0, 1], [1, 0]])
predicted = np.array([[0.1, 0.9], [0.8, 0.2], [0.3, 0.7], [0.6, 0.4], [0.9, 0.1]])
print("Categorical Correntropy (CC):", categorical_correntropy(actual, predicted))

actual = np.array([1, 0, 1, 1, 0])
predicted = np.array([[0.1, 0.9], [0.8, 0.2], [0.3, 0.7], [0.6, 0.4], [0.9, 0.1]])
print("Sparse Categorical Correntropy (SCC):", sparse_categorical_crossentropy(actual, predicted))

```