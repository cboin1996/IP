import requests
import os
import json
import time
import Message
import sys
import logging
#setup loggin for server script
pathToFolder = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('IP.py')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt='%(asctime)s %(name)s  %(levelname)-8s %(message)s',datefmt="%Y-%m-%d - %H:%M:%S")
fh = logging.FileHandler(os.path.join(pathToFolder, 'IPHistory.log'))
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
def getIp():
    try:
        req = requests.get('https://api.ipify.org').text
        return req
    except:
        logger.info("IP request failed.  Maybe wifi was down?")
        return None


def main(arguments):
    messager = Message.Messager()
    delay = float(sys.argv[1])
    lastIp = getIp()
    if lastIp != None:
        logger.info('Got IP of %s' % (lastIp))

    while True:
        logger.info('Checking for IP again in %s hours' % (sys.argv[1]))
        time.sleep(delay*3600)
        currentIp = getIp()
        # check for error on requests.. should only execute if wifi is up or requests were good.
        if lastIp != None and currentIp != None:
            if lastIp != currentIp:
                logger.info("IP change detected (%s --> %s).  Sending update text." % (lastIp, currentIp))
                messager.createSMS("Your ext. IP has changed from %s to --> %s." % (lastIp, currentIp))
            else:
                logger.info("No change in IP.. Last ext. Ip was: %s, current is: %s." % (lastIp, currentIp))
            lastIp = currentIp


if __name__=="__main__":

    main(sys.argv)
