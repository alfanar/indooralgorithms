import MySQLdb

db = MySQLdb.connect(
    host = 'localhost',
    user = 'root',
    passwd = '1234',
    db = 'Beacons')
major_minor = []
coordinates = []
points = []
scanner = ['1501', '1513', '1512', '1503', '1514', '1502']
cursor = db.cursor()
cursor.execute('SELECT * FROM
               +data')
result = cursor.fetchall()

if result:
    for z in result :
        major_minor.append(z[1])
        coordinates.append(z[2])
    #print major_minor
    #print coordinates

for x in  scanner:
    ind = major_minor.index(x)
    point = coordinates[ind]
    points.append(point)
print(points)
