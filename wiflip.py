'''
Created on 23 mars 2022

@author: garzol
'''

import os, sys, time
sys.path += ['.']


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtNetwork 
from PyQt5 import QtMultimedia 

from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtNetwork import QHostAddress, QTcpServer

#from PyQt5.QtWebEngineWidgets import QWebEngineView
#from PyQt5 import QtNetwork, QtOpenGL 
import math

import socket, socketserver

#import OpenGL.platform
#import OpenGL.platform.win32
#from OpenGL import *
#from OpenGL import GL 

from lwin import Ui_MainWindow

# import sys
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

#Here is the main window   
MSGLEN = 5
class MainForm(QtWidgets.QMainWindow):
    """
    This is the main window of the application
    Built by mygui.ui
    """
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        #print sys.getdefaultencoding()
        self.setWindowTitle("pipotage")

        self.ui = Ui_MainWindow()
        

        self.ui.setupUi(self)
        self.setupleds()
        self.msg68 = ""
        self.msg83 = ""
        
        # Create the server, binding to localhost on port 9999
        # HOST, PORT = "192.168.1.26", 23
        # server = Server()
        # server.sessionOpened()
        # server.accept()
        #
        # #server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock.bind((HOST, PORT))
        # self.write2Console("socket created \n")
        # self.write2Console(str((HOST, PORT)))
        #  # Receive data from the server and shut down
        # sock.listen()
        # conn, addr = sock.accept()
        # with conn:
        #     self.write2Console(f"Connected by {addr}")
        #     while True:
        #         data = conn.recv(1024)
        #         if not data:
        #             break
        #         conn.sendall(data)            
        #         self.write2Console(str(data))
        # print ("server started")
        # # Activate the server; this will keep running until you
        # # interrupt the program with Ctrl-C
        # server.serve_forever()     
        #
        # # server = Server()
        # # server.StartServer()
        #
        # # self.tcp = Messenger()
        # # self.tcp.slotSendMessage()
        
        self.settings = QtCore.QSettings('AA55', 'wiflip')
        
        # Then we look at our settings to see if there is a setting called geometry saved. Otherwise we default to an empty string
        geometry = self.settings.value('geometry', None)
        self.HOST     = self.settings.value('host', '192.168.1.26')
        self.PORT     = int(self.settings.value('port', '23'))
        # Then we call a Qt built in function called restoreGeometry that will restore whatever values we give it.
        # In this case we give it the values from the settings file.
        if geometry is not None:
            self.restoreGeometry(geometry)
        
        self.ui.pushButton.clicked.connect(self.connect)
        self.ui.lineEdit.setText(self.HOST)
        self.ui.lineEdit_2.setText(str(self.PORT))

        self.jingle = os.path.join(CURRENT_DIR, "alarm1-b238.wav")
 
    def disconnect(self):
        print("disconnect")
        self.ui.label_12.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
        self.ui.pushButton.clicked.connect(self.connect)
        self.ui.pushButton.clicked.disconnect(self.disconnect)
        self.ui.pushButton.setText("connect")
        self.thread.sock.close()
        self.thread.terminate()
        
    def connect(self):
        self.ui.pushButton.clicked.connect(self.disconnect)
        self.ui.pushButton.clicked.disconnect(self.connect)
        self.ui.pushButton.setText("disconnect")
        if  True:
            self.thread = Worker(HOST=self.HOST, PORT=self.PORT)

            self.thread.finished.connect(self.pipo)
            self.thread.output.connect(self.cmdMng)
            self.thread.connled.connect(self.connled)
    
            self.thread.start()
    

    def connled(self, state):
        if state == "green":
            self.ui.label_12.setPixmap(QtGui.QPixmap(":/x/ledgreen"))
        elif state == "grey":
            self.ui.pushButton.clicked.connect(self.connect)
            self.ui.pushButton.clicked.disconnect(self.disconnect)
            self.ui.pushButton.setText("connect")
            self.ui.label_12.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            QtMultimedia.QSound.play(self.jingle)
        elif state == "yellow":
            self.ui.label_12.setPixmap(QtGui.QPixmap(":/x/ledyellow"))

    #convenient routine to allow the outside for writing to the script edit text window
    def write2ScriptEdit(self, msg, insertMode=True):
        if insertMode:
            self.ui.plainTextEdit.insertPlainText(msg)
        else:
            self.ui.plainTextEdit.clear()
            self.ui.plainTextEdit.appendPlainText(msg)

    #convenient routine to allow the outside for writing to the script edit text window
    def write2Console(self, msg, insertMode=True):
        if insertMode:
            self.ui.consoleEdit.insertPlainText(msg)
        else:
            self.ui.consoleEdit.clear()
            self.ui.consoleEdit.appendPlainText(msg)

    def giveFocus2Edit(self):
        self.ui.plainTextEdit.setFocus()
        self.ui.plainTextEdit.centerOnScroll()
        self.ui.plainTextEdit.centerCursor()
           
    def pipo(self):
        print("pipoptage")
        self.thread.quit()
    
    def pipo2(self):
        print("pipoptage2")

    def cmdMng(self, data, typ):
        #print("received", data, typ, type(typ))
        if typ == 0:
            print("typ=0", str(data))
        #print(str(data), len(data), typ)
        else:
            if  typ == 65:  #'A'
                ballinplay = data[0:1]
                tableau1   = data[1:4]
                freeplay   = data[4:5]
                tableau2   = data[5:]
                x = fromBcd2Int(tableau1)
                if x == -1:
                    self.ui.lcdNumber_1.setDigitCount(0)
                else:
                    self.ui.lcdNumber_1.setDigitCount(6)
                    self.ui.lcdNumber_1.setProperty("value", x)
                x = fromBcd2Int(tableau2)
                if x == -1:
                    self.ui.lcdNumber_2.setDigitCount(0)
                else:
                    self.ui.lcdNumber_2.setDigitCount(6)
                    self.ui.lcdNumber_2.setProperty("value", x)
                self.ui.lcdNumber_6.setProperty("value", fromBcd2Int(ballinplay))
                self.ui.lcdNumber_5.setProperty("value", fromBcd2Int(freeplay))
            elif typ == 66:  #'B'
                tableau3   = data[1:4]
                x = fromBcd2Int(tableau3)
                if x == -1:
                    self.ui.lcdNumber_3.setDigitCount(0)
                else:
                    self.ui.lcdNumber_3.setDigitCount(6)
                    self.ui.lcdNumber_3.setProperty("value", x)
                tableau4   = data[5:]
                x = fromBcd2Int(tableau4)
                if x == -1:
                    self.ui.lcdNumber_4.setDigitCount(0)
                else:
                    self.ui.lcdNumber_4.setDigitCount(6)
                    self.ui.lcdNumber_4.setProperty("value", x)
            elif typ == 67:  #'C'
                #print("typ=67", str(data))
                if not data[0]&0x08:
                    self.ui.checkBox_1.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_1.setCheckState(QtCore.Qt.Unchecked)
                    
                if not data[0]&0x04:
                    self.ui.checkBox_2.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_2.setCheckState(QtCore.Qt.Unchecked)

                if not data[0]&0x02:
                    self.ui.checkBox_3.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_3.setCheckState(QtCore.Qt.Unchecked)

                if not data[0]&0x01:
                    self.ui.checkBox_4.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_4.setCheckState(QtCore.Qt.Unchecked)
                    
                if not data[0]&0x80:
                    self.ui.checkBox_5.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_5.setCheckState(QtCore.Qt.Unchecked)

                if not data[0]&0x40:
                    self.ui.checkBox_6.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_6.setCheckState(QtCore.Qt.Unchecked)
                    
                if not data[0]&0x20:
                    self.ui.checkBox_7.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_7.setCheckState(QtCore.Qt.Unchecked)

                if not data[0]&0x10:
                    self.ui.checkBox_8.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_8.setCheckState(QtCore.Qt.Unchecked)


                if not data[1]&0x08:
                    self.ui.checkBox_9.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_9.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x04:
                    self.ui.checkBox_10.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_10.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x02:
                    self.ui.checkBox_11.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_11.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x01:
                    self.ui.checkBox_12.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_12.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x80:
                    self.ui.checkBox_13.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_13.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x40:
                    self.ui.checkBox_14.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_14.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x20:
                    self.ui.checkBox_15.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_15.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x10:
                    self.ui.checkBox_16.setCheckState(QtCore.Qt.Checked) 
                else:
                    self.ui.checkBox_16.setCheckState(QtCore.Qt.Unchecked)

                    
                if not data[2]&0x08:
                    self.ui.checkBox_17.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_17.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x04:
                    self.ui.checkBox_18.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_18.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x02:
                    self.ui.checkBox_19.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_19.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x01:
                    self.ui.checkBox_20.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_20.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x80:
                    self.ui.checkBox_21.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_21.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x40:
                    self.ui.checkBox_22.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_22.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x20:
                    self.ui.checkBox_23.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_23.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x10:
                    self.ui.checkBox_24.setCheckState(QtCore.Qt.Checked) 
                else:
                    self.ui.checkBox_24.setCheckState(QtCore.Qt.Unchecked)

                    
                                   
                # self.ui.ldip1_2.setText(f"{data[0]:08b}")
                # self.ui.ldip2_2.setText(f"{data[1]:08b}")
                # self.ui.ldip3_2.setText(f"{data[2]:08b}")
                
            elif typ == 83:  #'S'
                #print(str(data))
                #self.write2Console(f"switches:\n{data[0]:08b}\n{data[1]:08b}\n{data[2]:08b}\n{data[3]:08b}\n{data[3]:08b}", insertMode=False)
                self.msg83 = f"switches:\n{data[0]:08b}\n{data[1]:08b}\n{data[2]:08b}\n{data[3]:08b}\n{data[4]:08b}"
                for i in range(8):
                    for j in range(5):
                        #print(i,j,data[j],data[j]&(1<<i))
                        if data[j]&(1<<i):
                            self.led[i][j].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                        else:
                            self.led[i][j].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                            
            elif typ == 68:  #'D'
                #print(str(data))
                #self.write2Console(f"diag {data[0]:08b} {data[1]:08b} {data[2]:08b}{data[3]:08b}", insertMode=True)
                self.msg68 = f"diag {data[0]:08b} {data[1]:08b} {data[2]:08b}{data[3]:08b}"

        self.write2Console(self.msg83+"\n"+self.msg68, insertMode=False)
            
            #int_val = int.from_bytes(data, "big", signed=False)
            #int_val *= 10
            #self.ui.lcdNumber_1.setProperty("value", 131)
    def closeEvent(self, event):

        # Now we define the closeEvent
        # This is called whenever a window is closed.
        # It is passed an event which we can choose to accept or reject, but in this case we'll just pass it on after we're done.
        
        # First we need to get the current size and position of the window.
        # This can be fetchesd using the built in saveGeometry() method. 
        # This is got back as a byte array. It won't really make sense to a human directly, but it makes sense to Qt.
        geometry = self.saveGeometry()

        # Once we know the geometry we can save it in our settings under geometry
        self.settings.setValue('geometry', geometry)
        self.settings.setValue('host', self.ui.lineEdit.text())
        self.settings.setValue('port', self.ui.lineEdit_2.text())

        # Finally we pass the event to the class we inherit from. It can choose to accept or reject the event, but we don't need to deal with it ourselves
        super(MainForm, self).closeEvent(event)


    def setupleds(self):
        rows, cols = (8, 5)
        self.led = [0]*8
        
        for i in range(8):
            rled=QtWidgets.QLabel(self.ui.groupBox)
            rled.setGeometry(QtCore.QRect(60+i*28, 90-28, 20, 20))
            rled.setText(f"S{i}")
            rled.setObjectName(f"sled_{i}")
            
        for i in range(5):
            rled=QtWidgets.QLabel(self.ui.groupBox)
            rled.setGeometry(QtCore.QRect(60-28, 90+i*36, 20, 20))
            rled.setText(f"R{i}")
            rled.setObjectName(f"rled_{i}")
            
        for i in range(8):
            self.led[i]=[0]*5
            for j in range(5):
                self.led[i][j]=QtWidgets.QLabel(self.ui.groupBox)
                self.led[i][j].setGeometry(QtCore.QRect(60+i*28, 90+j*36, 20, 20))
                self.led[i][j].setText("")
                if i%2 and j%2:
                    self.led[i][j].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                else:
                    self.led[i][j].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                self.led[i][j].setScaledContents(True)
                self.led[i][j].setObjectName(f"led_{i}{j}")

        # print (self.led)
        # for i in range(8):
        #     for j in range(5):
        #         if i%2 and j%2:
        #             self.led[i][j].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                    
