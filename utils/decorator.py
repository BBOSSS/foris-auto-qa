from decorator import decorator


@decorator
def exception_to_bool(func, *args, **kw):
    try:
        func(*args, **kw)
        return True
    except Exception as e:
        print(e)
        return False
