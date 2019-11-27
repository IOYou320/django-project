import time

def a_new_decorator(a_func):

    def wrapTheFunction():
        start_time = time.time()
        a_func()
        end_time = time.time()
        print('所耗时间',end_time - start_time)

    return wrapTheFunction

@a_new_decorator
def a_function_requiring_decoration():
    time.sleep(10)
    print("bbbbbbbbbbbbbbbbbbb")


a_function_requiring_decoration()