#!/usr/bin/python2.7

import Tkinter as tk
import subprocess
import os
import commands as cmd
import socket as sk
import cPickle as pic
from Crypto.Cipher import AES
import thread
import os
s=sk.socket(sk.AF_INET,sk.SOCK_DGRAM)
host=""
port=60201
server=''
s.bind((host,port))
def pick(msg):
	return pic.dumps(msg)
def rpick(msg):
	return pic.loads(msg)
def encrypt(msg):
	block=16
	padd='{'
	pmsg=pick(msg)
	ppmsg=pmsg+(block-len(pmsg)%block)*padd
	cipher=AES.new('\x195"\xd0\xc9\x88\xb8\xfa\x89\x92\x83\x87\x1ai5\xf1')
	ciphertxt=cipher.encrypt(ppmsg)
	return ciphertxt
	
def dcrypt(ciphertxt):
	padd='{'
	cipher=AES.new('\x195"\xd0\xc9\x88\xb8\xfa\x89\x92\x83\x87\x1ai5\xf1')
	plaintxt=cipher.decrypt(ciphertxt)
	rptxt=rpick(plaintxt)
	return rptxt

def sendto(msg):
	emsg=encrypt(msg)
	s.sendto(emsg,(server,50211))
def recvf():
	r=dcrypt(s.recv(1000))
	return r


LoginStatus=cmd.getstatusoutput('cat glacier/glogin.txt')[1]

top=tk.Tk()
top.title("Glacier")
root=tk.Frame(top)
login=tk.Frame(top)
logged=tk.Frame(top)
for f in (root,login,logged):
            f.grid(row=0, column=0, sticky="nsew")

def loginfn():
	info={'ch':1,'uname':logEntry1.get(),'passwd':logEntry2.get()}
	if info['uname']==''or info['passwd']=='':
		popinfo("Error","Invalid Entry")
	else:   
		sendto(info)
		LoginStatus=recvf()
		if LoginStatus=='True':
			os.system('echo "True" > glacier/glogin.txt')
			global userName
			userName=info['uname']
			loggedlabel.configure(text='Hi %s'%userName)
			log()
		else:
			popinfo("Error","Login Failed\nTry Again")
			logEntry2.delete(0,tk.END)
def log():
	logged.tkraise()
def logout():
	global LoginStatus
	LoginStatus='False'
	os.system('echo "False" > glacier/glogin.txt')		
	root.tkraise()
def popinfo(wtitle,msg):
	topWind=tk.Toplevel()
	topWind.title(wtitle)
	topWind.geometry('300x100')
	tMsg=tk.Message(topWind,text=msg,width=300)
	tMsg.pack(expand=1,fill=tk.X,padx=2,pady=2)
	tBtn=tk.Button(topWind,text="Close",command=topWind.destroy)
	tBtn.pack(padx=2,pady=2)
def signupfn():
	subprocess.Popen(["glacier/glaciersignup.py"])
	login.tkraise()
label=tk.Label(root, text='Glacier', font='Helvetica -24 bold').pack(fill=tk.Y, expand=1,side=tk.TOP,padx=2,pady=2)
mainFrame1=tk.Frame(root)
mainFrame2=tk.Frame(root)
mainBtn1=tk.Button(mainFrame1,text='login',command=login.tkraise).pack(side=tk.LEFT,padx=2,pady=2)
mainBtn2=tk.Button(mainFrame1,text='Signup',command=signupfn).pack(side=tk.RIGHT,padx=2,pady=2)
mainBtn3=tk.Button(mainFrame2,text='Quit',command=top.quit).pack(side=tk.RIGHT,padx=2,pady=2)
mainFrame1.pack(anchor=tk.CENTER)
mainFrame2.pack(anchor=tk.CENTER)

logFrame1=tk.Frame(login)
logFrame2=tk.Frame(login)
logFrame3=tk.Frame(login)
logBtn1=tk.Button(logFrame1,text='Username').pack(side=tk.LEFT,padx=2,pady=2)
logEntry1=tk.Entry(logFrame1)
logEntry1.pack(side=tk.RIGHT,padx=2,pady=2)
logBtn2=tk.Button(logFrame2,text='password').pack(side=tk.LEFT,padx=2,pady=2)
logEntry2=tk.Entry(logFrame2,show="*")
logEntry2.pack(side=tk.RIGHT,padx=2,pady=2)
logBtn3=tk.Button(logFrame3,text='Login',command=loginfn).pack(side=tk.LEFT,padx=2,pady=2)	
logBtn4=tk.Button(logFrame3,text='Cancel',command=root.tkraise).pack(side=tk.RIGHT,padx=2,pady=2)
logFrame1.pack(anchor=tk.CENTER)
logFrame2.pack(anchor=tk.CENTER)
logFrame3.pack(anchor=tk.CENTER)

userName=''
loggedFrame1=tk.Frame(logged)
loggedFrame2=tk.Frame(logged)
loggedFrame3=tk.Frame(logged)
loggedFrame4=tk.Frame(logged)		
loggedlabel=tk.Label(logged, text='Hi', font='Helvetica -24 bold')
loggedlabel.pack(fill=tk.Y, expand=1,side=tk.TOP,padx=2,pady=2)
loggedOpenBtn=tk.Button(loggedFrame1,text="Open",command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","virt-viewer","android"])).pack(side=tk.LEFT,padx=2,pady=2)
loggedOpenBtn=tk.Button(loggedFrame1,text="start",command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","virsh","start","android"])).pack(side=tk.LEFT,padx=2,pady=2)
loggedPauseBtn=tk.Button(loggedFrame2,text="Pause",command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","virsh","suspend","android"])).pack(side=tk.RIGHT,padx=2,pady=2)
loggedRestartBtn=tk.Button(loggedFrame2,text="Resume",command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","virsh","resume","android"])).pack(side=tk.LEFT,padx=2,pady=2)
loggedRestartBtn=tk.Button(loggedFrame3,text="Restart",command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","virsh","reboot","android"])).pack(side=tk.LEFT,padx=2,pady=2)
loggedShutBtn=tk.Button(loggedFrame3,text="Shutdown",command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","virsh","shutdown","android"])).pack(side=tk.RIGHT,padx=2,pady=2)
loggedDelBtn=tk.Button(loggedFrame4,text="Force Stop",bg='green',activebackground='red',command=lambda:subprocess.Popen(["ssh","-X","root@192.168.122.234","virsh","destroy","android"])).pack(padx=2,pady=2)
loggedOutBtn=tk.Button(loggedFrame4,text="Logout",bg='green',activebackground='red',command=logout).pack(padx=2,pady=2)
loggedFrame1.pack(anchor=tk.CENTER)
loggedFrame2.pack(anchor=tk.CENTER)
loggedFrame3.pack(anchor=tk.CENTER)
loggedFrame4.pack(anchor=tk.CENTER)


if LoginStatus=='True':
	root.tkraise()
else:root.tkraise()

top.resizable(0,0)
tk.mainloop()


