# !/bin/python

import sys
import os
import httplib

class DTCT:
	modulus='NO APPLICATION WAS FOUND FOR'
	heroku='no such app'


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
    me='Sub6.py'


def defit():
	global count
	count=0

	global result
	result=''

	global output
	output='result.txt'

	global domains
	domains=''




def Leav(s):
	print "\n"+STX.RED+s+"\n"+STX.White+STX.lin+STX.Green+'\n'
	exit();

def printx (s,con):
	print(s)
	global result
	if con==1:
		result = result+str(s)



def printnote(s,con):
	print (STX.brown+s+STX.Green)
	global result
	if con==1:
		result = result+str(s)

def printerror(s,con):
	print STX.RED+s+STX.Green
	global result
	if con==1:
		result = result+str(s)


def Investigate(ur,indx):
	
	if ur.startswith("http") is False:
		url="htttps://"+ur
	else:
		url=ur
	ur=ur.strip()
	printnote ("\n"+STX.lin+"\n [+] Checking ["+str(indx)+"]     ["+ur.strip()+"]   ",0)
	try:
		conn = httplib.HTTPConnection(ur) 
		conn.request("GET","/index.html")
		conn.sock.settimeout(5.0)
		res = conn.getresponse()
		source=res.read()

		printx( str(res.status)+ " "+str(res.reason)+"       \nContent-Length=["+str(len(source))+"]",1)
		redirectlink=res.getheader('location')
		server=res.getheader('server')
		if "None" not in str(redirectlink) :
			printx( STX.WARNING+"Redirects to > "+redirectlink+STX.Green,1 )
		if "None" not in str(server):
			printx( STX.Blue+"Server = "+str(server)+STX.Green,1)

		if DTCT.heroku in source.lower():
			printx (STX.UNDERlinE+"Heroku detected"+STX.Green,1)
		if DTCT.modulus in source.lower():
			printx (STX.UNDERlinE+"modulus.io detected"+STX.Green,1)

	except Exception, e:
		if "nor servname provided, or not known" in str(e):
			printerror( "Unreachable",1)
		else: 		
			printerror (str(e),1)


def execNow():
	global output
	


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
		Leav("\n +Usage     "+STX.me+"    [file]       [file]\n            "+STX.Green+STX.me+"   list.txt  output.txt\n")
	

	filepath = sys.argv[1]
	if os.path.isfile(filepath) is False:
		Leav(STX.Blue+'+[Yasta]! Error '+STX.RED+'\n    Input File not found \n    Path:"'+STX.Green+filepath+'"')
	if len(sys.argv) >2:	
		if len(sys.argv[2].strip) >1:
			output=sys.argv[2].strip()
	else:
		tmp = sys.argv[1].strip()
		lst = tmp.strip().split('/')
		output=lst[len(lst)-1].strip()
		output="Sup6_Resuilt__"+output

		print("Output file : "+output)



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
           ]<==========  \_____  \|  |  \ __ \/   __  \   ========>[..
           ]<==========  /        \  |  / \_\ \  |__\  \  ========>[..                       
                        /_______  /____/|___  /\_____  /
                                \/          \/       \/ 

Sub6 Sub-Domain Crawler and take overs detector By @YasserGersy
					This is BETA , Tools still under Development
"""
if __name__ == '__main__':
    defit()
    execNow()

    if result != '':
    	strm=open(output,'w')
    	strm.write(result)
    	strm.close()
    	printnote("\n"+STX.lin+"\nSaved to "+output,0)
    Leav('Done')


