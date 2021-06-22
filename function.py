import pandas
import time
from tqsdk import tafunc
from tqsdk.ta import KDJ
#获取一天的kdj
from dingmsg import dingmessage
from okex.Key_Consts import API_KEY, SECRET_KEY, PASSPHRASE
from okex.consts import COIN_TYPE, CCY, PERROD
from utils import timeStampTostr, nowTime
import okex.Trade_api as Trade
crossUpSended :bool = False
crossDownSended :bool = False
lastTimeSendMsg :int = 0
messageMap : dict = {}
upStatus :bool = True
downStatus :bool = True

import time
from tqsdk import tafunc
from tqsdk.ta import KDJ
#获取一天的kdj
from dingmsg import dingmessage
from okex.consts import COIN_TYPE , CCY
from utils import timeStampTostr, nowTime
import okex.Trade_api as Trade
crossUpSended :bool = False
crossDownSended :bool = False
lastTimeSendMsg :int = 0
messageMap : dict = {}
upStatus :bool = True
downStatus :bool = True
last_k :float = 0
last_d :float = 0
def isCrossUp(kList,dList,msg_pre):
    lenth :int = len(kList)
    k = float(kList[lenth - 1])
    k_1 = float(kList[lenth - 2])
    last_k = k
    d = float(dList[lenth - 1])
    d_1 = float(dList[lenth - 2])
    timeInt = int(nowTime())
    print('nowTime:' + str(timeInt))
    global lastTimeSendMsg
    global upStatus,downStatus
    # #状态校验，防止一个周期内
    msg_3 = ''
    if timeInt - lastTimeSendMsg > PERROD*60:
        #一个周期之后，上周期发生了向上金叉，但是中间又发生向下死叉，d仍然大于k.需要将状态纠正过来，认为是突破状态，金叉状态
        if (k_1 < d_1 and k < d) and downStatus:
            msg_3 = 'reverse to upstatuse ,go to jincha:'
            upStatus = True
            downStatus = False
            handleCropssDown(msg_pre,timeInt,msg_3)
         #   一个周期之后，上周期发生了，向下死叉，但是中间又发生向向上金叉，d仍然小于k.需将状态反转，并执行反向操作。
        if (k_1 > d_1 and k > d) and upStatus:
            msg_3 = 'reverse to upstatuse ,go to jincha:'
            upStatus = False
            downStatus = True
            handleCrossUp(msg_pre, timeInt, msg_3)
    #金叉
    if(k_1 < d_1 and k > d) and upStatus:
        downStatus = True
        upStatus = False
        handleCrossUp(msg_pre,timeInt,msg_3)
        # msg = msg_pre + " jincha:"
        # result_1 = closeTrade('short')
        # result_2 = buy()
        # msg = msg + str(result_1) + str(result_2)
        # print(msg)
        # dingmessage(msg)
        # lastTimeSendMsg = int(timeInt)
    #死叉
    if (k_1 > d_1 and k < d) and downStatus:
        upStatus = True
        downStatus = False
        handleCropssDown(msg_pre,timeInt,msg_3)
        # msg = msg_pre + " sicha:"
        # result_1 = closeTrade('long')
        # result_2 = sell()
        # msg = msg + str(result_1) + str(result_2)
        # print(msg)
        # dingmessage(msg)
        # lastTimeSendMsg = int(timeInt)

    print("klines k(n-2):"+str(k_1)+ ' d(n-2):'+str(d_1)+ ' k(n-1):'+ str(k) + ' d(n-1):'+str(d))
def handleCrossUp(msg_pre,timeInt,msg_3):
    msg = msg_pre + " jincha:"
    result_1 = closeTrade('short')
    result_2 = buy()
    msg = msg + str(result_1) + str(result_2)+str(msg_3)
    print(msg)
    dingmessage(msg)
    global lastTimeSendMsg
    lastTimeSendMsg = int(timeInt)
def handleCropssDown(msg_pre,timeInt,msg_3):
    msg = msg_pre + " sicha:"
    result_1 = closeTrade('long')
    result_2 = sell()
    msg = msg + str(result_1) + str(result_2)+str(msg_3)
    print(msg)
    dingmessage(msg)
    global lastTimeSendMsg
    lastTimeSendMsg = int(timeInt)
def buy():
    # flag是实盘与模拟盘的切换参数 flag is the key parameter which can help you to change between demo and real trading.
    flag = '1'  # 模拟盘 demo trading
    flag = '0'  # 实盘 real trading
    # trade api
    tradeAPI = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, flag)
    # 下单  Place Order
    print('buy request_time:'+nowTimStr())

    result = tradeAPI.place_order(instId= COIN_TYPE, tdMode='cross', side='buy',ccy=CCY,
                                   ordType='market', sz='200',posSide='long')
    print('buy success:'+nowTimStr())

    print(result)
    return result

def sell():
    # flag是实盘与模拟盘的切换参数 flag is the key parameter which can help you to change between demo and real trading.
    flag = '1'  # 模拟盘 demo trading
    flag = '0'  # 实盘 real trading
    # trade api
    print('sell request_time:'+nowTimStr())

    tradeAPI = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, flag)
    # 下单  Place Order
    result = tradeAPI.place_order(instId= COIN_TYPE, tdMode='cross', side='sell',ccy=CCY,
                                   ordType='market', sz='200',posSide='short')
    print('sell success:'+nowTimStr())

    print(result)
    return result
def closeTrade(posSideStr : str):
    # flag是实盘与模拟盘的切换参数 flag is the key parameter which can help you to change between demo and real trading.
    flag = '1'  # 模拟盘 demo trading
    flag = '0'  # 实盘 real trading
    # trade api
    tradeAPI = Trade.TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, flag)
    # 下单  Place Order
    print('closeTrade request_time:'+nowTimStr())

    result = tradeAPI.close_positions(instId = COIN_TYPE, mgnMode = 'cross', posSide = posSideStr)
    print('closeTrade success:'+nowTimStr())

    print(result)
    return result
def nowTimStr():
    timeInt = int(nowTime())
    print('nowTime:' + str(timeInt))
    time = timeStampTostr(timeInt)
    return time

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

    return

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