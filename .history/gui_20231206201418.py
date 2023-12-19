import tkinter as tk
from tkinter import font

# Constants for repeated values
BUBBLE_SPACING = 40
PADDING = 10
START_MARGIN = 30
TEXT_WIDTH_LIMIT = 300
BUBBLE_COLOR = "#f0f0f0"
BACKGROUND_COLOR = '#202225'
FONT_COLOR = '#ffffff'         
SEND_BUTTON_COLOR = "#5865F2"
PLACEHOLDER_COLOR = '#A0A0A0'
REGULAR_COLOR = FONT_COLOR

# ======================== Utility Functions ========================

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
              x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, 
              x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y1+radius,
              x1, y1+radius, x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def add_message_bubble(canvas, message, customFont):
    y_position = START_MARGIN + (BUBBLE_SPACING + PADDING * 2) * len(chat_bubbles)
    text_width = min(canvas.winfo_width(), TEXT_WIDTH_LIMIT)
    message_label = tk.Label(canvas, text=message, bg=BUBBLE_COLOR, fg="black", 
                             font=customFont, wraplength=text_width - 2*PADDING, justify='left')
    message_label.update_idletasks()
    label_width = message_label.winfo_reqwidth() + 2*PADDING
    label_height = message_label.winfo_reqheight() + 2*PADDING

    bubble = create_rounded_rectangle(canvas,
                                      canvas.winfo_width() - label_width - 20, y_position,
                                      canvas.winfo_width() - 20, y_position + label_height + PADDING,
                                      radius=20, fill=BUBBLE_COLOR)

    message_label_window = canvas.create_window(canvas.winfo_width() - label_width - 10,
                                                y_position + (label_height / 2) + PADDING / 2,
                                                window=message_label, anchor="w")

    return bubble, message_label_window

def toggle_input_state():
    if text_field['state'] == tk.NORMAL:
        text_field['state'] = tk.DISABLED
        send_button['state'] = tk.DISABLED
    else:
        text_field['state'] = tk.NORMAL
        send_button['state'] = tk.NORMAL

def send_message():
    message = text_field.get().strip()
    if message:
        bubble, message_label_window = add_message_bubble(chat_canvas, message, customFont)
        chat_bubbles.append((bubble, message_label_window))

        chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
        chat_canvas.update_idletasks()
        text_field.delete(0, tk.END)        

# ======================== Main Window Setup ========================

# Create the main window
window = tk.Tk()
window.title("IVA Interface")
window.resizable(False, False)
window.configure(bg='#333333')

# Frames for better layout
top_frame = tk.Frame(window, bg='#333333')
top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
bottom_frame = tk.Frame(window, bg='#333333')
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Canvas for chat bubbles
chat_canvas = tk.Canvas(top_frame, bg="white", highlightthickness=0, height=500)
chat_canvas.pack(side="left", fill="both", expand=True)

# Scrollbar for the Canvas
scrollbar = tk.Scrollbar(top_frame, command=chat_canvas.yview)
scrollbar.pack(side="right", fill="y")
chat_canvas.configure(yscrollcommand=scrollbar.set)

# Track the chat bubbles
chat_bubbles = []

# Custom font
customFont = font.Font(family="Helvetica", size=12)

# ======================== Input Text Field ========================

# Placeholder text color
def focus_in(event):
    if text_field.get() == 'Message IVA...':
        text_field.delete(0, tk.END)
        text_field.config(fg=REGULAR_COLOR)

 # Function to replace placeholder text
def focus_out(event):
    if not text_field.get():
        text_field.insert(0, 'Message IVA...')
        text_field.config(fg=PLACEHOLDER_COLOR)       

# Create an input text field with placeholder
text_field = tk.Entry(bottom_frame, width=40, font=customFont, fg=PLACEHOLDER_COLOR, bg="#40444B", borderwidth=2)
text_field.pack(side=tk.LEFT, padx=20, pady=5)
text_field.insert(0, 'Message IVA...')

# Bind focus in and focus out events
text_field.bind('<FocusIn>', focus_in)
text_field.bind('<FocusOut>', focus_out)

# ======================== Send Button ========================

# Bind the Enter key to the send_message function
text_field.bind("<Return>", lambda event: send_message())

# Function to change button color on hover
def on_enter(e):
    send_button['background'] = '#7289DA'

def on_leave(e):
    send_button['background'] = SEND_BUTTON_COLOR

# Updated send button
send_button = tk.Button(bottom_frame, text="Send", command=send_message, font=customFont, bg=SEND_BUTTON_COLOR, fg="white", borderwidth=0)
send_button.pack(side=tk.RIGHT, padx=10, pady=5)
send_button.bind("<Enter>", on_enter)
send_button.bind("<Leave>", on_leave)

# ======================== Microphone ========================

# Load the microphone image
mic_image = tk.PhotoImage(file="assets/mic.png") 

# Create a microphone toggle button
mic_button = tk.Button(bottom_frame, image=mic_image, command=toggle_input_state, bg="#333333", borderwidth=0)
mic_button.pack(side=tk.RIGHT, padx=2, pady=5)

# Start the GUI event loop
window.mainloop()