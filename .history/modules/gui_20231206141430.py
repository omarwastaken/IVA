import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Simple GUI")

# Create a text field
text_field = tk.Entry(window, width=40)
text_field.pack(side=tk.LEFT, padx=10, pady=10)

# Create a send button
send_button = tk.Button(window, text="Send")
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Run the application
window.mainloop()