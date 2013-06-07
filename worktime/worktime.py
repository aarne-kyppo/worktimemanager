#!/usr/bin/python
# -*- coding: utf-8 -*- 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from datetime import *
from datetime import time
import sys
from editwindow import EditWindow
from summarywindow import SummaryWindow
from worktimestamp import WorkTimeStamp
class WorkTime(QMainWindow):
	def __init__(self):
		super(WorkTime,self).__init__()
		a = QWidget()
		self.setCentralWidget(a)
		
		lay = QGridLayout(self.centralWidget())
		
		startbtn = QPushButton('Start')
		endbtn = QPushButton('End')
		sumbtn = QPushButton('Summary')
		self.time_edit = QTimeEdit()
		
		startbtn.clicked.connect(self.record)
		endbtn.clicked.connect(self.record)
		sumbtn.clicked.connect(self.summary)
		
		lay.addWidget(self.time_edit,0,0)
		lay.addWidget(startbtn,0,1)
		lay.addWidget(endbtn,0,2)
		lay.addWidget(sumbtn,1,0,1,3)
		
		#Creating actions
		importaction = QAction('Import',self)
		importaction.setShortcut('Ctrl+i')
		importaction.setStatusTip('Import worktime-file')
		importaction.triggered.connect(self.importFile)
		
		exportaction = QAction('Export',self)
		exportaction.setShortcut('Ctrl+e')
		exportaction.setStatusTip('Export worktime-file')
		exportaction.triggered.connect(self.exportFile)
		
		editaction = QAction('Edit timestamps',self)
		editaction.setShortcut('Ctrl+d')
		editaction.setStatusTip("Edit work-timestamps")
		editaction.triggered.connect(self.editStamps)
		
		#Adding menubar and menus
		menubar = self.menuBar()
		filemenu = menubar.addMenu("&File")
		editmenu = menubar.addMenu("&Edit")
		filemenu.addAction(importaction)
		filemenu.addAction(exportaction)
		#editmenu.addAction(editaction) #This property is not ready yet.
		
		self.time_edit.setTime(QTime.currentTime()) # Setting current time to time_edit(obviously).
		
		self.setWindowTitle('Worktime-manager')
		
		self.show()
	def record(self):#Records worktimestamp.
		d = datetime.today()
		#fname = QFileDialog.getOpenFileName(self,'Open file','/home/aarnek')
		f = open('/usr/share/worktime/worktime.txt',"a+")
		if self.sender().text() == 'Start':
			f.write('start:{0}:{1}:{2}:{3}:{4}\n'.format(d.year,d.month,d.day,self.time_edit.time().hour(),self.time_edit.time().minute()))
		else:
			f.write('end:{0}:{1}:{2}:{3}:{4}\n'.format(d.year,d.month,d.day,self.time_edit.time().hour(),self.time_edit.time().minute()))
		f.flush()
		f.close()
	def summary(self):
		sumwindow = SummaryWindow()
		sumwindow.exec_()
	def importFile(self):
		fname = QFileDialog.getOpenFileName(self,'Open file','/home')
		f = open(fname, "r")
		filetoimport = open('/usr/share/worktime/worktime.txt','a+')
		for line in f:
			filetoimport.write(line)
		f.close()
		filetoimport.close()
	def exportFile(self):
		fname = QFileDialog.getSaveFileName(self,'Save file','/home')
		f = open(fname, "a+")
		filetoexport = open('/usr/share/worktime/worktime.txt','r')
		for line in filetoexport:
			f.write(line)
		f.close()
		filetoexport.close()
	def editStamps(self):
		edit = EditWindow()
		edit.exec_()
