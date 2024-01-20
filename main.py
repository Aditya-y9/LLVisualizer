import tkinter as tk
from tkinter import ttk

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def insert_node(self, data, next_node):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            if next_node:
                new_node.next = next_node.next
                new_node.prev = next_node
                if next_node.next:
                    next_node.next.prev = new_node
                next_node.next = new_node
                if next_node == self.tail:
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

# Tkinter App
class LinkedListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linked List Visualization")

        self.canvas = tk.Canvas(root, width=800, height=400, bg='white')
        self.canvas.pack(pady=10)

        self.linked_list = LinkedList()
        self.cpp_code_var = tk.StringVar()

        self.next_node_var = tk.StringVar()
        self.next_node_var.set("None")

        self.create_buttons()

    def create_buttons(self):
        ttk.Button(self.root, text="Insert Node", command=self.insert_node).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.root, text="Delete Node", command=self.delete_node).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.root, text="Traverse", command=self.traverse).pack(side=tk.LEFT, padx=10)

        ttk.Label(self.root, text="Choose Next Node:").pack(side=tk.LEFT, padx=10)
        nodes = ["None"] + [str(i) for i in range(1, self.linked_list.length + 1)]
        ttk.Combobox(self.root, values=nodes, textvariable=self.next_node_var).pack(side=tk.LEFT, padx=10)

    def draw_node(self, data, x, y):
        box_size = 60
        self.canvas.create_rectangle(x, y, x + box_size, y + box_size, outline='black')
        self.canvas.create_text(x + box_size // 2, y + box_size // 2, text=str(data))
        return x + box_size

    def draw_arrow(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)

    def insert_node(self):
        data = self.linked_list.length + 1
        next_node_str = self.next_node_var.get()
        next_node = None if next_node_str == "None" else self.get_node_by_data(int(next_node_str))
        self.linked_list.insert_node(data, next_node)
        self.clear_canvas()
        self.draw_linked_list()
        self.draw_cpp_code(f"linkedList.insertNode({data}, {next_node_str});")

    def delete_node(self):
        data = self.linked_list.length
        if data > 0:
            self.linked_list.delete_node(data)
            self.clear_canvas()
            self.draw_linked_list()
            self.draw_cpp_code(f"linkedList.deleteNode({data});")

    def traverse(self):
        self.clear_canvas()
        self.draw_linked_list()
        cpp_code = self.linked_list.traverse()
        self.draw_cpp_code(cpp_code)

    def draw_linked_list(self):
        current = self.linked_list.head
        x = 20
        while current:
            x = self.draw_node(current.data, x, 200)
            if current.next:
                self.draw_arrow(x - 60, 230, x, 230)
            current = current.next

    def draw_cpp_code(self, code):
        self.cpp_code_var.set(code)
        ttk.Label(self.root, textvariable=self.cpp_code_var).pack(side=tk.BOTTOM)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.cpp_code_var.set("")

    def get_node_by_data(self, data):
        current = self.linked_list.head
        while current:
            if current.data == data:
                return current
            current = current.next
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkedListApp(root)
    root.mainloop()
