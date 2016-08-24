# !/bin/python
import requests
import sys
import os
import httplib


class STX:
    HEADER = '\033[95m'
    OKBlue = '\033[94m'
    OKGreen = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERlinE = '\033[4m'    	
    RED='\033[1;31m'
    brown='\033[0;33m'
    Blue='\033[0;34m'
    Green='\033[1;32m'
    White='\033[1;37m'
    lin="_________________________________________________________________________________________________"
    heroku='no such app'
    me='Sub6.py'


def defit():
	global count
	count=0

	global domains
	domains=''




def Leav(s):
	print "\n"+STX.RED+s+"\n"+STX.White+STX.lin+STX.Green+'\n'
	exit();

def printnote(s):
	print (STX.brown+s+STX.Green)

def printerror(s):
	print STX.RED+s+STX.Green

def Investigate(ur,indx):
	
	if ur.startswith("http") is False:
		url="htttps://"+ur
	else:
		url=ur
	ur=ur.strip()
	printnote ("\n"+STX.lin+"\n [+] Checking ["+str(indx)+"]     ["+ur.strip()+"]   ")
	try:
		conn = httplib.HTTPConnection(ur) 
		conn.request("GET","/index.html")
		conn.sock.settimeout(5.0)
		res = conn.getresponse()
		source=res.read()
		print str(res.status)+ " "+str(res.reason)+"       \nContent-Length=["+str(len(source))+"]"
		redirectlink=res.getheader('location')
		server=res.getheader('server')
		if "None" not in str(redirectlink) :
			print STX.WARNING+"Redirects to > "+redirectlink+STX.Green
		if "None" not in str(server):
			print STX.Blue+"Server = "+str(server)+STX.Green
		if STX.heroku in res.lower():
			print STX.UNDERlinE+"Heroku detected"+STX.Green

	except Exception, e:
		if "nor servname provided, or not known" in str(e):
			printerror( "Unreachable")
		else: 		
			printerror (str(e))


def execNow():
	


	# print 	STX.RED
	# print 	"|-------------------------------------------------------------|"
	# print 	"|-------------------------------------------------------------|"+STX.White
	# print 	"|------------    ++++++++++++++++++++++++++    ---------------|"
	# print 	"|------------    "+STX.Blue+"+"+STX.me+"+      ---------------|"
	# print 	"|------------    ++++++++++++++++++++++++++    ---------------|"+STX.RED
	# print 	"|-------------------------------------------------------------|"
	# print 	"|-------------------------------------------------------------|\n"+STX.Green
	# print   STX.lin


	if len(sys.argv) < 2:
		print STX.lin
		Leav("\n +Usage     "+STX.me+"  [file] \n            "+STX.Green+STX.me+"  list.txt\n")
	

	filepath = sys.argv[1]
	if os.path.isfile(filepath) is False:
		Leav('Error File not found \nPath:"'+STX.Green+filepath+'"')

	with open(filepath) as x :
		domains=x.readlines()
	for dom in domains:
		global count
		count=count+1
		if "." not in dom:
			continue 
		elif len(dom) < 5:
			continue
		else :			
			Investigate(dom,count)
	


if os.environ.get('OS','') == 'Windows_NT':
	os.system('cls')
else: 
	os.system('clear')


print"""
                          _________    ___.     ________
                         /   _____/__ _\_ |__  /  _____/
                         \_____  \|  |  \ __ \/   __  \ 
                         /        \  |  / \_\ \  |__\  \
                        
                        /_______  /____/|___  /\_____  /
                                \/          \/       \/ 

Sub6 Sub-Domain Crawler and take overs detector By @YasserGersy
					This is BETA , Tools still under Development
"""
if __name__ == '__main__':
    defit()
    execNow()
    Leav('Done')


