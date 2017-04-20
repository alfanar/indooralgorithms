#main server
 
import socket   #for sockets
import sys  #for exit
import three_max_RSSI
#size_string = ""
reply = ""
#this function search for element in list and return the indices where this element exists
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


#this function to calculate bytes number in a string
def utf8len(s):
    return len(s.encode('utf-8'))


major_minor2 = []
RSSI_arr = []
A_arr = []
max_ind = []
RSSI_INT2 = []
A_INT2 = []
count = 0
#proximity_number = 3
#sticker_number = 8
three_beacons_RSSI = []
three_beacons_A = []
three_beacons_major = []


# sending data through socketio from server (laptop) to client (scanner)
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5001 # Arbitrary non-privileged port
makestring = "" 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
s.listen(10)
print 'Socket now listening'


try:
    sock = bluez.hci_open_dev(dev_id)
    print "ble thread started"

except:
    print "error accessing bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

#wait to accept a connection - blocking call
conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])
data = conn.recv(1024)
print (data)

while True: 
      #Now receive data
      #reply = s.request.recv()
      size = 0
      buffer_size = 8000
      reply = s.recv(buffer_size)
      #size_string = reply.rsplit("end", 1)[1]
      #size = int(size_string)
      reply2 = reply.rsplit("end", 1)[0]
##      while True:
##          if size >= buffer_size:
##             reply2 = reply2 + s.recv(buffer_size)
##             size = sys.getsizeof(reply2)
##          else:
##              break
      finallist = reply2.split('$')


 # to get the RSSI and A in seperate array
      for x in finallist:
          k3 = finallist[count][92:95] 
          l = finallist[count][102:105]
          RSSI_arr.append(k3)
          A_arr.append(l)
          count = count + 1
      count = 0
      print("RSSI_ARRAY = " + str(RSSI_arr))
      print("A_ARRAY = " + str(A_arr))
 # convert RSSi_arr $ A_arr to array of int
      RSSI_INT2 = map(int, RSSI_arr)
      A_INT2 = map(int, A_arr)
 # concatenaate major and minor to search in the data base

      for j in finallist:
          k2 = finallist[count][76:79] + finallist[count][87]
          major_minor2.append(k2)
          count = count + 1
      count = 0
      print(major_minor2)

      if len(finallist) >= 3:
        # get the three max beacons RSSI:
         max_indecies = index_of_Three_max_RSSI(RSSI_INT2)
         for z in max_indecies :
             three_beacons_RSSI.append(RSSI_INT2[z])
             three_beacons_A.append( A_INT2[z])
             three_beacons_major.append(major_minor2[z])
      
      for beacon in finallist:
          print (beacon)
      #print(reply)
      print('-----------------------------')

      major_minor2 = []
      RSSI_arr = []
      A_arr = []
      three_beacons_RSSI = []
      three_beacons_A = []
      three_beacons_major = []


conn.close()
s.close()
