import tkinter as tk
from tkinter import ttk, simpledialog

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

        self.dev = ttk.Label(self.root, text="Made with ❤️ by Aditya Yedurkar")
        self.dev.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.spacing = 80  # Initial spacing between nodes
        self.create_buttons()

    def insert_node(self):
        data = self.linked_list.length + 1
        self.linked_list.insert_node(data)
        x = 20  + self.spacing
        self.draw_node(data, x, 200)
        self.spacing += 80  # Increase the spacing for the next node
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


    def make_reference(self):
        node_to_reference = simpledialog.askinteger("Make Reference", "Enter the data of the node to make reference from:", parent=self.root)
        node_referenced = simpledialog.askinteger("Make Reference", "Enter the data of the node to set as reference:", parent=self.root)

        # Find the coordinates of the nodes
        x1 = 60 + (node_to_reference - 1) * 80 + 60
        x2 = 60 + (node_referenced - 1) * 80 + 60

        # Draw arrow from node_to_reference to node_referenced
        self.draw_arrow(x1, 200, x2, 200)

        # Update the linked list logic
        current = self.linked_list.head
        node_to_reference_ptr = None
        node_referenced_ptr = None

        # Find the nodes in the linked list
        while current:
            if current.data == node_to_reference:
                node_to_reference_ptr = current
            elif current.data == node_referenced:
                node_referenced_ptr = current

            if node_to_reference_ptr and node_referenced_ptr:
                break

            current = current.next

        # Set the next reference
        if node_to_reference_ptr and node_referenced_ptr:
            node_to_reference_ptr.next = node_referenced_ptr

        # Redraw the linked list
        self.clear_canvas()
        self.draw_linked_list()
        self.draw_cpp_code(f"Node* nodeToReference = head;\nNode* nodeReferenced = head;\nwhile (nodeToReference->data != {node_to_reference})\n    nodeToReference = nodeToReference->next;\nwhile (nodeReferenced->data != {node_referenced})\n    nodeReferenced = nodeReferenced->next;\nnodeToReference->next = nodeReferenced;")


    def create_buttons(self):
        ttk.Button(self.root, text="Insert Node", command=self.insert_node).pack(side=tk.TOP, padx=10, pady=5)
        ttk.Button(self.root, text="Delete Node", command=self.delete_node).pack(side=tk.TOP, padx=10, pady=5)
        ttk.Button(self.root, text="Traverse", command=self.traverse).pack(side=tk.TOP, padx=10, pady=5)
        ttk.Button(self.root, text="Make Reference", command=self.make_reference).pack(side=tk.TOP, padx=10, pady=5)

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

        return x + box_size  # Return the updated x value


    def draw_arrow(self, x1, y1, x2, y2):
        y1 += 30
        y2 += 30
        arrow_head_size = 5
        arrow_length = 10
        self.canvas.create_line(x1, y1, x2 - arrow_length, y2, arrow=tk.LAST, width=2)

        # Calculate the arrowhead coordinates
        angle = math.atan2(y2 - y1, x2 - x1)
        x_head = x2 - arrow_head_size * math.cos(angle - math.pi / 6)
        y_head = y2 - arrow_head_size * math.sin(angle - math.pi / 6)

        x_tail = x2 - arrow_head_size * math.cos(angle + math.pi / 6)
        y_tail = y2 - arrow_head_size * math.sin(angle + math.pi / 6)

        # Draw the arrowhead polygon
        self.canvas.create_polygon(x2, y2, x_head, y_head, x_tail, y_tail, fill='black')


    def draw_linked_list(self):
        current = self.linked_list.head
        x = 60
        while current:
            x = self.draw_node(current.data, x + 60, 200)
            current = current.next

        # Reset x for drawing arrows
        x = 60
        current = self.linked_list.head
        while current and current.next:
            x_from = x + 60
            x_to = x + 60 + self.spacing
            x += self.spacing
            current = current.next


    def draw_cpp_code(self, code):
        ttk.Label(self.cpp_frame, text=code, wraplength=300, justify=tk.LEFT).pack(side=tk.TOP)

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkedListApp(root)
    root.mainloop()