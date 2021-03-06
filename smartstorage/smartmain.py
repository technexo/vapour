#!/usr/bin/python2.7
import os
import Tkinter as tk
import commands as cmd
import socket as sk
import cPickle as pic
from Crypto.Cipher import AES
import thread
import os
s=sk.socket(sk.AF_INET,sk.SOCK_DGRAM)
host=""
port=60401
server=""
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
	s.sendto(emsg,(server,50401))
def recvf():
	r=dcrypt(s.recv(1000))
	return r


LoginStatus=cmd.getstatusoutput('cat smartstorage/slogin.txt')[1]

top=tk.Tk()
top.title("Smart Storage")
root=tk.Frame(top)
signup=tk.Frame(top)
login=tk.Frame(top)
logged=tk.Frame(top)
manage=tk.Frame(top)
expand=tk.Frame(top)
shrink=tk.Frame(top)
for f in (root, signup, login,logged,manage,expand,shrink):
            f.grid(row=0, column=0, sticky="nsew")

def CONNECT():
	os.system('python3.4 smartstorage/connect.py')
def SHOWDISK():
	os.system('smartstorage/showdisk.sh')	
def OPEN():
	os.system('python3.4 smartstorage/mount.py')
def FORMAT():
	os.system('python3.4 smartstorage/format.py')
def DISCONNECT():
	os.system('python3.4 smartstorage/disconnect.py')

def loginfn():
	info={'ch':1,'uname':logEntry1.get(),'passwd':logEntry2.get()}
	if info['uname']==''or info['passwd']=='':
		popinfo("Error","Invalid Entry")
	else:
		sendto(info)
		LoginStatus=recvf()
		if LoginStatus=='True':
			os.system('echo "True" > smartstorage/slogin.txt')
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
	os.system('echo "False" > smartstorage/slogin.txt')		
	root.tkraise()
def popinfo(wtitle,msg):
	topWind=tk.Toplevel()
	topWind.title(wtitle)
	topWind.geometry('300x100')
	tMsg=tk.Message(topWind,text=msg,width=300)
	tMsg.pack(expand=1,fill=tk.X,padx=2,pady=2)
	tBtn=tk.Button(topWind,text="Close",command=topWind.destroy)
	tBtn.pack(padx=2,pady=2)
def getspin(sb,llimit,hlimit):
	
	sin=int(expandSB.get())
	if sin not in range(llimit,hlimit+1):
		popinfo("Error","Out of Range")
		if sin>=hlimit:
			sb.delete(0,tk.END)
			sb.insert(0,hlimit)
		else:
			sb.delete(0,tk.END)
			sb.insert(0,llimit)
def signcreate():
	uName=signUName.get()
	uPass=signPass.get()
	uCPass=signCPass.get()
	uSize=int(signSB.get())
	e=[]
	if not uName.isalpha() or uName=='':
		e.append("Username: Alphabet Only")
	if uPass!=uCPass or uPass=='':
			e.append("Password Not Matched")
	if  uSize not in range(1,101):
		e.append("Size Out of Range")
		
	def poperror(emsg):
		topWind=tk.Toplevel()
		topWind.title("Error")
		topWind.geometry('300x100')
		for emsg in e:
	        	tMsg=tk.Message(topWind,text=emsg,width=300).pack(expand=1,fill=tk.X)
		tBtn=tk.Button(topWind,text="Close",command=topWind.destroy)
		tBtn.pack(padx=2,pady=2)
	if uName=='' and uPass=='' and uCPass=='':
		popinfo("Error","Incomplete Form")
	elif e !=[]:
		poperror(e)
		signUName.delete(0,tk.END)
		signPass.delete(0,tk.END)
		signCPass.delete(0,tk.END)
		if uSize>=100:
			signSB.delete(0,tk.END)
			signSB.insert(0,'100')
		else:
			signSB.delete(0,tk.END)
			signSB.insert(0,'1')
	else:
		info={'ch':2,'uname':uName,'passwd':uPass,'disk':uSize}
		sendto(info)
		stat=recvf()
		if stat=="True":
			popinfo("Congrats","Account Created")
			login.tkraise()
		else: popinfo("Error","Already Exists")
	   
label=tk.Label(root, text='Smart Storage', font='Helvetica -24 bold').pack(fill=tk.Y, expand=1,side=tk.TOP,padx=2,pady=2)
mainFrame1=tk.Frame(root)
mainFrame2=tk.Frame(root)
mainBtn1=tk.Button(mainFrame1,text='login',command=login.tkraise).pack(side=tk.LEFT,padx=2,pady=2)
mainBtn2=tk.Button(mainFrame1,text='Signup',command=signup.tkraise).pack(side=tk.RIGHT,padx=2,pady=2)
mainBtn3=tk.Button(mainFrame2,text='Quit',command=top.quit).pack(side=tk.RIGHT,padx=2,pady=2)
mainFrame1.pack()
mainFrame2.pack()

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
logFrame1.pack()
logFrame2.pack()
logFrame3.pack()

