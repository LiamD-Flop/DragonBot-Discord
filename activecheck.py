import os

def check_pid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return True
    else:
        return False


while True:
    pid = open("/home/dbot/dragon/activecheck.txt", "r")
    pidid = pid.read()
    pid.close()
    if check_pid(int(pidid)):
        os.system("python3 /home/dbot/dragon/bot.py")
