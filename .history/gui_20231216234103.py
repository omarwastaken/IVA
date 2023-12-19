import pytz
import datetime
import threading
import tkinter as tk
from tkinter import font, ttk
from tkinter import messagebox
from main import process_input
from modules.utils import speak, recognize_speech
from modules.reminders import get_reminders_for_period, mark_reminder_as_done

class ChatInterface:
    """Class to create and manage the chat interface for IVA."""
    # ======================== Theme Constants ========================

    # Interface
    BACKGROUND_COLOR = '#202225'
    FONT_COLOR = '#ffffff'
    SEND_BUTTON_COLOR = "#5865F2"
    PLACEHOLDER_COLOR = '#A0A0A0'
    TODO_LIST_LABEL_BG = '#f0f0f0'
    TODO_LIST_LABEL_FG = '#333'
    TREEVIEW_HEADING_FONT_COLOR = 'blue'

    # Text
    FONT_FAMILY = "Helvetica"
    FONT_SIZE = 12
    LINE_SPACING = 12
    TODO_LIST_LABEL_FONT = ('Arial', 12, 'bold')
    TREEVIEW_HEADING_FONT = ('Calibri', 11, 'bold')
    TREEVIEW_FONT = ('Arial', 10)
    
    # Treeview
    TREEVIEW_ROW_HEIGHT = 25
    TREEVIEW_DONE_COLUMN_WIDTH = 50
    TREEVIEW_REMINDER_COLUMN_WIDTH = 250
    TREEVIEW_DATE_COLUMN_WIDTH = 150

    # Other Constants
    ENTRY_WIDTH = 40
    BUTTON_PADDING_X = 10
    BUTTON_PADDING_Y = 5

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

    def setup_ui(self):
        """Setup the main UI components of the chat interface."""
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=self.BACKGROUND_COLOR)
        self.paned_window.grid(row=0, column=0, sticky="nsew")
        # Chat Frame
        self.chat_frame = tk.Frame(self.paned_window, bg=self.BACKGROUND_COLOR)
        self.paned_window.add(self.chat_frame)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.setup_chat_components()
        # Reminders Frame
        self.features_frame = tk.Frame(self.paned_window, bg=self.BACKGROUND_COLOR)
        self.paned_window.add(self.features_frame)
        self.setup_reminders_components()

    def setup_chat_components(self):
        """Setup the components specific to the chat interface."""
        self.top_frame = tk.Frame(self.chat_frame, bg=self.BACKGROUND_COLOR)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame = tk.Frame(self.chat_frame, bg=self.BACKGROUND_COLOR)
        self.bottom_frame.grid(row=1, column=0, sticky="ew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.setup_chat_display()
        self.setup_input_field()
        self.setup_send_button()
        self.setup_microphone()

    def setup_chat_display(self):
        """Setup the chat display area."""
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
        self.chat_text.grid(row=0, column=0, sticky="nsew")
        scrollbar = tk.Scrollbar(self.top_frame, command=self.chat_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.chat_text.configure(yscrollcommand=scrollbar.set)    

    def setup_reminders_components(self):
        """Setup the components for additional features."""
        self.todo_list_label_frame = tk.Frame(self.features_frame, bg=self.TODO_LIST_LABEL_BG)
        self.todo_list_label_frame.pack(padx=20, pady=(10, 5), fill=tk.X)
        self.todo_list_label = tk.Label(self.todo_list_label_frame, text="Todo List", bg=self.TODO_LIST_LABEL_BG, fg=self.TODO_LIST_LABEL_FG, font=self.TODO_LIST_LABEL_FONT)
        self.todo_list_label.pack(side=tk.LEFT)
        self.toggle_view_button = tk.Button(self.todo_list_label_frame, text="Show Week", command=self.toggle_todo_view, bg=self.TODO_LIST_LABEL_BG, fg=self.TODO_LIST_LABEL_FG)
        self.toggle_view_button.pack(side=tk.RIGHT)
        # Treeview setup
        self.todo_list_tree = ttk.Treeview(self.features_frame, columns=('Reminder', 'Date'), style="Treeview")
        self.todo_list_tree.heading('#0', text='Done')
        self.todo_list_tree.heading('Reminder', text='Reminder')
        self.todo_list_tree.heading('Date', text='Time', anchor='center')
        self.todo_list_tree.column('#0', width=self.TREEVIEW_DONE_COLUMN_WIDTH, anchor='center', stretch=False)
        self.todo_list_tree.column('Reminder', width=self.TREEVIEW_REMINDER_COLUMN_WIDTH, stretch=False)
        self.todo_list_tree.column('Date', width=self.TREEVIEW_DATE_COLUMN_WIDTH, anchor='center', stretch=False)
        # Treeview packing with a bit of space reserved for the scrollbar
        self.todo_list_tree.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.BOTH, expand=True)
        # Vertical Scrollbar setup
        scrollbar = ttk.Scrollbar(self.features_frame, orient="vertical", command=self.todo_list_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.todo_list_tree.configure(yscrollcommand=scrollbar.set)
        self.todo_list_tree.bind('<Double-1>', self.mark_done)

        self.current_view = "day"  # Track the current view
        self.display_reminders()

    def toggle_todo_view(self):
        """Toggle between today's and this week's todo list."""
        if self.current_view == "day":
            self.current_view = "week"
            self.toggle_view_button.config(text="Show Today")
        else:
            self.current_view = "day"
            self.toggle_view_button.config(text="Show Week")
        self.display_reminders()    

    def mark_done(self, event):
        selected_item = self.todo_list_tree.selection()[0]
        mark_reminder_as_done(selected_item)
        self.todo_list_tree.delete(selected_item)

    def display_reminders(self):
        """Fetch and display reminders in the Todo list box based on the current view."""
        try:
            self.todo_list_tree.delete(*self.todo_list_tree.get_children())  # Clear existing entries
            reminders = get_reminders_for_period(self.current_view)
            if reminders:
                for reminder in reminders:
                    self.todo_list_tree.insert('', tk.END, text='✓', values=(reminder['summary'], reminder['time']), iid=reminder['id'])
            else:
                self.todo_list_tree.insert('', tk.END, text='', values=("No reminders for today.", ""))
        except Exception as e:
            self.todo_list_tree.insert('', tk.END, text='', values=(f"Error fetching reminders: {e}", ""))

    def initial_ai_message(self):
        """Handle the initial AI message with non-blocking speech."""
        initial_message = "How can I help you today?"
        self.append_message("➢ IVA: " + initial_message)
        threading.Thread(target=lambda: self.speak_threaded(initial_message), daemon=True).start()

    def speak_threaded(self, message):
        """Run the speak function in a separate thread."""
        speak(message)

    # ======================== UI Component Creation ========================

    def setup_input_field(self):
        """Setup the input text field."""
        self.text_field = tk.Entry(self.bottom_frame, width=self.ENTRY_WIDTH, font=font.Font(family="Helvetica", size=12), fg=self.PLACEHOLDER_COLOR, bg="#40444B", borderwidth=2)
        self.text_field.pack(side=tk.LEFT, padx=self.BUTTON_PADDING_X, pady=self.BUTTON_PADDING_Y)
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
        self.mic_button = tk.Button(self.bottom_frame, image=self.mic_image, command=self.toggle_and_manage_mic_mode, bg="#333333", borderwidth=0)
        self.mic_button.pack(side=tk.RIGHT, padx=2, pady=self.BUTTON_PADDING_Y)        

    # ======================== Event Handling ========================

    def send_message(self, event=None):
        """Handle sending of a message."""
        message = self.text_field.get().strip()
        if message:
            self.append_message("➣ User: " + message)
            self.text_field.delete(0, tk.END)
            if self.mic_mode:
                self.listen_process_and_respond()
            else:
                threading.Thread(target=self.process_text_message, args=(message,), daemon=True).start()

    def toggle_and_manage_mic_mode(self):
        """Toggle microphone input state and manage listening process."""
        if self.mic_mode:
            self.mic_mode = False
            self.text_field['state'] = tk.NORMAL
            self.send_button['state'] = tk.NORMAL
        else:
            self.mic_mode = True
            self.text_field['state'] = tk.DISABLED
            self.send_button['state'] = tk.DISABLED
            self.listen_process_and_respond()        

    def listen_process_and_respond(self):
        """Start the listening and responding process in a separate thread."""
        if self.mic_mode:
            threading.Thread(target=self.speech_recognition_and_response, daemon=True).start()

    def speech_recognition_and_response(self):
        """Handle the speech recognition and response in a separate thread."""
        text = recognize_speech()
        if text:
            self.root.after(0, lambda: self.append_message("--> User: " + text))
            self.root.after(0, self.start_typing_animation)
            response = process_input(text, self.previous_questions_and_answers)
            self.root.after(0, lambda: [self.stop_typing_animation(), self.append_message("➢ IVA: " + response) if response else None])
            speak(response)
            if self.mic_mode:
                self.listen_process_and_respond()        

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
        chat_interface = ChatInterface(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"An unrecoverable error occurred: {e}")