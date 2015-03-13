"""
Utility class
Creates an iterator that wraps back around
automatically when it reaches the end.
Provides methods to seek forward/backward
and move current position forward/backward

2015.3.12 chris.harrington.jp@gmail.com

V. 0.1.0

"""

class Looper():
    
    def __init__(self, min, max, current):
        self.min = min          #Minimum value
        self.max = max          #Length of the sequence
        self.current = current  #Current value/count/position
        
    #Increment by 1
    #Redundant, but maybe faster than get_offset?
    def increment(self):
        cur = self.current
        cur += 1
        if cur == self.max:
            cur = self.min
        self.current = cur

    #Decrement by 1
    #Redundant, but maybe faster than get_offset?
    def decrement(self):
        cur = self.current
        cur -= 1
        if cur < self.min:
            cur = max - 1
        self.current = cur
            
    #Get value at offset
    def get_offset(self, offset):
        amount = offset % self.max
        result = self.current + amount
        result = result % self.max
        return amount
        
    #Set current position (count) to offset
    def set_offset(self, offset):
        self.current = self.get_offset(offset)
