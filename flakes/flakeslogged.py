#!/usr/bin/python2.7

import Tkinter as tk
import subprocess
import os

logged=tk.Tk()
logged.title("Flakes")
f=tk.Frame(logged)
loggedFrame2=tk.Frame(logged)
w,h=128,128
baseImg=tk.PhotoImage(width=w,height=h,file='flakes/apps/base.gif')
baseLabel=tk.Label(f,image=baseImg)
baseLabel.image=baseImg
baseBtn=tk.Button(f,text='Base',command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","libreoffice5.1","--base"]))
calcImg=tk.PhotoImage(width=w,height=h,file='flakes/apps/calc.gif')
calcLabel=tk.Label(f,image=calcImg)
calcLabel.image=calcImg
calcBtn=tk.Button(f,text='Calc',command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","libreoffice5.1", "--calc"]))
impressImg=tk.PhotoImage(width=w,height=h,file='flakes/apps/impress.gif')
impressLabel=tk.Label(f,image=impressImg)
impressLabel.image=impressImg
impressBtn=tk.Button(f,text='Impress',command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","libreoffice5.1", "--impress"]))
drawImg=tk.PhotoImage(width=w,height=h,file='flakes/apps/draw.gif')
drawLabel=tk.Label(f,image=drawImg)
drawLabel.image=drawImg
drawBtn=tk.Button(f,text='Draw',command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","libreoffice5.1", "--draw"]))
writerImg=tk.PhotoImage(width=w,height=h,file='flakes/apps/writer.gif')
writerLabel=tk.Label(f,image=writerImg)
writerLabel.image=writerImg
writerBtn=tk.Button(f,text='Writer',command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","libreoffice5.1", "--writer"]))
mathImg=tk.PhotoImage(width=w,height=h,file='flakes/apps/math.gif')
mathLabel=tk.Label(f,image=mathImg)
mathLabel.image=mathImg
mathBtn=tk.Button(f,text='Math',command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","libreoffice5.1", "--math"]))

baseLabel.grid(row=0,column=0,padx=5,pady=5,sticky='nsew')
baseBtn.grid(row=1,column=0,padx=5,pady=5,sticky='ew')
calcLabel.grid(row=0,column=1,padx=5,pady=5,sticky='nsew')
calcBtn.grid(row=1,column=1,padx=5,pady=5,sticky='ew')
impressLabel.grid(row=0,column=2,padx=5,pady=5,sticky='nsew')
impressBtn.grid(row=1,column=2,padx=5,pady=5,sticky='ew')
drawLabel.grid(row=2,column=0,padx=5,pady=5,sticky='nsew')
drawBtn.grid(row=3,column=0,padx=5,pady=5,sticky='ew')
writerLabel.grid(row=2,column=1,padx=5,pady=5,sticky='nsew')
writerBtn.grid(row=3,column=1,padx=5,pady=5,sticky='ew')
mathLabel.grid(row=2,column=2,padx=5,pady=5,sticky='nsew')
mathBtn.grid(row=3,column=2,padx=5,pady=5,sticky='ew')

quit=tk.Button(loggedFrame2, text='Close', command=logged.quit, bg='red', fg='blue', activeforeground='white', activebackground='green').pack(padx=2,pady=2)
f.pack()
loggedFrame2.pack()

logged.resizable(0,0)
tk.mainloop()
