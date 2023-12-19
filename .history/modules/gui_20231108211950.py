import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor, QPainter, QBrush, QPen, QFont


class ChatBubble(QTextEdit):
    def __init__(self, text, sender):
        super().__init__()
        self.setReadOnly(True)
        self.setPlainText(text)
        
        # Set bubble style based on sender
        if sender == "ai":
            self.setStyleSheet("QTextEdit { background-color: #DCF8C6; border-radius: 10px; margin: 5px; }")
            self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        else:  # user
            self.setStyleSheet("QTextEdit { background-color: #34B7F1; color: white; border-radius: 10px; margin: 5px; }")
            self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Enable word wrap and disable scrollbars
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Set font
        font = self.font()
        font.setPointSize(10)
        self.setFont(font)



class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('IVA Chat')
        self.setGeometry(100, 100, 400, 500)
        self.setWindowIcon(QIcon('chat_icon.png'))  # Set a path to your chat window icon
        
        # Chat display area
        self.chat_display = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_display)
        
        # Input field and buttons
        self.text_entry = QLineEdit()
        self.text_entry.setPlaceholderText("Type a message...")
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)
        self.mic_button = QPushButton('🎤')
        self.mic_button.clicked.connect(self.record_audio)
        
        # Overall layout
        layout = QVBoxLayout()
        layout.addWidget(self.chat_display)
        layout.addWidget(self.text_entry)
        layout.addWidget(self.send_button)
        layout.addWidget(self.mic_button)
        
        # Set the layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Display a placeholder message from IVA
        self.display_message("Hello, I'm IVA. I'm here to help you!", sender="ai")

    def send_message(self):
        message = self.text_entry.text()
        if message:
            self.display_message(message, sender="user")
            self.text_entry.clear()

    def display_message(self, message, sender):
        # Create a chat bubble with the message
        bubble = ChatBubble(message, sender)
        self.chat_layout.addWidget(bubble)

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
