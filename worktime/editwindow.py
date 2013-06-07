from PyQt4.QtGui import *
from PyQt4.QtCore import *
class EditWindow(QMainWindow):
	def __init__(self):
		super(EditWindow,self).__init__()
		
		self.txt = QTextEdit()
		self.cancelbtn = QPushButton('Cancel')
		self.savebtn = QPushButton('Save')
		
		self.cancelbtn.clicked.connect(self.cancelEdit)
		self.savebtn.clicked.connect(self.saveEdit)
		
		w = QWidget()
		self.setCentralWidget(w)
		lay = QGridLayout(self.centralWidget())
		
		lay.addWidget(self.txt,0,0,1,4)
		lay.addWidget(self.cancelbtn,1,0)
		lay.addWidget(self.savebtn,1,1)
		self.setGeometry(100,100,500,300)
		self.setWindowTitle('Edit work-timestamps')
		self.show()
		self.printFile()
	def printFile(self):
		self.f = open('/usr/share/worktime/worktime.txt','r+')
		for line in self.f:
			self.txt.append(line[:-1])
	def cancelEdit(self):
		self.f.close()
		self.close()
	def saveEdit(self):
		self.f.write(self.txt.toPlainText())
		self.f.close()
		self.close()
