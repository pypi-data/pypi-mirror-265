from typing import Any, Callable
from functools import wraps


def entrypoint(func: Callable) -> Callable:
    """Execute the function to decorate function if the script is run directly.

    This is equivalent to:
    ```python
    if __name__ == "__main__":
        func()
    ```

    (where `func` is the decorated function)

    Args:
        func (Callable): The function to decorate

    Returns:
        Callable: The decorated function
    """
    if func.__module__ == "__main__":
        func()
    return func


def bind(*args, **kwargs) -> Callable:
    """Bind arguments to a function.

    Example:
    ```python
    from jjjxutils.decorators import bind

    @bind(2, 3)
    def addition(x, y) -> int:
        return x + y
    ```

    This will make `addition` a function that takes no arguments and returns 5.

    Returns:
        Callable: _description_
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args_, **kwargs_) -> Any:
            return func(*args, *args_, **kwargs, **kwargs_)

        return wrapper

    return decorator


def compute(func: Callable) -> Any:
    """Execute the function and save the result.

    This is equivalent to:
    ```python
    func = func()
    ```

    This is useful when you want to execute code or calculate a value at import time, but still want to keep it in a seperate scope.

    Args:
        func (Callable): The function to decorate

    Returns:
        Any: The return value of the function
    """
    return func()
