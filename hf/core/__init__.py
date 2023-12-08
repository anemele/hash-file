import hashlib


def w1(func: str):
    def f(file: str, caps: bool) -> str:
        with open(file, 'rb') as fp:
            # 3.11+
            obj = hashlib.file_digest(fp, func)
        digest = obj.hexdigest()
        return digest.upper() if caps else digest

    f.__name__ = func
    return f


def w2(func: str):
    def f(data: bytes, caps: bool) -> str:
        digest = hashlib.new(func, data).hexdigest()
        return digest.upper() if caps else digest

    f.__name__ = func
    return f
