""" Adsafe 
 About the Program : The program has two mode Basic(Gives the result as True or False for a particular class) and Advanced(Gives a rating of 1 to 5 (5 being very bad)
 How do i use it ? : You can send 3 arguments (<url name>,<html of the url>,<list of the links on the url>) to any of the functions (Basic or Advanced) and the program will return you a json  array with the result.(A csv is also generated)
 Parsing a list of links : Pass the json file to the perform function in "chisafe.py"(bean.py uses beanstalk to process the links)"""
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from Numeric import *
from sys import argv
import cPickle as pickle
import nltk.util
import pycurl
import socket
import numpy
import time
import csv
from numpy import *
import directory
class Bayesian:
                     
    def __init__(self,count,c):
        global C
        global word_list_all
        self.count = count
        self.c = c
        if (self.count == 0):
            word_list,A = Bucket_Processing().return_()
            self.word_list = word_list
            self.word_list_all = []
            self.A = A                                                  
        if not(self.count == 0):
            self.word_list = word_list_all
	    self.A = self.normalise(C)                            
    def learning(self):                                       
        global C
        global word_list_all
        ini_length_word_list = len(self.word_list)
        length_link_text,length_list_link_text =0,0
        region_text = zeros([7],Int)
        region_link = zeros([7],Int) 
        i,site_value_text,site_value_link=0,0.0,0.0
        word_list_text = self.word_list                                                            
        word_list_link = self.word_list                                                            
        text = pickle.load(open('pfile_text.p'))
        link_text = str(text).lower().split(None)
	last = link_text[-1].strip(']')
	last = last + ','
	link_text.remove(link_text[-1])
	link_text.append(last)
        length_link_text = len(link_text)
        text = pickle.load(open('pfile_link.p'))
        list_link_text = str(text).lower().split(None)
	last = list_link_text[-1].strip(']')
	last = last + ','
	list_link_text.remove(list_link_text[-1])
	list_link_text.append(last)
	length_list_link_text = len(list_link_text)
        for word in link_text: 
            if word in word_list_text:
                ind = word_list_text.index(word)
                for i in range(2,9):
                    if self.A[ind][i]==1 and self.A[ind][9]==0:   
                        region_text[i-2]+=1
                    elif self.A[ind][i]==1 and self.A[ind][9]==1: 
			num = self.A[ind][10]
                        region_text[num-2]+=10		    
                site_value_text = site_value_text + self.A[ind][1]
                self.A[ind][0]+=1
        site_class_text = self.find_max(region_text)+2 
        mini_text,maxim_text,mini_link,maxim_link=0,0,0,0
        text_limit_good,text_limit_bad,link_limit_good,link_limit_bad =0.25*length_link_text,-0.25*length_link_text,0.1*length_list_link_text,-0.1*length_list_link_text
          
        if (site_value_text > text_limit_good  ):
            for ind,word in enumerate(self.word_list):
                if word in link_text:
                    if(mini_text > self.A[ind][1]):
                        mini_text = self.A[ind][1]

        if (site_value_text <=text_limit_bad ):
            for ind,word in enumerate(self.word_list):
                if word in link_text:
                    if(maxim_text < self.A[ind][1]):
                        maxim_text = self.A[ind][1]        
    
    
        for word in list_link_text: 
            if word in word_list_link:
                ind = word_list_link.index(word) 
                for i in range(2,9):
                    if self.A[ind][i]==1 and self.A[ind][9]==0:  
                        region_link[i-2]+=1
                    elif self.A[ind][i]==1 and self.A[ind][9]==1:  
			num = self.A[ind][10]
                        region_link[num-2]+=10
                site_value_link = site_value_link + self.A[ind][1]
                self.A[ind][0]+=1 
        site_class_link = self.find_max(region_link)+2 
    
    
        if (site_value_link > link_limit_good ):
            for ind,word in enumerate(self.word_list):
                if word in list_link_text:
                    if(mini_link > self.A[ind][1]):
                        mini_link = self.A[ind][1]
    
    
        if (site_value_link <=link_limit_bad ):
            for ind,word in enumerate(self.word_list):
                if word in list_link_text:
                    if(maxim_link < self.A[ind][1]):
                        maxim_link = self.A[ind][1] 
        text_limit_good,text_limit_bad,link_limit_good,link_limit_bad =0.25*length_link_text,-0.25*length_link_text,0.1*length_list_link_text,-0.1*length_list_link_text
    
    
        if (site_value_text > text_limit_good): 
            for word in link_text:
                if word not in word_list_link:               
                    word_list_link.append(word)
                    ind = self.word_list.index(word)
                    if((site_value_text > text_limit_good)and(site_value_link > link_limit_good)):
                        self.A[ind][1] = abs(min(mini_link,mini_text))                       
                    else:
                        self.A[ind][1] = -max(maxim_link,maxim_text,site_value_text,site_value_link)                        
                    f=0
                    for i in range(1,7):
                        if (region_text[i]>=1):
                            f=1
                            self.A[ind][i+2]=1
                        if (f==0):
                            self.A[ind][2]=1                                                                         

        if (site_value_text <= text_limit_bad): 
            for word in link_text:
                if word not in word_list_link:                
                    word_list_link.append(word)
                    ind = self.word_list.index(word)
                    if((site_value_text > text_limit_good)and(site_value_link > link_limit_good)):
                        self.A[ind][1] = abs(min(mini_link,mini_text))                       
                    else:
                        self.A[ind][1] = -max(maxim_link,maxim_text,site_value_text,site_value_link)                        
                    f=0
                    for i in range(1,7):
                        if (region_text[i]>=1):
                            f=1
                            self.A[ind][i+2]=1
                        if (f==0):
                            self.A[ind][2]=1                           

        if (site_value_link > link_limit_good): 
            for word in list_link_text:
                if word not in word_list_text:                
                    word_list_text.append(word)
                    ind = self.word_list.index(word)
                    if((site_value_text > text_limit_good)and(site_value_link > link_limit_good)):
                        self.A[ind][1] = abs(min(mini_link,mini_text))                  
                    else:
                        self.A[ind][1] = -max(maxim_link,maxim_text,site_value_text,site_value_link)                        
                    f=0
                    for i in range(1,7):
                        if (region_link[i]>=1):
                            f=1
                            self.A[ind][i+2]=1
                        if (f==0):
                            self.A[ind][2]=1                        

        if (site_value_link <= link_limit_bad): 
            for word in list_link_text:
                if word not in word_list_text:                     
                    word_list_text.append(word)
                    ind = self.word_list.index(word)
                    if((site_value_text > text_limit_good)and(site_value_link > link_limit_good)):
                        self.A[ind][1] = abs(min(mini_link,mini_text))           
                    else:

                        self.A[ind][1] = -max(maxim_link,maxim_text,site_value_text,site_value_link)
                    f=0
                    for i in range(1,7):
                        if (region_link[i]>=1):
                            f=1
                            self.A[ind][i+2]=1
                        if (f==0):
                            self.A[ind][2]=1 
                        
        word_list_all = self.word_list
        C = self.A
        return region_text,region_link,length_list_link_text,length_link_text
    
    def find_max(self,a):
        maxi=0
        max_index=0
        for i in range(6):
            if(maxi < a[i]):
                maxi=a[i]
                max_index = i
        return max_index
    def normalise(self,B):
        norm_fac=0.0
        for ind,word in enumerate(self.word_list):
            norm_fac = norm_fac + B[ind][0]
        for ind,word in enumerate(self.word_list):
            B[ind][1] = (B[ind][1])/norm_fac
        return B  

