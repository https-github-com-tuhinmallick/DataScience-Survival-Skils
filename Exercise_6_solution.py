import sys  # System-specific parameters and functions

from PyQt5.QtWidgets import (QApplication, QFileDialog, QWidget,QMainWindow,
                             QLabel, QVBoxLayout, QShortcut, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeySequence
import imageio as io

# Preparing the environment for the image:
class ImageWidget(QLabel):
    def __init__(self):
        super().__init__() #super() is used to refer the superclass from the subclass.
        # In this case "ImageL" is a subclass of QLabel
    
        self.setAlignment(Qt.AlignCenter)   # The widget will be displayed in the center
        self.setText('Drop an image here')  # Text to help the user
        self.setStyleSheet('''
           QLabel{
                border-style: dashed;
                border-width: 2px;
                border-radius: 10px;
                border-color: #aaa;
                font: 14px
           }
        '''
        ) # style of the QLabel


    def setPixmap(self, im):
        super().setPixmap(im)




#Let's define our widget
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Drag and drop app')
        self.setMinimumSize(250, 300)

        ## 
        #Enable drop events
        self.setAcceptDrops(True) 
        ##


        ### SAVE YOUR IMAGE in self.im!
        self.im = None 

        ## ADD A MENU BAR
        self.menu = self.menuBar()

        # Main top menu
        self.file = self.menu.addMenu("&File")
        self.file.addAction("Open", self.open)
        self.file.addAction("Save", self.save)
        self.file.addAction("Close", self.close)


        
        # CREATE A CENTRAL WIDGET TO SHOW IMAGE
        w = QWidget(self)
        self.setCentralWidget(w)
        self.mainLayout = QVBoxLayout()
        w.setLayout(self.mainLayout)
        
  
        self.displayPicture = ImageWidget() #we configure the widget to add
        self.mainLayout.addWidget(self.displayPicture) # we add the widget to the window


        # TODO 
        # We want to bind the typical "Ctrl+S" to the save function:

        ## Solution:
        self.add = QShortcut(QKeySequence("Ctrl+S"), self)
        self.add.activated.connect(self.save)
        ##------------------------------------------------##



    def setImage(self, im):
        self.displayPicture.setPixmap(QPixmap(im))

    def open(self):
        fn, _ = QFileDialog.getOpenFileName(filter="*.png;*.jpg")

        if fn:
            print(fn)
            self.im = io.imread(fn)
            self.setImage(fn)
    
    ###
    # TODO
    # Add code for drag & drop, use Google search
    ## Solution:
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            #If you select multiple images, we will display only the first one
            fn = event.mimeData().urls()[0].toLocalFile()
            self.im = io.imread(fn)
            self.setImage(fn)
            event.accept()
        else:
            event.ignore()

    ####-------------------------------------------------------------------####
    
    # TODO
    # Here comes the saving routine
    # Solution:
    def save(self):
        try:
            # SAVE THE IMAGE
            io.imwrite("test.png", self.im)
            
            # If succeeded show a popup window/message box with information layout:
            QMessageBox.information(self, 
            "file saved", 
            "Image was saved succesfully!")
        except:
            # otherwise a popup window/message box with critical layout:
            QMessageBox.critical(self, 
            "Meaningful error", 
            "Something went wrong!")
            
    ##-------------------------------------##

def main():

    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()