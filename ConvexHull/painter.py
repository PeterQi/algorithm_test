import matplotlib.pyplot as plt
import MySQLdb

con = 0
cur = 0
try:
    con = MySQLdb.connect(host = "localhost", user = "algorithm_user", passwd = "123456", db = "algorithm")
    cur = con.cursor()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
query = 'SELECT * FROM `convexhull` WHERE algorithm_id = 0'
cur.execute(query)
results0 = cur.fetchall()
query = 'SELECT * FROM `convexhull` WHERE algorithm_id = 1'
cur.execute(query)
results1 = cur.fetchall()
query = 'SELECT * FROM `convexhull` WHERE algorithm_id = 2'
cur.execute(query)
results2 = cur.fetchall()

cur.close()
con.close()


x = []
y = []
for i in results0:
    x.append(i[1])
    y.append(i[2])
plt.plot(x, y)
x = []
y = []
for i in results1:
    x.append(i[1])
    y.append(i[2])
plt.plot(x, y)
plt.show()
x = []
y = []
for i in results2:
    x.append(i[1])
    y.append(i[2])
plt.plot(x, y)
plt.show()