# sub6
subdomain take over detector and crawler 


<img src='http://i.imgur.com/CLgFPKp.png' onerror='alert("deleted");' /> 

  +Usage     
			
		    python sub6.py    -i list.txt  -o output.txt       -s phpinfo.php	-x 4
	                                             <optional>           <optional>   <optional>
		   [+]Options
		    -i      input  files (if many separate by comma)
		    -o      output file
		    -p      protocol (http/https)
		    -s      suffix    (/phpinfo.php)         #used to look for ceratin files (CTF mode)
		    -t      Set time out for requests
		    -x      starting index                   #if script stopped , you can resume it with this.
		    -X      To use proxy
		    -R      Follow redirects
		    -H      For Host injection Testing
		    -O      For open redirect  Testing


