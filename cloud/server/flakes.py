#!/usr/bin/python
import socket as sk
import cPickle as pic
from Crypto.Cipher import AES
from pymongo import MongoClient
client=MongoClient()
cloud=client.cloud
saas=cloud.saas
s=sk.socket(sk.AF_INET,sk.SOCK_DGRAM)
host=""
port=50100
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
	s.sendto(emsg,(server,60101))
def recvf():
	r=dcrypt(s.recv(1000))
	return r

def insert(q):
	saas.insert(q)
	
	
def find(q):
	fdoc=saas.find({'uname':q['uname'],'passwd':q['passwd']})
	if fdoc.count()==1:
		for p in fdoc:
			fresult=p
	else:fresult=False
	return fresult
def sfind(q):
	fdoc=saas.find({'uname':q['uname']})
	if fdoc.count()>=1:
		for p in fdoc:
			fresult=p
	else:fresult=False
	return fresult

def login(recvd):
	if find(recvd)!=False:
		sendto('True')
	else:
		sendto('False')
		
def signup(recvd):
	if sfind(recvd)==False:
		insert(recvd)
		sendto('True')
	else:
		sendto('False')

while True:
		recvd=recvf()
		if recvd['ch']==1:
			login(recvd)
		elif recvd['ch']==2:
			signup(recvd)

