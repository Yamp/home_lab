from multiprocessing import Process
import os


def info(title):
    print(f'Title: {title} Module name: {__name__}, parent process {os.getppid()}, process id: {os.getpid()}')


def f(name):
    info('function f')
    print('hello', name)


if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
