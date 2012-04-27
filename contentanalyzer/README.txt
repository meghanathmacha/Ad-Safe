1) Install the package "Chisafe" using "sudo python setup.py install" or sudo easy_install Chisafe-0.0.0-py2.6.egg.
2) Make a json file of the urls you need to parse the jsonfile should be in the format {"url":"id_url"}.
3) Run beanstalkd -l <host> -p <port1> , beanstalkd -l <host> -p <port2> 
4) Start parsing by  
>>>import chisafe
>>>chisafe.queue(<json file name>,<host>,<port1>,<port2>) 
4) Results of the parsed urls are stored in "Chisafe.csv" and "Chisafe.json" in appropriate formats. 
5) There are clearer instructions in the respective programs if you wish to go through.
6)The score of the urls are in the order "porn text,porn links,violence text ,violence links,racism text,racism links,drugs text,drugs links,alcohol text,alcohol links,tobacco text,tobacco links" 
