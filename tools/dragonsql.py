import MySQLdb
import random

###    I know repeating the MySQLdb.connect :(  I made it a function in the new version, didn't bother to do it here.

def WelcomeChannelSet(s):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT welcomechannel FROM dragon_servers WHERE sid={}".format(s))
    rows = cursor.fetchall()[0]
    welcomeChannel = rows[0]
    cnx.commit()
    cursor.close()
    cnx.close()

    if str(welcomeChannel) == "0":
        return False
    else:
        return True

def GetWelcomeChannel(s):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT welcomechannel FROM dragon_servers WHERE sid={}".format(s))
    rows = cursor.fetchall()[0]
    welcomeChannel = rows[0]
    cnx.commit()
    cursor.close()
    cnx.close()

    return welcomeChannel

def SetWelcomeChannel(s,c):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("UPDATE dragon_servers set welcomechannel={} WHERE sid={}".format(c, s))
    cnx.commit()
    cursor.close()
    cnx.close()

def CheckUserExist(u, s):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT id FROM dragon_bank WHERE uid={} AND sid={}".format(u, s))
    rowsamount = cursor.rowcount
    if rowsamount == 0:
        UserExists = False
    else:
        UserExists = True
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserExists

def GetRank(u):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT rank FROM dragon_vip WHERE uid={}".format(u))
    rowsamount = cursor.rowcount
    if rowsamount == 0:
        UserExists = "not"
    else:
        rowsamount = cursor.fetchall()[0]
        UserExists = rowsamount[0]
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserExists

def AddRank(u, r):
    if GetRank(u) == "not":
        cnx = MySQLdb.connect(host='', user='', passwd='', db='')
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO dragon_vip (uid, rank) VALUES ({}, {})".format(u, r))
        cnx.commit()
        cursor.close()
        cnx.close()
    else:
        cnx = MySQLdb.connect(host='', user='', passwd='', db='')
        cursor = cnx.cursor()
        cursor.execute("UPDATE dragon_vip set rank={} WHERE uid={}".format(r, u))
        cnx.commit()
        cursor.close()
        cnx.close()

def RemoveRank(u):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("UPDATE dragon_vip SET rank=0 WHERE uid={}".format(u))
    cnx.commit()
    cursor.close()
    cnx.close()

def DragonBan(u, r):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO dragon_bans (uid, reason) VALUES ({}, '{}')".format(u, r))
    cnx.commit()
    cursor.close()
    cnx.close()

def DragonUnBan(u):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM dragon_bans WHERE uid={}".format(u))
    cnx.commit()
    cursor.close()
    cnx.close()

def CheckVip(u):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT id FROM dragon_vip WHERE uid={}".format(u))
    rowsamount = cursor.rowcount
    if rowsamount == 0:
        UserExists = False
    else:
        UserExists = True
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserExists

def CheckBoosters(u):
    if CheckVip(u):
        cnx = MySQLdb.connect(host='', user='', passwd='', db='')
        cursor = cnx.cursor()
        cursor.execute("SELECT rank FROM dragon_vip WHERE uid={}".format(u))
        rows = cursor.fetchall()
        rows = rows[0]
        rows = rows[0]
        cnx.commit()
        cursor.close()
        cnx.close()
    else:
        rows = 0
    return rows

def CheckBan(u):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT id FROM dragon_bans WHERE uid={}".format(u))
    rowsamount = cursor.rowcount
    if rowsamount == 0:
        UserExists = False
    else:
        UserExists = True
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserExists

def BanList():
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT uid, reason FROM dragon_bans")
    rows = cursor.fetchall()
    cnx.commit()
    cursor.close()
    cnx.close()
    return rows

def GetDataRows():
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM dragon_bank")
    rowsamount = cursor.rowcount
    cnx.commit()
    cursor.close()
    cnx.close()
    return rowsamount

def GetSQLInfo():
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT dragon_bank.id, dragon_bans.id, dragon_crews.cid, dragon_crew_members.mid, dragon_vip.id FROM dragon_bank, dragon_bans, dragon_vip, dragon_crews, dragon_crew_members")
    rowsamount = cursor.rowcount
    cnx.commit()
    cursor.close()
    cnx.close()
    return rowsamount

def Mug(u, s):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT cash FROM dragon_bank WHERE uid={} AND sid={}".format(u, s))
    rowsamount = cursor.rowcount
    if rowsamount == 0:
        cash = random.randint(100, 5000)
    else:
        rows = cursor.fetchall()[0]
        if rows[0] > 0:
            cash = rows[0]
            cash = int(cash * 0.1)
            ChangeMoney(u, s, -cash, "cash")
        else:
            cash = 0
    cnx.commit()
    cursor.close()
    cnx.close()
    return cash

def Hack(u, s):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT bank FROM dragon_bank WHERE uid={} AND sid={}".format(u, s))
    rowsamount = cursor.rowcount
    if rowsamount == 0:
        cash = random.randint(100, 5000)
    else:
        rows = cursor.fetchall()[0]
        if rows[0] > 0:
            cash = rows[0]
            cash = int(cash * 0.05)
            ChangeMoney(u, s, -cash, "bank")
        else:
            cash = 0
    cnx.commit()
    cursor.close()
    cnx.close()
    return cash

