import hashlib


def w1(func: str):
    def f(file: str) -> str:
        with open(file, 'rb') as fp:
            # 3.11+
            obj = hashlib.file_digest(fp, func)
        return obj.hexdigest()

    f.__name__ = func
    return f


def w2(func: str):
    def f(data: bytes) -> str:
        return hashlib.new(func, data).hexdigest()

    f.__name__ = func
    return f
