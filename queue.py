# Implementacion de una cola en Python


class Queue:
    """Implementacion de una cola"""
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        print('QUEUE')
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def display(self):
        return self.items

queue=Queue()
