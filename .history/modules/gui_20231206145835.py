import tkinter as tk
from tkinter import font

def send_message():
    message = text_field.get().strip()
    if message:
        # Create a label for the chat bubble
        message_label = tk.Label(chat_canvas, text=message, bg="#DCF8C6", fg="black", font=customFont, wraplength=200, justify="left", padx=5, pady=3)
        chat_canvas.create_window(300, 20 + (30 * len(chat_bubbles)), window=message_label, anchor="ne", width=200)
        chat_bubbles.append(message)
        text_field.delete(0, tk.END)
        chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))

# Create the main window
window = tk.Tk()
window.title("Stylish Chat GUI")
window.resizable(False, False)
window.configure(bg='#333333')

# Custom font
customFont = font.Font(family="Helvetica", size=12)

# Frames for better layout
top_frame = tk.Frame(window, bg='#333333')
top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
bottom_frame = tk.Frame(window, bg='#333333')
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Canvas for chat bubbles
chat_canvas = tk.Canvas(top_frame, bg="white", highlightthickness=0)
chat_canvas.pack(side="left", fill="both", expand=True)

# Scrollbar for the Canvas
scrollbar = tk.Scrollbar(top_frame, command=chat_canvas.yview)
scrollbar.pack(side="right", fill="y")
chat_canvas.configure(yscrollcommand=scrollbar.set)

# Track the chat bubbles
chat_bubbles = []

# Create a text field
text_field = tk.Entry(bottom_frame, width=40, font=customFont, fg='#555555')
text_field.pack(side=tk.LEFT, padx=10, pady=5)

# Create a send button
send_button = tk.Button(bottom_frame, text="Send", command=send_message, font=customFont, bg="#0084ff", fg="white")
send_button.pack(side=tk.RIGHT, padx=10, pady=5)

window.mainloop()