class Bucket_Processing:
    
    
    def __init__(self):
        self.word_list = []
        self.A = zeros([1000000,11],Float)
        self.i = 0

    def return_(self):
        
        self.perform()
        return self.word_list,self.A    
    
    def frequency(self,text,freq,num,factor):
        word_list_temp ,word_list_tempo,links_list,word_list_temporary=[],[],[],[]   
        word_list_temp = str(text).lower().split(None)
	 
        for word in word_list_temp:
            if word not in self.word_list:
                self.word_list.append(word)
        for word in word_list_temp:
            freq[word] = freq.get(word, 0) + 1       
            keys = freq.keys()   
        for ind,word in enumerate(self.word_list):
            try:
                self.A[ind][0]= self.A[ind][0] + int(freq[word]) 
            except Exception as e:
                continue  
        norm_f =0.0
        p=0.0
        for word in freq:
            norm_f = norm_f + freq[word]
    
        for word in freq:
            p= freq[word]/norm_f
            freq[word]=p 
    
        for word in word_list_temp:
            ind = self.word_list.index(word)
            if(self.A[ind][2] == 1):
                self.A[ind][2] = 0
                self.A[ind][num] = 1
            elif(self.A[ind][2]!=1):
                self.A[ind][num] = 1
	    if (factor == 1):
		if(self.A[ind][2]!=1):
			self.A[ind][9]=1
			self.A[ind][10]=num
		
	      
        for ind,word in enumerate(self.word_list):                                                    
            try:
                if(self.A[ind][2]==1):
                    self.A[ind][1] =  self.A[ind][1] + float(freq[word])
                elif(self.A[ind][2]!=1) and (self.A[ind][9]==1):
                    self.A[ind][1] =  self.A[ind][1] - 10*float(freq[word])
                elif(self.A[ind][2]!=1) and (self.A[ind][9]==0):
                    self.A[ind][1] =  self.A[ind][1] - float(freq[word])				
            except Exception as e:
                continue
        return self.A 
 
    def perform(self):
        good_word_freq,bad_porn_freq,bad_violence_freq,bad_racism_freq,bad_drugs_freq,bad_alcohol_freq,bad_tobacco_freq = {},{},{},{},{},{},{}
	bad_porn,bad_violence,bad_racism,bad_drugs,bad_alcohol,bad_tobacco = {},{},{},{},{},{}
        good_text,porn_text,violence_text,racism_text,drugs_text, alcohol_text,tobacco_text = [],[],[],[],[],[],[]
	bad_porn_text,bad_violence_text,bad_racism_text,bad_drugs_text, bad_alcohol_text,bad_tobacco_text = [],[],[],[],[],[]

        good_text = self.openandstem('good_temp.txt')
        self.frequency(good_text,good_word_freq,2,0)
    
        porn_text = self.openandstem('porn_temp.txt')
        self.frequency(porn_text,bad_porn_freq,3,0)
    
        violence_text = self.openandstem('violence_temp.txt')
        self.frequency(violence_text,bad_violence_freq,4,0)
    
        racism_text = self.openandstem('racism_temp.txt')
        self.frequency(racism_text,bad_racism_freq,5,0)
    
        drugs_text = self.openandstem('drugs_temp.txt')  
        self.frequency(drugs_text,bad_drugs_freq,6,0)
    
        alcohol_text = self.openandstem('alcohol_temp.txt')
        self.frequency(alcohol_text,bad_alcohol_freq,7,0)
    
        tobacco_text = self.openandstem('tobacco_temp.txt')
        self.frequency(tobacco_text,bad_tobacco_freq,8,0)

        bad_porn_text = self.openandstem('porn_bad.txt')
        self.frequency(bad_porn_text,bad_porn,3,1)
    
        bad_violence_text = self.openandstem('violence_bad.txt')
        self.frequency(bad_violence_text,bad_violence,4,1)
    
        bad_racism_text = self.openandstem('racism_bad.txt')
        self.frequency(bad_racism_text,bad_racism,5,1)
    
        bad_drugs_text = self.openandstem('drugs_bad.txt')  
        self.frequency(bad_drugs_text,bad_drugs,6,1)
    
        bad_alcohol_text = self.openandstem('alcohol_bad.txt')
        self.frequency(bad_alcohol_text,bad_alcohol,7,1)
    
        bad_tobacco_text = self.openandstem('tobacco_bad.txt')
        self.frequency(bad_tobacco_text,bad_tobacco,8,1)
	 
    
        return True
 
    def openandstem(self,file1):
        path = directory.path()
        doc = open(path+'/text/'+file1, 'r').read()
        return Stemming().stem(doc)  


