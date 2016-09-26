# !/bin/python
# Cross-Domain Crawler and subdomain take over detector
# Author: YasserGersy gersy.ch2@gmail.com
import sys,getopt
import os,datetime
try:
	import requests
except ImportError :
	print('\n Requests not installed ...\n Exiting...')
	exit()
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
    yel = '\033[93m'
    White='\033[1;37m'
    UseProx=False
    allow_redirects=False
    lin="_______________________________________________________________________________________________________________________"
    havlin='----------------------------'
    me='Sub6.py'
    ver='v1.1'
    sufx=''
    timeout=(5,15)
    TimedOutList=[]
    protocol='http'
    HosInjection=False
    OpenRedirectorLink='rapid7.com'
    OpenRedirector=False
    startIndex=0
    proxyDict = { "http"  : "http://127.0.0.1:8080", "https" : "https://127.0.0.1:8080",   "ftp"   : "ftp://127.0.0.1:8080"}
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:47.0) Gecko/20100101 Firefox/47.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5'}
def defit():
	global count,result,domains,output_file,input_file,opts,args,authurl
	count=0
	result=''
	domains=''
	output_file='result.txt'
	input_file=''
	opts={}
	args={}
	authurl=[]
	

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
def Investigate(hostp,indx,AddToResult,trycounter,proto,ForceHTTP):
	global result
	evilhost=hostp+'evil.com'
	if STX.HosInjection:
		STX.headers['Host']=evilhost
	else:
		STX.headers['Host']=hostp

	host=hostp.strip()
	if host.startswith("http") is False:
		url=proto.lower()+"://"+host
	else:
		url=host
	sfx= ""
	if(len(STX.sufx.strip()) > 0) :
		if STX.sufx.startswith('/')is False :		
			sfx="/"+STX.sufx
		else:
			sfx=STX.sufx
	TryTestingOpenRedirect=STX.OpenRedirector

	if sfx=="" and STX.OpenRedirector:
		sfx='//'+STX.OpenRedirectorLink
		TryTestingOpenRedirect=False

	url=url+sfx

	printnote ("\n"+(STX.lin if ForceHTTP==False else STX.havlin)+STX.Green+"\n [+] "+spaces("Checking ["+str(trycounter)+"]["+str(indx)+"]",27)+"      "+spaces("["+url.strip()+"]",50)+('' if STX.HosInjection==False else (STX.RED+"  :["+STX.headers['Host']+"]")),0)
	requestDone=False
	requestSuccess=False
	requestErrorMSG=''
	resultobject=url
	procOverHTTP=False
	redirectlink=''
	while requestDone is False:
		try:
			if STX.UseProx is False:
				res=requests.get(url,timeout=STX.timeout,headers=STX.headers,allow_redirects=STX.allow_redirects)
			else:
				res=requests.get(url,timeout=STX.timeout,headers=STX.headers,allow_redirects=STX.allow_redirects,proxies=STX.proxyDict)

			requestDone=requestSuccess=True
		except Exception, e:
			requestSuccess=False
			requestDone=True
			requestErrorMSG=str(e)
			if "nor servname provided, or not known" in requestErrorMSG:
				requestErrorMSG='Unreachable'
			elif 'Read timed out' in requestErrorMSG:
				requestErrorMSG='Read timed out'
				STX.TimedOutList.append(hostp)
				resultobject=resultobject+'\n'+requestErrorMSG+'\n'
			elif 'Max retries exceeded with url' in requestErrorMSG:
				requestErrorMSG='Connection Timed out'
				if hostp not in STX.TimedOutList and AddToResult==True:
					STX.TimedOutList.append(hostp)
					resultobject=resultobject+'\n'+requestErrorMSG+'\n'
			elif "doesn't match either of" in requestErrorMSG:
				resultobject=resultobject+'\n SSL Error'
				requestErrorMSG='SSL Error'+(', Retrying Over HTTP..' if ForceHTTP==False else "")
				procOverHTTP=True
			printerror ('\n'+requestErrorMSG,1)

	if requestSuccess:
		source=res.text.lower()
		printx( '\n '+STX.magenta+str(res.status_code)+ " "+spaces(res.reason,25)+STX.brown+"        "+spaces("Content-Length=["+str(len(source))+"]",52),1)
		redirectlink=getheader(res,'location')
		server=getheader(res,'server')
		authheader=getheader(res,'WWW-Authenticate')

		
		if "None" not in str(server) and len(server) >1:
			printx( STX.Blue+"Server = ["+str(server+"]")+STX.Green,1)
			resultobject=resultobject+'\nServer:'+server+'\n'

		if authheader != "" and 'None' not in str(authheader):	
			print('Authentication on '+host+'WWW-Authenticate:'+authheader)
			resultobject=resultobject+'\nAuthentication:'+authheader

		if "None" not in str(redirectlink) and '' != str(redirectlink):
			printx( STX.White+("\n Redirects to                         ")+redirectlink+" "+STX.Green,1 )
			resultobject=resultobject+'\nRedirect:'+redirectlink

		if evilhost in source:
			printx(STX.yel+('\n [ Vulnerable to Host injection : 40% ]'),0)

		if (redirectlink.startswith('http://'+STX.OpenRedirectorLink) or redirectlink.startswith('https://'+STX.OpenRedirectorLink) or '//'+STX.OpenRedirectorLink==redirectlink or STX.OpenRedirectorLink==redirectlink) and STX.OpenRedirector:
			printx(STX.yel+'\nOpen redirector Detected',0)
			resultobject=resultobject+'\n Vulnerable to open redirect'

		foundunclaimed=False
		for si in DTCT.providerslist:
			if DTCT.providerslist[si] in source:
				printx (STX.UNDERlinE+"["+si+"] Subdomain TO is detected"+STX.Green,1)
				foundunclaimed=True
				resultobject=resultobject+'\nHosted at '+si+'\n'
	if AddToResult:
		result=result+resultobject+'\n\n'

	if ForceHTTP==False or STX.protocol=='both':
		if procOverHTTP :
			Investigate(hostp,(str(indx)+'] [HTTP'),AddToResult,trycounter,'http',True)
		elif proto=='http' and redirectlink.startswith('https:') :
			Investigate(hostp,(str(indx)+'] [HTTPS'),AddToResult,trycounter,'https',True)




