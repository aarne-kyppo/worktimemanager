#!/usr/bin/python
# -*- coding: utf-8 -*- 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from worktimestamp import WorkTimeStamp
from datetime import *
from datetime import time
class SummaryWindow(QMainWindow): #Window to show working hours in each day and some statistics.
	def __init__(self):
		super(SummaryWindow,self).__init__()
		
		self.setCentralWidget(QWidget())
		
		layout = QGridLayout(self.centralWidget())
		
		self.sumtxt = QTextEdit()
		self.cancelbtn = QPushButton('Cancel')
		self.savebtn = QPushButton('Save')
		
		layout.addWidget(self.sumtxt,0,0)
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
		return timestamp
