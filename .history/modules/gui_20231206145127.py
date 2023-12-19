import tkinter as tk
from tkinter import font

def send_message():
    # Get the message from the text field
    message = text_field.get()
    # Clear the text field
    text_field.delete(0, tk.END)
    # Add the message to the chat display
    if message.strip() != "":
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, message + "\n", 'right')
        chat_display.config(state=tk.DISABLED)
        # Scroll to the bottom
        chat_display.see(tk.END)

# Create the main window
window = tk.Tk()
window.title("Stylish Chat GUI")
window.resizable(False, False)
window.configure(bg='#333333')  # Set a background color

# Custom font
customFont = font.Font(family="Helvetica", size=12)

# Frames for better layout
top_frame = tk.Frame(window, bg='#333333')
top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
bottom_frame = tk.Frame(window, bg='#333333')
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create a chat display area
chat_display = tk.Text(top_frame, width=50, height=15, bg="#FFFFFF", fg="#000000", font=customFont)
chat_display.tag_configure('right', justify='right')
chat_display.pack(padx=10, pady=10)

# Create a text field
text_field = tk.Entry(bottom_frame, width=40, font=customFont, fg='#555555')
text_field.pack(side=tk.LEFT, padx=10, pady=5)
text_field.insert(0, "Type your message here...")

# Create a send button
send_button = tk.Button(bottom_frame, text="Send", command=send_message, font=customFont, bg="#0084ff", fg="white")
send_button.pack(side=tk.RIGHT, padx=10, pady=5)

window.mainloop()