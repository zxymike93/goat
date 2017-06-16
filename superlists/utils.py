import time


def date():
    value = time.localtime(int(time.time()))
    format = '%Y/%m/%d %H:%M:%S'
    date = time.strftime(format, value)
    return date


def log(*args, **kwargs):
    dt = date()
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)
