from tkinter import Tk, Label, Entry, Button, Frame, Text, PhotoImage

# Define window and basic layout
window = Tk()
window.title("My AI Assistant")
window.geometry("600x400")

chat_frame = Frame(window, bg="#eeeeee", height=300)
chat_frame.pack(fill="both", expand=True)

# User and AI avatars
user_avatar = PhotoImage(file="user.png")
ai_avatar = PhotoImage(file="ai.png")

user_label = Label(chat_frame, image=user_avatar, bg="#eeeeee")
user_label.pack(side="left", padx=10, pady=10)

ai_label = Label(chat_frame, image=ai_avatar, bg="#eeeeee")
ai_label.pack(side="right", padx=10, pady=10)

# Chat window and input field
chat_window = Text(chat_frame, bg="#dddddd", font=("Arial", 12))
chat_window.pack(fill="both", expand=True)

input_field = Entry(chat_frame, bg="#ffffff", font=("Arial", 12))
input_field.pack(fill="x", side="bottom", pady=10)

# Submit button and mic button (not yet functional)
submit_button = Button(chat_frame, text="Send", font=("Arial", 12), bg="#cccccc")
submit_button.pack(side="right", padx=5)

mic_button = Button(chat_frame, text="Mic", font=("Arial", 12), bg="#cccccc")
mic_button.pack(side="right", padx=5)

# Function to handle user input and display chat bubbles
def send_message():
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
