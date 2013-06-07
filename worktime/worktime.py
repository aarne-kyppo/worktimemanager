#!/usr/bin/python
# -*- coding: utf-8 -*- 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from datetime import *
from datetime import time
import sys
class WorkTimeStamp():
	def __init__(self,isEnd, year, month, day, hour, minute):
		self.isEnd = isEnd
		self.datetimeobject = datetime(int(year),int(month),int(day),int(hour),int(minute))
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
class SummaryWindow(QMainWindow):
	def __init__(self):
		super(SummaryWindow,self).__init__()
		
		self.sumtxt = QTextEdit()
		
		self.setCentralWidget(self.sumtxt)
		
		self.setGeometry(100,100,300,300)
		self.setWindowTitle('Summary')
		self.show()
		self.printSummary(self.getTimeStamps())
	def __del__(self):
		print 'deleted'
	def printSummary(self,timestamps):
		#This function pops one timestamp of timestamp-list and finds timestamp with same date to find
		#starting- and ending timestamps.
		sumworktime = 0
		workdays = 0
		while len(timestamps)>=2:#Each timestamp has to have pair(end and start)
			stampa = timestamps.pop()
			i=0
			while i < len(timestamps):#Loop to iterate timestamps to find timestamp with same date as popped timestamp
				#Checking date
				if timestamps[i].datetimeobject.year == stampa.datetimeobject.year and timestamps[i].datetimeobject.month == stampa.datetimeobject.month and timestamps[i].datetimeobject.day == stampa.datetimeobject.day:
					stampb = timestamps.pop(i)
					if stampa.isEnd == True:#This could be done otherway also
						delta = stampa.datetimeobject - stampb.datetimeobject
					else:
						delta = stampb.datetimeobject - stampa.datetimeobject
					worktime = delta - timedelta(minutes =+30)#Lunchbreak
					sumworktime = sumworktime + worktime.seconds/60
					_hours = worktime.seconds/3600
					_minutes = worktime.seconds/60-_hours*60
					workdays = workdays+1
					self.sumtxt.append('{0}.{1}.{2} {3} h {4} min start: {5} end: {6}'.format(stampa.datetimeobject.day,stampa.datetimeobject.month,stampa.datetimeobject.year,_hours,_minutes,str(stampb.datetimeobject.hour) + ':' + str(stampb.datetimeobject.minute),str(stampa.datetimeobject.hour) + ':' + str(stampa.datetimeobject.minute)))
					break
				i = i + 1
		avgworktime = 60*7 + 15 #Minutes in day per average
		#Balance in hours and minutes
		balance = sumworktime - avgworktime*workdays
		balancehours = int(balance/60)
		balanceminutes = balance - balancehours*60
		self.sumtxt.append('\nSaldo on {0} h {1} min'.format(balancehours,balanceminutes))
		#Whole working time
		sumworktimehours = int(sumworktime/60)
		sumworktimeminutes = sumworktime - sumworktimehours*60
		self.sumtxt.append(u'Kokonaistyöaika on {0} h {1} min'.format(sumworktimehours,sumworktimeminutes))
		#Working time left
		workinghours = 20*27*60 #You may need to change this
		left = workinghours - sumworktime
		lefthours = int(left/60)
		leftminutes = left - lefthours*60
		self.sumtxt.append(u'Työaikaa jäljellä: {0} h {1} min'.format(lefthours,leftminutes))
		points = round(float(sumworktime)/(27*60),3)
		self.sumtxt.append(u'Olet suorittanut jo {0} opintopistettä, eli {1}% tarvittavasta opintopistemäärästä.'.format(points,round(float(sumworktime)/(20*27*60)*100,2)))
	def getTimeStamps(self):
		workfile = '/usr/share/worktime/worktime.txt'
		f = open(workfile,"r")
		timestamps = []
		for line in f:
			parts = line.split(':') #':' is separator between values
			if parts[0] == 'start':
				timestamps.append(WorkTimeStamp(False,parts[1],parts[2],parts[3],parts[4],parts[5]))
			else:
				timestamps.append(WorkTimeStamp(True,parts[1],parts[2],parts[3],parts[4],parts[5]))
		f.close()
		return timestamps
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
		editmenu.addAction(editaction)
		
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
