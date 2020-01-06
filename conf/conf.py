import os
import yaml

global s

def init_state(filename=os.path.abspath(os.path.dirname(__file__)) + "\conf.yaml"):
    f = open(filename, encoding="utf-8")
    y = yaml.load(f, Loader=yaml.FullLoader)


if __name__ == '__main__':
    print(init_state())
