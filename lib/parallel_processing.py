from threading import Thread
from multiprocessing import Process

running_processes = dict()
running_threads = dict()


def multi_thread(thread_list_identifier):

    def decorator(function):

        def wrapper(*args, **kwargs):

            global running_processes

            if thread_list_identifier not in running_threads:
                running_threads[thread_list_identifier] = list()

            thread = Thread(target=function, args=args, kwargs=kwargs)
            thread.setDaemon(True)
            thread.start()

            running_threads[thread_list_identifier].append(thread)

        return wrapper

    return decorator