import tkinter as tk
from tkinter import simpledialog

class ChatApp:
    def __init__(self, root):
        self.root = root
        root.title("Chat App")

        self.canvas = tk.Canvas(root, height=400, width=500)
        self.canvas.pack(side=tk.LEFT, fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(root, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.frame = tk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.msg_frame = tk.Frame(root)
        self.msg_frame.pack(fill=tk.X)

        self.entry_msg = tk.Entry(self.msg_frame, width=40)
        self.entry_msg.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.send_button = tk.Button(self.msg_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.display_message("Hello! How can I help you today?", "left")

        self.root.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        # Adjust the scrollregion to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Resize the canvas frame to match the canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

        # Update the wraplength for each label to fit the new window width
        for label in self.frame.winfo_children():
            label.configure(wraplength=event.width - 20)

    def send_message(self):
        msg = self.entry_msg.get()
        self.display_message(msg, "right")
        self.entry_msg.delete(0, tk.END)

    def display_message(self, msg, side):
        label = tk.Label(self.frame, text=msg, bg="#e0e0e0", anchor='w', justify=tk.LEFT)
        label.pack(pady=5, fill='x', padx=(10 if side == "right" else 100, 100 if side == "right" else 10), anchor=('e' if side == "right" else 'w'))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
