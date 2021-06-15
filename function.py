import pandas
from tqsdk import tafunc
from tqsdk.ta import KDJ
#获取一天的kdj
def kdj(klines : pandas.DataFrame):
    klines.rename(columns={ 0:'date',1:'open',2:'high',3:'low',4:'close', 5:'vol', 6:'volCcy'},inplace=True)
    print("klines:"+str(klines))

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