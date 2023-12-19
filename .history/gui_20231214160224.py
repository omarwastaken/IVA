import tkinter as tk
from tkinter import font
from tkinter import messagebox
import threading
from main import process_input
from modules.utils import speak, recognize_speech

class ChatInterface:
    """Class to create and manage the chat interface for IVA."""
    # ======================== Constants and Configurations ========================

    # Interface
    CHAT_AREA_WIDTH = 600
    ENTRY_WIDTH = 40
    BUTTON_PADDING_X = 10
    BUTTON_PADDING_Y = 5

    # Colors
    BACKGROUND_COLOR = '#202225'
    FONT_COLOR = '#ffffff'
    SEND_BUTTON_COLOR = "#5865F2"
    PLACEHOLDER_COLOR = '#A0A0A0'

    # Text
    FONT_FAMILY = "Helvetica"
    FONT_SIZE = 12
    LINE_SPACING = 12

    # ======================== Initialization and Setup ========================

    def __init__(self, root):
        """Initialize the ChatInterface with the root window."""
        self.root = root
        self.previous_questions_and_answers = []
        self.mic_mode = False

        try:
            self.setup_ui()
            self.initial_ai_message()
        except Exception as e:
            messagebox.showerror("Initialization Error", f"An error occurred during initialization: {e}")
            self.root.destroy()

    def initial_ai_message(self):
        """Handle the initial AI message with non-blocking speech."""
        initial_message = "How can I help you today?"
        self.append_message("➢ IVA: " + initial_message)
        threading.Thread(target=lambda: self.speak_threaded(initial_message), daemon=True).start()

    def speak_threaded(self, message):
        """Run the speak function in a separate thread."""
        speak(message)

    def setup_ui(self, ):
        """Setup the main UI components of the chat interface."""
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=self.BACKGROUND_COLOR)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        self.chat_frame = tk.Frame(self.paned_window, bg=self.BACKGROUND_COLOR)
        self.paned_window.add(self.chat_frame, width=self.CHAT_AREA_WIDTH)
        self.top_frame = tk.Frame(self.chat_frame, bg=self.BACKGROUND_COLOR)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_frame = tk.Frame(self.chat_frame, bg=self.BACKGROUND_COLOR)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        # Chat Text with customizable font and line spacing
        chat_text_font = font.Font(family=self.FONT_FAMILY, size=self.FONT_SIZE)
        self.chat_text = tk.Text(
            self.top_frame,
            bg="white",
            fg="black",
            font=chat_text_font,
            state=tk.DISABLED,
            wrap=tk.WORD,
            spacing3=self.LINE_SPACING
        )
        self.chat_text.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(self.top_frame, command=self.chat_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.chat_text.configure(yscrollcommand=scrollbar.set)
        self.setup_input_field()
        self.setup_send_button()
        self.setup_microphone()

    # ======================== UI Component Creation ========================

    def setup_input_field(self):
        """Setup the input text field."""
        self.text_field = tk.Entry(self.bottom_frame, font=font.Font(family="Helvetica", size=12), fg=self.PLACEHOLDER_COLOR, bg="#40444B", borderwidth=2)
        self.text_field.grid(row=0, column=1, sticky="ew", padx=self.BUTTON_PADDING_X, pady=self.BUTTON_PADDING_Y)
        self.text_field.insert(0, 'Message IVA...')
        self.text_field.bind('<FocusIn>', self.focus_in)
        self.text_field.bind('<FocusOut>', self.focus_out)
        self.text_field.bind("<Return>", self.send_message)

    def setup_send_button(self):
        """Setup the send button"""
        self.send_button = tk.Button(self.bottom_frame, text="Send", command=self.send_message, font=font.Font(family="Helvetica", size=12), bg=self.SEND_BUTTON_COLOR, fg="white", borderwidth=0)
        self.send_button.pack(side=tk.RIGHT, padx=self.BUTTON_PADDING_X, pady=self.BUTTON_PADDING_Y)
        self.send_button.bind("<Enter>", lambda e: self.send_button.config(background='#7289DA'))
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(background=self.SEND_BUTTON_COLOR))

    def setup_microphone(self):
        """Setup the microphone button."""
        try:
            self.mic_image = tk.PhotoImage(file="assets/mic.png")
        except tk.TclError as e:
            messagebox.showerror("Resource Load Error", f"Failed to load microphone image: {e}")
            self.mic_image = None
        self.mic_button = tk.Button(self.bottom_frame, image=self.mic_image, command=self.toggle_input_state, bg="#333333", borderwidth=0)
        self.mic_button.pack(side=tk.RIGHT, padx=2, pady=self.BUTTON_PADDING_Y)        

    # ======================== Event Handling ========================

    def send_message(self, event=None):
        """Handle sending of a message."""
        message = self.text_field.get().strip()
        if message:
            self.append_message("➢ User: " + message)
            self.text_field.delete(0, tk.END)
            threading.Thread(target=self.process_and_display_response, args=(message,), daemon=True).start()

    def process_and_display_response(self, message):
        """Process the user message and display the AI's response."""
        self.start_typing_animation()
        response = process_input(message, self.previous_questions_and_answers)
        self.root.after(0, lambda: [self.stop_typing_animation(), self.append_message("➢ IVA: " + response) if response else None])
        speak(response)

    def append_message(self, message):
        """Append a message to the chat text widget."""
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, message + "\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)

    def focus_in(self, event):
        """Handle focus-in event on the text field."""
        if self.text_field.get() == 'Message IVA...':
            self.text_field.delete(0, tk.END)
            self.text_field.config(fg=self.FONT_COLOR)

    def focus_out(self, event):
        """Handle focus-out event on the text field."""
        if not self.text_field.get():
            self.text_field.insert(0, 'Message IVA...')
            self.text_field.config(fg=self.PLACEHOLDER_COLOR) 

    def toggle_input_state(self):
        """Toggle microphone input state."""
        if self.mic_mode:
            self.mic_mode = False
            self.text_field['state'] = tk.NORMAL
            self.send_button['state'] = tk.NORMAL
        else:
            self.mic_mode = True
            self.text_field['state'] = tk.DISABLED
            self.send_button['state'] = tk.DISABLED
            self.listen_and_convert_speech()

    def listen_and_convert_speech(self):
        """Convert speech to text and send as a message."""
        if self.mic_mode:
            text = recognize_speech()
            if text:
                self.append_message("--> User: " + text)
                threading.Thread(target=self.process_and_display_response, args=(text,), daemon=True).start()               

    # ======================== Animation and Visual Effects ========================

    def start_typing_animation(self):
        """Start the typing animation."""
        self.typing_message = "IVA is typing"
        self.append_message(self.typing_message)
        self.typing_animation_id = self.root.after(500, self.update_typing_animation)

    def update_typing_animation(self):
        """Update the typing animation."""
        dots = self.typing_message.count('.') % 3 + 1
        self.typing_message = "IVA is typing" + "." * dots
        self.replace_last_message(self.typing_message)
        self.typing_animation_id = self.root.after(500, self.update_typing_animation)

    def stop_typing_animation(self):
        """Stop the typing animation."""
        if hasattr(self, 'typing_animation_id'):
            self.root.after_cancel(self.typing_animation_id)
            self.replace_last_message("")

    def replace_last_message(self, new_message):
        """Replace the last message in the chat text widget."""
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete("end-2l", "end-1l")
        if new_message:
            self.chat_text.insert(tk.END, new_message + "\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)

# ======================== Main Execution ========================

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.title("IVA Interface")
        root.configure(bg=ChatInterface.BACKGROUND_COLOR)
        root.geometry("800x600")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        chat_interface = ChatInterface(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"An unrecoverable error occurred: {e}")