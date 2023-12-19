import tkinter as tk
from tkinter import Canvas, Entry, Button, Scrollbar, Frame

def send_message(event=None):
    user_message = user_input.get()
    if user_message:
        add_chat_bubble(user_message, "right")
        user_input.delete(0, tk.END)
        # Here you can add the logic to get AI's response
        add_chat_bubble("AI's response here", "left")

def add_chat_bubble(message, side):
    bubble = Canvas(chat_frame, width=300, height=50, bg=bg_color, highlightthickness=0)
    bubble.pack(pady=5, anchor=tk.E if side == "right" else tk.W)
    bubble.create_oval(10, 10, 50, 50, fill=msg_color, outline=msg_color)
    bubble.create_polygon((50, 30, 70, 20, 70, 40), fill=msg_color, outline=msg_color)
    bubble.create_text(60, 25, text=message, anchor=tk.W, font=("Arial", 12), width=250)

root = tk.Tk()
root.title("Chat with AI")
root.geometry("400x500")

bg_color = "#f0f0f0"
msg_color = "#dff9fb"

# Chat area
chat_frame = Frame(root, bg=bg_color)
chat_frame.place(relwidth=0.8, relheight=0.8)

# Scrollbar
scrollbar = Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# User input area
user_input = Entry(root, bg=msg_color, font=("Arial", 12))
user_input.place(relwidth=0.74, relheight=0.06, rely=0.82)
user_input.focus()
user_input.bind("<Return>", send_message)

# Send button
send_button = Button(root, text="Send", command=send_message)
send_button.place(relx=0.76, rely=0.82, relwidth=0.24, relheight=0.06)

# Sample AI message
add_chat_bubble("Hello, how can I assist you?", "left")

root.mainloop()
