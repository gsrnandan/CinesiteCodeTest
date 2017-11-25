from PyQt4 import QtGui,QtCore


class ColorBox(QtGui.QPushButton):

    def __init__(self,parent=None):
        super(ColorBox,self).__init__(parent)
        
        self._userColor = QtGui.QColor(QtCore.Qt.yellow)      
        self.setFixedSize(160,30)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.setStyleSheet("QWidget { background-color: rgba(%d,%d,%d,%d)}" % self._userColor.getRgb())

    def mousePressEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            col = QtGui.QColorDialog.getColor(self._userColor, self)
   
            if col.isValid():
                rgb = (col.red(), col.green(), col.blue())
                self.setStyleSheet("QWidget { background-color: rgb(%d,%d,%d) }" % rgb)
                self._userColor = col
        print col

    def get_color(self):
        return self._userColor


if __name__ == "__main__":
    app = QtGui.QApplication([])
    c = ColorBox("Set Color")
    c.show()
    app.exec_()