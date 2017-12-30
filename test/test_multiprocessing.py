
""" Multiprocessing
    '''''''''''''''
    * Process : Process(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)
        - run()
        - start()
        - join([timeout])
        - name
        - is_alive()
        - daemon
        - pid
        - exitcode
        - authkey
        - sentinel
        - terminate()
        x ProcessError
        x BufferTooShort
        x AuthenticationError
        x TimeoutError
    * Queue : Queue([maxsize])
        - qsize()
        - empty()
        - full()
        - put(obj[, block[, timeout]])
        - put_nowait(obj)
        - get([block[, timeout]])
        - get_nowait()
        - close()
        - join_thread()
        - cancel_join_thread()
    * Pool : Pool([processes[, initializer[, initargs[, maxtasksperchild[, context]]]]])
        - apply(func[, args[, kwds]])
        - apply_async(func[, args[, kwds[, callback[, error_callback]]]])
        - map(func, iterable[, chunksize])
        - map_async(func, iterable[, chunksize[, callback[, error_callback]]])
        - imap(func, iterable[, chunksize])
        - imap_unordered(func, iterable[, chunksize])
        - starmap(func, iterable[, chunksize])
        - starmap_async(func, iterable[, chunksize[, callback[, error_callback]]])
        - close()
        - terminate()
        - join()
"""
import sys
import threading
import random
import time
# from multiprocessing import Process, Queue

# class Counter(threading.Thread):
    
#     order = 0

#     def __init__(self, name):
#         super().__init__()
#         self.name = name
#         self.current = 1
#         self.max = 10

#     def __str__(self):
#         if self.current == self.max:
#             return "{} jusqua {} en position {}".format(self.name, self.max, Counter.order)
#         else:
#             return "{} : {}".format(self.name, self.current)

#     def run(self):
#         while self.max != self.current:
#             print(self)
#             time.sleep(random.random())
#             self.add()
#         Counter.order += 1
#         print(self)

#     def add(self):
#         self.current += 1

# c1 = Counter("Toto")
# c2 = Counter("Titi")
# c3 = Counter("Tata")

# c1.start()
# c2.start()
# c3.start()

class Compte:

    def __init__(self):
        self.solde = 0

    def add(self, s):
        self.solde += s
        print("Add : {}".format(s))

    def remove(self, s):
        self.solde -= s
        print("Remove : {}".format(s))

    def opNull(self, s):
        self.solde += s
        print("Add : {}".format(s))
        self.solde -= s
        print("Remove : {}".format(s))

    def __str__(self):
        return "Solde: {} €".format(self.solde)

class Operation(threading.Thread):

    def __init__(self, name, compte):
        super().__init__()
        self.name = name
        self.compte = compte

    def run(self):
        while True:
            r = random.random()
            n = self.getName()
            print(n)
            # self.compte.add(r)
            # self.compte.remove(r)
            self.compte.opNull(r)
            solde = self.compte.solde
            print(n)
            if solde != 0:
                print("{} : ** solde = {} €".format(n, solde))
                sys.exit()

co = Compte()
for i in range(20):
    op = Operation("A{}".format(i), co)
    op.start()
