#!/usr/bin/env python3.4
import os
import tkinter
from time import sleep
top = tkinter.Tk()
top.title('Disconnect')
top.geometry('400x50')


active=os.system('df -hT | grep nfs4 &> /dev/null')
if active ==0:
	os.system("umount  /run/media/root/vapourbox/ " )
	sleep(2)
	isfile=os.system('test -d /run/media/root/vapourbox')
	if isfile!=0:
		os.system('rmdir /run/media/vapourbox')
	label = tkinter.Label(top, text='Disconnected From Vapour Box', font='Helvetica -20 bold')
	label.pack()	
	quit = tkinter.Button(top, text='Exit',command=top.quit)
	quit.pack()

else :
	label = tkinter.Label(top, text='NO ACTIVE SESSION', font='Helvetica -20 bold')
	label.pack()
	quit = tkinter.Button(top, text='Exit',command=top.quit)
	quit.pack()
tkinter.mainloop()
