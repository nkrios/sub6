# !/bin/python

import sys,getopt
import os,datetime
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
    havlin='----------------------------'
    me='Sub6.py'
    sufx=''


def defit():
	global count,result,domains,output_file,input_file,opts,args,sufx
	count=0
	result=''
	domains=''
	output_file='result.txt'
	input_file=''
	opts={}
	args={}
	sufx=''




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
	global sufx
	if ur.startswith("http") is False:
		url="htttps://"+ur
	else:
		url=ur
	ur=ur.strip()
	sfx= ""
	if(len(sufx.strip()) > 0):
		sfx="/"+sufx
	printnote ("\n"+STX.lin+"\n [+] Checking ["+str(indx)+"]     ["+ur.strip()+sfx+"]   ",0)
	try:
		conn = httplib.HTTPConnection(ur) 
		conn.request("GET",sufx)
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
	global output_file,input_file,sufx


	if len(sys.argv) < 2:
		print STX.lin
		Leav("\n +Usage     "+STX.me+"    -f [from_file]      -o [output_file]      -s [suffix]<optional>\n            "+STX.Green+STX.me+"    -f list.txt 	   -o output.txt         -s phpinfo.php\n")
	
	opts,args = getopt.getopt(sys.argv[1:],'i:o:s:')
	for o,a in opts:
		if o=='-i' or o=='-input' or o=='-f':
			input_file=a
		elif  o=='-o' or o=='-output' or o=='-to':
			output_file=a
		elif o=='-sufx' or o=='-s':
			sufx=a;


	
	if os.path.isfile(input_file) is False:
		Leav(STX.Blue+STX.havlin+'\n+[Yasta]! Error '+STX.RED+'\n    Input File not found \n    Path:"'+STX.Green+input_file+'"\n'+STX.Blue+STX.havlin)

	
	printx(STX.lin,0)
	printnote("started at "+str(datetime.datetime.now()),0)
	printx("input file  :"+input_file,0)
	printx("output file :"+output_file,0)
	printx("suffix      :"+sufx,0)
	with open(input_file) as x :
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


print STX.RED
print"                          _________    ___.     ________"+STX.RED
print"                         /   _____/__ _\_ |__  /  _____/"+STX.Green
print"           ]<=========="+STX.RED+"  \_____  \|  |  \ __ \/   __  \   "+STX.Green+"========>[.."
print"           ]<=========="+STX.RED+"  /        \  |  / \_\ \  |__\  \  "+STX.Green+"========>[.."+STX.RED
print"                        /_______  /____/|___  /\_____  /"
print"                                \/          \/       \/ "+STX.Green
print"""
                    +Sub6 Sub-Domain Crawler and take overs detector By @YasserGersy
					This is BETA , Tools still under Development
"""
if __name__ == '__main__':
    defit()
    execNow()

    if result != '':
    	strm=open(output_file,'w')
    	strm.write(result)
    	strm.close()
    	printnote("\n"+STX.lin+"\nSaved to "+output_file,0)
    Leav('\n Done')


