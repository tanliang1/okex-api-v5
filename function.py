import pandas
import time
from tqsdk import tafunc
from tqsdk.ta import KDJ
#获取一天的kdj
from dingmsg import dingmessage
from okex.consts import COIN_TYPE, API_KEY, SECRET_KEY, PASSPHRASE, CCY
from utils import timeStampTostr, nowTime
import okex.Trade_api as Trade
crossUpSended :bool = False
crossDownSended :bool = False
lastTimeSendMsg :int = 0
messageMap : dict = {}
upStatus :bool = True
downStatus :bool = True

def isCrossUp(kList,dList,msg_pre):
    lenth :int = len(kList)
    k_1 = float(kList[lenth - 2])
    k = float(kList[lenth - 1])
    d_1 = float(dList[lenth - 2])
    d = float(dList[lenth - 1])
    global upStatus,downStatus
    if(k_1 < d_1 and k > d) and upStatus:
        msg = msg_pre + " jincha:"
        downStatus = True
        upStatus = False
        result_1 = closeTrade('short')
        result_2 = buy()
        msg = msg + str(result_1) + str(result_2)
        print(msg)
        dingmessage(msg)

    if (k_1 > d_1 and k < d) and downStatus:
        msg = msg_pre + " sicha:"
        upStatus = True
        downStatus = False
        result_1 = closeTrade('long')
        result_2 = sell()
        msg = msg + str(result_1) + str(result_2)
        print(msg)
        dingmessage(msg)

    print("klines k(n-2):"+str(k_1)+ ' d(n-2):'+str(d_1)+ ' k(n-1):'+ str(k) + ' d(n-1):'+str(d))

def buy():
    # flag是实盘与模拟盘的切换参数 flag is the key parameter which can help you to change between demo and real trading.
    flag = '1'  # 模拟盘 demo trading
    flag = '0'  # 实盘 real trading
    # trade api
    tradeAPI = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, flag)
    # 下单  Place Order
    result = tradeAPI.place_order(instId= COIN_TYPE, tdMode='cross', side='buy',ccy=CCY,
                                   ordType='market', sz='1',posSide='long')
    print(result)
    return result

def sell():
    # flag是实盘与模拟盘的切换参数 flag is the key parameter which can help you to change between demo and real trading.
    flag = '1'  # 模拟盘 demo trading
    flag = '0'  # 实盘 real trading
    # trade api
    tradeAPI = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, flag)
    # 下单  Place Order
    result = tradeAPI.place_order(instId= COIN_TYPE, tdMode='cross', side='sell',ccy=CCY,
                                   ordType='market', sz='1',posSide='short')

    print(result)
    return result
def closeTrade(posSideStr : str):
    # flag是实盘与模拟盘的切换参数 flag is the key parameter which can help you to change between demo and real trading.
    flag = '1'  # 模拟盘 demo trading
    flag = '0'  # 实盘 real trading
    # trade api
    tradeAPI = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, flag)
    # 下单  Place Order
    result = tradeAPI.close_positions(instId = COIN_TYPE, mgnMode = 'cross', posSide = posSideStr)
    print(result)
    return result


def kdj(klines : pandas.DataFrame,code :str,period :int):
    timeInt = int(nowTime())
    print('nowTime:' + str(timeInt))

    time = timeStampTostr(timeInt)
    klines.rename(columns={ 0:'date',1:'open',2:'high',3:'low',4:'close', 5:'vol', 6:'volCcy'},inplace=True)
    kdj = KDJ(klines, 9, 3, 3)
    kList = list(kdj["k"])
    dList = list(kdj["d"])
    jList = list(kdj["j"])
    msg_pre = code + ' period' + str(period) + ' time'+ time
    isCrossUp(kList,dList,msg_pre)
    crossup = tafunc.crossup(kdj["k"], kdj["d"])
    crossDown = tafunc.crossdown(kdj["k"], kdj["d"])
    crossUpList = list(crossup)
    crossDownList = list(crossDown)

    print("crossUpList:"+str(crossUpList))
    print("crossDownList:"+str(crossDownList))

    f = open(str(code)+'.txt', 'a')
    try:
        global lastTimeSendMsg
        #timeInt = klines['date'][len(klines) - 1]

        print('time:' + str(time))

        if crossUpList[len(crossUpList) - 1] == 1:
            msg = code +'  period:'+str(period)+" time:" + str(time) + "  kdj jincha\n"
            global crossUpSended
            if(int(timeInt) - lastTimeSendMsg > period*1000*60):
               crossUpSended = False
            if(crossUpSended == False):
                print(msg)
                dingmessage(msg)
                f.write(msg)
                crossUpSended = True
                lastTimeSendMsg = int(timeInt)
        if crossDownList[len(crossDownList) - 1] == 1:
            msg = code +'  period:'+str(period)+"  time:" + str(time) + "  kdj sicha\n"
            global crossDownSended
            if (int(timeInt) - lastTimeSendMsg > period*1000*60):
                crossDownSended = False
            if (crossDownSended == False):
                print(msg)
                dingmessage(msg)
                f.write(msg)
                f.close()
                crossDownSended = True
                lastTimeSendMsg = int(timeInt)
    except IndexError as ie:
        print(ie)