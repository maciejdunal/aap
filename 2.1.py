import functools

def func_decorator(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        parameters = {}

        for i, arg in enumerate(args):
            parameters[f'arg{i+1}'] = type(arg).__name__

        for name, value in kwargs.items():
            parameters[name] = type(value).__name__

        print(f"Function name: '{func.__name__}' , parameters name: {parameters}")

        return func(*args, **kwargs)
    
    return wrapper

# Example usage
@func_decorator
def function123(a, b, c, d):
    print("main function aaa")

# Test
function123(a= 10, b=2.11, c="text", d=False)