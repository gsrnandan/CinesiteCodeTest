#import subprocess
#import prman
from PyQt4 import QtGui,QtCore
import os
from arnoldRender import ArnoldRender as _ArnoldRender
from colorBox import ColorBox as _ColorBox

_SceneName = "sphere"

class PrWindow(QtGui.QWidget):
    def __init__(self,parent = None):
        super(PrWindow, self).__init__(parent=parent)

        self.image_viewer = QtGui.QLabel('Render Image')
        self.log_viewer = QtGui.QTextEdit('Render Log')
        self.log_viewer.setFixedSize(400,300)
        self.render_btn = QtGui.QPushButton('Render')
        self.setColor_btn = _ColorBox("Set Color")
        main_layout = QtGui.QVBoxLayout()
        top_layout =QtGui.QHBoxLayout()
        bottom_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(self.image_viewer)
        top_layout.addWidget(self.log_viewer)
        bottom_layout.addWidget(self.render_btn)
        bottom_layout.addWidget(self.setColor_btn)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
        self._connect_slots()

        # Create a render object
        objColor = self.setColor_btn.getColor()
        print type(objColor.getRgb())
        self.arnoldRender = _ArnoldRender(_SceneName,objColor.getRgb())


    def _connect_slots(self):
        self.render_btn.clicked.connect(self.call_render)

    def call_render(self):
        self.arnoldRender.setColor(self.setColor_btn.getColor().getRgb())
        self.arnoldRender.renderGeo()    
        self.set_image('./' + _SceneName + '.jpg')
        self.set_text('./sphere.log')

    def set_image(self,path):
        if os.path.exists(path):
            image = QtGui.QPixmap(path)
            self.image_viewer.setPixmap(image)

    def set_text(self,path):
        if os.path.exists(path):
            with open(path,'r') as f:
                for line in f:
                    self.log_viewer.append(line)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = PrWindow()
    widget.show()
    app.exec_()