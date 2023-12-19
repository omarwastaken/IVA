import threading
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QTextEdit, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QSizePolicy)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from main import process_input
from modules.utils import speak, recognize_speech


class ChatInterface(QMainWindow):
    # Constants and Configurations
    ENTRY_WIDTH = 250
    BUTTON_PADDING = 5

    # Colors and Styles
    BACKGROUND_COLOR = '#202225'
    FONT_COLOR = '#ffffff'
    SEND_BUTTON_COLOR = "#5865F2"
    PLACEHOLDER_COLOR = '#A0A0A0'

    # Text
    FONT_FAMILY = "Helvetica"
    FONT_SIZE = 12
    LINE_SPACING = 12

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IVA Interface")
        self.setStyleSheet(f"background-color: {self.BACKGROUND_COLOR};")
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        # Chat display
        self.chatText = QTextEdit(self)
        self.chatText.setReadOnly(True)
        self.chatText.setFont(QFont(self.FONT_FAMILY, self.FONT_SIZE))
        self.layout.addWidget(self.chatText)

        # Input area
        self.bottomLayout = QHBoxLayout()
        self.inputField = QLineEdit(self)
        self.inputField.setFixedWidth(self.ENTRY_WIDTH)
        self.inputField.setFont(QFont(self.FONT_FAMILY, self.FONT_SIZE))
        self.inputField.setStyleSheet("color: {}; background-color: #40444B;".format(self.PLACEHOLDER_COLOR))
        self.inputField.setText("Message IVA...")
        self.inputField.returnPressed.connect(self.sendMessage)
        self.bottomLayout.addWidget(self.inputField)

        self.sendButton = QPushButton("Send", self)
        self.sendButton.setStyleSheet(f"background-color: {self.SEND_BUTTON_COLOR}; color: white;")
        self.sendButton.clicked.connect(self.sendMessage)
        self.bottomLayout.addWidget(self.sendButton)

        self.layout.addLayout(self.bottomLayout)

        # Initial AI message
        initial_message = "How can I help you today?"
        self.appendMessage("➢ IVA: " + initial_message)
        threading.Thread(target=lambda: speak(initial_message), daemon=True).start()

    def sendMessage(self):
        message = self.inputField.text().strip()
        if message:
            self.appendMessage("➢ User: " + message)
            self.inputField.clear()
            threading.Thread(target=self.processAndDisplayResponse, args=(message,), daemon=True).start()

    def processAndDisplayResponse(self, message):
        response = process_input(message)
        self.chatText.append("➢ IVA: " + response)
        speak(response)

    def appendMessage(self, message):
        self.chatText.append(message)


if __name__ == "__main__":
    app = QApplication([])
    chatInterface = ChatInterface()
    chatInterface.show()
    app.exec()
