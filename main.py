import tkinter as tk
from tkinter import ttk
from mailcap import show

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

# Tkinter App
class LinkedListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linked List Visualization")

        self.canvas = tk.Canvas(root, width=800, height=400, bg='white')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.cpp_frame = ttk.Frame(root)
        self.cpp_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        self.linked_list = LinkedList()
        self.cpp_code_var = tk.StringVar()

        self.next_node_var = tk.StringVar()
        self.next_node_var.set("None")

        self.dev = ttk.Label(self.root, text="Made with ❤️by Aditya Yedurkar")
        self.dev.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.create_buttons()

    def create_buttons(self):
        ttk.Button(self.root, text="Insert Node", command=self.insert_node).pack(side=tk.TOP, padx=10, pady=5)
        ttk.Button(self.root, text="Delete Node", command=self.delete_node).pack(side=tk.TOP, padx=10, pady=5)
        ttk.Button(self.root, text="Traverse", command=self.traverse).pack(side=tk.TOP, padx=10, pady=5)
        ttk.Button(self.root, text="Set Next Reference", command=self.set_next_reference).pack(side=tk.TOP, padx=10, pady=5)

        ttk.Label(self.root, text="Choose Next Node:").pack(side=tk.TOP, padx=10, pady=5)
        nodes = ["None"] + [str(i) for i in range(1, self.linked_list.length + 1)]
        ttk.Combobox(self.root, values=nodes, textvariable=self.next_node_var).pack(side=tk.TOP, padx=10, pady=5)

    def draw_node(self, data, x, y):
        box_size = 60
        self.canvas.create_rectangle(x, y, x + box_size, y + box_size, outline='black', width=2)

        # Draw data compartment
        self.canvas.create_rectangle(x + 5, y + 5, x + box_size - 5, y + 25, outline='black', fill='white')
        self.canvas.create_text(x + box_size // 2, y + 15, text=f"Data: {data}", font=('Arial', 8))

        # Draw next compartment
        next_data = self.linked_list.get_next_data_by_node(data)
        next_text = f"Next: {next_data}" if next_data is not None else "Next: None"
        self.canvas.create_rectangle(x + 5, y + 25, x + box_size - 5, y + box_size - 5, outline='black', fill='white')
        self.canvas.create_text(x + box_size // 2, y + box_size - 10, text=next_text, font=('Arial', 8))

        return x + box_size

    def draw_arrow(self, x1, y1, x2, y2):
        arrow_head_size = 5
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            dx /= length
            dy /= length
            x2 = x1 + dx * 40  # Adjust arrow length to 40 pixels
            y2 = y1 + dy * 40  # Adjust arrow length to 40 pixels

        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2)
        self.canvas.create_polygon(x2, y2, x2 - arrow_head_size * dx - arrow_head_size * dy,
                                   y2 - arrow_head_size * dy + arrow_head_size * dx,
                                   x2 - arrow_head_size * dx + arrow_head_size * dy,
                                   y2 - arrow_head_size * dy - arrow_head_size * dx, fill='black')

    def insert_node(self):
        data = self.linked_list.length + 1
        self.linked_list.insert_node(data)
        self.clear_canvas()
        self.draw_linked_list()
        self.draw_cpp_code(f"linkedList.insertNode({data});")

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

    def set_next_reference(self):
        next_node_str = self.next_node_var.get()
        if next_node_str != "None":
            data = self.linked_list.length
            next_node_data = int(next_node_str)
            next_x = self.draw_node(next_node_data, 20 + (next_node_data - 1) * 70, 200)
            current_x = 20 + (data - 1) * 70
            self.draw_arrow(current_x, 230, next_x, 230)
            self.linked_list.head.next = Node(next_node_data)  # Adjust the linked list manually
            self.draw_cpp_code(f"linkedList.head->next = new Node({next_node_data});")

    def draw_linked_list(self):
        current = self.linked_list.head
        x = 20
        while current:
            x = self.draw_node(current.data, x+40, 200)
            if current.next:
                # next_x = self.draw_node(current.next.data, x + 40, 200)
                self.draw_arrow(x, 230, x+40, 230)
            current = current.next

    def draw_cpp_code(self, code):
        ttk.Label(self.cpp_frame, text=code, wraplength=300, justify=tk.LEFT).pack(side=tk.TOP)

    def clear_canvas(self):
        self.canvas.delete("all")


if __name__ == "__main__":
    root = tk.Tk()
    app = LinkedListApp(root)
    root.mainloop()
