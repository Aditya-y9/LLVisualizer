from Node import Node

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def insert_node(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1

    def delete_node(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                self.length -= 1
                break
            current = current.next

    def traverse(self):
        current = self.head
        cpp_code = "Node* current = head;\nwhile (current) {\n    // Process current node (current->data)\n    current = current->next;\n}"
        return cpp_code

    def get_next_data_by_node(self, data):
        current = self.head
        while current:
            if current.data == data and current.next:
                return current.next.data
            current = current.next
        return None
