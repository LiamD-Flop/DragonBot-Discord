import MySQLdb
import random

###    I know repeating the MySQLdb.connect :(  I made it a function in the new version, didn't bother to do it here.


def NewServer(s, u, n):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO dragon_servers (sid, uid, name) VALUES ({}, {}, '{}')".format(s, u, n))
    cnx.commit()
    cursor.close()
    cnx.close()

def InServer(s):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT id FROM dragon_servers WHERE sid={}".format(s))
    rowsamount = cursor.rowcount
    if rowsamount == 0:
        ServerExists = False
    else:
        ServerExists = True
    cnx.commit()
    cursor.close()
    cnx.close()
    return ServerExists
