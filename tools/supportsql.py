import MySQLdb
import random

###    I know repeating the MySQLdb.connect :(  I made it a function in the new version, didn't bother to do it here.

def CreateReport(u, r):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO dragon_reports (rid, report) VALUES ({}, '{}')".format(u, r))
    cnx.commit()
    cursor.close()
    cnx.close()

def RespondReport(u, r):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT id, rid, report, open, closed FROM dragon_reports WHERE id={}".format(r))
    rowsamount = cursor.fetchall()[0]
    TakeReport = []
    if rowsamount[3] == 1 and not rowsamount[4] == 1:
        TakeReport.append(True)
        for y in rowsamount:
            TakeReport.append(y)
        UpdateReport(u,r)
    else:
        TakeReport.append(False)
    cnx.commit()
    cursor.close()
    cnx.close()
    return TakeReport

def UpdateReport(u, r):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("UPDATE dragon_reports SET aid={}, open={} WHERE id={}".format(u, 0, r))
    cnx.commit()
    cursor.close()
    cnx.close()

def CloseReport(r):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("UPDATE dragon_reports SET closed={} WHERE id={}".format(1, r))
    cnx.commit()
    cursor.close()
    cnx.close()
