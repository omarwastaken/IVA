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

        self.frame.bind("<Configure>", self.on_frame_configure)
        self.root.bind("<Configure>", self.on_root_configure)

        self.msg_frame = tk.Frame(root)
        self.msg_frame.pack(fill=tk.X)

        self.entry_msg = tk.Entry(self.msg_frame, width=40)
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        self.send_button = tk.Button(self.msg_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10)

        self.display_message("Hello! How can I help you today?", "left")

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_root_configure(self, event=None):
        # Reset the canvas window to encompass the inner frame when resizing
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

        # Update the wraplength for each message label to match the new canvas width
        for label in self.frame.winfo_children():
            label.config(wraplength=canvas_width - 120)  # Adjust wraplength based on the canvas size

    def send_message(self):
        msg = self.entry_msg.get()
        self.display_message(msg, "right")
        self.entry_msg.delete(0, tk.END)

    def display_message(self, msg, side):
        msg_color = "#DCF8C6" if side == "right" else "#E0E0E0"
        label = tk.Label(self.frame, text=msg, bg=msg_color, anchor='w', justify=tk.LEFT, wraplength=self.canvas.winfo_width() - 120)
        label.pack(pady=5, padx=(10, 100) if side == "right" else (100, 10), anchor='e' if side == "right" else 'w')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
