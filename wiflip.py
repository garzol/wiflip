'''
Created on 23 mars 2022

dockWidget_2
dockWidget
@author: garzol switches reset
'''

import os, sys, time
from time import sleep
from functools import partial
from builtins import staticmethod

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

from about import Ui_AboutDialog
from help import Ui_HelpDialog
from settings import Ui_DialogSettings

# import sys
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

#Here is the main window   
MSGLEN = 5

aboutContent = '''
<table cellpadding="10"><tr>
<td><img src=":/x/images/aa55_logo_2.ico"/></td>
<td valign="middle"></td>
<p><span style=" font-size:18pt; font-weight:600;">%(productName)s</span></p>
<p><span style=" font-size:12pt;">%(copyright)s</span></p>
<p><span style=" font-size:12pt;">Software product from AA55</span></p>
<p><span style=" font-size:12pt;">Version %(version)s - %(date)s</span></p>
<p><span style=" font-size:10pt;">WiFlip allows user to connect to a pinball MPU and collect data from the pinball</span></p>
<p><span style=" font-size:10pt;">One can emulate Gottlieb and Recel pinball machines</span></p>
<p><span style=" font-size:10pt;">On Recel, this interface is required to replace the original miniprinter, which now became nowhere to be found</span></p>
<p><span style=" font-size:10pt;"><a href="https://www.pps4.fr">https://www.pps4.fr</a></span></p>
</td></tr></table>
'''

VERSION = "0.80"
DATE    = "2024-08-31"

#Here is the about dialog box
class MyAbout(QtWidgets.QDialog):
    """
    This dialog box was created with QT
    in about.ui
    """
    def __init__(self, parent=None):
        super(MyAbout, self).__init__(parent)
        #QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.ui.aboutContent.setText( aboutContent % {
            'productName': 'WiFlip',
            'version'    : "V "+ VERSION,
            'date'       : DATE,
            'copyright'  : 'by AA55 Consulting'} )

#Here is the about dialog box
class MyHelp(QtWidgets.QDialog):
    """
    This dialog box was created with QT
    in help.ui
    """
    def __init__(self, parent=None):
        super(MyHelp, self).__init__(parent)
        #QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_HelpDialog()
        self.ui.setupUi(self)
        #self.ui.webEngineView.load(QtCore.QUrl.fromLocalFile('/Users/garzol/git/wiflip_tracer/index.htm'))
        self.ui.textBrowser.append('''
<b>V0.80</b><br>correction of bug when loading nvr data file was not actually sending data<br>
<b>V0.78</b><br>original version<br>
'''
)
        self.ui.textBrowser_2.setSource(QtCore.QUrl('qrc:///help/index.htm'))
      
 
