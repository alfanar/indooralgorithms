import math
import numpy


position_a = (-2.45,1.0) # first beacon position
position_b = (-4.31,1.25) # second beacon position
position_c = (-2.71,-0.75) # third beacon position
RSSI_a = -69 # RSSI of the first beacon
RSSI_b = -65 # RSSI of the second beacon
RSSI_c = -70 # RSSI of the third beacon
A1 = -68 # measured power of the first beacon
A2 = -68 # measured power of the second beacon
A3 = -68 # measured power of the third beacon


def distance_to_RSSI(RSSI,txpower) :
    if (RSSI == 0):
        return (-1.0)
    ratio =((RSSI*1.0)/txpower)
    if (ratio < 1.0):
        return (ratio**10)
    else :
        distance = ((0.89976)* (ratio**7.7095) + 0.111)
        return (distance)

d1 = distance_to_RSSI(RSSI_a,A1) # distance of the first beacon
d2 = distance_to_RSSI(RSSI_b,A2) # distance of the second beacon
d3 = distance_to_RSSI(RSSI_c,A3) # distance of the third beacon

def gettrileteration (position_a,position_b,position_c,d1,d2,d3):
    xa = position_a[0]
    ya = position_a[1]
    xb = position_b[0]
    yb = position_b[1]
    xc = position_c[0]
    yc = position_c[1]
    
    S = (pow(xc,2) - pow(xb,2) + pow(yc,2) - pow(yb,2) + pow(d2,2) - pow(d3,2)) / 2.0
    T = (pow(xa,2) - pow(xb,2) + pow(ya,2) - pow(yb,2) + pow(d2,2) - pow(d1,2)) / 2.0
    y = ((T * (xb - xc)) - (S *(xb - xa))) / (((ya - yb) *(xb - xc)) - ((yc - yb) * (xb - xa)))
    x = ((y * (ya - yb)) - T) / (xb - xa)
    return (x , y)

current_position = gettrileteration (position_a,position_b,position_c,d1,d2,d3)
print (current_position)
