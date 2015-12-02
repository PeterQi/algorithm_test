import matplotlib.pyplot as plt
import MySQLdb
def time_set(algorithm_id):
    con = 0
    cur = 0
    try:
        con = MySQLdb.connect(host = "localhost", user = "algorithm_user", passwd = "123456", db = "algorithm")
        cur = con.cursor()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    query = 'SELECT num, avg(time) FROM `search` WHERE algorithm_id = "'+algorithm_id+'" group by num order by num'
    cur.execute(query)
    results = cur.fetchall()
    
    cur.close()
    con.close()
    return results

if __name__ == "__main__":
    id = "branch_cut"
    t1 = time_set(id)
    #tBFS = time_set("BFS")
    #tDFS = time_set("DFS")
    #tsBFS = time_set("sBFS")
    #tsDFS = time_set("sDFS")
    
    x = []
    y = []
    for i in t1:
        x.append(i[0])
        y.append(i[1])
    plt.title("performance")
    plt.plot(x, y)
    plt.ylabel("time(s)")
    plt.xlabel("points number")
    
    #x = []
    #y = []
    #for i in tDFS:
    #    x.append(i[0])
    #    y.append(i[1])
    ##plt.plot(x, y)    
    #
    #x = []
    #y = []
    #for i in tsBFS:
    #    x.append(i[0])
    #    y.append(i[1])
    #plt.plot(x, y)
    #
    #x = []
    #y = []
    #for i in tsDFS:
    #    x.append(i[0])
    #    y.append(i[1])
    #plt.plot(x, y)
    
    plt.show()