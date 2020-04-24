import threading

############ thread utilities #############
class StopLoop(Exception):
    'Exception raised from in_loop_func when stop_flag of ReusableLoopThread is on.'
    pass

class ReusableLoopThread():
    def __init__(self, in_loop_func, before_loop_func=None, after_loop_func=None):
        self.__stop_flag    = False
        self.__thread       = None
        self.__in_loop_func = in_loop_func
        self.__before_loop_func = before_loop_func
        self.__after_loop_func = after_loop_func

    def _loop(self):
        if self.__before_loop_func is not None:
            self.__before_loop_func()

        try:
            while not self.__stop_flag:
                self.__in_loop_func()
        except StopLoop:
            pass

        if self.__after_loop_func is not None:
            self.__after_loop_func()    

    def start(self):
        if self.is_alive():
            self.stop()
        
        self.clear_stop_flag()
        self.__thread = threading.Thread(target=self._loop)
        self.__thread.start()

    def stop(self):
        self.set_stop_flag()
        if self.is_alive():
            self.__thread.join()
    
    def is_alive(self):
        return self.__thread is not None and self.__thread.is_alive()      

    def set_stop_flag(self):
        self.__stop_flag = True

    def clear_stop_flag(self):
        self.__stop_flag = False    
        
    def check_should_be_stop(self, raise_error=True):
        if self.__stop_flag and raise_error:
            raise StopLoop
        return self.__stop_flag 

