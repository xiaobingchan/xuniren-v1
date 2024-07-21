# coding: utf-8
import SparkApi
import time
#以下密钥信息从控制台获取   https://console.xfyun.cn/services/bm35
appid = "da15ae5e"     #填写控制台中获取的 APPID 信息
api_secret = "Mzg4MDBmYzZjMWY1YjE1ODIwOTI4YzRj"   #填写控制台中获取的 APISecret 信息
api_key ="96e4dfe7579d46b8cf09c993499c6883"    #填写控制台中获取的 APIKey 信息

#domain = "4.0Ultra" 
domain = "generalv3.5"      # Max版本
#domain = "generalv3"       # Pro版本
#domain = "general"         # Lite版本

#Spark_url = "wss://spark-api.xf-yun.com/v4.0/chat" # ultra服务地址
Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"   # Max服务地址
#Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"  # Pro服务地址
#Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite服务地址

#初始上下文内容，当前可传system、user、assistant 等角色
text =[
    {"role": "system", "content": "你现在扮演李白，你豪情万丈，狂放不羁；接下来请用李白的口吻和用户对话。"} , # 设置对话背景或者模型角色
    {"role": "user", "content": "你是谁"},  # 用户的历史问题
    {"role": "assistant", "content": "....."} , # AI的历史回答结果
    {"role": "user", "content": "你会做什么"}  # 最新的一条问题，如无需上下文，可只传最新一条问题
]

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

def Spark():
    while(1):
        Input = input("\n" +"我:")
        question = checklen(getText("user",Input))
        SparkApi.answer =""
        #print("星火:",end ="")
        SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
        # print(SparkApi.answer)
        #getText("assistant",SparkApi.answer)

def SparkOne():    
    Input = input("\n" +"我:")
    question = checklen(getText("user",Input))
    SparkApi.answer =""
    #print("星火:",end ="")
    SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    # print(SparkApi.answer)
    #getText("assistant",SparkApi.answer)

if __name__ == '__main__':

    while(1):
        Input = input("\n" +"我:")
        question = checklen(getText("user",Input))
        SparkApi.answer =""
        #SSSprint("星火:",end ="")
        SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
        print(SparkApi.answer)
        #getText("assistant",SparkApi.answer)
