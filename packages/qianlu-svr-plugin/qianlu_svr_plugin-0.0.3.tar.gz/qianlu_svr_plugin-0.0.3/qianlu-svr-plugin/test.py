import sys
from os import path

sys.path.append(path.dirname(path.abspath(__file__)))
from server import QianluService


class testService(object):
    def __init__(self):
        pass

    def test(self, args):
        print(f"test: {args}")
        return {"code": 1, "msg": "success", "data": {}}


if __name__ == '__main__':
    qianluSvr = QianluService()
    qianluSvr.register("testService", testService())
    qianluSvr.run()
