import inspect


class CallLogger:
    def __getattribute__(self, name):
        returned = object.__getattribute__(self, name)
        if inspect.isfunction(returned) or inspect.ismethod(returned) and not returned.__name__[0] == '_':
            print('called ', returned.__name__, self.__class__.__name__)
        return returned