class Content_Classifier_2:

    
    def __init__(self,region_text,region_link,length_list_link_text,length_link_text):
	self.region_text,self.region_link,self.length_list_link_text,self.length_link_text = region_text,region_link,length_list_link_text,length_link_text	
	
         
    def classify_text(self,i):
	if self.length_link_text <= 800 :

        	if(self.region_text[i]>float(self.length_link_text)/4): 
        	    return 5       
        	elif ((self.region_text[i]>float(self.length_link_text)/6 and self.region_text[i]<=float(self.length_link_text)/4 + 1)):
        	    return 4        
        	elif((self.region_text[i]<=float(self.length_link_text)/6 + 1 and self.region_text[i]>float(self.length_link_text)/8)):
        	    return 3       
        	elif((self.region_text[i]<=float(self.length_link_text)/8 + 1 and self.region_text[i]>float(self.length_link_text)/10)):
        	    return 2
        	elif(self.region_text[i]<=float(self.length_link_text)/10 + 1):
        	    return 1
 	elif self.length_link_text >800 :
        	if(self.region_text[i]>133): 
        	    return 5       
        	elif (self.region_text[i]>100 and self.region_text[i]<=133):
        	    return 4        
        	elif(self.region_text[i]<=100 and self.region_text[i]>80):
        	    return 3       
        	elif(self.region_text[i]<=80 and self.region_text[i]>66):
        	    return 2
        	elif(self.region_text[i]<=66):
        	    return 1
		     
        
    def classify_link(self,i):
	if self.length_list_link_text <=800:

	        if (self.region_link[i]>float(self.length_list_link_text)/4): 
	            return 5
	        elif((self.region_link[i]>float(self.length_list_link_text)/6 and self.region_link[i]<=float(self.length_list_link_text)/4 + 1)):  
	            return 4
	        elif((self.region_link[i]<=float(self.length_list_link_text)/6 + 1 and self.region_link[i]>float(self.length_list_link_text)/8)):   
	            return 3       
	        elif((self.region_link[i]<=float(self.length_list_link_text)/8 + 1 and self.region_link[i]>float(self.length_list_link_text)/10)):          
	            return 2       
	        elif(self.region_link[i]<=float(self.length_list_link_text)/10 + 1):
	            return 1    

	elif self.length_list_link_text >800:
	        if (self.region_link[i]>133): 
	            return 5
	        elif(self.region_link[i]>100 and self.region_link[i]<=133):  
	            return 4
	        elif(self.region_link[i]<=100 and self.region_link[i]>80):   
	            return 3       
	        elif(self.region_link[i]<=80 and self.region_link[i]>66):          
	            return 2       
	        elif(self.region_link[i]<=66):
	            return 1 			
