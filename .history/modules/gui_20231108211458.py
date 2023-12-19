import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('IVA')
        self.setGeometry(100, 100, 400, 500)
        self.setWindowIcon(QIcon('chat_icon.png'))  # Set a path to your chat window icon

        # Main layout
        layout = QVBoxLayout()

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #FFFFFF;")  # Set chat background to white
        layout.addWidget(self.chat_display)

        # Text entry field
        self.text_entry = QLineEdit()
        self.text_entry.setStyleSheet("margin: 10px;")
        layout.addWidget(self.text_entry)

        # Send button
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        # Mic button
        self.mic_button = QPushButton('🎤')
        self.mic_button.clicked.connect(self.record_audio)
        layout.addWidget(self.mic_button)

        # Set main layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Display a placeholder message from IVA
        self.display_message("Hello, I'm IVA. I'm here to help you!", sender="ai")

    def send_message(self):
        message = self.text_entry.text()
        if message:
            # Display user message
            self.display_message(message, sender="user")
            self.text_entry.clear()
            # Here, handle sending the message to the IVA and getting the response

    def display_message(self, message, sender="IVA"):
        # Adjust the colors and padding for each sender
        color = "#E1FFC7" if sender == "IVA" else "#CAF7E3"
        text_color = "#555555" if sender == "IVA" else "#FFFFFF"
        alignment = "left" if sender == "IVA" else "right"
        max_width = "300px"  # Maximum width of chat bubble
        border_radius = "15px"  # Adjust the border radius here

        # HTML content for the chat bubble
        bubble = f'''<div style="text-align: {alignment}; margin: 5px;">
                        <div style="display: inline-block; background: {color}; color: {text_color}; border-radius: {border_radius}; padding: 10px; max-width: {max_width}; overflow-wrap: break-word;">
                            {message}
                        </div>
                    </div>'''
        self.chat_display.append(bubble)

    def record_audio(self):
        # Placeholder for audio recording functionality
        pass


def main():
    app = QApplication(sys.argv)
    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
