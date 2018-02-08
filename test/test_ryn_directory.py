
from bases import BaseDirectory, BaseManager

if __name__ == "__main__":
    directory = BaseDirectory()
    m1 = BaseManager("test-manager", "test", "mdltest")
    m1.status = True
    m2 = BaseManager("raw-manager", "raw", "mdlraw")
    m2.status = True
    m3 = BaseManager("rule-manager", "rule", "mdlrule")
    m3.status = True
    directory.add(m1)
    directory.add(m2)
    directory.add(m3)
    print("Find : {}".format(directory.find("mdltest").name))