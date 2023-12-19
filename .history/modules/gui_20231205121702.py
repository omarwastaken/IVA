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

        self.display_message("Hello! How can I help you today?", "right")

    def send_message(self):
        msg = self.entry_msg.get()
        self.display_message(msg, "left")
        self.entry_msg.delete(0, tk.END)

    def display_message(self, msg, side):
        label = tk.Label(self.frame, text=msg, bg="#e0e0e0", wraplength=250)
        label.pack(pady=5, padx=(10 if side == "left" else 100, 100 if side == "left" else 10), anchor=('w' if side == "left" else 'e'))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
