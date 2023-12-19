import tkinter as tk
from tkinter import font

def send_message():
    message = text_field.get().strip()
    if message:
        # Adjust the y-position for each new message
        y_position = 20 + (40 * len(chat_bubbles))

        # Create a label for the chat bubble with left-aligned text
        message_label = tk.Label(chat_canvas, text=message, bg="#ADD8E6", fg="black", font=customFont, wraplength=200, justify="left", anchor="w", padx=10, pady=5)

        # Calculate the x-position based on the message width
        message_width = message_label.winfo_reqwidth()
        x_position = chat_canvas.winfo_width() - 20  # 20 pixels padding from the right side

        # Place the chat bubble on the canvas
        chat_canvas.create_window(x_position, y_position, window=message_label, anchor="ne", width=message_width)
        
        # Append to the list of chat bubbles
        chat_bubbles.append(message)

        # Update the scroll region and scroll to the bottom
        chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
        chat_canvas.yview_moveto('1.0')

        # Clear the text field
        text_field.delete(0, tk.END)


def toggle_text_field():
    if text_field['state'] == tk.NORMAL:
        text_field['state'] = tk.DISABLED
        send_button['state'] = tk.DISABLED
    else:
        text_field['state'] = tk.NORMAL
        send_button['state'] = tk.NORMAL

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

# Bind the Enter key to the send_message function
text_field.bind("<Return>", lambda event: send_message())

# Create a send button
send_button = tk.Button(bottom_frame, text="Send", command=send_message, font=customFont, bg="#0084ff", fg="white")
send_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Load the microphone image
mic_image = tk.PhotoImage(file="assets/mic.png") 

# Create a microphone toggle button
mic_button = tk.Button(bottom_frame, image=mic_image, command=toggle_text_field, bg="#333333", borderwidth=0)
mic_button.pack(side=tk.RIGHT, padx=2, pady=5)

# Start the GUI event loop
window.mainloop()