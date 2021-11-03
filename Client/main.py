from os import pardir
import socket
import cv2
import time
from winreg import REG_EXPAND_SZ
import json
import numpy as np

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9090
MAX_FILE_SIZE = 409600

def getListProcess(s):
    listProcess = []
    s.sendall(b'process running')
    while True:
        data = s.recv(4096) 
        data = data.decode('utf8')
        if data == 'done':
            break
        listProcess.append(data)
    return listProcess

def killProcess(s, processId):
    s.sendall(b'kill process')
    while True:
        data = s.recv(1024)
        if data.decode('utf8') == 'Received request kill process':
            s.sendall(bytes(str(processId), 'utf8'))
            break

def getListApplication(s):
    s.sendall(b'application running')
    ret = []
    while True:
        data = s.recv(4096)
        data = data.decode('utf8')
        if data == 'done':
            break
        ret.append(data)    
    return ret

def startApplication(s, appName):
    s.sendall(b'start application')
    while True:
        data = s.recv(1024)
        if data.decode('utf8') == 'application name':
            break
    s.sendall(bytes(appName, 'utf8'))
    code = s.recv(1024)
    return code
    pass

def startKeyHook(s):
    s.sendall(b'start key hook')
    data = s.recv(1024)
    return data.decode('utf8')

def stopKeyHook(s):
    s.sendall(b'stop key hook')
    data = s.recv(1024)
    return data.decode('utf8')

def getRecordedString(s):
    s.sendall(b'get recorded string')
    data = s.recv(4096)
    return data.decode('utf8')

def sendFile(s, path):
    file = open(path)
    fileData = file.read()
    s.sendall(b'send file')
    while True:
        respone = s.recv(1024)
        if respone.decode('utf8') == 'ready to recvive':
            break
    s.sendall(bytes(fileData, 'utf8'))
    while True:
        respone = s.recv(1024)
        if respone:
            return respone.decode('utf8')

def regGetValue(s, keyPath, valueName):
    s.sendall(b'reg get value')
    time.sleep(0.1)
    s.sendall(bytes(keyPath, 'utf8'))
    time.sleep(0.1)
    s.sendall(bytes(valueName, 'utf8'))
    respone = s.recv(1024)
    return respone.decode('utf8')

def regSetValue(s, keyPath, valueName, regData, dataType):
    s.sendall(b'reg set value')
    time.sleep(0.1)
    s.sendall(bytes(keyPath, 'utf8'))
    time.sleep(0.1)
    s.sendall(bytes(regData, 'utf8'))
    time.sleep(0.1)
    s.sendall(bytes(valueName, 'utf8'))
    time.sleep(0.1)
    s.sendall(bytes(dataType, 'utf8'))
    respone = s.recv(1024)
    return respone.decode('utf8')

def regDeleteValue(s, keyPath, valueName):
    s.sendall(b'reg delete value')
    time.sleep(0.1)
    s.sendall(bytes(keyPath, 'utf8'))
    time.sleep(0.1)
    s.sendall(bytes(valueName, 'utf8'))
    respone = s.recv(1024)
    return respone.decode('utf8')

def regCreateKey(s, keyPath):
    s.sendall(b'reg create key')
    time.sleep(0.1)
    s.sendall(bytes(keyPath, 'utf8'))
    respone = s.recv(1024)
    return respone.decode('utf8')

def regDeleteKey(s, keyPath):
    s.sendall(b'reg delete key')
    time.sleep(0.1)
    s.sendall(bytes(keyPath, 'utf8'))
    respone = s.recv(1024)
    return respone.decode('utf8')

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, int(SERVER_PORT)))
        respone = s.recv(10 * 1024)
        buff = np.fromstring(respone, np.uint8)
        buff = buff.reshape(1, -1)
        img = cv2.imdecode(buff, cv2.IMREAD_COLOR)
        cv2.imshow('', img)
        cv2.waitKey(0)
    #    temp = []
    #    temp.append(("123123", "23123", 31231))
    #    temp.append(("2312", "23123", 31231))
    #    temp.append(("1erwerwer", "23123", 31231))
    #    temp.append(("eqwewqe", "23123", 31231))
    #    temp = json.dumps(temp).encode()
    #    s.sendall(temp)