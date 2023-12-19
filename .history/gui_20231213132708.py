import tkinter as tk
from tkinter import font
from tkinter import messagebox
import threading
from main import process_input

class ChatInterface:
    """Class to create and manage the chat interface for IVA."""
    # ======================== Constants and Configurations ========================

    BUBBLE_SPACING = 40
    PADDING = 10
    TEXT_WIDTH_LIMIT = 300
    CHAT_AREA_WIDTH = 750
    LABEL_OFFSET = 20
    START_MARGIN = 30
    WINDOW_OFFSET = 10
    BUBBLE_RADIUS = 20
    CHAT_AREA_HEIGHT = 600
    ENTRY_WIDTH = 40
    BUTTON_PADDING_X = 10
    BUTTON_PADDING_Y = 5
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
        self.chat_bubbles = []
        self.previous_questions_and_answers = []
        self.typing_animation_id = None
        self.typing_bubble_id = None
        self.is_typing_animation_active = False
        self.bubble_margin_top = self.START_MARGIN

        try:
            self.setup_ui()
            self.add_ai_message("How can I help you today?")
        except Exception as e:
            messagebox.showerror("Initialization Error", f"An error occurred during initialization: {e}")
            self.root.destroy()

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
        """Process the user's message and display the AI's response."""
        self.root.after(0, self.show_typing_animation)
        response = process_input(message, self.previous_questions_and_answers)
        self.root.after(0, lambda: [self.hide_typing_animation(), self.add_ai_message(response) if response else None])

    def add_ai_message(self, message):
        """Add a message from the AI to the chat interface."""
        if self.is_typing_animation_active and self.typing_bubble_id is not None:
            self.update_message_bubble(self.typing_bubble_id, message)
            self.typing_bubble_id = None
        else:
            self.add_message_bubble(message, is_user=False)    

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
        """Toggle the input state between enabled and disabled."""
        state = tk.NORMAL if self.text_field['state'] == tk.DISABLED else tk.DISABLED
        self.text_field['state'] = state
        self.send_button['state'] = state               

    # ======================== Utility Functions ========================

        def refresh_chat_view(self):
        """Refresh the view of the chat canvas."""
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.yview_moveto(1) 


    # ======================== Chat Bubble Management ========================    

    def add_message_bubble(self, message, is_user=True):
        """Add a message bubble to the chat canvas and return its index."""
        label_width, label_height = self.calculate_label_dimensions(message)
        bubble_x1, bubble_x2, window_x = self.calculate_bubble_position(label_width, is_user)
        if not self.chat_bubbles:
            y_position = self.bubble_margin_top
        else:
            last_bubble = self.chat_bubbles[-1]
            last_bubble_coords = self.chat_canvas.coords(last_bubble[0])
            y_position = last_bubble_coords[3] + self.BUBBLE_SPACING
        bubble = self.create_rounded_rectangle(bubble_x1, y_position, bubble_x2, y_position + label_height, radius=self.BUBBLE_RADIUS, fill=self.BUBBLE_COLOR)
        message_label_window = self.create_message_label(message, y_position, label_height, window_x)
        self.chat_bubbles.append((bubble, message_label_window))
        self.refresh_chat_view()
        return len(self.chat_bubbles) - 1

    def update_message_bubble(self, bubble_id, new_message):
        """Update the text of a message bubble."""
        if bubble_id is not None and 0 <= bubble_id < len(self.chat_bubbles):
            _, message_label_window = self.chat_bubbles[bubble_id]
            if str(message_label_window) in self.chat_canvas.children:
                message_label = self.chat_canvas.nametowidget(message_label_window)
                message_label.config(text=new_message)

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
            if self.typing_bubble_id < len(self.chat_bubbles):
                bubble, message_label_window = self.chat_bubbles.pop(self.typing_bubble_id)
                self.chat_canvas.delete(bubble)
                self.chat_canvas.delete(message_label_window)
            self.typing_bubble_id = None
        self.is_typing_animation_active = False
        self.refresh_chat_view()   
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Create a rounded rectangle on the canvas."""
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
                  x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2,
                  x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y1+radius,
                  x1, y1+radius, x1, y1]
        return self.chat_canvas.create_polygon(points, **kwargs, smooth=True)

    def calculate_label_dimensions(self, message):
        text_width = min(self.CHAT_AREA_WIDTH, self.TEXT_WIDTH_LIMIT)
        message_label = tk.Label(self.chat_canvas, text=message, bg=self.BUBBLE_COLOR, fg="black",
                                 font=self.customFont, wraplength=text_width - 2 * self.PADDING, justify='left')
        message_label.update_idletasks()
        return message_label.winfo_reqwidth() + 2 * self.PADDING, message_label.winfo_reqheight() + 2 * self.PADDING

    def calculate_bubble_position(self, label_width, is_user):
        if is_user:
            bubble_x1 = self.CHAT_AREA_WIDTH - label_width - self.LABEL_OFFSET
            bubble_x2 = self.CHAT_AREA_WIDTH - self.LABEL_OFFSET
            window_x = self.CHAT_AREA_WIDTH - label_width - self.WINDOW_OFFSET
        else:
            bubble_x1 = self.LABEL_OFFSET
            bubble_x2 = label_width + self.LABEL_OFFSET
            window_x = self.WINDOW_OFFSET + self.LABEL_OFFSET
            print(f"AI Message - bubble_x1: {bubble_x1}, bubble_x2: {bubble_x2}, label_width: {label_width}")
        return bubble_x1, bubble_x2, window_x

    def create_and_add_bubble(self, bubble_x1, y_position, bubble_x2, label_height, message, window_x):
        bubble = self.create_rounded_rectangle(bubble_x1, y_position, bubble_x2, y_position + label_height, radius=self.BUBBLE_RADIUS, fill=self.BUBBLE_COLOR)
        message_label_window = self.create_message_label(message, y_position, label_height, window_x)
        self.chat_bubbles.append((bubble, message_label_window))
        return len(self.chat_bubbles) - 1

    def create_message_label(self, message, y_position, label_height, window_x):
        message_label = tk.Label(self.chat_canvas, text=message, bg=self.BUBBLE_COLOR, fg="black",
                                 font=self.customFont, wraplength=self.TEXT_WIDTH_LIMIT - 2 * self.PADDING, justify='left')
        message_label_window = self.chat_canvas.create_window(window_x, y_position + label_height / 2, window=message_label, anchor="w")
        return message_label_window0


if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.title("IVA Interface")
        root.configure(bg=ChatInterface.BACKGROUND_COLOR)
        chat_interface = ChatInterface(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"An unrecoverable error occurred: {e}")