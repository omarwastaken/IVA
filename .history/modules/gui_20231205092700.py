import tkinter as tk
from PIL import ImageTk, Image

# Define window and basic layout
window = tk.Tk()
window.title("IVA")
window.geometry("600x400")

# Create circle images for user and AI
user_image = Image.new("RGB", (50, 50), color="#cccccc").convert("RGBA")
ai_image = Image.new("RGB", (50, 50), color="#007bff").convert("RGBA")

# Add antialiasing for smoother edges
user_image = user_image.resize((50, 50), Image.BILINEAR)
ai_image = ai_image.resize((50, 50), Image.BILINEAR)

# Create chat frame and add avatars
chat_frame = tk.Frame(window, bg="#eeeeee", height=300)
chat_frame.pack(fill="both", expand=True)

user_avatar = tk.Label(chat_frame, image=ImageTk.PhotoImage(user_image), bg="#eeeeee")
user_avatar.pack(side="left", padx=10, pady=10)

ai_avatar = tk.Label(chat_frame, image=ImageTk.PhotoImage(ai_image), bg="#eeeeee")
ai_avatar.pack(side="right", padx=10, pady=10)

# Chat window and input field
chat_window = tk.Text(chat_frame, bg="#dddddd", font=("Arial", 12))
chat_window.pack(fill="both", expand=True)

input_field = tk.Entry(chat_frame, bg="#ffffff", font=("Arial", 12))
input_field.pack(fill="x", side="bottom", pady=10)

# Submit button and mic button (not yet functional)
submit_button = tk.Button(chat_frame, text="Send", font=("Arial", 12), bg="#cccccc")
submit_button.pack(side="right", padx=5)

mic_button = tk.Button(chat_frame, text="Mic", font=("Arial", 12), bg="#cccccc")
mic_button.pack(side="right", padx=5)

# Function to handle user input and display chat bubbles
def send_message():
    END = ""
    message = input_field.get()
    chat_window.insert(END, f"User: {message}\n", tags="user")
    input_field.delete(0, "end")

    # Simulate AI response (replace with actual AI processing)
    ai_response = "This is a sample AI response."
    chat_window.insert(END, f"AI: {ai_response}\n", tags="ai")

# Bind Enter key to send message
input_field.bind("<Return>", send_message)

# Bind button click to submit message (optional)
submit_button.bind("<Button-1>", send_message)

# Run the main loop
window.mainloop()