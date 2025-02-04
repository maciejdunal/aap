# Napisz dekorator funkcji, który będzie logował informację o nazwie i typie
# wszystkich parametrów wejściowych funkcji dekorowanej w postaci:
# {<nazwa_parametru>: <typ_danych>, ...}.

import functools
import logging

logging.basicConfig(level=logging.INFO)

def func_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        parameters = {}

        for i, arg in enumerate(args):
            parameters[f'arg{i+1}'] = type(arg).__name__

        for name, value in kwargs.items():
            parameters[name] = type(value).__name__

        logging.info(f"Function '{func.__name__}' parameters: {parameters}")
        return func(*args, **kwargs)
    
    return wrapper

@func_decorator
def example_function(a, b, c, d):
    logging.info("Function executed")

example_function(110, 2.1111, "test123213", False)