def BankLeaderboard(s):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT uid, (cash + bank) as 'LeaderB' FROM dragon_bank WHERE sid={} ORDER BY LeaderB DESC".format(s))
    rows = cursor.fetchall()
    cnx.commit()
    cursor.close()
    cnx.close()
    return rows

def NewBankUser(u, s):
    if not CheckUserExist(u, s):
        cnx = MySQLdb.connect(host='', user='', passwd='', db='')
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO dragon_bank (uid, sid) VALUES ({}, {})".format(u, s))
        NewCreation = True
        cnx.commit()
        cursor.close()
        cnx.close()
    else:
        NewCreation = False
    return NewCreation

def JoinCrew(c, u):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO dragon_crew_members (uid, cid) VALUES ({}, {})".format(u, c))
    cnx.commit()
    cursor.close()
    cnx.close()

def GetBalance(u, s):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT cash, bank, total FROM dragon_bank WHERE uid={} AND sid={}".format(u, s))
    UserMoney = cursor.fetchall()[0]
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserMoney

def GetVault(c):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT vault FROM dragon_crews WHERE cid={}".format(c))
    UserMoney = cursor.fetchall()[0]
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserMoney

def GetCrew(u):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT cid, cname, vault FROM dragon_crews WHERE uid={}".format(u))
    UserMoney = cursor.fetchall()[0]
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserMoney

def GetMemCrew(u, s):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT cid, uid, rid FROM dragon_crew_members WHERE uid={} AND sid={}".format(u, s))
    UserMoney = cursor.fetchall()[0]
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserMoney

def GetCrewInfo(c):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT dragon_crew_members.uid, dragon_crews.cname, dragon_crews.uid, dragon_crews.vault FROM dragon_crew_members, dragon_crews WHERE dragon_crew_members.cid={} AND dragon_crews.cid={}".format(c, c))
    UserMoney = cursor.fetchall()
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserMoney

def GetPimps(u, s):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT pimp FROM dragon_bank WHERE uid={} AND sid={}".format(u, s))
    UserMoney = cursor.fetchall()[0]
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserMoney

def ChangePimped(u, s, a):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    PrevM = GetPimps(u, s)[0]
    a = PrevM + a
    cursor = cnx.cursor()
    cursor.execute("UPDATE dragon_bank SET pimp={} WHERE uid={} AND sid={}".format(a, u, s))
    cnx.commit()
    cursor.close()
    cnx.close()

def CheckCrewExist(s, n):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT cid FROM dragon_crews WHERE cname='{}' AND sid={}".format(n, s))
    rowsamount = cursor.rowcount
    if rowsamount == 0:
        UserExists = False
    else:
        UserExists = True
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserExists

def CheckCOwner(u, s):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT cid FROM dragon_crews WHERE uid={} AND sid={}".format(u, s))
    rowsamount = cursor.rowcount
    if rowsamount == 0:
        UserExists = False
    else:
        UserExists = True
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserExists

def ChangeCrewVault(u, c, m):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    PrevM = GetVault(c)[0]
    m = PrevM + m
    cursor = cnx.cursor()
    cursor.execute("UPDATE dragon_crews SET vault={} WHERE cid={}".format(m, c))
    cnx.commit()
    cursor.close()
    cnx.close()

def CheckUserInCrew(u):
    cnx = MySQLdb.connect(host='', user='', passwd='', db='')
    cursor = cnx.cursor()
    cursor.execute("SELECT cid FROM dragon_crew_members WHERE uid={}".format(u))
    rowsamount = cursor.rowcount
    if rowsamount == 0:
        UserExists = False
    else:
        UserExists = True
    cnx.commit()
    cursor.close()
    cnx.close()
    return UserExists

def CreateCrew(u, s, n):
    if not CheckCrewExist(s, n):
        cnx = MySQLdb.connect(host='', user='', passwd='', db='')
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO dragon_crews (cname, uid, sid) VALUES ('{}', {}, {})".format(n, u, s))
        NewCreation = True
        CrewID = cursor.lastrowid
        JoinCrew(CrewID, u)
        cnx.commit()
        cursor.close()
        cnx.close()
    else:
        NewCreation = False
    return NewCreation

def ChangeMoney(u, s, m, t):
    if t == "bank":
        cnx = MySQLdb.connect(host='', user='', passwd='', db='')
        PrevM = GetBalance(u, s)[1]
        m = PrevM + m
        cursor = cnx.cursor()
        cursor.execute("UPDATE dragon_bank SET bank={} WHERE uid={} AND sid={}".format(m, u, s))
        cnx.commit()
        cursor.close()
        cnx.close()
    elif t == "cash":
        cnx = MySQLdb.connect(host='', user='', passwd='', db='')
        PrevM = GetBalance(u, s)[0]
        m = PrevM + m
        cursor = cnx.cursor()
        cursor.execute("UPDATE dragon_bank SET cash={} WHERE uid={} AND sid={}".format(m, u, s))
        cnx.commit()
        cursor.close()
        cnx.close()
    elif t == "total":
        cnx = MySQLdb.connect(host='', user='', passwd='', db='')
        PrevM = GetBalance(u, s)[2]
        m = PrevM + m
        cursor = cnx.cursor()
        cursor.execute("UPDATE dragon_bank SET total={} WHERE uid={} AND sid={}".format(m, u, s))
        cnx.commit()
        cursor.close()
        cnx.close()
