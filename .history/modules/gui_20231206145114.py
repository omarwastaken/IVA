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
window.title("Chat GUI")

# Make the window unresizable
window.resizable(False, False)

# Create a chat display area
chat_display = tk.Text(window, width=50, height=15, state=tk.DISABLED)
chat_display.tag_configure('right', justify='right')
chat_display.pack(padx=10, pady=10)

# Create a text field
text_field = tk.Entry(window, width=40)
text_field.pack(side=tk.LEFT, padx=10, pady=5)

# Create a send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Run the application
window.mainloop()
