
import time

def timeStampTostr(timeStamp):
    time_local = time.localtime(timeStamp)
    timeLocal = time.strftime('%Y-%m-%d %H:%M:%S', time_local)
    return timeLocal


def nowTime():
    return time.time()