class MySettings(QtWidgets.QDialog): 
    """
    This dialog box was created with QT
    in settings.ui
    """
    statusCmd = pyqtSignal(int, str)
    def __init__(self, parent=None):
        super(MySettings, self).__init__(parent)
        #QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_DialogSettings()
        self.ui.setupUi(self)

        self.ui.label.setText("")
        
        self.flags=[self.ui.checkBox_flag0, self.ui.checkBox_flag1, self.ui.checkBox_flag2, self.ui.checkBox_flag3,
                    self.ui.checkBox_flag4, self.ui.checkBox_flag5, self.ui.checkBox_flag6, self.ui.checkBox_flag7]

        #self.ui.groupBox.stateChanged.connect(self.test)
        for cb in self.flags:
            cb.stateChanged.connect(self.modsc)

        self.ui.radioButton_startnormal.clicked.connect(self.modscr)
        self.ui.radioButton_startmnprn.clicked.connect(self.modscr)
        self.ui.radioButton_startfactory.clicked.connect(self.modscr)
        
        
        self.ui.toolButton_reset.clicked.connect(self.resetthepin)
        

        self.refreshdlg()
        
        
    def refreshdlg(self):
        #select sys config
        memtyp = 0
        papa = self.parent()
    
        print("message request is", b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            papa.thread.sock.send(b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            dlg = QMessageBox(self.parent())
            dlg.setWindowTitle("www")
            dlg.setText("No connection.")
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec()
            self.ui.label.setText("Not connected")
            
            self.ui.groupBox.setDisabled(True)
            self.ui.groupBox_2.setDisabled(True)


        self.timertout = QTimer(singleShot=True, timeout=self.timeoutt)
        self.timertout.start(5000)
        
        self.statusCmd.connect(self.cmdDone)   
        #next lines to emulate the thing
        self.timerpipo = QTimer(singleShot=True, timeout=self.fpipo)
        self.timerpipo.start(4000)
              
        
        
    def resetthepin(self):
        papa = self.parent()
        print("message request is", b'YBXQZ')
        try:
            papa.thread.sock.send(b'YBXQZ')
        except:
            pass
        
        #self.refreshdlg()
        
    def modscr(self):
        sc_mode = 0
        if self.ui.radioButton_startmnprn.isChecked():
            sc_mode = 1
        elif self.ui.radioButton_startnormal.isChecked():
            sc_mode = 2

        papa = self.parent()
        
        memtyp = 0
        addr   = 3
        bbyt   = sc_mode
        baddr = addr.to_bytes(1, byteorder='big')
        bbyt = bbyt.to_bytes(1, byteorder='big')
        print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        try:
            papa.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        except:
            pass
            
        print("message request is", b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            papa.thread.sock.send(b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
             
    def modsc(self):
        sc_flags1 = 0
        for i in range(8):
            sc_flags1 |= ((1 if (self.flags[i].isChecked()==True) else 0)<<i)

        

        papa = self.parent()

        memtyp = 0
        addr   = 4
        bbyt   = sc_flags1
        baddr = addr.to_bytes(1, byteorder='big')
        bbyt = bbyt.to_bytes(1, byteorder='big')
        print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        try:
            papa.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
        except:
            pass
            
        print("message request is", b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            papa.thread.sock.send(b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
                
         
               
    def cmdDone(self, cmdcode, status):   
        print(cmdcode, status)
        self.timertout.stop()
        papa = self.parent()
        if cmdcode == 82 and status == "done":
            papa.ui.rb_sysconf.setChecked(True)  #we expect the others to turn unchecked...
            sc_formatString =  f"{papa.nvrlist[0][1]:02X}"+f"{papa.nvrlist[1][1]:02X}"+f"{papa.nvrlist[2][1]:02X}"
            sc_mode         =  papa.nvrlist[3][1]
            sc_flags1       =  papa.nvrlist[4][1]
            print(f"sc_formatString: {sc_formatString} sc_mode: {sc_mode} sc_flags1: {sc_flags1:08b}")
            if sc_mode == 1:
                self.ui.radioButton_startmnprn.setChecked(True)
            elif sc_mode == 2:
                self.ui.radioButton_startnormal.setChecked(True)
            else:
                self.ui.radioButton_startfactory.setChecked(True)
                
            for i in range(8):
                self.flags[i].setChecked(sc_flags1&(1<<i)!=0)
                
            if sc_formatString != "AA55C3":
                self.ui.label.setText(f"Bad format string : {sc_formatString}")
                
    def test(self):
        self.statusCmd.emit("zobi")

    def processOneThing(self):
        print("elapsed")
        
    def timeoutt(self):
        print("Time out")
        dlg = QMessageBox(self.parent())
        dlg.setWindowTitle("I have a question!")
        dlg.setText("Time out. Please, check your connection")
        dlg.setIcon(QMessageBox.Warning)
        button = dlg.exec()

        if button == QMessageBox.Ok:
            self.ui.label.setText("Can't find device")
        
    def fpipo(self):
        pass
        #self.statusCmd.emit(82, "done")
        
    def closeEvent(self, event):
        QtWidgets.QDialog.closeEvent(self, event)
        
        
class MainForm(QtWidgets.QMainWindow):
    """
    This is the main window of the application
    Built by mygui.ui
    """
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        #print sys.getdefaultencoding()

        self.version   = VERSION
        self.date      = DATE
        self.game_type = "Recel"
        #self.game_type = "Gottlieb"

    

        self.ui = Ui_MainWindow()
        

        
        

        self.ui.setupUi(self)
        self.setWindowTitle("WiFlip "+ self.game_type + " - V" + self.version + "(" +self.date +")")

        self.settings = QtCore.QSettings('AA55', 'wiflip')

        self.settings.setValue("MainWindow/default/geometry", 
                             self.saveGeometry())
        self.settings.setValue("MainWindow/default/windowState", 
                             self.saveState())        

        
        # Then we look at our settings to see if there is a setting called geometry saved. Otherwise we default to an empty string
        geometry = self.settings.value('geometry', None)
        state    = self.settings.value('state', None)
        self.HOST     = self.settings.value('host', '192.168.1.26')
        self.PORT     = int(self.settings.value('port', '23'))
        self.face     = self.settings.value('face', 'fair_fight')
        self.fontsz   = self.settings.value('font-sz', '12')
        # Then we call a Qt built in function called restoreGeometry that will restore whatever values we give it.
        # In this case we give it the values from the settings file.
        if geometry is not None:
            self.restoreGeometry(geometry)
            
        if state is not None:
            self.restoreState(state)

        for act in  self.ui.menuFont_size.actions():                 
            if act.text() == self.fontsz:
                act.setChecked(True)
            else:
                act.setChecked(False)                 
        
        self.fontsz = int(self.fontsz)
        
        if self.game_type == "Recel":
            DP = 92
            BY = 69
            BX = 10

            self.setupmatchleds()
            if self.face == 'crazy_race':
                self.ui.label.setPixmap(QtGui.QPixmap(":/x/images/1x/crazy_race_480.png"))
                #self.ui.label.setStyleSheet("background-image: url(images/1x/crazy_race_480.png);")
            else:
                self.ui.label.setPixmap(QtGui.QPixmap(":/x/images/1x/fair_fight_480.png"))
                #self.ui.label.setStyleSheet("background-image: url(images/1x/fair_fight_480.png);")
                
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
            #self.ui.label.setStyleSheet("background-image: url(images/1x/pinballbell480.png);")
            self.ui.label.setPixmap(QtGui.QPixmap(":/x/images/1x/pinballbell480.png"))

        if self.game_type == "Gottlieb":
            self.swmRows, self.swmCols = (8, 5)
        else:
            self.swmRows, self.swmCols = (10, 4)

        self.Swtttext = [[None for x in range(self.swmCols)] for y in range(self.swmRows)]       

        if self.game_type == "Recel":
            self.Swtttext[0][0] = "Ball Home"
            self.Swtttext[8][0] = "Fault"
            self.Swtttext[8][1] = "Coin 3"
            self.Swtttext[8][2] = "Coin 1"
            self.Swtttext[8][3] = "Coin 2"
            self.Swtttext[9][0] = "Tilt"
            self.Swtttext[9][1] = "Replays"
            self.Swtttext[9][2] = "Button 2"
            self.Swtttext[9][3] = "Button 1"
            
            self.setupgpios()
            self.setupb2s()

        self.setupleds()

        self.setupnvram()
            
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
        
        self.ui.actionAbout_wiflip.triggered.connect(self.launchAbout)
        self.ui.actionHelp.triggered.connect(self.launchHelp)
        self.ui.actionSettings.triggered.connect(self.launchSettings)


        self.ui.menuFont_size.triggered.connect(self.changefontpt)


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
        
        
        #nvrams read/write
        self.ui.pb_rmem.clicked.connect(self.send_reqrread)
        self.ui.pb_flash.clicked.connect(self.send_reqflash)
        self.ui.pb_write_byte.clicked.connect(self.send_reqwrbyte)
        self.ui.pb_wmem.clicked.connect(self.send_reqwriteall)
        
        #switch simu
        self.ui.pushButton_sw.clicked.connect(self.send_reqswclose)
        

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

        #Reset the window settings on this event
        # QtCore.QObject.connect(self.ui.actionClear_all, 
        #                        QtCore.SIGNAL("triggered()"), 
        #                        self.clearSettin)
        self.ui.actionClear_all_2.triggered.connect(self.clearSettin)
        self.ui.actionFair_Fight.triggered.connect(self.actionFair_Fight)
        self.ui.actionCrazy_Race.triggered.connect(self.actionCrazy_Race)

        self.ui.actionSave_nvram.triggered.connect(self.actionSaveNvr)
        self.ui.actionLoad_nvr.triggered.connect(self.actionLoadNvr)

        self.ui.dockWidget_4.hide()
        self.ui.dockWidget_5.setEnabled(False)
        self.ui.dockWidget_6.hide()

    def changefontpt(self, action):

        
        sz = int(action.text())     

        for act in  self.ui.menuFont_size.actions():                 
            if act.text() == action.text():
                act.setChecked(True)
            else:
                act.setChecked(False)                 
        myfont   =  QtGui.QFont("Courier New", sz)
        
        self.settings.setValue('font-sz', str(sz))
        self.fontsz = sz
        
        fm = QFontMetrics(myfont)
        w = fm.boundingRect("0B0000").width()
        h = fm.boundingRect("0B0000").height()
    
        for i in range(16):
            for j in range(16):
                self.nibbleField[i][j].setFixedWidth(w+10)
                self.nibbleField[i][j].setFixedHeight(h+10)
                self.nibbleField[i][j].setFont(myfont)
            
            
    def actionSaveNvr(self):
        nvrfileStr = self.settings.value('nvrfileStr', None)
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                            "Save nvr data",
                                                            nvrfileStr,
                                                            "Nvr data (*.nvr)")
        

        if filename:
            self.settings.setValue("nvrfileStr", filename)
            #print (filename)
            #print(self.nvrlist)
            with open(filename, "w") as f:
                # write contents      
                for i in range(128):
                    val = self.nvrlist[i][1]
                    f.write(f"0X{i:02X}:0X{val:02X}"+os.linesep)      
            
        
    def actionLoadNvr(self):
        nvrfileStr = self.settings.value('nvrfileStr', None)
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load File",
                                       nvrfileStr,
                                       "NVR data file (*.nvr)")

        if filename:
            with open(filename, "r") as f:
                # read contents      
                lines = f.read().splitlines() 
                #print("lines", lines)
                for ln in lines:
                    mycod = ln.split(":")
                    if len(mycod) == 2:
                        #print(mycod)
                        try:
                            addr = int(mycod[0], 0)
                            byte = int(mycod[1], 0)
                        except:
                            addr = byte = -1
                        #print(addr, byte)
                        if addr >= 0 and addr <= 127 and byte >= 0 and byte <= 255:
                            lb = byte&0xF
                            hb = (byte&0xF0)>>4
                            r  = (addr//8)
                            l  = (addr%8)
                            #print(addr, r, l)
                            self.nvrlist[addr] = ( -1, byte)
                            self.nibbleField[r][2*l].setText(f"{lb:1X}")
                            self.nibbleField[r][2*l+1].setText(f"{hb:1X}")
                            self.nibbleField[r][2*l].setStyleSheet("background:rgb(120, 120, 120);color:rgb(255, 255, 255);")
                            self.nibbleField[r][2*l+1].setStyleSheet("background:rgb(120, 120, 120);color:rgb(255, 255, 255);")
                #print(self.nvrlist)      
                
    def launchAbout(self):
        """
        Starts the about dialog box
        """
        myabout=MyAbout(self)
        myabout.show()

    def launchHelp(self):
        """
        Starts the about dialog box
        """
        myhelp=MyHelp(self)
        myhelp.show()
                
    def launchSettings(self):
        """
        Starts the about dialog box
        """
        self.mysettings=MySettings(self)
        #self.mysettings.show()
        self.mysettings.exec()
                  
    def actionFair_Fight(self):
        #self.ui.label.setStyleSheet("background-image: url(images/1x/fair_fight_480.png);")
        self.ui.label.setPixmap(QtGui.QPixmap(":/x/images/1x/fair_fight_480.png"))
        self.face = 'fair_fight'
    def actionCrazy_Race(self):
        #self.ui.label.setStyleSheet("background-image: url(images/1x/crazy_race_480.png);")
        self.ui.label.setPixmap(QtGui.QPixmap(":/x/images/1x/crazy_race_480.png"))
        self.face = 'crazy_race'
        
    def clearSettin(self):
        """
        Called by a menu item of the menu bar
        Used to reset windowing to factory default
        """
        print("clearsettings")
        reply = QMessageBox.question(self, 
                                           'Please confirm',
                                           "You are about to clear your window settings. Are you sure ?", 
                                           QMessageBox.Yes | 
                                           QMessageBox.No, 
                                           QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.restoreGeometry(self.settings.value("MainWindow/default/geometry"))
            self.restoreState(self.settings.value("MainWindow/default/windowState"))
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.setValue("state", self.saveState())
            self.settings.sync()

        

    def send_reqswclose(self):
        try:
            strb = int(self.ui.lineEdit_swstrb.text(), 0)
        except:
            strb = 0
        strb = strb.to_bytes(1, byteorder='big')
        try:
            ret = int(self.ui.lineEdit_swret.text(), 0)
        except:
            ret = 0
        ret = ret.to_bytes(1, byteorder='big')
     
        print("message request is", b'YS'+strb+ret+ret)
        try:
            self.thread.sock.send(b'YS'+strb+ret+ret)
        except:
            pass
    
          
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
 
    def send_reqwriteall(self): 
        self.linenb = 0
        if   self.ui.rb_sysconf.isChecked():
            memtyp = 0
        elif self.ui.rb_mnprn.isChecked():
            memtyp = 2
        elif self.ui.rb_nvram.isChecked():
            memtyp = 1
        else:
            memtyp = 3
        print("global write to nvram", memtyp)

        for addr in range(128):
            init_byte = self.nvrlist[addr][0]
            byte      = self.nvrlist[addr][1]
            
            if byte != init_byte:
                #print("want to write", byte, "at address", addr)
                baddr = addr.to_bytes(1, byteorder='big')
                bbyt = byte.to_bytes(1, byteorder='big')

                print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)

                try:
                    self.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+baddr+bbyt)
                except:
                    pass
                
    def send_reqwrbyte(self):
        self.linenb = 0
        if   self.ui.rb_sysconf.isChecked():
            memtyp = 0
        elif self.ui.rb_mnprn.isChecked():
            memtyp = 2
        elif self.ui.rb_nvram.isChecked():
            memtyp = 1
        else:
            memtyp = 3
        
        try:
            addr = int(self.ui.lineEdit_addr.text(), 0)&0x7F
        except:
            addr = 0
        addr = addr.to_bytes(1, byteorder='big')
            
        try:
            mybyte = int(self.ui.lineEdit_byte.text(), 0)&0xFF
        except:
            mybyte = 0
        mybyte = mybyte.to_bytes(1, byteorder='big')
            
        print("message request is", b'YW'+memtyp.to_bytes(1, byteorder='big')+addr+mybyte)

        try:
            self.thread.sock.send(b'YW'+memtyp.to_bytes(1, byteorder='big')+addr+mybyte)
        except:
            pass
        
    def send_reqflash(self):
        self.linenb = 0
        if   self.ui.rb_sysconf.isChecked():
            memtyp = 0
        elif self.ui.rb_mnprn.isChecked():
            memtyp = 2
        elif self.ui.rb_nvram.isChecked():
            memtyp = 1
        else:
            memtyp = 3
            
        print("message request is", b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            self.thread.sock.send(b'YF'+memtyp.to_bytes(1, byteorder='big')+b'XX')
        except:
            pass
                
    def send_reqrread(self):    
        self.linenb = 0
        if   self.ui.rb_sysconf.isChecked():
            memtyp = 0
        elif self.ui.rb_mnprn.isChecked():
            memtyp = 2
        elif self.ui.rb_nvram.isChecked():
            memtyp = 1
        else:
            memtyp = 3
            
        print("message request is", b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')

        try:
            self.thread.sock.send(b'YR'+memtyp.to_bytes(1, byteorder='big')+b'XX')
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
            if   self.ui.rb_sysconf.isChecked():
                memtyp = "sys conf"
            elif self.ui.rb_mnprn.isChecked():
                memtyp = "miniprinter"
            elif self.ui.rb_nvram.isChecked():
                memtyp = "nvram live"
            else:
                memtyp = "unknown source"

            print(f"Dump RAM {memtyp} in progress")
            self.write2Console(f"NVRAM Current ({memtyp})\r\n", insertMode=True)

            #write into memory inspection area            
            for r in range(16):
                for l in range(8):
                    lb = data[r*8+l]&0xF
                    hb = data[r*8+l]&0xF0
                    hb = hb>>4
                    self.nibbleField[r][2*l].setText(f"0X{lb:01X}")
                    self.nibbleField[r][2*l].setStyleSheet("background:rgb(21, 120, 34);color:rgb(255, 255, 255);")
                    self.nibbleField[r][2*l+1].setText(f"0X{hb:01X}")
                    self.nibbleField[r][2*l+1].setStyleSheet("background:rgb(21, 120, 34);color:rgb(255, 255, 255);")

                    self.nvrlist[r*8+l] = (data[r*8+l], data[r*8+l]) #(init value, current value)
                    
            #write again but  to  console, this time.        
            for r in range(8):
                self.write2Console(f"{r:02X}\t")
                for l in range(16):
                    self.write2Console(f"{data[r*16+l]:02X} ", insertMode=True)
                self.write2Console(f"\r\n", insertMode=True)
            
            print("Dump RAM terminated")
            try:
                self.mysettings.statusCmd.emit(82, "done")   
            except:
                pass     
            
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
            #print("Y got", data[0], data[1], data[2], data[3], data[4], io_os, io_is)
            self.ui.label_out.setText(f"{io_os:016b}")
            self.ui.label_inp.setText(f"{io_is:016b}")
            
            self.ui.lcdNumber.setProperty("value", data[4]&0x0F)
            
            for i in range(24):
                byten = 6 - (i // 8)
                if data[byten]&(1<<(i%8)):
                    self.gpioled[i].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                else:
                    self.gpioled[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))

            for i in range(16):
                byten = 8 - (i // 8)
                if data[byten]&(1<<(i%8)):
                    self.b2led[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                else:
                    self.b2led[i].setPixmap(QtGui.QPixmap(":/x/ledon.png"))
                    

            # if data[4]&0x01:
            #     self.ui.label_bonus1.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
            # else:
            #     self.ui.label_bonus1.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            # if data[4]&0x02:
            #     self.ui.label_bonus2.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
            # else:
            #     self.ui.label_bonus2.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            # if data[4]&0x04:
            #     self.ui.label_bonus4.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
            # else:
            #     self.ui.label_bonus4.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            # if data[4]&0x08:
            #     self.ui.label_bonus8.setPixmap(QtGui.QPixmap(":/x/ledon.png"))
            # else:
            #     self.ui.label_bonus8.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
                
                
                
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
                    c = cols-1 - i%cols
                    r = bytenumber*2
                    if bitnumber<4:
                        r+=1
                    #print(i, bitnumber, bytenumber, r,c)
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
        self.settings.setValue('face', self.face)

        # Finally we pass the event to the class we inherit from. It can choose to accept or reject the event, but we don't need to deal with it ourselves
        super(MainForm, self).closeEvent(event)


    def magarzolerie(self, i, j):
        '''
        slot for handling signal textchanged in nibbleField
        which is changing color to red
        '''
        #print("zobi", i, j)
        try:
            mynibble   = int(self.nibbleField[i][j].text(), 0)
        except:
            try:
                mynibble = int("0x"+self.nibbleField[i][j].text(), 16)
            except:
                mynibble = -1

        if mynibble != mynibble&0xF:
            badentry = True
            mynibble = 0
        else:
            badentry =  False    
        #print("mynibble", mynibble)    
        pnibblenum = i*16+j
        pbytenum   = pnibblenum//2
        
        #modify current ([1])
        if pnibblenum%2:
            #this is a hi nibble
            mynewbyte = (mynibble<<4) + (self.nvrlist[pbytenum][1] & 0x0F)
            self.nvrlist[pbytenum] = (self.nvrlist[pbytenum][0], mynewbyte)
        else:
            #this is a lo nibble
            mynewbyte = mynibble    + (self.nvrlist[pbytenum][1] & 0xF0)
            self.nvrlist[pbytenum] = (self.nvrlist[pbytenum][0], mynewbyte)

        if badentry == True:
            self.nibbleField[i][j].setStyleSheet("background:rgb(160, 160, 10);color:rgb(255, 255, 255);")
            self.nibbleField[i][j].setToolTip("Bad entry. Will take it as 0")
        elif self.nvrlist[pbytenum][1] == self.nvrlist[pbytenum][0]:            
            self.nibbleField[i][j].setStyleSheet("background:rgb(22, 140, 35);color:rgb(255, 255, 255);")
            self.nibbleField[i][j].setToolTip("Nibble OK")
        else:
            self.nibbleField[i][j].setStyleSheet("background:rgb(140, 34, 35);color:rgb(255, 255, 255);")
            self.nibbleField[i][j].setToolTip("Nibble OK")
            

    def setupb2s(self):
        self.b2led = [0]*16
        self.b2tooltip = [
            "L/51",   #IO-0
            "L/52",   #IO-1
            "L/54",   #IO-2
            "L/58",   #IO-3
            "L/41",   #IO-4
            "L/42",   #IO-5
            "L/44",   #IO-6
            "L/48",   #IO-7
            "L/31",   #IO-8
            "L/32",   #IO-9
            "L/34",   #IO-10
            "L/38",   #IO-11
            "L/21",   #IO-12
            "L/22",   #IO-13
            "L/24",   #IO-14
            "L/28",   #IO-15
            ]

        for i in range(16):
            self.b2led[i]=QtWidgets.QLabel(self.ui.groupBox_7)
            #self.gpioled[i].setGeometry(QtCore.QRect(60+i*28, 90, 20, 20))
            self.b2led[i].setText("")
            self.b2led[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            self.ui.horizontalLayout_16.addWidget(self.b2led[i])
            self.b2led[i].setMaximumSize(QtCore.QSize(31, 31))
            self.b2led[i].setScaledContents(True)
            self.b2led[i].setObjectName(f"b2led_{i}")
            #self.gpioled[i].mousePressEvent = lambda _, x=i, y=j : self.foo(x, y)
            try:
                self.b2led[i].setToolTip(self.b2tooltip[i])
            except:
                self.b2led[i].setToolTip(f"b2led_{i}")
        
        
    def setupgpios(self):
        self.gpioled = [0]*24
        self.gpiotooltip = [
            "C/#F",  #0     group 3-1
            "C/#E",  #1     group 3-2
            "C/#D",  #2     group 3-4
            "C/#C",  #3     group 3-8
            
            "C/#B",  #4     group 4-1
            "C/#A",  #5     group 4-2
            "C/#9",  #6     group 4-4
            "C/#8",  #7     group 4-8
            
            "C/#7",  #8     group 5-1
            "C/#6 (knocker)",  #9     group 5-2
            "NC",    #10     group 5-4
            "Sound-100K",    #11     group 5-8
            
            "Sound-10K",     #12     group 6-1
            "Sound-1K",      #13     group 6-2
            "Sound-100",     #14     group 6-4
            "Sound-10",      #15     group 6-8
            
            "L/61 (bonus)",  #16    group 7-1
            "L/62 (bonus)",  #17    group 7-2
            "L/64 (bonus)",  #18    group 7-4
            "L/68 (bonus)",  #19    group 7-8
            
            "L/71",   #20    group 8-1
            "L/72",   #21    group 8-2
            "L/74",   #22    group 8-4
            "PLAY SIGNAL",   #23    group 8-8
            
            ]
        
        for i in range(24):
            self.gpioled[i]=QtWidgets.QLabel(self.ui.groupBox_5)
            #self.gpioled[i].setGeometry(QtCore.QRect(60+i*28, 90, 20, 20))
            self.gpioled[i].setText("")
            self.gpioled[i].setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
            self.ui.horizontalLayout_13.addWidget(self.gpioled[i])
            self.gpioled[i].setMaximumSize(QtCore.QSize(31, 31))
            self.gpioled[i].setScaledContents(True)
            self.gpioled[i].setObjectName(f"gpioled_{i}")
            #self.gpioled[i].mousePressEvent = lambda _, x=i, y=j : self.foo(x, y)
            try:
                self.gpioled[i].setToolTip(self.gpiotooltip[i])
            except:
                self.gpioled[i].setToolTip(f"gpioled_{i+1}")

               
    def setupnvram(self):
        self.nibbleField = [0]*16
        myfont   =  QtGui.QFont("Courier New", self.fontsz)
        
        myfont10 =  QtGui.QFont("Courier New", 10)
        fm = QFontMetrics(myfont)
        w = fm.boundingRect("0B0000").width()
        
        for i in range(16):
            etiq=QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
            etiq.setText(f"{i:02X}")
            etiq.setObjectName(f"SRlab_{i}")
            #etiq.setStyleSheet("text-align:center;")
            etiq.setAlignment(Qt.AlignCenter)
            etiq.setFont(myfont)
            self.ui.gridLayout_7.addWidget(etiq, 0, i+1, 1, 1)
            

        for i in range(16):
            etiq=QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
            etiq.setText(f"{i:02X}")
            etiq.setObjectName(f"RRlab_{i}")
            #etiq.setStyleSheet("text-align:center;")
            etiq.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            etiq.setFont(myfont)
            self.ui.gridLayout_7.addWidget(etiq, i+1, 0, 1, 1)

        # for i in range(cols):
        #     rled=QtWidgets.QLabel(self.ui.groupBox)
        #     rled.setGeometry(QtCore.QRect(60-28, 90+i*36, 20, 20))
        #     rled.setText(f"R{i}")
        #     rled.setObjectName(f"rled_{i}")

        self.nvrlist = [(0, 0)]*128        

        for i in range(16):
            self.nibbleField[i] = [0]*16
            for j in range(16):
                self.nibbleField[i][j] = QtWidgets.QLineEdit(self.ui.scrollAreaWidgetContents)
                self.nibbleField[i][j].setObjectName(f"nibbles_{i}{j}")
                #self.nibbleField[i][j].setGeometry(QtCore.QRect(60+i*28, 90+j*36, 20, 20))
                self.nibbleField[i][j].setText("0")
                self.nibbleField[i][j].setStyleSheet("background:rgb(120, 120, 120);color:rgb(255, 255, 255);")
                self.nibbleField[i][j].setAlignment(Qt.AlignCenter)
                self.nibbleField[i][j].setFont(myfont)

                self.nibbleField[i][j].setFixedWidth(w+10)
                self.ui.gridLayout_7.addWidget(self.nibbleField[i][j], i+1, j+1, 1, 1)
                self.nibbleField[i][j].textChanged.connect(partial(self.magarzolerie, i, j))

                #self.nibbleField[i][j].setTextMargins (left, top, right, bottom)
                self.nibbleField[i][j].setTextMargins (1, 3, 1, 3)

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
            rled.setText(f"R{chr(i+0x41)}")
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
                self.led[i][j].mousePressEvent = lambda _, x=i, y=j : self.foo(x, y)
                self.led[i][j].setToolTip(self.Swtttext[i][j])


        # print (self.led)
        # for i in range(8):
        #     for j in range(5):
        #         if i%2 and j%2:
        #             self.led[i][j].setPixmap(QtGui.QPixmap(":/x/ledon.png"))


    def foo(self, i, j):
        strb = i.to_bytes(1, byteorder='big')
        ret  = (1<<j).to_bytes(1, byteorder='big')

        print("message request is", b'YS'+strb+ret+ret)
        try:
            self.thread.sock.send(b'YS'+strb+ret+ret)
        except:
            pass
   
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
            elif received == b'Y':   #IO status 7 bytes Oh, Ol, Ih, Il gpioEF, gpioCD, gpioAB
                framesz = 9
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
                # if received == b'R':
                #     print(received, msg)
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
