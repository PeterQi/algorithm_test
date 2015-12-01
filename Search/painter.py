import MySQLdb
def time_set(algorithm_id):
    con = 0
    cur = 0
    try:
        con = MySQLdb.connect(host = "202.118.236.205", user = "web_user", passwd = "79007295", db = "algorithm")
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
    for t in t1:
        print t