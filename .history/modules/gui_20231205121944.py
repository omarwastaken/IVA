import tkinter as tk
from tkinter import simpledialog

class ChatApp:
    def __init__(self, root):
        self.root = root
        root.title("Chat App")

        self.canvas = tk.Canvas(root, height=400, width=500)
        self.canvas.pack(pady=10)

        self.scrollbar = tk.Scrollbar(root, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.msg_frame = tk.Frame(root)
        self.msg_frame.pack()

        self.entry_msg = tk.Entry(self.msg_frame, width=40)
        self.entry_msg.pack(side=tk.LEFT, padx=10)

        self.send_button = tk.Button(self.msg_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.display_message("Hello! How can I help you today?", "left")

    def send_message(self):
        msg = self.entry_msg.get()
        self.display_message(msg, "right")
        self.entry_msg.delete(0, tk.END)

    def display_message(self, msg, side):
        # Align all labels to the left but adjust padding to differentiate sides
        label = tk.Label(self.frame, text=msg, bg="#e0e0e0", wraplength=250)
        if side == "left":
            label.pack(pady=5, padx=(10, 10), anchor='w')
        else:  # User messages on the right
            label.pack(pady=5, padx=(10, 10), anchor='w')

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
