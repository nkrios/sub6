# sub6
subdomain take over detector and crawler 

<!--
/*<img src='http://i.imgur.com/CLgFPKp.png' onerror='alert("deleted");' /> 
*/


![Usage](ScreenShotUsg.png]
-->
<img src='http://i.imgur.com/5Mxlmlw.png' /> 



 +Usage     
			
		    python sub6.py    -i list.txt  -o output.txt       -s phpinfo.php	-x 4
	                                             <optional>           <optional>   <optional>
		   [+]Options
		    -i      input  files                  twitterdomains.txt    #if many separate by comma
		    -o      output file                   twitterResult.txt
		    -p      protocol                      http or https
		    -s      suffix                        phpinfo.php           #used to look for ceratin files (CTF mode)
		    -t      Set time out for requests     5                     #in seconds
		    -x      starting index                1:                    #if script stopped , you can resume it with this.
		    -X      To use proxy                  #prompt
		    -R      Follow redirects
		    -H      For Host injection Testing
		    -O      For open redirect  Testing


