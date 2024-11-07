import time
from filefifo import Filefifo

# Initialize Filefifo and define global flag
data = Filefifo(10, name='capture_250Hz_01.txt')
read_data = []
time_spent = []
On = True

class Scale:
    
    def __init__(self, readtime, plottime):
        self.readtime = readtime
        self.plottime = plottime
        self.state = self.read
        
    def execute(self):
        self.state()
    
    def read(self):
        data_from_data = data.get()
        read_data.append(data_from_data)
        time.sleep_ms(1)
        
        self.state = self.dont_read
    
    def dont_read(self):
        time_spent.append(1)
        print(f"{len(time_spent)}ms")
        
        if len(time_spent) == self.readtime * 100:
            self.state = self.scale
        
        else:
            self.state = self.read
    
    def scale(self):
        print("aika mennyt")
        # print(read_data)
        
        old_min = min(read_data)
        old_max = max(read_data)
        new_min = 0
        new_max = 100
        
        for i in read_data:
            scaled = ((i - old_min)/(old_max - old_min)) * (new_max - new_min) + new_min
            print(scaled)
        
        On += False

scaling = Scale(2,10)

while On:
    scaling.execute()
    
