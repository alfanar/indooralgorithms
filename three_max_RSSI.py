
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

def index_of_Three_max_RSSI (x):
    final = []
    three_max = []
    max_rssi_id = []
    index = []
    # make a copy x in l
    l = list(x) 
    for i in range(len(l)):
        a = max(l)
        final.append(a)
        l.remove(a)
    #print (final)
    for i in range (0,3):
        three_max.append(final[i])
    three_max = list(set(three_max)) # remove duplication
    #print(three_max)
    
    for n in three_max:
        index = index + all_indices(n,x)
    if len(index) >= 3:
       for i in range (0,3):
           max_rssi_id.append(index[i])
           
    return(max_rssi_id)

