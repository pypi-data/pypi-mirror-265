from typing import Callable, TypeVar
from functools import wraps

T = TypeVar('T')

def trying(fn: Callable[..., T], *args, **kwargs) -> T|Exception:
    '''
    Takes in a function and--separately!--its' parameters (necessary so it can be evaluated by the function, rather than before the call) and returns the result or the first exception raised by the function. Does not catch other `BaseException` subclasses.

    Parameters
    ----------
    `fn` : `Callable[..., T]`
        function that may raise an exception
    
    `*args`
        any positional arguments to pass to `fn`

    `**kwargs`
        any keyword argumetns to pass to `fn`

    Returns
    -------
    `T|Exception`
        Either the result of `fn(*args, **kwargs)` or the first `Exception` it raised
    '''    
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        return e


def trying_genexpr(genexpr, *args, **kwargs) -> T|Exception:
    '''
    Takes in a function and--separately!--its' parameters (necessary so it can be evaluated by the function, rather than before the call) and returns the result or the first exception raised by the function. Does not catch other `BaseException` subclasses.

    Parameters
    ----------
    `genexpr`
        generator expression whose next yield gets returned
    
    `*args`
        any positional arguments to pass to `fn`

    `**kwargs`
        any keyword argumetns to pass to `fn`

    Returns
    -------
    `T|Exception`
        Either the result of `fn(*args, **kwargs)` or the first `Exception` it raised
    '''    
    try:
        return next(genexpr)
    except Exception as e:
        return e


def wrap_in_trying(fn: Callable[..., T]) -> Callable[..., T|Exception]:
    '''
    Takes in a function and returns a function that returns either the result or the first exception raised by the function. Does not catch other `BaseException` subclasses.

    Parameters
    ----------
    fn : Callable[..., T]
        Function that may raise an Exception

    Returns
    -------
    Callable[..., T|Exception]
    '''    
    @wraps(fn)
    def inner(*args, **kwargs):
        return trying(fn, *args, **kwargs)
    
    return inner