""" Initially open two ports using beanstalkd -l 127.0.0.x -p 113xx and change the beanstalkc.connection command accordingly.
 	chisafe.py has a function namely "queue" which takes the json file(along with the absolute path) which consists the list of sites in the format {"url":"id_url"}
	The final answer is stored in "Chisafe.json" and also "Chisafe.csv" in a proper format
  Usage for a list of sites : chisafe.queue(<json file>,<host>,<port1>,<port2>) or simply chisafe.queue(<json file>) 
  Usage for a single site : chisafe.spider(<url>,<id_url>)
  Result : Chisafe.json , Chisafe.csv 
  DEFAULT_PORT1 is for the Jobs to be queued
  DEFAULT_PORT2 is for the jobs that are buried"""
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT1 = 11300
DEFAULT_PORT2 = 11302
import beanstalkc
import sys
from contentanalyzer import ContentAnalyzer
import threading
import pycurl
import nltk.util
from sgmllib import SGMLParser
import urllib2
import pycurl
import socket
import json
from pprint import pprint
import time
timeout =3
socket.setdefaulttimeout(timeout)
import csv
import json
from google_safe_browser import GoogleSafeBrowser
fd_2 = open('Chisafe.csv','a')
p = ContentAnalyzer()
class URLLister(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.urls = []

	def start_a(self, attrs):
		href = [v for k, v in attrs if k=='href']
		if href:
			self.urls.extend(href)
def Google_Safe(seed):
	     global p
	     if(GoogleSafeBrowser(seed).malware() is True):
	         score,remark = p.Advanced(seed.strip('\n')+'Malware Not Processed'+' ',' ',[])
		 return score,remark
	     elif(GoogleSafeBrowser(seed).phishing() is True):
	    	 score,remark = p.Advanced(seed.strip('\n')+'Phishing Not Processed'+' ',' ',[])
 		 return score,remark		 
	     else:
		 return True
def spider(seed,id_url):
    global p
    fd_2 = open('Chisafe.csv','a')
    json_2 = open('Chisafe.json','a') 	
    seed = 'http://'+seed
    if(Google_Safe(seed) == True):
	try :
             t = Test()
	     c = pycurl.Curl()
	     c.setopt(pycurl.FOLLOWLOCATION, 1)
	     c.setopt(pycurl.MAXREDIRS, 3) 
	     c.setopt(pycurl.CONNECTTIMEOUT,5)
	     c.setopt(pycurl.TIMEOUT, 5)
	     c.setopt(pycurl.NOSIGNAL, 1) 
	     c.setopt(pycurl.HEADER, 1) 
	     c.setopt(pycurl.URL,seed)
	     c.setopt(pycurl.HTTPGET, 1)
	     c.setopt(pycurl.WRITEFUNCTION, t.body_callback)
	     c.perform()
	     page = t.contents  
	     links = read(seed)	   
	     score, remark = p.Advanced(seed,page,links)
	     
	     links = []
	     print("DONE : %s" % seed)
	     
        except Exception as e :
            print ("ERROR : %s %s " % (seed,e))			
	    score, remark = p.Advanced(seed.strip('\n')+str(e).strip('\n'),' ',[])

    	reswriter = csv.writer(fd_2,delimiter  = ',')
    	row = json.dumps({id_url.strip('\n'):[seed,score,remark]})
    	json_2.write(row)
    	reswriter.writerow([id_url.strip('\n')+' ',' '+seed.strip('\n')+' ',score,' '+remark]) 
    else:
	score,remark = Google_Safe(seed,p)
    	reswriter = csv.writer(fd_2,delimiter  = ',')
    	row = json.dumps({id_url.strip('\n'):[seed,score,remark]})
    	json_2.write(row)
    	reswriter.writerow([id_url.strip('\n')+' ',' '+seed.strip('\n')+' ',score,' '+remark]) 
	 
def read(link)	:
	usock = urllib2.urlopen(link)
	parser = URLLister()   
	parser.feed(usock.read())
	parser.close()
	return parser.urls

class Test:
        def __init__(self):
                self.contents = ''

        def body_callback(self, buf):
                self.contents = self.contents + buf  

def timeout(spider,seed,id_url,timeout_duration=10):
    """This function will spawn a thread and run the given function
    using the args, kwargs and return the given default value if the
    timeout_duration is exceeded.
    """ 
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None
        def run(self):
            self.result = spider(seed,id_url)
    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.isAlive():
        return it.result
    else:
        return it.result

def queue(jsonfile,host = DEFAULT_HOST,port1 = DEFAULT_PORT1,port2 = DEFAULT_PORT2):
	open('Chisafe.csv','w')
	open('Chisafe.json','w') 	 	 	
	bean = beanstalkc.Connection(host, port1)
	bean_bury = beanstalkc.Connection(host, port2)
	seedlist = {}
	json_data = open(jsonfile)
	seedlist = json.load(json_data)
	json_data.close()
	for seed in seedlist:    
  		print 'Put on Que: %s'  % seed.strip('\n')
  		bean.put(str(seed), ttr =5)
	while True:
		job = bean.reserve() 		
		try:
    			timeout(spider,job.body,seedlist[job.body])        
 	 	except :
    			job.bury()
			bean_bury.put(job.body) 
			print  "Job Buried: %s" % job.body 
		job.delete()
		bean.kick()	
