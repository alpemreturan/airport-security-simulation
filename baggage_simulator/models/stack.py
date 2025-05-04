class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        
class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        temp = self.top
        self.top = self.top.next
        return temp.data

    def is_empty(self):
        return self.top is None

    def to_list(self):
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result