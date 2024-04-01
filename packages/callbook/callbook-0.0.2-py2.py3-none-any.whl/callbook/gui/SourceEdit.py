from PyQt5.QtGui import QFont, QFontMetrics, QColor, QCursor
from .Document import StandardItem, Document
from PyQt5.Qsci import QsciScintilla, QsciLexerCPP
from PyQt5.QtCore import pyqtSignal, QPoint
from PyQt5.QtWidgets import QDialog, QWidget, QDialogButtonBox, QVBoxLayout, QPlainTextEdit, QPushButton


class AnnotationDialog(QDialog):
    CustomDeleteStatus = 100

    def __init__(self, parent: QWidget = None, txt: str = '') -> None:
        super().__init__(parent)
        self.setWindowTitle("Annotation")

        font = QFont('Inconsolata')
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        buttonDelete = QPushButton('Delete')
        self.buttonBox.addButton(
            buttonDelete, QDialogButtonBox.ButtonRole.ActionRole)
        buttonDelete.clicked.connect(self.custom_delete)

        self.layout = QVBoxLayout()
        self.edit = QPlainTextEdit()
        self.edit.setPlainText(txt)
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.resize(800, 600)
        self.setWindowOpacity(0.9)
        pos = QCursor.pos()
        self.move(pos)

    def custom_delete(self):
        self.done(self.CustomDeleteStatus)


class SourceEdit(QsciScintilla):
    sourceChanged = pyqtSignal(str)
    annotationChanged = pyqtSignal(int, str)
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(SourceEdit, self).__init__(parent)

        # Set the default font
        font = QFont()
        font.setFamily('Inconsolata')  # Courier
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setUtf8(True)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        # Set CPP lexer
        # Set style for Python comments (style number 1) to a fixed-width
        # courier.
        #
        lexer = QsciLexerCPP()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"), self.ARROW_MARKER_NUM)
        self.setAnnotationDisplay(
            QsciScintilla.AnnotationDisplay.AnnotationBoxed)
        self.SendScintilla(self.SCI_STYLESETBACK,
                           QsciScintilla.STYLE_CALLTIP, QColor(255, 255, 204))

        # Indentation
        #
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setTabIndents(True)
        self.setAutoIndent(True)

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # not too small
        self.setMinimumSize(600, 450)
        self.textChanged.connect(self.onTextChanged)
        self.isItemChanged = False

    def setDocument(self, doc: Document):
        self.document: Document = doc
        self.document.curItemChanged.connect(self.onCurItemChanged)
        self.sourceChanged.connect(doc.onSourceChanged)
        self.annotationChanged.connect(doc.onAnnocationChanged)

    def onCurItemChanged(self, item: StandardItem) -> None:
        self.isItemChanged = True
        content = self.document.get_source(item.functionData)
        self.setText(content)
        self.isItemChanged = False
        annotations = self.document.get_annotations(item.functionData)
        for k, v in annotations.items():
            self.annotate(k, v, QsciScintilla.STYLE_CALLTIP)
            self.markerAdd(k, self.ARROW_MARKER_NUM)

    def onTextChanged(self) -> None:
        if self.isItemChanged:
            return

        self.sourceChanged.emit(self.text())

    def annotation(self, nline) -> str:
        # There is a bug in the following cpp method
        # QString QsciScintilla::annotation(int line) const
        # So its parent implementation self.annotation(nline) won't return correct value
        # This method is an reimplementation of the method QsciScintilla::annotation
        size = self.SendScintilla(self.SCI_ANNOTATIONGETTEXT, nline, 0)
        buf = bytearray(size)
        self.SendScintilla(self.SCI_ANNOTATIONGETTEXT, nline, buf)
        string = buf.decode('utf-8')
        return string

    def on_margin_clicked(self, nmargin, nline, modifiers):
        txt = ''
        if self.markersAtLine(nline) != 0:
            txt = self.annotation(nline)

        dlg = AnnotationDialog(self, txt)
        result = dlg.exec()
        if result == QDialog.DialogCode.Accepted:
            new_txt = dlg.edit.toPlainText()
            if new_txt == txt:
                return

            if new_txt:
                self.annotate(nline, new_txt, QsciScintilla.STYLE_CALLTIP)
                self.markerAdd(nline, self.ARROW_MARKER_NUM)
                self.annotationChanged.emit(nline, new_txt)
            else:
                self.clearAnnotations(nline)
                self.markerDelete(nline, self.ARROW_MARKER_NUM)
                self.annotationChanged.emit(nline, '')

        elif result == AnnotationDialog.CustomDeleteStatus:
            self.clearAnnotations(nline)
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
            self.annotationChanged.emit(nline, '')