signFrame1=tk.Frame(signup)
signFrame2=tk.Frame(signup)
signUNameBtn=tk.Button(signFrame1,text='Username')
signUName=tk.Entry(signFrame1)
signPassBtn=tk.Button(signFrame1,text='Password')
signPass=tk.Entry(signFrame1,show="*")
signCPassBtn=tk.Button(signFrame1,text='Confirm Password')
signCPass=tk.Entry(signFrame1,show="*")
signSizeBtn=tk.Button(signFrame1,text='Size of Disk(MB)')
signSB=tk.Spinbox(signFrame1,from_=1,to=100)
signUNameBtn.grid(row=0,column=0,sticky='we',padx=2,pady=2)
signUName.grid(row=0,column=1,sticky='we',padx=2,pady=2)
signPassBtn.grid(row=1,column=0,sticky='we',padx=2,pady=2)
signPass.grid(row=1,column=1,sticky='we',padx=2,pady=2)
signCPassBtn.grid(row=2,column=0,sticky='we',padx=2,pady=2)
signCPass.grid(row=2,column=1,sticky='we',padx=2,pady=2)
signSizeBtn.grid(row=3,column=0,sticky='we',padx=2,pady=2)
signSB.grid(row=3,column=1,sticky='we',padx=2,pady=2)
signCreateBtn=tk.Button(signFrame2,text='Create',command=signcreate).pack(side=tk.LEFT,padx=2,pady=2)
signCancelBtn=tk.Button(signFrame2,text='Cancel',command=root.tkraise).pack(side=tk.RIGHT,padx=2,pady=2)
signFrame1.pack()
signFrame2.pack()


loggedFrame1=tk.Frame(logged)
loggedFrame2=tk.Frame(logged)
loggedFrame3=tk.Frame(logged)		
loggedlabel=tk.Label(logged, text='Hi', font='Helvetica -24 bold')
loggedlabel.pack(fill=tk.Y, expand=1,side=tk.TOP,padx=2,pady=2)

Connect=tk.Button(loggedFrame1, text='Connect', command=CONNECT, bg='goldenrod1', fg='blue', activeforeground='white', activebackground='grey').pack(fill=tk.X,side=tk.LEFT, expand=1,padx=2,pady=2)
Showdisk=tk.Button(loggedFrame2, text='Show Disk', command=SHOWDISK, bg='goldenrod1', fg='blue', activeforeground='white', activebackground='grey').pack(fill=tk.X,side=tk.LEFT, expand=1,padx=2,pady=2)
Open=tk.Button(loggedFrame2, text='Open Disk', command=OPEN, bg='goldenrod1', fg='blue', activeforeground='white', activebackground='grey').pack(fill=tk.X,side=tk.RIGHT, expand=1,padx=2,pady=2)
Format=tk.Button(loggedFrame3, text='Format', command=FORMAT, bg='goldenrod1', fg='blue', activeforeground='white', activebackground='grey').pack(fill=tk.X, expand=1,padx=2,pady=2)
Disconnect=tk.Button(loggedFrame1, text='Disconnect', command=DISCONNECT, bg='goldenrod1', fg='blue', activeforeground='white', activebackground='grey').pack(fill=tk.X,side=tk.RIGHT, expand=1,padx=2,pady=2)
quit=tk.Button(loggedFrame3, text='Exit', command=logout, bg='red', fg='blue', activeforeground='white', activebackground='green').pack(fill=tk.X, expand=1,padx=2,pady=2)
loggedFrame1.pack()
loggedFrame2.pack()
loggedFrame3.pack()

manageFrame1=tk.Frame(manage)
manageFrame2=tk.Frame(manage)
manageBtn1=tk.Button(manageFrame1,text="Expand", command=expand.tkraise).pack(side=tk.LEFT,padx=2,pady=2)
manageBtn2=tk.Button(manageFrame1,text="Shrink", command=shrink.tkraise).pack(side=tk.RIGHT,padx=2,pady=2)
manageBtn3=tk.Button(manageFrame2, text="Cancel",command=logged.tkraise).pack(padx=2,pady=2)
manageFrame1.pack()
manageFrame2.pack()

expandFrame1=tk.Frame(expand)
expandFrame2=tk.Frame(expand)
expandBtn1=tk.Button(expandFrame1, text="Amount to expand").pack(side=tk.LEFT,padx=2,pady=2)
expandSB=tk.Spinbox(expandFrame1,from_=1,to=200)
expandSB.pack(side=tk.RIGHT,padx=2,pady=2)
expandBtn2=tk.Button(expandFrame2, text="Expand",command=lambda: getspin(expandSB,1,200)).pack(side=tk.LEFT,padx=2,pady=2)
expandBtn3=tk.Button(expandFrame2,text="Cancel",command=manage.tkraise).pack(side=tk.LEFT,padx=2,pady=2)
expandFrame1.pack()
expandFrame2.pack()

shrinkFrame1=tk.Frame(shrink)
shrinkFrame2=tk.Frame(shrink)
shrinkBtn1=tk.Button(shrinkFrame1, text="Amount to Shrink").pack(side=tk.LEFT,padx=2,pady=2)
shrinkSB=tk.Spinbox(shrinkFrame1,from_=1,to=100)
shrinkSB.pack(side=tk.RIGHT,padx=2,pady=2)
shrinkBtn2=tk.Button(shrinkFrame2, text="Shrink",command=lambda: getspin(shrinkSB,1,100)).pack(side=tk.LEFT,padx=2,pady=2)
shrinkBtn3=tk.Button(shrinkFrame2,text="Cancel",command=manage.tkraise).pack(side=tk.LEFT,padx=2,pady=2)
shrinkFrame1.pack()
shrinkFrame2.pack()

root.tkraise()
top.resizable(0,0)
tk.mainloop()


