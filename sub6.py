# !/bin/python

import sys,getopt
import os,datetime
import requests

requests.packages.urllib3.disable_warnings()

class DTCT:
	modulus='NO APPLICATION WAS FOUND FOR'
	heroku='no such app'
	githubio="<p><strong>There isn't a GitHub Pages site here.</strong></p>".lower()
	providerslist={'Modulus.io':modulus,'Heroku':heroku,'Github.io':githubio}

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
    magenta='\033[1;35m'
    White='\033[1;37m'
    lin="_________________________________________________________________________________________________"
    havlin='----------------------------'
    me='Sub6.py'
    sufx=''
    timeout=(5,15)
    TimedOutList=[]


def defit():
	global count,result,domains,output_file,input_file,opts,args,sufx,authurl
	count=0
	result=''
	domains=''
	output_file='result.txt'
	input_file=''
	opts={}
	args={}
	authurl=[]
	sufx=''




def Leav(s):
	print "\n"+STX.RED+s+"\n"+STX.White+STX.lin+STX.Green+'\n'
	exit();

def printx (s,con):
	sys.stdout.write(s)
	sys.stdout.flush()


def printnote(s,con):
	sys.stdout.write(STX.brown+s)
	sys.stdout.flush()
def printerror(s,con):
	sys.stdout.write(STX.FAIL+s)
	sys.stdout.flush()
def getheader(rqust,headername):
	res=''
	try:
		res=rqust.headers[headername]
	except Exception ,n :
		res=''
	return res
def spaces(s,i):
	s=str(s)
	lens=len(s)
	if lens < i:
		for i in range(0,i-lens):
			s=s+' '
	return s
def Investigate(hostp,indx):
	global sufx,result
	host=hostp.strip()
	if host.startswith("http") is False:
		url="http://"+host
	else:
		url=host
	sfx= ""
	if(len(sufx.strip()) > 0):
		if sufx.startswith('/') is False:		
			sfx="/"+sufx
	printnote ("\n"+STX.lin+"\n [+] "+spaces("Checking ["+str(indx)+"]",22)+"     ["+url.strip()+sfx+"]   ",0)
	requestDone=False
	requestSuccess=False
	requestErrorMSG=''
	resultobject=url
	while requestDone is False:
		try:
			res=requests.get(url,timeout=STX.timeout)
			requestDone=requestSuccess=True
		except Exception, e:
			requestSuccess=False
			requestDone=True
			requestErrorMSG=str(e)
			if 'Max retries exceeded with url' in requestErrorMSG:
				requestErrorMSG='Connection Timed out'
				if hostp not in STX.TimedOutList:
					STX.TimedOutList.append(hostp)
					resultobject=resultobject+requestErrorMSG+'\n'
			if "nor servname provided, or not known" in str(e):
				printerror( "Unreachable",1)
			
			printerror ('\n'+requestErrorMSG,1)

	if requestSuccess:
		source=res.text.lower()
		printx( '\n '+STX.magenta+str(res.status_code)+ " "+spaces(res.reason,20)+STX.Green+"       Content-Length=["+str(len(source))+"]",1)
		redirectlink=getheader(res,'location')
		server=getheader(res,'server')
		authheader=getheader(res,'WWW-Authenticate')

		if "None" not in str(redirectlink) and '' not in str(redirectlink):
			printx( STX.WARNING+"\n Redirects to >> [ "+redirectlink+STX.Green+" ]",1 )
			resultobject=resultobject+'Redirect:'+redirectlink+'\n'
		
		if "None" not in str(server):
			printx( STX.Blue+"		Server = "+str(server)+STX.Green,1)
			resultobject=resultobject+'Server:'+server+'\n'
		if authheader != "" and 'None' not in str(authheader):	
			print('Authentication on '+host+'WWW-Authenticate:'+authheader)
			resultobject=resultobject+'Authentication:'+authheader+'\n'

		foundunclaimed=False
		for si in DTCT.providerslist:
			if DTCT.providerslist[si] in source:
				printx (STX.UNDERlinE+"["+si+"] detected"+STX.Green,1)
				foundunclaimed=True
				resultobject=resultobject+'Hosted at '+si+'\n'
	result=resultobject+'\n'

	

def getabsolutepath(p):
	workingdir=os.getcwd()+'/'
	workingdir=workingdir.replace('//','/')
	p=p.replace(workingdir,'')
	p=workingdir+p
	return p

def execNow():
	global output_file,input_file,sufx,count
	inputfileList=[]
	arglen=len(sys.argv)
	if arglen < 2:
		print STX.lin
		Leav("\n +Usage     "+STX.me+"    -i [input_file]     -o [output_file]      -s [suffix]<optional>\n            "+STX.Green+STX.me+"    -i list.txt 	   -o output.txt         -s phpinfo.php\n")
	
	opts,args = getopt.getopt(sys.argv[1:],'i:o:s:t:')
	for o,a in opts:
		if o=='-i' :
			input_file=a
		elif  o=='-o' :
			output_file=a
		elif o=='-s':
			sufx=a;
		elif o=='-t':
			time=''.join(c for c in a if c.isdigit())
			time=int(time)
			STX.timeout=(time,time*3)

	if arglen > 1 and input_file=="":
		input_file=sys.argv[1]
	
	##Repairing relative paths
	if ',' not in input_file:
		input_file=getabsolutepath(input_file)
	output_file=getabsolutepath(output_file)

	if os.path.isfile(input_file) is False and ',' not in input_file:
		Leav(STX.Blue+STX.havlin+'\n+[Yasta]! Error '+STX.RED+'\n    Input File not found \n    Path:"'+STX.Green+input_file+'"\n'+STX.Blue+STX.havlin)

	try:
		with open('providers.txt') as strm:
			lines=strm.readlines()
			for l in lines:
				if ':' in l:
					arr=l.split(':')
					site=arr[0]
					delimeter=arr[1]
					if delimeter !="" and site not in DTCT.providerslist and l.startswith('#')==False:
						DTCT.providerslist[site]=delimeter
	except Exception,e:
		printnote('No list found , i will use the built in',0)
	
	printnote(STX.lin+"\nStarted at        : "+str(datetime.datetime.now()),0)
	printx("\nInput file        : [ "+input_file+" ]",0)
	printx("\nOutput file       : [ "+output_file+"  ]",0)
	printx('\nDomains loaded    : '+str(len(DTCT.providerslist)),0)
	printx('\nConnection TimeOut: '+str(STX.timeout),0)
	if sufx != "":
		printx("suffix      :"+sufx,0)
	if ',' in input_file :
		arr=input_file.split(',')
		for f in arr:
			if f not in fileList:
				inputfileList.append(f)
	else:
		inputfileList.append(input_file)

	for inp in inputfileList:
		with open(inp) as x :
			domains=x.readlines()
		for dom in domains:
			count=count+1
			if "." not in dom:
				continue 
			elif len(dom) < 5:
				continue
			else :			
				Investigate(dom,count)

	if len(STX.TimedOutList) > 0:
		count =count+1
		for dom in STX.TimedOutList:
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


