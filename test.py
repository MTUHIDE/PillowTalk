from threading import Thread
from time import sleep

class TestThread(Thread):

    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout

    def run(self):
        print(f"Sleeping for {self.timeout} seconds")
        while (self.timeout > 0):
            sleep(1)
            self.timeout -= 1
            print(self.timeout)
            
        print(f"Done")
    
    def updateTime(self, timeout):
        print(f"Set timeout to {timeout} seconds")
        self.timeout = timeout

temp = TestThread(10)
temp.start()

temp = TestThread(20)
temp.start()

print(temp.is_alive())
sleep(2)
temp.updateTime(2)

temp.join() # Wait for temp to finish

print(temp.is_alive())