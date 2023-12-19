import sys

from PyQt5.QtCore import QAbstractListModel, QMargins, QPoint, QRectF, QSize, Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QTextDocument, QTextOption

# from PyQt5.QtGui import
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QListView,
    QMainWindow,
    QPushButton,
    QStyledItemDelegate,
    QVBoxLayout,
    QWidget,
)

USER_ME = 0
USER_THEM = 1

BUBBLE_COLORS = {USER_ME: "#90caf9", USER_THEM: "#a5d6a7"}
USER_TRANSLATE = {USER_ME: QPoint(20, 0), USER_THEM: QPoint(0, 0)}

BUBBLE_PADDING = QMargins(15, 5, 35, 5)
TEXT_PADDING = QMargins(25, 15, 45, 15)


class MessageDelegate(QStyledItemDelegate):
    """
    Draws each message.
    """

    _font = None

    def paint(self, painter, option, index):
        painter.save()
        # Retrieve the user,message uple from our model.data method.
        user, text = index.model().data(index, Qt.DisplayRole)

        trans = USER_TRANSLATE[user]
        painter.translate(trans)

        # option.rect contains our item dimensions. We need to pad it a bit
        # to give us space from the edge to draw our shape.
        bubblerect = option.rect.marginsRemoved(BUBBLE_PADDING)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        # draw the bubble, changing color + arrow position depending on who
        # sent the message. the bubble is a rounded rect, with a triangle in
        # the edge.
        painter.setPen(Qt.NoPen)
        color = QColor(BUBBLE_COLORS[user])
        painter.setBrush(color)
        painter.drawRoundedRect(bubblerect, 10, 10)

        # draw the triangle bubble-pointer, starting from the top left/right.
        if user == USER_ME:
            p1 = bubblerect.topRight()
        else:
            p1 = bubblerect.topLeft()
        painter.drawPolygon(p1 + QPoint(-20, 0), p1 + QPoint(20, 0), p1 + QPoint(0, 20))

        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        # draw the text
        doc = QTextDocument(text)
        doc.setTextWidth(textrect.width())
        doc.setDefaultTextOption(toption)
        doc.setDocumentMargin(0)

        painter.translate(textrect.topLeft())
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        _, text = index.model().data(index, Qt.DisplayRole)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        doc = QTextDocument(text)
        doc.setTextWidth(textrect.width())
        doc.setDefaultTextOption(toption)
        doc.setDocumentMargin(0)

        textrect.setHeight(doc.size().height())
        textrect = textrect.marginsAdded(TEXT_PADDING)
        return textrect.size()


class MessageModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.messages = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Here we pass the delegate the user, message tuple.
            return self.messages[index.row()]

    def setData(self, index, role, value):
        self._size[index.row()]

    def rowCount(self, index):
        return len(self.messages)

    def add_message(self, who, text):
        """
        Add an message to our message list, getting the text from the QLineEdit
        """
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.messages.append((who, text))
            # Trigger refresh.
            self.layoutChanged.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Layout the UI
        l = QVBoxLayout()

        self.message_input = QLineEdit("Enter message here")

        # Buttons for from/to messages.
        self.btn1 = QPushButton("<")
        self.btn2 = QPushButton(">")

        self.messages = QListView()
        self.messages.setResizeMode(QListView.Adjust)
        # Use our delegate to draw items in this view.
        self.messages.setItemDelegate(MessageDelegate())

        self.model = MessageModel()
        self.messages.setModel(self.model)

        self.btn1.pressed.connect(self.message_to)
        self.btn2.pressed.connect(self.message_from)

        l.addWidget(self.messages)
        l.addWidget(self.message_input)
        l.addWidget(self.btn1)
        l.addWidget(self.btn2)

        self.w = QWidget()
        self.w.setLayout(l)
        self.setCentralWidget(self.w)

    def resizeEvent(self, e):
        self.model.layoutChanged.emit()

    def message_to(self):
        self.model.add_message(USER_ME, self.message_input.text())

    def message_from(self):
        self.model.add_message(USER_THEM, self.message_input.text())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()