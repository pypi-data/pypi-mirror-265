from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QDialogButtonBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QPainter, QPen
from PyQt5.QtCore import Qt, QEvent
import importlib.metadata

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # super().__init__(parent, Qt.FramelessWindowHint)
        # super().__init__(parent, Qt.SplashScreen)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setWindowTitle("About")
        self.setFont(QFont("Arial", 10))

        try:
            version = importlib.metadata.version("callbook")
        except importlib.metadata.PackageNotFoundError:
            version = "Unknown"

        version_label = QLabel(f"Version: {version}")
 
        ok_button = QDialogButtonBox(QDialogButtonBox.Ok)
        ok_button.clicked.connect(self.accept)
        ok_button.setFixedWidth(100)

        ok_layout = QHBoxLayout()
        #ok_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        ok_layout.addStretch(1)
        ok_layout.addWidget(ok_button)
        #ok_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        ok_layout.addStretch(1)
        
        layout = QVBoxLayout()
        layout.addWidget(version_label)
        layout.addLayout(ok_layout)
        
        self.setLayout(layout)
        self.setFixedSize(240, 180)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawRect(self.rect())
