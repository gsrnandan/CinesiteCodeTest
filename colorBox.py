from PyQt4 import QtGui,QtCore

import constants


class ColorBox(QtGui.QPushButton):

    def __init__(self, parent=None, color=None):
        super(ColorBox,self).__init__(parent)
        self._userColor = None      
        
        self.setFixedSize(160,30)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.userColor = QtGui.QColor(color or constants.DefaultColor)

        self.clicked.connect(self._changeColor)      


    @property
    def userColor(self):
        return self._userColor

    @userColor.setter
    def userColor(self, color):
        if isinstance(color, tuple):
            color = QtGui.QColor(color)
        self._userColor = color
        self.setStyleSheet(
            "QPushButton {background-color: rgba(%d, %d, %d, %d)}" % self._userColor.getRgb()
        )

    def _changeColor(self):
        col = QtGui.QColorDialog.getColor(self._userColor, self)
        if col.isValid():
            self.userColor = col
        
        
    # def mousePressEvent(self, e):
    #     if e.buttons() == QtCore.Qt.LeftButton:
    #         col = QtGui.QColorDialog.getColor(self._userColor, self)
   
    #         if col.isValid():
    #             rgb = (col.red(), col.green(), col.blue())
    #             self.setStyleSheet("QPushButton { background-color: rgb(%d,%d,%d) }" % rgb)
    #             self._userColor = col
    #     print col

    # def getColor(self):
    #     return self._userColor


if __name__ == "__main__":
    app = QtGui.QApplication([])
    c = ColorBox("Set Color")
    c.show()
    app.exec_()