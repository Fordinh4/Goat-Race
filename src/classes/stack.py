#----------------------------------------------------
# Stack implementation
# Author: CMPUT 175 team
# Updated by: Quoc Dinh
#----------------------------------------------------

class Stack:
    '''
    An object in this class represents a single stack
    '''    
    def __init__(self) -> None:
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if len(self.items) > 0:
            return self.items.pop()
        else:
            raise
    
    def peek(self):
        if len(self.items) > 0:
            return self.items[len(self.items) - 1]
        else:
            raise
    
    def isEmpty(self):
        return self.items == []
    
    def size(self):
        return len(self.items)