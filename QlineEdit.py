import cv2
import sys
from PySide import QtGui, QtCore
from threading import Thread


class MainWindow(QtGui.QMainWindow):
    def __init__(self, cam=0, parent=None):
        super(MainWindow, self).__init__(parent)

        self.title = "Image"

        widget = QtGui.QWidget()
        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)

        self.image = QtGui.QLabel()

        self.layout.addWidget(self.image)
        self.layout.addStretch()

        self.setCentralWidget(widget)
        widget.setLayout(self.layout)

        self.setMinimumSize(640, 480)
        self.frame = cv2.imread("image.jpg")

        try:
            self.height, self.width = self.frame.shape[:2]

            img = QtGui.QImage(self.frame, self.width, self.height, QtGui.QImage.Format_RGB888)
            img = QtGui.QPixmap.fromImage(img)
            self.image.setPixmap(img)

        except:
            pass

    def closeEvent(self, event):
        cv2.destroyAllWindows()
        event.accept()


if __name__ == "__main__":
    print(cv2.__version__)
    print(sys.version) 
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(0)
    window.show()
    sys.exit(app.exec_())