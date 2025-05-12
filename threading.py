# IMPORTS
import os
import time, threading
import logging, pendulum
from logging.handlers import TimedRotatingFileHandler

# Create logging folder
try:
    os.mkdir("logs")
except:
    pass

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a TimedRotatingFileHandler that rotates daily
log_filename = './logs/logfile.log'
file_handler = TimedRotatingFileHandler(log_filename, when='M', interval=1, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)


# This lock is shared by multiple threads for avoiding deadlocks. You might need multiple or one might
# suffice, depends on your logic.
# create thread lock
thread_lock = threading.Lock()

# define your class, you can have multiple classes
class My_Class_A(threading.Thread):
    
    def __init__(self, parameter_one):

        threading.Thread.__init__(self)
        self.parameter_one = parameter_one
    
    def function_A(parameter_one):
        
        # do something
        # keep try/except/finally etc for better outcomes and easy debugging
        return parameter_one        
    
    def run(self):

        # This infinite loop is completely dependent on your logic and use-case.
        # If your thread needs to run only once, no need of this. Example: Your job is 
        # run by the OS Cron Scheduler. 
        # If your script is running on a TMUX, it is likely you might need this loop.
        while(True):

            try:
                # do something
                # acquire lock
                thread_lock.acquire()

                # do something on resource
                print(My_Class_A.function_A(self.parameter_one))
                logger.info(My_Class_A.function_A(self.parameter_one))

            except Exception as E:
                print("Error occurred:", E)

            finally:
                # make sure to release resource lock, otherwise other threads will not be able to utilize 
                # the resource and your script will be in a deadlock
                thread_lock.release()
                time.sleep(15)
            
            # fail-safe for first run
            break



# create threads for your classes
T1 = My_Class_A(parameter_one = "One: %s" %(pendulum.now().to_datetime_string()))
T2 = My_Class_A(parameter_one = "Two: %s" %(pendulum.now().to_datetime_string()))

# set threads in daemon mode
T1.setDaemon(True)
T2.setDaemon(True)

# start threads
T1.start()
T2.start()

# sync thread to main python thread
T1.join()
T2.join()