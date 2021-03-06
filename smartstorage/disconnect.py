#!/usr/bin/env python3.4
import os
import tkinter
from time import sleep
top = tkinter.Tk()
top.title('Disconnect')
top.geometry('400x50')


active=os.system('iscsiadm -m session &> /dev/null')
if active ==0:
	os.system("umount  /run/media/root/cloud/ " )
	os.system("iscsiadm --mode node --targetname iqn.2003-01.org.linux-iscsi.vapour.x8664:sn.853ebf511960 --portal 192.168.122.234:3260 --logout ")
	sleep(2)
	isfile=os.system('test -d /run/media/root/cloud')
	if isfile!=0:
		os.system('rmdir /run/media/cloud')
	label = tkinter.Label(top, text='Disconnected From Smart Storage', font='Helvetica -20 bold')
	label.pack()	
	quit = tkinter.Button(top, text='Exit',command=top.quit)
	quit.pack()

else :
	label = tkinter.Label(top, text='NO ACTIVE SESSION', font='Helvetica -20 bold')
	label.pack()
	quit = tkinter.Button(top, text='Exit',command=top.quit)
	quit.pack()
tkinter.mainloop()
