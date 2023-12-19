import tkinter as tk
from tkinter import simpledialog

class ChatApp:
    def __init__(self, root):
        self.root = root
        root.title("Chat App")

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(root, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.frame = tk.Frame(self.canvas, bg="white")
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.msg_frame = tk.Frame(root, bg="white")
        self.msg_frame.pack(fill=tk.X)

        self.entry_msg = tk.Entry(self.msg_frame, width=40)
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

        self.send_button = tk.Button(self.msg_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.root.bind('<Configure>', self.on_resize)
        self.display_message("Hello! How can I help you today?", "left")

    def send_message(self):
        msg = self.entry_msg.get()
        self.display_message(msg, "right")
        self.entry_msg.delete(0, tk.END)

    def display_message(self, msg, side):
        message_frame = tk.Frame(self.frame, bg="white")
        message_frame.pack(fill=tk.X, pady=5)

        label = tk.Label(message_frame, text=msg, bg="#e0e0e0", anchor='w', justify=tk.LEFT, wraplength=self.root.winfo_width() - 20)
        label.pack(padx=(10, 100) if side == "right" else (100, 10), anchor='e' if side == "right" else 'w')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_resize(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    app = ChatApp(root)
    root.mainloop()
