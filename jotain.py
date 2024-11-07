from filefifo import Filefifo

def peak_to_peak():
    hz = 250
    interval = 1 / hz
    data = Filefifo(10, name='capture_250Hz_01.txt')
    
    last_value = data.get() # 0
    current_value = data.get() # 1
    
    peaks = []
    peak_time = []
    
    for sample in range(2, 1000):
        next_value = data.get()
        
        if current_value > last_value and current_value > next_value:
            peaks.append(sample)
            time_of_sample = (sample * interval)
            peak_time.append(time_of_sample)
            
            print(f"PEAK: {sample}, TIME: {time_of_sample}")
            
        if len(peaks) >= 4:
            break
        
        last_value = current_value
        current_value = next_value

peak_to_peak()
