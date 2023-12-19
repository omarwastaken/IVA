import tkinter as tk
from tkinter import font

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1, x2-radius, y1,
              x2-radius, y1, x2, y1,
              x2, y1+radius, x2, y2-radius,
              x2, y2-radius, x2, y2,
              x2-radius, y2, x1+radius, y2,
              x1+radius, y2, x1, y2,
              x1, y2-radius, x1, y1+radius,
              x1, y1+radius, x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def send_message():
    global last_message_bottom  # Add a global variable to track the bottom of the last message

    message = text_field.get().strip()
    if message:
        bubble_spacing = 10  # Space above and below the text inside the bubble
        padding = 10  # Space on the sides of the text inside the bubble

        # Calculate the width needed for the text and add some padding for the bubble
        text_width = min(chat_canvas.winfo_width(), 300) - 2 * padding  # max bubble width of 300 pixels

        # Create a label for the text with left alignment
        message_label = tk.Label(chat_canvas, text=message, bg="#ADD8E6", fg="black", font=customFont, wraplength=text_width, justify='left')
        message_label.update_idletasks()  # Update the label's layout to get the correct dimensions
        label_width = message_label.winfo_reqwidth() + 2 * padding
        label_height = message_label.winfo_reqheight() + 2 * bubble_spacing

        # Initial y-position for the first bubble or spacing from the last bubble
        initial_offset = 50
        y_position = last_message_bottom + bubble_spacing if chat_bubbles else initial_offset

        # Create a rounded rectangle for the chat bubble
        bubble = create_rounded_rectangle(chat_canvas,
                                          chat_canvas.winfo_width() - label_width - 20, y_position,
                                          chat_canvas.winfo_width() - 20, y_position + label_height,
                                          radius=20,
                                          fill="#ADD8E6")

        # Place the label on top of the rounded rectangle
        message_label_window = chat_canvas.create_window(chat_canvas.winfo_width() - label_width - 10,
                                                         y_position + bubble_spacing,
                                                         window=message_label,
                                                         anchor="nw")

        # Append to the list of chat bubbles
        chat_bubbles.append((bubble, message_label_window))

        # Update the last message bottom position
        last_message_bottom = y_position + label_height

        # Update the scroll region and scroll to the bottom
        chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
        chat_canvas.yview_moveto('1.0')

        # Clear the text field
        text_field.delete(0, tk.END)

# Initialize the last message bottom position
last_message_bottom = 0

# Toggle function for the microphone button
def toggle_text_field():
    if text_field['state'] == tk.NORMAL:
        text_field['state'] = tk.DISABLED
        send_button['state'] = tk.DISABLED
    else:
        text_field['state'] = tk.NORMAL
        send_button['state'] = tk.NORMAL

# Create the main window
window = tk.Tk()
window.title("IVA Interface")
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
chat_canvas = tk.Canvas(top_frame, bg="white", highlightthickness=0, height=600)
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