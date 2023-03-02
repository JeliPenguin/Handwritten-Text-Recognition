class Stack():
    def __init__(self,size =3 ):
        self.size = size
        self.stack = []
        self.top = -1
    def alter_size(self,new_size):
        self.size = new_size
    def push(self,item):
        if len(self.stack) == self.size:
            print("Stack is full")
        else: 
            self.stack.append(item)
            self.top += 1
    def peak(self):
        if self.top == -1:
            print("Stack is empty")
        else:
            print(self.stack[self.top])
    def pop(self):
        if self.top == -1:
            print("Stack is already empty")
        else:
            return self.stack[self.top]
            del self.stack[self.top]
            self.top -= 1