class Worker(QThread):
    output = pyqtSignal(bytearray, int)
    connled = pyqtSignal(str)
    def __init__(self, parent = None, HOST="192.168.1.26", PORT=23):
        QThread.__init__(self, parent)
        self.exiting = False
                
        #HOST, PORT = "192.168.1.26", 23

        self.HOST = HOST
        self.PORT = PORT
        
        
        
        #
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try:
        #     self.sock.bind((HOST, PORT))
        # except OSError as error :
        #     print(error)
        #     self.exiting = True
        #     self.wait()
            
    def __del__(self):    
        self.exiting = True
        self.wait()
        
    def render(self):    
        self.start()

    
    def quit(self):
        print("zzz")
        self.sock.close()
        
    def run(self):        
        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.
        
        print("Hi, ")

        while True:
            self.connled.emit("yellow")

            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(10.0)
                self.sock.connect((self.HOST, self.PORT))
                break
            except:
                print("waiting for host...")
                #self.connled.emit("grey")
                time.sleep(2)
            
        print("connected")

        self.connled.emit("green")

        # Receive data from the server and shut down
        while True:
            framesz = 0

            try:
                received = self.sock.recv(1)
            except socket.error as e:
                print(f"socket read error 1: {e}")
                break
            except ConnectionResetError:
                print("socket ConnectionResetError")
                break
            except Exception as e:
                print("unexpected exception when checking if a socket is closed")
                break
            if received == b'A' or received == b'B':
                framesz = 8
            elif received == b'C':
                #3 bytes
                framesz = 3
            elif received == b'D':
                framesz = 4
            elif received == b'S':
                framesz = 5
                  
            if  framesz > 0:               
                tsz = framesz
                msg = b''
                while tsz > 0:
                    try:
                        msg += self.sock.recv(tsz)
                    except socket.error as e:
                        print(f"socket read error 2: {e}")
                        break
                    lm  = len(msg)
                    if lm == framesz:
                        #print(f"message type {received} : {msg}")
                        #self.ui.lcdNumber_1.value = 345
                        self.output.emit(bytearray(msg), received[0])
                        break
                    tsz -= lm
                print(received, msg)
            else:
                pass
                #print(received)

        self.sock.close()
        
        self.connled.emit("grey")
        
        
        # self.sock.listen()
        # conn, addr = self.sock.accept()
        # with conn:
        #     self.output.emit(bytearray(f"Connected by {addr}".encode("ascii")), 0)
        #     chunk = list()
        #     while True:
        #         try:
        #             data = conn.recv(1024)
        #             #data = conn.recvfrom(5)
        #         except:
        #             data = None
        #             break
        #         if not data:
        #             break
        #         buf_ptr=0
        #         while buf_ptr<len(data):
        #             while len(chunk) < MSGLEN:
        #                 resteafaire = MSGLEN - len(chunk)
        #                 restealire  = len(data) - buf_ptr
        #                 if restealire <= 0:
        #                     break
        #                 #handlin desync cases
        #                 if not chunk:
        #                     if data[buf_ptr] != 49: #'1' is code of start frame
        #                         print("sync", data[buf_ptr])
        #                         buf_ptr += 1
        #                         break
        #                 nb2add = min(resteafaire, restealire)
        #                 chunk += data[buf_ptr:buf_ptr+nb2add]
        #                 buf_ptr += nb2add
        #
        #             if len(chunk) >= MSGLEN:
        #                 self.output.emit(bytearray(chunk), 1) 
        #                 print("received chunk", chunk)
        #                 chunk = list()
        #
        #
        #         #conn.sendall(data)            
        # print("pipi")

            

class MSCGui:
    
    def __init__(self):
        self.mainWindow = None

    def runApp(self, argv=['WiFlipApp']):
        """Start WiFlip"""
        print("""Start WiFlip""")
        
            
        
        #HOST = "192.167.1.1"
        #PORT = 23
        
        print(argv)
        app = QtWidgets.QApplication(argv)
        

        self.showGui()
        app.exec_()

    def showGui(self, parent=None):
        """Show the MSC gui

        In contrast to runApp, this method supposes that the Qt Application object has
        already been created.
        """
        
        self.mainWindow = MainForm( parent=parent )
        self.mainWindow.show()



def fromBcd2Int(barr):
    ret=0
    nbf = 0
    for bi in barr:
        d1=(~bi&0xF0)>>4
        if d1 == 0xF:
            d1 = 0
            nbf += 1
        ret = ret*10+d1
        d2=(~bi&0x0F)
        if d2 == 0xF:
            d2 = 0
            nbf += 1
        ret = ret*10+d2
    if nbf == 2*len(barr):
        ret = -1
    return ret
        
        
if __name__ == '__main__':
    MSCGui().runApp(argv=sys.argv)
