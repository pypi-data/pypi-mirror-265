# Example Usage
```
# Import the required functions from your package
from nn_metrics.metrics import (
    mean_absolute_percentage_error,
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    binary_cross_entropy,
    categorical_correntropy,
    sparse_categorical_crossentropy
)

# Example usage:
actual = [10, 20, 30, 40, 50]
predicted = [12, 18, 28, 41, 48]

# Calculate and print error metrics
print("Mean Absolute Percentage Error (MAPE):", mean_absolute_percentage_error(actual, predicted))
print("Mean Absolute Error (MAE):", mean_absolute_error(actual, predicted))
print("Mean Squared Error (MSE):", mean_squared_error(actual, predicted))
print("Root Mean Squared Error (RMSE):", root_mean_squared_error(actual, predicted))
```