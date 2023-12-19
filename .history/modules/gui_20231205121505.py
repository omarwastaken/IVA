import tkinter as tk
from tkinter import simpledialog

class ChatApp:
    def __init__(self, root):
        self.root = root
        root.title("Chat App")

        self.text_area = tk.Text(root, height=20, width=50)
        self.text_area.pack(pady=10)

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
        if side == "left":
            self.text_area.insert(tk.END, f"You: {msg}\n")
        else:
            self.text_area.insert(tk.END, f"User 2: {msg}\n")
        self.text_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
