class Queue():
    def __init__(self,size = 3):
        self.size = size
        self.front = 0
        self.rear = -1
        self.queue = []
    def alter_size(self,new_size):
        self.size = new_size
    def enqueue(self,item):
        if len(self.queue) == self.size:
            print("The queue is full")
        else:
            self.queue.append(item)
            self.rear += 1
    def dequeue(self):
        if self.front > self.rear:
            print("End of queue")
        else:
            return_item = self.queue[self.front]
            self.queue[self.front] = "DELETED"
            self.front += 1
            return return_item