class ContentAnalyzer_Utils:    
          
    def __init__(self,string,html,links):
	self.string = string
        self.html = html
        self.links = links
        self.k = 0
        self.timeout =10
        socket.setdefaulttimeout(self.timeout)
      
    def read_text(self):                              
        seed_list = []
        pure_text = nltk.util.clean_html(self.html)
        stemmed_text = Stemming().stem(pure_text) 
        
        seed_list = self.links
        link_stemmed_text = Stemming().stem(self.fetch_page())
    
        return stemmed_text,link_stemmed_text,self.k

    def fetch_page(self):               
	    link_pure_text = []
	    for seed in self.links:
		if 'http://' or 'https://'or 'www'in seed:
			seed = seed
		elif len(seed)<15:
			seed = str(self.string.strip('\n'))+'/'+str(seed)			
	    	try:		
		    	self.k = self.k + 1
                	if self.k==3:
				self.k = 0
                    		break
                    	t = Test()
                   	c = pycurl.Curl()
		    	c.setopt(pycurl.MAXREDIRS, 3) 
	            	c.setopt(pycurl.CONNECTTIMEOUT, 5)
  		    	c.setopt(pycurl.TIMEOUT, 5)
                    	c.setopt(pycurl.HEADER, 1) 
			c.setopt(pycurl.NOSIGNAL, 1) 
                    	c.setopt(pycurl.FOLLOWLOCATION, 1)
                    	c.setopt(pycurl.URL,seed)
                    	c.setopt(pycurl.WRITEFUNCTION,t.body_callback)
                    	c.perform()
                    	c.close()
                    	link_pure_text.append(nltk.util.clean_html(t.contents))	    
	    	except Exception as e:
                    continue	
            return link_pure_text
    
                    
class Test:
        def __init__(self):
                self.contents = ''

        def body_callback(self, buf):
                self.contents = self.contents + buf 

