import tkinter as tk
from tkinter import font

def send_message():
    message = text_field.get().strip()
    if message:
        # Adjust the y-position for each new message
        y_position = 20 + (40 * len(chat_bubbles))

        # Calculate the width needed for the text and add some padding for the bubble
        message_width = min(chat_canvas.winfo_width(), 300)  # max bubble width of 300 pixels

        # Create a rounded rectangle for the chat bubble
        bubble = chat_canvas.create_rectangle(chat_canvas.winfo_width() - message_width - 20,
                                              y_position - 10,  # Add some padding above the text
                                              chat_canvas.winfo_width() - 20,
                                              y_position + 20,  # Add some padding below the text
                                              outline="#ADD8E6",
                                              fill="#ADD8E6",
                                              width=2,
                                              roundness=20)

        # Create a label for the text
        message_label = tk.Label(chat_canvas, text=message, bg="#ADD8E6", fg="black", font=customFont, wraplength=message_width - 20)
        message_label_window = chat_canvas.create_window(chat_canvas.winfo_width() - 20 - (message_width / 2),
                                                         y_position,
                                                         window=message_label,
                                                         anchor="center")

        # Append to the list of chat bubbles (to keep references to them)
        chat_bubbles.append((bubble, message_label_window))

        # Update the scroll region and scroll to the bottom
        chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
        chat_canvas.yview_moveto('1.0')

        # Clear the text field
        text_field.delete(0, tk.END)

# Rest of your code remains the same...

# Start the GUI event loop
window.mainloop()
