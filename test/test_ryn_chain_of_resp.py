import abc

class ChocoCrocks(object):

    def __init__(self):
        self.name = "ChocoCrocks"

    def __str__(self):
        return "I'm a {}".format(self.name)

class Cacao(object):

    def __init__(self):
        self.name = "Cacao"

    def __str__(self):
        return "I'm a {}".format(self.name)

class Chocolate(object):

    def __init__(self):
        self.name = "Chocolate"

    def __str__(self):
        return "I'm a {}".format(self.name)

class Handler(metaclass=abc.ABCMeta):
    """
    Define an interface for handling requests.
    Implement the successor link.
    """

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_request(self, data):
        pass


class ConcreteHandler1(Handler):
    """
    Handle request, otherwise forward it to the successor.
    """

    def handle_request(self, data):
        if isinstance(data, Cacao):  # if can_handle:
            print("Handler 1")
            print(data)
        elif self._successor is not None:
            self._successor.handle_request(data)


class ConcreteHandler2(Handler):
    """
    Handle request, otherwise forward it to the successor.
    """

    def handle_request(self, data):
        if isinstance(data, Chocolate):  # if can_handle:
            print("Handler 2")
            print(data)
        elif self._successor is not None:
            self._successor.handle_request(data)

class ConcreteHandler3(Handler):
    """
    Handle request, otherwise forward it to the successor.
    """

    def handle_request(self, data):
        if isinstance(data, ChocoCrocks):  # if can_handle:
            print("Handler 3")
            print(data)
        elif self._successor is not None:
            self._successor.handle_request(data)


def main():
    concrete_handler_1 = ConcreteHandler1()
    concrete_handler_2 = ConcreteHandler2(concrete_handler_1)
    concrete_handler_3 = ConcreteHandler3(concrete_handler_2)
    concrete_handler_3.handle_request(ChocoCrocks())


if __name__ == "__main__":
    main()
