import tkinter as tk
from tkinter import Canvas, Entry, Button, Scrollbar, Frame

def send_message(event=None):
    user_message = user_input.get()
    if user_message:
        add_chat_bubble(user_message, "right")
        user_input.delete(0, tk.END)
        # Here you can add the logic to get AI's response
        add_chat_bubble("AI's response here", "left")
        canvas.update_idletasks()
        canvas.yview_moveto('1.0')  # Auto-scroll to the bottom

def add_chat_bubble(message, side):
    canvas_width = canvas.winfo_width()
    bubble_width = 300
    if side == "right":
        x1 = canvas_width - bubble_width - 10  # 10 pixels padding from the right edge
    else:
        x1 = 10  # 10 pixels padding from the left edge
    bubble = canvas.create_rectangle(x1, canvas.winfo_height(), x1+bubble_width, canvas.winfo_height()+50, fill=msg_color, outline=msg_color)
    text = canvas.create_text(x1+20, canvas.winfo_height() + 25, text=message, anchor=tk.W, font=("Arial", 12), width=bubble_width-40)
    canvas.move(bubble, 0, -60)  # Move the bubble up by its own height plus a little padding
    canvas.move(text, 0, -60)  # Move the text up by its own height plus a little padding

root = tk.Tk()
root.title("Chat with AI")
root.geometry("400x500")

bg_color = "#f0f0f0"
msg_color = "#dff9fb"

# Chat area
canvas_frame = Frame(root, bg=bg_color)
canvas_frame.place(relwidth=0.8, relheight=0.8)

# Canvas for messages
canvas = Canvas(canvas_frame, bg=bg_color)
canvas.pack(expand=True, fill='both')

# Scrollbar for canvas
scrollbar = Scrollbar(canvas_frame, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill='y')
canvas.configure(yscrollcommand=scrollbar.set)

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
