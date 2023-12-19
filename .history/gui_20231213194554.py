import tkinter as tk
from tkinter import font
from tkinter import messagebox
import threading
from main import process_input
from modules.utils import speak, recognize_speech

class ChatInterface:
    """Class to create and manage the chat interface for IVA."""
    # ======================== Constants and Configurations ========================
    
    #interface
    BUBBLE_SPACING = 40
    PADDING = 10
    TEXT_WIDTH_LIMIT = 300
    CHAT_AREA_WIDTH = 750
    START_MARGIN = 40
    WINDOW_OFFSET = 10
    CHAT_AREA_HEIGHT = 600
    ENTRY_WIDTH = 40
    BUTTON_PADDING_X = 10
    BUTTON_PADDING_Y = 5

    #Colors
    BUBBLE_COLOR = "#f0f0f0"
    BACKGROUND_COLOR = '#202225'
    FONT_COLOR = '#ffffff'
    SEND_BUTTON_COLOR = "#5865F2"
    PLACEHOLDER_COLOR = '#A0A0A0'
    REGULAR_COLOR = FONT_COLOR

    # ======================== Initialization and Setup ========================

    def __init__(self, root):
        """Initialize the ChatInterface with the root window."""
        self.root = root
        self.chat_bubbles = {}
        self.previous_questions_and_answers = []
        self.typing_animation_id = None
        self.typing_bubble_id = None
        self.is_typing_animation_active = False
        self.bubble_margin_top = self.START_MARGIN
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
        self.add_ai_message(initial_message)
        threading.Thread(target=lambda: self.speak_threaded(initial_message), daemon=True).start()

    def speak_threaded(self, message):
        """Run the speak function in a separate thread."""
        speak(message)

    def setup_ui(self):
        """Setup the main UI components of the chat interface."""
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=self.BACKGROUND_COLOR)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        self.chat_frame = tk.Frame(self.paned_window, bg=self.BACKGROUND_COLOR)
        self.paned_window.add(self.chat_frame, width=self.CHAT_AREA_WIDTH)
        self.top_frame = tk.Frame(self.chat_frame, bg=self.BACKGROUND_COLOR)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_frame = tk.Frame(self.chat_frame, bg=self.BACKGROUND_COLOR)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.chat_canvas = tk.Canvas(self.top_frame, bg="white", highlightthickness=0, height=self.CHAT_AREA_HEIGHT, width=self.CHAT_AREA_WIDTH)
        self.chat_canvas.pack(side="left", fill="both", expand=False)
        scrollbar = tk.Scrollbar(self.top_frame, command=self.chat_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        self.customFont = font.Font(family="Helvetica", size=12)
        self.setup_input_field()
        self.setup_send_button()
        self.setup_microphone()

    # ======================== UI Component Creation ========================

    def setup_input_field(self):
        """Setup the input text field."""
        self.text_field = tk.Entry(self.bottom_frame, width=self.ENTRY_WIDTH, font=self.customFont, fg=self.PLACEHOLDER_COLOR, bg="#40444B", borderwidth=2)
        self.text_field.pack(side=tk.LEFT, padx=self.BUTTON_PADDING_X, pady=self.BUTTON_PADDING_Y)
        self.text_field.insert(0, 'Message IVA...')
        self.text_field.bind('<FocusIn>', self.focus_in)
        self.text_field.bind('<FocusOut>', self.focus_out)
        self.text_field.bind("<Return>", self.send_message)

    def setup_send_button(self):
        """Setup the send button"""
        self.send_button = tk.Button(self.bottom_frame, text="Send", command=self.send_message, font=self.customFont, bg=self.SEND_BUTTON_COLOR, fg="white", borderwidth=0)
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
            self.add_message_bubble(message, is_user=True)
            self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
            self.chat_canvas.yview_moveto(1)
            self.text_field.delete(0, tk.END)
            threading.Thread(target=self.process_and_display_response, args=(message,), daemon=True).start()

    def process_and_display_response(self, message):
    self.root.after(0, self.show_typing_animation)
    response = process_input(message, self.previous_questions_and_answers)
    self.root.after(0, lambda: [self.hide_typing_animation(), self.add_ai_message(response) if response else None])
    speak(response)
    if self.mic_mode:
        self.root.after(1000, self.listen_and_convert_speech)

    def add_ai_message(self, message):
        """Add a message from the AI to the chat interface."""
        if self.is_typing_animation_active and self.typing_bubble_id is not None:
            self.update_message_bubble(self.typing_bubble_id, message)
            self.is_typing_animation_active = False
        else:
            self.typing_bubble_id = self.add_message_bubble(message, is_user=False)

    def focus_in(self, event):
        """Handle focus-in event on the text field."""
        if self.text_field.get() == 'Message IVA...':
            self.text_field.delete(0, tk.END)
            self.text_field.config(fg=self.REGULAR_COLOR)

    def focus_out(self, event):
        """Handle focus-out event on the text field."""
        if not self.text_field.get():
            self.text_field.insert(0, 'Message IVA...')
            self.text_field.config(fg=self.PLACEHOLDER_COLOR) 

    def toggle_input_state(self):
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
        if self.mic_mode:
            text = recognize_speech()
            if text:
                self.add_message_bubble(text, is_user=True)
                threading.Thread(target=self.process_and_display_response, args=(text,), daemon=True).start()               

    # ======================== Utility Functions ========================

    def refresh_chat_view(self):
        """Refresh the view of the chat canvas."""
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.yview_moveto(1) 

    # ======================== Chat Bubble Management ========================    

    def add_message_bubble(self, message, is_user=True):
        """Add a message bubble to the chat canvas."""
        bubble_frame = tk.Frame(self.chat_canvas, bg=self.BUBBLE_COLOR)
        message_label = tk.Label(bubble_frame, text=message, bg=self.BUBBLE_COLOR, fg="black",
                                 font=self.customFont, wraplength=self.TEXT_WIDTH_LIMIT - 2 * self.PADDING, justify='left')
        message_label.pack(padx=self.PADDING, pady=self.PADDING)
        bubble_id = self.chat_canvas.create_window((self.CHAT_AREA_WIDTH / 2, self.bubble_margin_top), window=bubble_frame, anchor="w" if is_user else "e", width=self.TEXT_WIDTH_LIMIT)
        self.bubble_margin_top += bubble_frame.winfo_reqheight() + self.BUBBLE_SPACING
        self.chat_bubbles[bubble_id] = message_label
        self.refresh_chat_view()
        return bubble_id

    def update_message_bubble(self, bubble_id, new_message):
        """Update the text of an existing message bubble."""
        if bubble_id in self.chat_bubbles:
            message_label = self.chat_bubbles[bubble_id]
            message_label.config(text=new_message)
        else:
            print(f"Bubble with ID {bubble_id} not found.")

    # ======================== Animation and Visual Effects ======================== 

    def show_typing_animation(self):
        """Show a typing animation in the chat interface."""
        if self.typing_animation_id is None:
            self.typing_message = "IVA is typing"
            self.typing_bubble_id = self.add_message_bubble(self.typing_message, is_user=False)
            self.is_typing_animation_active = True 
            self.animate_typing()

    def animate_typing(self):
        """Animate the typing message with dots."""
        if self.is_typing_animation_active:
            dots = self.typing_message.count('.') % 3 + 1
            self.typing_message = "IVA is typing" + "." * dots
            self.update_message_bubble(self.typing_bubble_id, self.typing_message)
            self.typing_animation_id = self.root.after(500, self.animate_typing)

    def hide_typing_animation(self):
        """Hide the typing animation from the chat interface."""
        if self.typing_animation_id is not None:
            self.root.after_cancel(self.typing_animation_id)
            self.typing_animation_id = None
        if self.typing_bubble_id is not None:
            self.typing_bubble_id = None
        self.is_typing_animation_active = False
        self.refresh_chat_view()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.title("IVA Interface")
        root.configure(bg=ChatInterface.BACKGROUND_COLOR)
        chat_interface = ChatInterface(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"An unrecoverable error occurred: {e}")