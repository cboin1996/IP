import requests
import os
import json
import time
import Message
    
def getIp():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        print("Could not connect to website")


def main():
    messager = Message.Messager()

    #while True:
    ip = getIp()
    messager.createSMS(ip)

if __name__=="__main__":
    
    main()
