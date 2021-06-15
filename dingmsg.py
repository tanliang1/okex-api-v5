import json
import requests



def dingmessage(msg):
    # 请求的URL，WebHook地址
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=1b70ff7a909420ad0c7497dba47fdc4071c533ca562c3ef4957cbc7de0447351"
    #构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
        }
    #构建请求数据
    key = "tanliang"
    message ={

        "msgtype": "text",
        "text": {
            "content": msg+key
        },
        "at": {

            "isAtAll": True
        }
    }
    #对请求的数据进行json封装
    message_json = json.dumps(message)
    #发送请求
    info = requests.post(url=webhook,data=message_json,headers=header)
    #打印返回的结果
    print(info.text)
    #redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='asdf456987', db=0)
    #redis_conn = redis.Redis(connection_pool=redis_pool)
    #redis_conn.set()
    #print(redis_conn.get(""))
