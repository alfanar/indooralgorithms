import blescan
import sys
import socket
import bluetooth._bluetooth as bluez

# this function count number of bytes in a string
def utf8len(s):
    return len(s.encode('utf-8'))
# this function serach for elemnt in list and return the indices where this element exists
def all_indices(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices

#initial values
dev_id = 0
major_minor = []
indeicies = []
proximity_number = 3
sticker_number = 8
nl = []
finallist = []
count = 0

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
     
print 'Socket Created'
 
host = '192.168.1.108';
port = 5001;
replay_array = []
try:
    remote_ip = socket.gethostbyname( host )

 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
 
#Connect to remote server
s.connect((remote_ip , port))
 
print 'Socket Connected to ' + host + ' on ip ' + remote_ip
 
#Send some data to remote server
message = "send packet"
 
try :
    #Set the whole string
    s.sendall(message)
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()
 
print 'Message send successfully'

#now keep talking to the server

while True:
    returnedList = blescan.parse_events(sock,20)
    # concatenate major with minor
    for x in returnedList:
        k = returnedList[count][76:79] + returnedList[count][87]
        major_minor.append(k)
        count = count + 1
    count = 0
    #print(major_minor)
    
    for proximity in range (1 , proximity_number + 1):
        x1 = all_indices(str(150) + str(proximity), major_minor)
       # this if to return the max index where the duplicated packet exists 
        if len(x1):
           m1 = max (x1)
           indeicies.append(m1)
           
    for sticker in range (1 , sticker_number + 1):
        x2 = all_indices(str(151) + str(sticker), major_minor)
      # this if to return the max index where the duplicated packet exists 
        if len(x2):
           m2 = max (x2)
           indeicies.append(m2)
    #print (indeicies)
    # order the indeicies from smallest to largest
    for i in range(len(indeicies)):
        a = min(indeicies)
        nl.append(a)
        indeicies.remove(a)
    #print( nl)
    for n in range (0, len(nl)):
    # finallist is the list after removing duplicated packets 
        finallist.append(returnedList[n])
    # we append concatenate with end to know the end of each reding 
    finallist.append('end')
    #num_byte = utf8len(returnedList) + 8
    #returnedList.append(str(num_byte))
    #data_string = pickle.dumps(returnedList) # this line enable me to send the list as it is without sperating it to bytes
    makestring = ''.join(map(str, finallist))
    conn.sendall(makestring)
    for beacon in finallist:
        print (beacon)
    print('---------------------')

    major_minor = []
    nl = []
    indeicies = []
    finallist =[]
s.close()