class Stemming:
    
    def __init__(self):
        pass
    
    def stem(self,input_text):
       tokenizer = RegexpTokenizer('\s+', gaps=True)
       stemmed_text=[]
       lemmatizer = WordNetLemmatizer()
       stemmer = PorterStemmer() 
       text = tokenizer.tokenize(str(input_text))
       filtered_text = self.stopword(text)            
       for word in filtered_text:
           if word.isalpha():
		if len(word)>4:
               		stemmed_text.append(stemmer.stem_word(word).lower())
		else:
			stemmed_text.append(word.lower())
       for word in stemmed_text:
          if len(word) < 3 :
               stemmed_text.remove(word)      
       ' '.join(stemmed_text)
      
       return stemmed_text   
   
   
    def stopword(self,text):
          filtered_text = text[:]  
          stopset = set(stopwords.words('english'))      
          for word in text:                
             if len(word) < 3 or word.lower() in stopset: 
                 filtered_text.remove(word) 
          return filtered_text 
             

class ContentAnalyzer:

    def __init__(self):
        global data1,data2,i,class1,class2
        data2 = zeros([12],int)
	class2 = zeros([12],int)
	i = 0             
       
    def Advanced(self,string,html,link):
        start_time = time.time()
        global i
        global j
        global data2
	global class2
	        
        if(i==0):
            stemmed_text,link_stemmed_text,c = ContentAnalyzer_Utils(string,html,link).read_text()
	    path = directory.path()
            doc = open(path+'/text/'+'news.txt', 'r').read()
            self.news_list = Stemming().stem(doc)
	    doc = open(path+'/text/'+'games.txt', 'r').read()
  	    self.games_list = Stemming().stem(doc)
	    doc = open(path+'/text/'+'medicine.txt', 'r').read()
	    self.med_list = Stemming().stem(doc)  
            pickle.dump(stemmed_text, open('pfile_text.p','wb'))
            pickle.dump(link_stemmed_text,open('pfile_link.p','wb'))
	    region_text,region_link,length_list_link_text,length_link_text = Bayesian(i,c).learning()
            p = Content_Classifier_2(region_text,region_link,length_list_link_text,length_link_text)
            k = 0
            sitecounter = 0
            for u in range(1,7):
                data2[k] = p.classify_text(u)
	        k = k + 1
                data2[k] = p.classify_link(u)
                k = k + 1
            i = 1
        elif(i==1):
            stemmed_text,link_stemmed_text,c = ContentAnalyzer_Utils(string,html,link).read_text()
            pickle.dump(stemmed_text, open('pfile_text.p','wb'))
            pickle.dump(link_stemmed_text,open('pfile_link.p','wb'))
	    region_text,region_link,length_list_link_text,length_link_text = Bayesian(i,c).learning()     
            p = Content_Classifier_2(region_text,region_link,length_list_link_text,length_link_text )
	
            k = 0
            sitecounter = 0
            for u in range(1,7):
                data2[k] = p.classify_text(u)
                k = k + 1
                data2[k] = p.classify_link(u)
                k = k + 1
            
        
        s = []
       
        s[:] = data2
	value = self.check_advanced(data2,stemmed_text)
	if(sum(data2) !=12):	
		value = value + ' ' +self.reason(data2)
	elif(sum(data2) == 12):
		value = 'SAFE'
        if sum(data2)==0 and len(stemmed_text) <=20: value = "Not-Enough-Text-on-Site"
	elif len(stemmed_text)==0 : value = "ERROR"

	return s, value		

    def check_advanced(self,data,stemmed_text):
	news,games,med=0,0,0
	if data[2]>2 and sum(data)==11+data[2]:
	    for word in self.news_list:
	        if word in stemmed_text:
			news+=1
	    for word in self.games_list:
		if word in stemmed_text:
			games+=1
	    if(news >=15):
		return "News-Site"
	    elif(games >=15):
		return "Games-Site"
	elif (data[6]>2 or data[7]>2) and (sum(data)==10+data[6]+data[7] or sum(data)==11+data[6]):
	    for word in self.med_list:
			med+=1
	    if(med >=15):
		return "Medicines"
	else:
	    return "No-Remark"
    def find_max(self,a):
        maxi=0
        max_index=0
        for i in range(12):
            if(maxi < a[i]):
                maxi=a[i]
                max_index = i
        return max_index
    def reason(self,data):
	class_bad = ['Porn','Violence','Racism','Drugs/Medicine','Alcohol','Tobacco']
	max_ind = self.find_max(data)
	return class_bad[int(max_ind)/2]
	   
	     


