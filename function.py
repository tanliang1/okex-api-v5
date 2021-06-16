import pandas
from tqsdk import tafunc
from tqsdk.ta import KDJ
#获取一天的kdj
from dingmsg import dingmessage
from utils import timeStampTostr

crossUpSended :bool = False
crossDownSended :bool = False
lastTimeSendMsg :int = 0

messageMap : dict = {}
def kdj(klines : pandas.DataFrame,code :str,period :int):
    klines.rename(columns={ 0:'date',1:'open',2:'high',3:'low',4:'close', 5:'vol', 6:'volCcy'},inplace=True)
    kdj = KDJ(klines, 9, 3, 3)
    kList = list(kdj["k"])
    dList = list(kdj["d"])
    jList = list(kdj["j"])
    crossup = tafunc.crossup(kdj["k"], kdj["d"])
    crossDown = tafunc.crossdown(kdj["k"], kdj["d"])
    crossUpList = list(crossup)
    crossDownList = list(crossDown)
    print("crossup:"+str(crossUpList))
    print("crossDo:"+str(crossDownList))
    print("klines len:"+str(len(klines)))
    f = open(str(code), 'a')
    try:
        global lastTimeSendMsg
        timeInt = klines['date'][len(klines) - 1]
        print('timeInt:' + str(timeInt))
        if crossUpList[len(crossUpList) - 1] == 1:
            time = timeStampTostr(timeInt/1000)
            msg = code +" time:" + str(time) + "  kdj金叉\n"
            global crossUpSended
            if(timeInt - lastTimeSendMsg > 1000*60):
               crossUpSended = False
            if(crossUpSended == False):
                print(msg)
                dingmessage(msg)
                f.write(msg)
                crossUpSended = True
                lastTimeSendMsg = timeInt
        if crossDownList[len(crossDownList) - 1] == 1:
            time = timeStampTostr(timeInt)
            msg = code +" time:" + str(time) + "  kdj死叉\n"
            global crossDownSended
            if (timeInt - lastTimeSendMsg > 1000 * 60):
                crossUpSended = False
            if (crossDownSended == False):
                print(msg)
                dingmessage(msg)
                f.write(msg)
                f.close()
                crossDownSended = True
                lastTimeSendMsg = timeInt
    except IndexError as ie:
        print(ie)