def getabsolutepath(p):
	workingdir=os.getcwd()+'/'
	workingdir=workingdir.replace('//','/')
	p=p.replace(workingdir,'')
	p=workingdir+p
	return p
def arraytostr(x):
	if len(x)==1:
		return str(x)
	res=''
	for l in x:
		res=res+l+', '
	return res[0,len(res)-2]

def execNow():
	global output_file,input_file,count
	inputfileList=[]
	arglen=len(sys.argv)
	if arglen < 2:
		print STX.lin
		msg=("""   +Usage     
			
		    python sub6.py    -i list.txt  -o output.txt       -s phpinfo.php	-x 4
	                                             <optional>           <optional>   <optional>
		   """+STX.yel+"""[+]Options
		    -i      input  files (if many separate by comma)
		    -o      output file
		    -p      protocol (http/https)
		    -s      suffix    (/phpinfo.php)         #used to look for ceratin files
		    -t      Set time out for requests
		    -x      starting index                   #if script stopped , you can resume it with this.
		    -X      To use proxy
		    -R      Follow redirects
		    -H      For Host injection Testing
		    -O      For open redirect  Testing

		            """)
		Leav(msg)
	opts,args='',''
	try:
		opts,args = getopt.getopt(sys.argv[1:],'i:I:o:s:S:t:T:p:P:x:X:r:R:h:H:O:')
	except Exception,e:
		printerror(str(e))
	output_file=''
	for o,a in opts:
		if o=='-i' :		#i > input
			input_file=a
			if output_file =='' and ',' not in input_file:
				output_file =input_file+'__Sub6.result'
		elif  o=='-o' :		#o > output
			output_file=a
		elif  o=='-p' :		#p > protocol
			a=a.lower()[1:]
			if a=='httpandhttps' or a=='http,https' or a='http&https' or a=='both':
				STX.protocol='both'
			if a=='http' or a=='https':
				STX.protocol=a
		elif o=='-s':		#s > sufx  
			STX.sufx=a;
			if STX.sufx.startswith('='):
				STX.sufx=STX.sufx[1:]
		elif o=='-t':		#t > timeout 
			time=''.join(c for c in a if c.isdigit())
			time=int(time)
			STX.timeout=(time,time*4)
		elif o=='-x': 		# x > startindex
			val=''.join(c for c in a if c.isdigit())
			val=int(val)
			STX.startIndex=val
		elif o== '-R':       #R > allow follow redirects
			STX.allow_redirects=True
		elif o == '-H':
			STX.HosInjection=True
		elif o =='-O':
			STX.OpenRedirector=True
		elif o=='-X':       # X > use proxy
			STX.UseProx=True
			printx('Please provide proxy details',0)
			httpprx=raw_input('\nWhat proxy you want to use (ex 127.0.0.1:8080) press enter for default or no to disable : ')
			if httpprx.lower()=='no':
				STX.UseProx=False
			elif httpprx == '':
				httpprx='127.0.0.1:8080'
			proxyDict = { "http"  : "http://"+httpprx, "https" : "https://"+httpprx,   "ftp"   : "ftp://127.0.0.1:8080"}
    	

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
		xio='debugging'
		#printnote('No list found , i will use the built in',0)
	
	domains=[]
	if ',' in input_file :
		arr=input_file.split(',')
		for f in arr:
			if f not in inputfileList:
				inputfileList.append(f)
	else:
		inputfileList.append(input_file)

	for inp in inputfileList:
		with open(inp) as x :
			ds=x.readlines()
			for dline in ds :
				dline=dline.strip()
				if dline=='' or '.' not in dline:
					continue
				if dline not in domains:
					domains.append(dline)

	printnote(STX.lin+"\n[+] Info"+STX.White,0)
	spx=len(str(inputfileList))
	if len(output_file)>spx:
		spx=len(output_file)
	printx("\n   Input file"+("s" if len(inputfileList)>1 else ' ')+"        : [ "+spaces(input_file,spx)+" ]",0)
	printx("\n   Output file        : [ "+spaces(output_file,spx)+" ]",0)
	printx('\n   Domains Loaded     : '+str(len(domains)),0)
	printx('\n   SubDomain Paterns  : '+str(len(DTCT.providerslist)),0)
	printx('\n   Protocol           : '+STX.protocol.upper(),0)
	printx('\n   Connection TimeOut : '+str(STX.timeout).replace(',',':Connection,').replace(')',':ReadingResponse)'),0)
	printx('' if len(STX.sufx)  < 2 else ('\n   Suffix             : '+('' if STX.sufx.startswith('/') else '/')+STX.sufx),0)
	printx('' if STX.startIndex<1 else ('\n   Starting Index     : '+str(STX.startIndex)),0)
	printx('' if STX.UseProx is False else '\n   Using Proxy        : '+str(STX.proxyDict),0)
	printx('' if STX.HosInjection is False else '\n   Mode:              : Subdomain TO , Host Injection '+(',Open Redirects' if STX.OpenRedirector else '')+(', CTF' if len(STX.sufx) > 2 else ''),0)
	tm=str(datetime.datetime.now())
	printnote("\n"+STX.yel+"Started at         : "+tm,0)
	result=STX.lin+'Started at '+tm+'\n'
	
	
	if STX.startIndex >= len(domains):
		STX.startIndex=0
	trycounter=1
	for dom in domains:
		count=count+1
		if count<STX.startIndex:
			continue
		if "." not in dom:
			continue 
		elif len(dom) < 5:
			continue
		else :			
			Investigate(dom,count,True,trycounter,STX.protocol,False)
 
	trycounter=2
	if len(STX.TimedOutList)>0:
		print ('\n'+STX.lin+'\n [+] Retrying Timedout Domains .... ')
		if len(STX.TimedOutList) > 0:
			count =count+1
			for dom in STX.TimedOutList:
				if "." not in dom:
					continue 
				elif len(dom) < 5:
					continue
				else :			
					Investigate(dom,count,False,trycounter,STX.protocol,False)
	


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
					This is BETA , Tool  stills under Development
"""

if __name__ == '__main__':
    defit()
    try:
    	execNow()
    except KeyboardInterrupt,n:
    	printerror('\nAborted By user',0)
    if STX.startIndex>0:
    	olddata=''
    	try:
	    	with open(output_file) as rd:
    			olddata=rd.read()
    	except Exception:
    		olddata=''
    	result=olddata+'\n\n'+result
    if result != '':
    	strm=open(output_file,'w')
    	strm.write(result)
    	strm.close()
    	printnote("\n"+STX.lin+"\nSaving Result to 		:"+output_file,0)
    Leav('\n Done')
