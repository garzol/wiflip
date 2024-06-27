'''
Created on 23 mars 2022

dockWidget_2
dockWidget
@author: garzol
'''

import os, sys, time
from time import sleep

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


        self.game_type = "Recel"
        #self.game_type = "Gottlieb"


        self.ui = Ui_MainWindow()
        

        
        

        self.ui.setupUi(self)
        self.setWindowTitle("WiFlip "+ self.game_type)

        
        
        if self.game_type == "Recel":
            DP = 92
            BY = 69
            BX = 10

            self.setupmatchleds()
            self.ui.label.setStyleSheet("background-image: url(images/1x/fair_fight_480.png);")
            self.ui.wplayer1.setGeometry(QtCore.QRect(200, 350, 220, 38))
            self.ui.wplayer2.setGeometry(QtCore.QRect(200, 350, 220, 38))
            self.ui.wplayer3.setGeometry(QtCore.QRect(200, 350, 220, 38))
            self.ui.wplayer4.setGeometry(QtCore.QRect(200, 350, 220, 38))
            self.ui.ballinplay.setGeometry(QtCore.QRect(200, 350, 272//6, 38))
            self.ui.credit.setGeometry(QtCore.QRect(200, 350, 272//6, 38))
            self.ui.wplayer1.move(QPoint(BX,BY))
            self.ui.wplayer2.move(QPoint(BX,BY+DP))
            self.ui.wplayer3.move(QPoint(BX,BY+2*DP-4))
            self.ui.wplayer4.move(QPoint(BX,BY+3*DP-7))
            self.ui.credit.move(QPoint(50,15))
            self.ui.ballinplay.move(QPoint(64,405))  #ballinplay is actually freeplay here
            self.setupballinplay()
            for i in range(5):
                self.bip[i].setVisible (True)
                self.bipt[i].setVisible(True)
            self.bip[5].setVisible (False)
            self.bipt[5].setVisible(False)
            self.tiltIndicator.setVisible(True)
        
        elif self.game_type == "Gottlieb":   
            self.ui.label.setStyleSheet("background-image: url(images/1x/pinballbell480.png);")
            
        if self.game_type == "Gottlieb":
            self.swmRows, self.swmCols = (8, 5)
        else:
            self.swmRows, self.swmCols = (10, 4)

        self.setupleds()
            
        self.msg68 = ""
        self.msg83 = ""
        
        
        self.lastAstate = 0
        self.lastBstate = 0
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
        state    = self.settings.value('state', None)
        self.HOST     = self.settings.value('host', '192.168.1.26')
        self.PORT     = int(self.settings.value('port', '23'))
        # Then we call a Qt built in function called restoreGeometry that will restore whatever values we give it.
        # In this case we give it the values from the settings file.
        if geometry is not None:
            self.restoreGeometry(geometry)
            
        if state is not None:
            self.restoreState(state)

        self.ui.pushButton.clicked.connect(self.connect)
        self.ui.lineEdit.setText(self.HOST)
        self.ui.lineEdit_2.setText(str(self.PORT))

        self.jingle = os.path.join(CURRENT_DIR, "alarm1-b238.wav")

        #trace button
        self.ui.pushButton_3.clicked.connect(self.send_trace)
        self.ui.pushButton_6.clicked.connect(self.send_gptrace)
        #dump button
        self.ui.pushButton_2.clicked.connect(self.send_dump)
 
 
        #nvrdump button
        self.ui.pushButton_R_dump.clicked.connect(self.send_nvrdump)

        #gpdump button
        self.ui.pushButton_4.clicked.connect(self.send_gpdump)
 
        #dpdump button
        self.ui.pushButton_5.clicked.connect(self.send_dpdump)
        
        #IOL control
        self.ui.iolButton.clicked.connect(self.send_iol)
        
        #Selection of hm6508 mode
        self.ui.pushButton_iram.clicked.connect(self.send_hmintern)
        self.ui.pushButton_hram.clicked.connect(self.send_hmreal)
        
        # font = QtGui.QFont()
        # font.setPointSize(5)
        # #font.setBold(True)
        # #font.setWeight(75)
        # self.ui.pushButton.setFont(font)
        font = QtGui.QFont("courier new")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ui.label_inp.setFont(font)
        self.ui.label_out.setFont(font)
        self.linenb = 0


        uilabels = [
            self.ui.label_D0_F, self.ui.label_D0_E, self.ui.label_D0_D, self.ui.label_D0_C,
            self.ui.label_D0_B, self.ui.label_D0_A, self.ui.label_D0_9, self.ui.label_D0_8,
            self.ui.label_D0_7, self.ui.label_D0_6, self.ui.label_D0_5, self.ui.label_D0_4,
            self.ui.label_D0_3, self.ui.label_D0_2, self.ui.label_D0_1, self.ui.label_D0_0
                    ]
        self.last_uilabels = ["00"]*16
        self.vientdecliquer = 0

        
        
    def send_trace(self): 
        try:
            self.thread.sock.send(b' t')
        except:
            pass
        
    def send_dump(self): 
        self.linenb = 0
        try:
            self.thread.sock.send(b' d')
        except:
            pass

    def send_gptrace(self): 
        try:
            self.thread.sock.send(b' U')
        except:
            pass
        
        
    def send_nvrdump(self): 
        self.linenb = 0
        print("send command R")
        try:
            self.thread.sock.send(b' R')
        except:
            pass
        
    def send_gpdump(self): 
        self.linenb = 0
        try:
            self.thread.sock.send(b' G')
        except:
            pass
        
    def send_dpdump(self): 
        self.linenb = 0
        try:
            self.thread.sock.send(b' C')
        except:
            pass
        
    def send_hmreal(self): 
        self.linenb = 0
        try:
            self.thread.sock.send(b' h')
        except:
            pass
        
    def send_hmintern(self): 
        self.linenb = 0
        try:
            self.thread.sock.send(b' i')
        except:
            pass
        
    def send_iol(self): 
        try:
            cmd = self.ui.lineEdit_Cmd.text()
            cmd = int(cmd, 16)+0x90
        except:
            cmd = 0
        try:
            acc = self.ui.lineEdit_Acc.text()
            acc = int(acc, 16)+0xA0
        except:
            acc = 0
        startcode = 0xB0
        mybytes = bytearray()
        #mybytes.append(startcode)
        mybytes.append(cmd)
        mybytes.append(acc)
        mybytes.append(startcode)
        
        
        try:
            self.thread.sock.send(mybytes)
        except:
            print("error not sending anything")
            pass
        
        self.vientdecliquer = 1
        print("sent:", mybytes)
        
        # mybytes = bytearray([
        #                         0xB0,0x08,0x0, 
        #                      ])   
        # #                     #     0x09,0x0,0xB0, 0x0A,0x0,0xB0, 0x0B,0x0,0xB0,
        # #                     #     0x0C,0x0,0xB0, 0x0D,0x0,0xB0, 0x0E,0x0,0xB0, 0x0F,0x0,0xB0,
        # #                     #     0xB1
        # #                     # ])
        #
        # sleep(1.1)
        # try:
        #     self.thread.sock.send(mybytes)
        # except:
        #     print("error2 not sending anything")
        #     pass
        #
        # print("sent:", mybytes)
        # mybytes = bytearray([
        #                         0xB0,0x09,0x0, 
        #                      ])   
        # #                     #     0x09,0x0,0xB0, 0x0A,0x0,0xB0, 0x0B,0x0,0xB0,
        # #                     #     0x0C,0x0,0xB0, 0x0D,0x0,0xB0, 0x0E,0x0,0xB0, 0x0F,0x0,0xB0,
        # #                     #     0xB1
        # #                     # ])
        #
        # sleep(1.1)
        # try:
        #     self.thread.sock.send(mybytes)
        # except:
        #     print("error2 not sending anything")
        #     pass
        #
        # print("sent:", mybytes)
        #
        #

    def disconnect(self):
        print("disconnect")
        self.ui.label_12.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
        self.ui.pushButton.clicked.connect(self.connect)
        self.ui.pushButton.clicked.disconnect(self.disconnect)
        self.ui.pushButton.setText("connect")
        # try:
        #     self.thread.sock.close()
        # except:
        #     pass
        self.thread.terminate()
        
    def connect(self):
        self.ui.pushButton.clicked.connect(self.disconnect)
        self.ui.pushButton.clicked.disconnect(self.connect)
        self.ui.pushButton.setText("disconnect")
        if  True:
            #self.thread = Worker(HOST=self.HOST, PORT=self.PORT)
            self.thread = Worker(HOST=self.ui.lineEdit.text(), 
                                 PORT=self.ui.lineEdit_2.text())

            self.thread.finished.connect(self.pipo)
            self.thread.output.connect(self.cmdMng)
            self.thread.connled.connect(self.connled)
    
            self.thread.start()
    

    def connled(self, state):
        if state == "green":
            self.ui.label_12.setPixmap(QtGui.QPixmap(":/x/ledgreen"))
        elif state == "grey":
            try:
                self.ui.pushButton.clicked.connect(self.connect)
                self.ui.pushButton.clicked.disconnect(self.disconnect)
            except:
                pass
            
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
        print("close conn. thread")
        self.thread.quit()
    
    def pipo2(self):
        print("pipoptage2")

    def cmdMng(self, data, typ):
        #print("received", data, typ, type(typ))
        if typ == 0:
            print("typ=0", str(data))
        elif typ == 84:   #T
            # 8b ROM data
            #12b ROM addr
            # 1b reset state
            # 1b read/write state
            # 1b w_io state
            # 1b bagotting checker
            #print("recu", data[0], data[1], data[2])
            #print("typ=54", str(data))
            self.linenb      += 1
            ramdata      = data[0]
            romdata      = data[1]
            romaddr      = data[2]+(data[3]&0x0F)*0x100
            bagotti  = 1 if data[3]&0x80 else 0
            wiostate = 1 if data[3]&0x40 else 0
            rwstate  = 1 if data[3]&0x20 else 0
            rststate = 1 if data[3]&0x10 else 0
            ramaddr      = data[4]+256*bagotti
            #print(f"{romaddr:03X}\t{romdata:02X} rst={rststate} rw={rwstate} wio={wiostate} bagot={bagotti}")
            self.write2Console(f"{self.linenb:03d} {romaddr:03X} {romdata:02X}\t{ramaddr:03X} {ramdata:02X}\t  rst={rststate} rw={rwstate} wio={wiostate} bgt={bagotti}\r\n", insertMode=True)
            #print("typ=3", str(data))
        #print(str(data), len(data), typ)
        elif typ == 82:    #R
            print("Dump RAM in progress")
            self.write2Console(f"NVRAM Current\r\n", insertMode=True)
            for r in range(16):
                self.write2Console(f"{r:02X}\t")
                for l in range(8):
                    self.write2Console(f"{data[r*8+l]:02X} ", insertMode=True)
                self.write2Console(f"\r\n", insertMode=True)
                    
            
        elif typ == 71:   #G
            # 8b ROM data
            # 8b RAM data
            #12b ROM addr
            # "1010"
            self.linenb      += 1
            romdata      = data[0]
            ramdata      = data[1]
            romaddr      = data[2]+(data[3]&0x0F)*0x100
            gpaddr       = ((data[3]&0x30 )>>4)*0x100 + data[4]
            ramaddr      = data[4]
            #print(f"{romaddr:03X}\t{romdata:02X} rst={rststate} rw={rwstate} wio={wiostate} bagot={bagotti}")
            #next line for GP case (game prom spying
            #self.write2Console(f"{self.linenb:03d} romaddr={romaddr:03X} romdata={romdata:02X}\t ramdata={ramdata:02X}\t gpaddr={gpaddr:03X}\r\n", insertMode=True)
            #next line for standard trace of specific instruction
            self.write2Console(f"{self.linenb:03d} {romaddr:03X} {romdata:02X}\t ramaddr={ramaddr:03X}\t ramdata={ramdata:02X}\r\n", insertMode=True)
            #print("typ=3", str(data))
        #print(str(data), len(data), typ)
        elif typ == 89:   #Y for IO status
            io_os = data[0]*256 + data[1]
            io_is = data[2]*256 + data[3]
            #print("Y got", data[0], data[1], data[2], data[3], io_os, io_is)
            self.ui.label_out.setText(f"{io_os:016b}")
            self.ui.label_inp.setText(f"{io_is:016b}")
        else:
            if  typ == 65:  #'A'
                dspAstate = 1 if data[0]&0x80 else 0
                dspBstate = 1 if data[0]&0x40 else 0
                if   dspAstate == 0 and self.lastAstate == 1:
                    self.ui.label_DAState.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                elif dspAstate == 1 and self.lastAstate == 0:
                    self.ui.label_DAState.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                self.lastAstate = dspAstate
                if   dspBstate == 0 and self.lastBstate == 1:
                    self.ui.label_DBState.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                elif dspBstate == 1 and self.lastBstate == 0:
                    self.ui.label_DBState.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                self.lastBstate = dspBstate
                
                if   self.game_type == "Gottlieb":   
                    ballinplay = data[1:2]
                    tableau1   = data[2:5]
                    freeplay   = data[5:6]
                    tableau2   = data[6:]
                else:  #Recel case
                    ballinplay = data[9:7:-1]     #tilt/game over/ball in play | match number
                    tableau1   = data[7:3:-1]+b'0' #data[8] contains the dots state
                    freeplay   = data[1::-1]      #freeplay|extra ball, here
                    tableau2   = data[-7::]  +b'0' #data[-6] contains dots
                    
                aff1 = [self.ui.lcd1_6, self.ui.lcd1_5, self.ui.lcd1_4, self.ui.lcd1_3, self.ui.lcd1_2, self.ui.lcd1_1]
                aff2 = [self.ui.lcd2_6, self.ui.lcd2_5, self.ui.lcd2_4, self.ui.lcd2_3, self.ui.lcd2_2, self.ui.lcd2_1]
                aff5 = [self.ui.lcd5_2, self.ui.lcd5_1]
                aff6 = [self.ui.lcd6_2, self.ui.lcd6_1]

                aff3 = [self.ui.lcd3_6, self.ui.lcd3_5, self.ui.lcd3_4, self.ui.lcd3_3, self.ui.lcd3_2, self.ui.lcd3_1]
                aff4 = [self.ui.lcd4_6, self.ui.lcd4_5, self.ui.lcd4_4, self.ui.lcd4_3, self.ui.lcd4_2, self.ui.lcd4_1]

                if   self.game_type == "Gottlieb":                   
                    afflcdi(aff1, data[2:])
                    afflcdi(aff2, data[6:])
                    afflcdi(aff5, data[1:])
                    afflcdi(aff6, data[5:])
                else:
                    #player 1
                    data2=[((data[4]&0x0F)<<4)+((data[4]&0xF0)>>4),
                           ((data[3]&0x0F)<<4)+((data[3]&0xF0)>>4),
                           ((data[2]&0x0F)<<4)+0x0F]
                    
                    afflcdi(aff1, data2)   #tableau 1

                    #player2                    
                    data2=[((data[8]&0x0F)<<4)+((data[8]&0xF0)>>4),
                           ((data[7]&0x0F)<<4)+((data[7]&0xF0)>>4),
                           ((data[6]&0x0F)<<4)+0x0F]
                    
                    
                    afflcdi(aff2, data2)     #tableau 2
                    
                    #afflcdi(aff5, data[5:])    #match number
                    afflcdi(aff6, data[1:])    #freeplay/EB

                    #match number
                    for i in range(10):
                        #print(i,(~data[5]&0x0F),data[5])
                        if i==(~data[5]&0x0F):
                            self.mled[i].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                        else:
                            self.mled[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))

                    #ball in play + game over
                    bstat = (data[5]&0x70)>>4
                    bstat = bstat ^ 0b0111
                    #print(f"{bstat:04b}   { ((data[5]&0x70))>>4:04b}")
                    for i in range(5):
                        if i==bstat:
                            self.bip[i].setVisible (True)
                            self.bipt[i].setVisible(True)
                        else:
                            self.bip[i].setVisible (False)
                            self.bipt[i].setVisible(False)
                    
                    if bstat== 7:
                        self.bip[5].setVisible (True)
                        self.bipt[5].setVisible(True)
                    else:
                        self.bip[5].setVisible (False)
                        self.bipt[5].setVisible(False)
                        
                                
                    #tilt
                    if ((~data[5]&0x80)):
                        self.tiltIndicator.setVisible(True)
                    else:
                        self.tiltIndicator.setVisible(False)
                        

                    
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
                dspAstate = 1 if data[0]&0x80 else 0
                dspBstate = 1 if data[0]&0x40 else 0
                if   dspAstate == 0 and self.lastAstate == 1:
                    self.ui.label_DAState.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                elif dspAstate == 1 and self.lastAstate == 0:
                    self.ui.label_DAState.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                self.lastAstate = dspAstate
                if   dspBstate == 0 and self.lastBstate == 1:
                    self.ui.label_DBState.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                elif dspBstate == 1 and self.lastBstate == 0:
                    self.ui.label_DBState.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                self.lastBstate = dspBstate

                if   self.game_type == "Gottlieb":   
                    tableau3   = data[2:5]
                    tableau4   = data[6:]
                else:
                           
                    tableau3   = data[-7::]    + b'0'
                    tableau4   = data[7:2:-1]  + b'0'

                x = fromBcd2Int(tableau3)
                if x == -1:
                    self.ui.lcdNumber_3.setDigitCount(0)
                else:
                    self.ui.lcdNumber_3.setDigitCount(6)
                    self.ui.lcdNumber_3.setProperty("value", x)
                    
                    
                x = fromBcd2Int(tableau4)
                if x == -1:
                    self.ui.lcdNumber_4.setDigitCount(0)
                else:
                    self.ui.lcdNumber_4.setDigitCount(6)
                    self.ui.lcdNumber_4.setProperty("value", x)
                    
                aff3 = [self.ui.lcd3_6, self.ui.lcd3_5, self.ui.lcd3_4, self.ui.lcd3_3, self.ui.lcd3_2, self.ui.lcd3_1]
                aff4 = [self.ui.lcd4_6, self.ui.lcd4_5, self.ui.lcd4_4, self.ui.lcd4_3, self.ui.lcd4_2, self.ui.lcd4_1]
                aff5 = [self.ui.lcd5_2, self.ui.lcd5_1]  #credits

                if   self.game_type == "Gottlieb":                                  
                    afflcdi(aff3, data[2:])
                    afflcdi(aff4, data[6:])
                else:
                    #player 4
                    data2=[((data[4]&0x0F)<<4)+((data[4]&0xF0)>>4),
                           ((data[3]&0x0F)<<4)+((data[3]&0xF0)>>4),
                           ((data[2]&0x0F)<<4)+0x0F]
                           
                    afflcdi(aff4, data2)   #tableau 4
                    
                    #player3                    
                    data2=[((data[8]&0x0F)<<4)+((data[8]&0xF0)>>4),
                           ((data[7]&0x0F)<<4)+((data[7]&0xF0)>>4),
                           ((data[6]&0x0F)<<4)+0x0F]
                    
                    afflcdi(aff3, data2)     #tableau 3
                    
                    afflcdi(aff5, data[1:])    #credits

                
                    
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


                if not data[1]&0x01:
                    self.ui.checkBox_9.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_9.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x02:
                    self.ui.checkBox_10.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_10.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x04:
                    self.ui.checkBox_11.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_11.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x08:
                    self.ui.checkBox_12.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_12.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x10:
                    self.ui.checkBox_13.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_13.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x20:
                    self.ui.checkBox_14.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_14.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x40:
                    self.ui.checkBox_15.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_15.setCheckState(QtCore.Qt.Unchecked)

                if not data[1]&0x80:
                    self.ui.checkBox_16.setCheckState(QtCore.Qt.Checked) 
                else:
                    self.ui.checkBox_16.setCheckState(QtCore.Qt.Unchecked)

                    
                if not data[2]&0x01:
                    self.ui.checkBox_17.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_17.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x02:
                    self.ui.checkBox_18.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_18.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x04:
                    self.ui.checkBox_19.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_19.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x08:
                    self.ui.checkBox_20.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_20.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x10:
                    self.ui.checkBox_21.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_21.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x20:
                    self.ui.checkBox_22.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_22.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x40:
                    self.ui.checkBox_23.setCheckState(QtCore.Qt.Checked)
                else:
                    self.ui.checkBox_23.setCheckState(QtCore.Qt.Unchecked)

                if not data[2]&0x80:
                    self.ui.checkBox_24.setCheckState(QtCore.Qt.Checked) 
                else:
                    self.ui.checkBox_24.setCheckState(QtCore.Qt.Unchecked)

                    
                                   
                # self.ui.ldip1_2.setText(f"{data[0]:08b}")
                # self.ui.ldip2_2.setText(f"{data[1]:08b}")
                # self.ui.ldip3_2.setText(f"{data[2]:08b}")

            elif typ == 80: #'P'
                #print(str(data))
                uilabels = [
                    self.ui.label_D0_F, self.ui.label_D0_E, self.ui.label_D0_D, self.ui.label_D0_C,
                    self.ui.label_D0_B, self.ui.label_D0_A, self.ui.label_D0_9, self.ui.label_D0_8,
                    self.ui.label_D0_7, self.ui.label_D0_6, self.ui.label_D0_5, self.ui.label_D0_4,
                    self.ui.label_D0_3, self.ui.label_D0_2, self.ui.label_D0_1, self.ui.label_D0_0
                            ]
                #for i in range(16):
                for i in range(16):
                    #print(uilabels[i].text()[-2:])
                    if  uilabels[i].text()[-2:] != f"{data[2*i+1]:02X}":
                        uilabels[i].setStyleSheet("QLabel { background-color : red; color : white; }")
                    else:
                        if self.vientdecliquer >= 50:
                            uilabels[i].setStyleSheet("QLabel { background-color : green; color : white; }")
                            self.vientdecliquer = 0
                        else:
                            self.vientdecliquer += 1
                            
                    
                    
                    
                    self.last_uilabels[i] = uilabels[i].text()[-2:]
                    uilabels[i].setText(f"{data[2*i]:02X} {data[2*i+1]:02X}")
                    
                        
                
            elif typ == 83:  #'S'
                #print(len(data),"\t",str(data))
                rows, cols = self.swmRows, self.swmCols  #(8,5) or (10,4)  

                #self.write2Console(f"switches:\n{data[0]:08b}\n{data[1]:08b}\n{data[2]:08b}\n{data[3]:08b}\n{data[4]:08b}", insertMode=False)
                self.msg83 = f"switches:\n{data[0]:08b}\n{data[1]:08b}\n{data[2]:08b}\n{data[3]:08b}\n{data[4]:08b}"
                #print(self.msg83)
                for i in range(rows*cols):
                    bitnumber  = i%8
                    bytenumber = i//8
                    r = i//cols
                    c = i%cols
                    if data[bytenumber]&(1<<bitnumber):
                        self.led[r][c].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                    else:
                        self.led[r][c].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                            
            elif typ == 68:  #'D'
                #print(str(data))
                #self.write2Console(f"diag {data[0]:08b} {data[1]:08b} {data[2]:08b}{data[3]:08b}", insertMode=True)
                self.msg68 = f"diag {data[0]:08b} {data[1]:08b} {data[2]:08b}{data[3]:08b}"

        #self.write2Console(self.msg83+"\n"+self.msg68, insertMode=False)
            
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
        print("bye")
        geometry = self.saveGeometry()
        
        #print(geometry)
        # Once we know the geometry we can save it in our settings under geometry
        self.settings.setValue('geometry', geometry)
        self.settings.setValue('state', self.saveState())
        self.settings.setValue('host', self.ui.lineEdit.text())
        self.settings.setValue('port', self.ui.lineEdit_2.text())

        # Finally we pass the event to the class we inherit from. It can choose to accept or reject the event, but we don't need to deal with it ourselves
        super(MainForm, self).closeEvent(event)


    def setupleds(self):
        rows, cols = self.swmRows, self.swmCols    
        self.led = [0]*rows
        
        for i in range(rows):
            rled=QtWidgets.QLabel(self.ui.groupBox)
            rled.setGeometry(QtCore.QRect(60+i*28, 90-28, 20, 20))
            rled.setText(f"S{i}")
            rled.setObjectName(f"sled_{i}")
            
        for i in range(cols):
            rled=QtWidgets.QLabel(self.ui.groupBox)
            rled.setGeometry(QtCore.QRect(60-28, 90+i*36, 20, 20))
            rled.setText(f"R{i}")
            rled.setObjectName(f"rled_{i}")
            
        for i in range(rows):
            self.led[i]=[0]*cols
            for j in range(cols):
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

    def setupballinplay(self):
        self.bip = [0]*6
        self.bipt = [0]*6
        for i in range(5):
            self.bip[i]=QtWidgets.QLabel(self.ui.centralwidget)
            self.bip[i].setGeometry(QtCore.QRect(300+i*30, 365, 20, 20))
            self.bip[i].setPixmap(QtGui.QPixmap(":/x/ledyellow"))
            self.bip[i].setScaledContents(True)
            self.bip[i].setObjectName(f"bip{i}")
            
            self.bipt[i]=QtWidgets.QLabel(self.ui.centralwidget)
            self.bipt[i].setGeometry(QtCore.QRect(300+i*30, 365, 20, 20))
            self.bipt[i].setStyleSheet("QLabel { background-color : transparent; color : darkGreen; font-size: 14; font-weight: bold;}")
            self.bipt[i].setText(f"  {i+1} ")
            self.bipt[i].setScaledContents(True)
            self.bipt[i].setObjectName(f"bipt{i}")

        self.bip[5]=QtWidgets.QLabel(self.ui.centralwidget)
        self.bip[5].setGeometry(QtCore.QRect(300, 365, 20, 20))
        self.bip[5].setPixmap(QtGui.QPixmap(":/x/ledyellow"))
        self.bip[5].setScaledContents(True)
        self.bip[5].setObjectName(f"bip5")
        
        self.bipt[5]=QtWidgets.QLabel(self.ui.centralwidget)
        self.bipt[5].setGeometry(QtCore.QRect(300, 365, 100, 20))
        self.bipt[5].setStyleSheet("QLabel { background-color : orange; color : white; font-weight: bold;}")
        self.bipt[5].setText(f"  GAME OVER")
        self.bipt[5].setScaledContents(True)
        self.bipt[5].setObjectName(f"bipt5")


        self.tiltIndicator = QtWidgets.QLabel(self.ui.centralwidget)
        self.tiltIndicator.setGeometry(QtCore.QRect(175, 425, 50, 20))
        self.tiltIndicator.setStyleSheet("QLabel { background-color : orange; color : white; font-weight: bold;}")
        self.tiltIndicator.setText(f" T I L T")
        self.tiltIndicator.setScaledContents(True)

    def setupmatchleds(self):
        
        self.mled  = [0]*10
        self.mledt = [0]*10
        
        # for i in range(8):
        #     rled=QtWidgets.QLabel(self.ui.groupBox)
        #     rled.setGeometry(QtCore.QRect(60+i*28, 90-28, 20, 20))
        #     rled.setText(f"S{i}")
        #     rled.setObjectName(f"sled_{i}")
            
        ccenter = (419.0, 165.0)
        cr      =  28.0

        for i in range(10):
            self.mledt[i]=QtWidgets.QLabel(self.ui.centralwidget)
            xc = ccenter[0] + (cr+20)*math.cos(2.0*math.pi*i/10.0 + math.pi/2.0)
            yc = ccenter[1] + (cr+20)*math.sin(2.0*math.pi*i/10.0 + math.pi/2.0)
            xc = int(xc)
            yc = int(yc)
            self.mledt[i].setGeometry(QtCore.QRect(xc, yc, 20, 20))
            self.mledt[i].setStyleSheet("QLabel { background-color : black; color : white; }")

            self.mledt[i].setText(str(i)+"0")
            self.mledt[i].setScaledContents(True)
            self.mledt[i].setObjectName(f"matchledt_{i}")
          
        for i in range(10):
            self.mled[i]=QtWidgets.QLabel(self.ui.centralwidget)
            xc = ccenter[0] + cr*math.cos(2.0*math.pi*i/10.0 + math.pi/2.0)
            yc = ccenter[1] + cr*math.sin(2.0*math.pi*i/10.0 + math.pi/2.0)
            xc = int(xc)
            yc = int(yc)
            self.mled[i].setGeometry(QtCore.QRect(xc, yc, 20, 20))
            self.mled[i].setText("")
            self.mled[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            self.mled[i].setScaledContents(True)
            self.mled[i].setObjectName(f"matchled_{i}")



                    
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
        print("socket close")
        self.sock.close()
        
    def run(self):        
        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.
        
        print("Hi, connection to", (self.HOST, self.PORT))

        while True:
            self.connled.emit("yellow")

            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #self.sock.settimeout(20.0)
                #self.sock.setblocking(False)
                self.sock.connect((self.HOST, int(self.PORT)))
                break
            except Exception as e:
                print("connection delayed")
                print(e)
                print("waiting for host...")
                
                #self.connled.emit("grey")
                time.sleep(2)
            
        print("connected")
        print("hostname ", socket.gethostname())

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
            
            #print("received", received[0])
            if received == b'A' or received == b'B':
                framesz = 9
            elif received == b'C':
                #3 bytes
                framesz = 3
            elif received == b'D':
                framesz = 4
            elif received == b'Y':   #IO status 4 bytes Oh, Ol, Ih, Il
                framesz = 4
            elif received == b'S':
                framesz = 5
            elif received == b'T':
                framesz = 5
            elif received == b'G':
                framesz = 5
            elif received == b'R':
                framesz = 128
            elif received == b'P':
                #print("P")
                framesz = 32 #32
            else:
                framesz = 0

                  
            if  framesz > 0:               
                tsz = framesz
                msg = b''
                while tsz > 0:
                    try:
                        msg += self.sock.recv(1)  #(tsz)
                    except socket.error as e:
                        print(f"socket read error 2: {e}")
                        break
                    lm  = len(msg)
                    #print("lm", framesz, lm, msg)
                    if lm == framesz:
                        #print(f"message ack {received} : {msg[0]} {msg[1]} ")
                        #self.ui.lcdNumber_1.value = 345
                        self.output.emit(bytearray(msg), received[0])
                        break
                    #tsz -= lm
                    tsz -= 1
                #print(received, msg)
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

def swapint(v):
    return ((v&0x0F)<<4)+((v&0xF0)>>4)      
   
def afflcdi(afftab, data):
    #print(type(data))     => bytearray
    #print(type(data[0]))  => int
    
    for idx in range(len(afftab)):
        afftab[idx].setHexMode()
        if not idx%2:
            #pair
            dx = (~data[idx//2]&0xF0)>>4
        else:
            #impair
            dx = (~data[idx//2]&0x0F)
            
        if dx == 0xF:
            afftab[idx].setDigitCount(0)
        else:
            afftab[idx].setDigitCount(1)
            afftab[idx].display(dx)
            

    
    
    
    
            
if __name__ == '__main__':
    MSCGui().runApp(argv=sys.argv)
