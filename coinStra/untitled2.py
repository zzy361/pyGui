import wx
import time
import api.OkcoinSpotAPI as okapi
import api.winmax_api_v02 as wmapi
import api.zhongbi_api as zbapi
import api.huobi_api as hbapi
from CoinStrategy import *

class  stragety1(wx.Panel):
    def __init__(self, parent,returnF,sendsignal):
        self.themeColor = (200,0,0)
        enter_font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        font = wx.Font(14, wx.ROMAN,wx.ITALIC,wx.FONTWEIGHT_BOLD)
        self.para = [10,90,0.01,0.1,0.1]
        self.sendsignal = sendsignal
        self.returnF = returnF
        wx.Panel.__init__(self, parent)
        
        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        self.logger = wx.TextCtrl(self, pos=(300, 20), size=(470, 250), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # A button
        self.button1 = wx.Button(self, label=u"开始运行", pos=(60, 280))
        self.Bind(wx.EVT_BUTTON, self.raiseStra, self.button1)
        self.button1 .SetForegroundColour('white')
        self.button1 .SetBackgroundColour(self.themeColor)
        
        
        self.button2 = wx.Button(self, label=u"停止运行", pos=(180, 280))
        self.Bind(wx.EVT_BUTTON, self.stopStra, self.button2)
        self.button2 .SetForegroundColour('white')
        self.button2 .SetBackgroundColour(self.themeColor)

        self.button3 = wx.Button(self, label="return", pos=(600, 280))
        self.Bind(wx.EVT_BUTTON, self.reToChoose, self.button3)
        self.button3 .SetForegroundColour('white')
        self.button3 .SetBackgroundColour(self.themeColor)

        self.lblhear = wx.StaticText(self, label=u"选择币种：", pos=(20, 20))
        self.lblhear.SetForegroundColour(self.themeColor)
        self.lblhear.SetFont(font)
        
        self.sampleList = [u'BTC', u'ETH',u'WKT']
        self.coin_name = 'BTC'
        self.edithear = wx.ComboBox(self,value = 'BTC', pos=(150, 20), size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
        
        
        self.lblname1 = wx.StaticText(self, label=u"入场点:", pos=(20, 60))
        self.lblname1.SetForegroundColour(self.themeColor)
        self.lblname1.SetFont(font)
        
        self.editname1 = wx.TextCtrl(self,value='10', pos=(150, 60), size=(140, -1))
        self.editname1.SetForegroundColour('gray')
        self.editname1.SetFont(enter_font)
        self.Bind(wx.EVT_TEXT, self.EvtText1, self.editname1)

        self.lblname2 = wx.StaticText(self, label=u"出场点:", pos=(20, 100))
        self.lblname2.SetForegroundColour(self.themeColor)
        self.lblname2.SetFont(font)
        self.editname2 = wx.TextCtrl(self,value='90', pos=(150, 100), size=(140, -1))
        self.editname2.SetForegroundColour('gray')
        self.editname2.SetFont(enter_font)
        self.Bind(wx.EVT_TEXT, self.EvtText2, self.editname2)
        
        self.lblname3 = wx.StaticText(self, label=u"单笔交易量:", pos=(20, 140))
        self.lblname3.SetForegroundColour(self.themeColor)
        self.lblname3.SetFont(font)
        self.editname3 = wx.TextCtrl(self,value='0.01', pos=(150, 140), size=(140, -1))
        self.editname3.SetForegroundColour('gray')
        self.editname3.SetFont(enter_font)
        self.Bind(wx.EVT_TEXT, self.EvtText3, self.editname3)
        
        self.lblname4 = wx.StaticText(self, label=u"止损:", pos=(20, 180))
        self.lblname4.SetForegroundColour(self.themeColor)
        self.lblname4.SetFont(font)
        self.editname4 = wx.TextCtrl(self,value='0.1', pos=(150, 180), size=(140, -1))
        self.editname4.SetForegroundColour('gray')
        self.editname4.SetFont(enter_font)
        self.Bind(wx.EVT_TEXT, self.EvtText4, self.editname4)
        
        self.lblname5 = wx.StaticText(self, label=u"止赢:", pos=(20, 220))
        self.lblname5.SetForegroundColour(self.themeColor)
        self.lblname5.SetFont(font)
        self.editname5 = wx.TextCtrl(self,value='0.1', pos=(150, 220), size=(140, -1))
        self.editname5.SetForegroundColour('gray')
        self.editname5.SetFont(enter_font)
        self.Bind(wx.EVT_TEXT, self.EvtText5, self.editname5)
    
    def EvtText1(self, event):
        if float(event.GetString()) <= 50 and float(event.GetString()) >= 1:
            self.para[0] = float(event.GetString())
        else:
            wx.MessageBox(u"输入错误", "Error" ,wx.OK | wx.ICON_ERROR)
            
    def EvtText2(self, event):
        if float(event.GetString()) <= 100:
            self.para[1] = float(event.GetString())
        else:
            wx.MessageBox(u"输入错误", "Error" ,wx.OK | wx.ICON_ERROR)
            
    def EvtText3(self, event):
        if float(event.GetString()) <= 1:
            self.para[2] = float(event.GetString())
        else:
            wx.MessageBox(u"输入错误", "Error" ,wx.OK | wx.ICON_ERROR)
            
    def EvtText4(self, event):
        if float(event.GetString()) <= 1:
            self.para[3] = float(event.GetString())
        else:
            wx.MessageBox(u"输入错误", "Error" ,wx.OK | wx.ICON_ERROR)
    
    def EvtText5(self, event):
        if float(event.GetString()) <= 1:
            self.para[4] = float(event.GetString())
        else:
            wx.MessageBox(u"输入错误", "Error" ,wx.OK | wx.ICON_ERROR)
    
    def EvtComboBox(self, event):
        if event.GetString() == u'BTC':
            self.coin_name = 'BTC'
        elif event.GetString() == u'ETH':
            self.coin_name = 'ETH'
        elif event.GetString() == u'WKT':
            self.coin_name = 'WKT'

    def reToChoose(self,event):
        self.returnF(event)

    def raiseStra(self, event):
        global mapi
        print(self.coin_name,self.para,mapi,self.logger,self.sendsignal)
        self.stra = CoinStrategy(self.coin_name,self.para,mapi,self.logger,self.sendsignal)
        self.stra.start()

    def stopStra(self, event):
        try:
            self.stra.stop()
            del self.stra
            self.logger.AppendText('程序已经停止\n')
        except:
            wx.MessageBox(u"输入错误", "Error" ,wx.OK | wx.ICON_ERROR)
            
class  stragety2(stragety1):
    pass

class  stragety3(stragety1):
    pass    
    
class  chooseStragety(wx.Panel):
    def __init__(self, parent,function):
        self.themeColor = (200,0,0)

        wx.Panel.__init__(self, parent)
        self.function = function
        # A button
        self.button1 = wx.Button(self, label="Strategy1", pos=(80, 40),size = (140,70))
        self.Bind(wx.EVT_BUTTON, self.tranStrategy1, self.button1)
        self.button1 .SetForegroundColour('white')
        self.button1 .SetBackgroundColour(self.themeColor)
        txt = '说明1WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
        Label1 = wx.StaticText(self, -1, txt, pos=(280, 50),size = (400,120))
        
        self.button2 = wx.Button(self, label="Strategy2", pos=(80, 140),size = (140,70))
        self.Bind(wx.EVT_BUTTON, self.tranStrategy2, self.button2)
        self.button2 .SetForegroundColour('white')
        self.button2 .SetBackgroundColour(self.themeColor)
        txt = '说明2SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS'
        Label2 = wx.StaticText(self, -1, txt, pos=(280, 150),size = (400,120))
        
        self.button3 = wx.Button(self, label="Strategy3", pos=(80, 240),size = (140,70))
        self.Bind(wx.EVT_BUTTON, self.tranStrategy3, self.button3)
        self.button3 .SetForegroundColour('white')
        self.button3 .SetBackgroundColour(self.themeColor)
        
        txt = '说明3XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        Label3 = wx.StaticText(self, -1, txt, pos=(280, 250),size = (400,120))
        
    def tranStrategy1(self, event):
        self.function(event,1)
            
    def tranStrategy2(self, event):
        self.function(event,2)
        
    def tranStrategy3(self, event):
        self.function(event,3)
        
class Login(wx.Panel):
    def __init__(self, parent,function):
        self.parent = parent
        self.function = function
        wx.Panel.__init__(self, parent)
        
        enter_font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        self.themeColor = (200,0,0)
        #font = wx.Font(14, wx.DEFAULT, wx.BOLD, wx.NORMAL, True)
        font = wx.Font(14, wx.ROMAN,wx.ITALIC,wx.FONTWEIGHT_BOLD)
        exchangeLabel = wx.StaticText(self, -1, 'exchange', pos=(180, 50))
        exchangeLabel.SetForegroundColour(self.themeColor)
        exchangeLabel.SetFont(font)

        self.exchangeInput = wx.TextCtrl(self, -1, 'winmax', pos=(300, 50), size=(180, -1))
        self.exchangeInput.SetForegroundColour('gray')
        self.exchangeInput.SetFont(enter_font)
        
        accountLabel = wx.StaticText(self, -1, 'api_key', pos=(180, 120))
        accountLabel.SetForegroundColour(self.themeColor)
        accountLabel.SetFont(font)

        self.accountInput = wx.TextCtrl(self, -1, '', pos=(300, 120), size=(180, -1))
        self.accountInput.SetForegroundColour('gray')
        self.accountInput.SetFont(enter_font)

        passwordLabel = wx.StaticText(self, -1, 'sercet_key', pos=(180, 190))
        passwordLabel.SetFont(font)
        passwordLabel.SetForegroundColour(self.themeColor)

        self.passwordInput = wx.TextCtrl(self, -1, '', pos=(300, 190), size=(180, -1), style=wx.TE_PASSWORD)
        self.passwordInput.SetForegroundColour('gray')
        self.passwordInput.SetFont(enter_font)

        sureButton = wx.Button(self, -1, 'login', pos=(400, 250), size=(180, 60))
        sureButton.SetForegroundColour('white')
        sureButton.SetBackgroundColour(self.themeColor)
        # 为【确定Button】绑定事件
        self.Bind(wx.EVT_BUTTON, self.sureEvent, sureButton)


    def sureEvent(self, event):
        exchange = self.exchangeInput.GetValue()
        account = self.accountInput.GetValue()
        password = self.passwordInput.GetValue()
        if exchange == 'winmax':
            self.mapi = wmapi.winmax_api(account,password)
        elif exchange == 'okex':
            self.mapi = okapi.OKCoinSpot(account,password)
        elif exchange == 'zhongbi':
            self.mapi = zbapi.zb_api(account,password)
        elif exchange == 'huobi':
            self.mapi = hbapi.huobi_api(account,password)
        else:
            wx.MessageBox('there is no such exchange', 'Error' ,wx.OK | wx.ICON_ERROR)
            return
        
        global mapi
        mapi = self.mapi
           
        info = self.mapi.account_info()
        if info == None:
            wx.MessageBox('wrong password or wrong account', 'Error' ,wx.OK | wx.ICON_ERROR)
        else:
            self.function(event)


class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,'trade tool',size=(800,400))
        
        self.panel_login = Login(self,self.onReturnToChooseStragety)
        self.panel_chooseStrategy = chooseStragety(self,self.onSwitchStragety)
        self.panel_StragetyOne = stragety1(self,self.onReturnToChooseStragety,self.signal)
        self.panel_StragetyTwo = stragety2(self,self.onReturnToChooseStragety,self.signal)
        self.panel_StragetyThree = stragety3(self,self.onReturnToChooseStragety,self.signal)
        self.panel_chooseStrategy.Hide()
        self.panel_StragetyOne.Hide()
        self.panel_StragetyTwo.Hide()
        self.panel_StragetyThree.Hide()
        
# 		 the combobox Control
        self.statusbar = self.CreateStatusBar()
#        将状态栏分割为3个区域,比例为1:2:3
#        self.statusbar.SetFieldsCount(3)
#        self.statusbar.SetStatusWidths([-1, -2, -3])
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_login, 1, wx.EXPAND)
        self.sizer.Add(self.panel_chooseStrategy, 1, wx.EXPAND)
        self.sizer.Add(self.panel_StragetyOne, 1, wx.EXPAND)
        self.sizer.Add(self.panel_StragetyTwo, 1, wx.EXPAND)
        self.sizer.Add(self.panel_StragetyThree, 1, wx.EXPAND)

        self.SetSizer(self.sizer)

    def onReturnToChooseStragety(self, event):
        self.SetTitle('Choose_Stragety')
        if self.panel_login.IsShown():
            self.panel_login.Hide()
        elif self.panel_StragetyOne.IsShown():
        	self.panel_StragetyOne.Hide()
        elif self.panel_StragetyTwo.IsShown():
        	self.panel_StragetyTwo.Hide()
        elif self.panel_StragetyThree.IsShown():
        	self.panel_StragetyThree.Hide()
            
        self.panel_chooseStrategy.Show()
        self.Layout()

    def onSwitchStragety(self,event,stragetyNo):
    	self.panel_chooseStrategy.Hide()
    	if stragetyNo == 1:
            self.SetTitle('Stragety1')
            self.panel_StragetyOne.Show()
    	elif stragetyNo == 2:
            self.SetTitle('Stragety2')
            self.panel_StragetyTwo.Show()
    	elif stragetyNo == 3:
            self.SetTitle('Stragety3')
            self.panel_StragetyThree.Show()
    	self.Layout()

    def signal(self):
        t = time.localtime(time.time()) 
        StrYMDt = time.strftime("%Y-%m-%d %H:%M", t) 
        self.SetStatusText('last running time is '+StrYMDt,0)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()