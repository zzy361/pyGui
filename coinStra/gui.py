import wx
import winmax_api_v02 as wmapi
import time
from CoinStrategy import *


wmex = wmapi.winmax_api("","")        
        
class  PanelTwo(wx.Panel):
    def __init__(self, parent,sendsignal):
        self.themeColor = (200,0,0)
        enter_font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        font = wx.Font(14, wx.ROMAN,wx.ITALIC,wx.FONTWEIGHT_BOLD)
        self.para = [0,0,0,0,0]
        self.sendsignal = sendsignal
        wx.Panel.__init__(self, parent)
        
        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        self.logger = wx.TextCtrl(self, pos=(300, 20), size=(470, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # A button
        self.button1 = wx.Button(self, label=u"开始运行", pos=(60, 280))
        self.Bind(wx.EVT_BUTTON, self.raiseStra, self.button1)
        self.button1 .SetForegroundColour('white')
        self.button1 .SetBackgroundColour(self.themeColor)
        
        
        self.button2 = wx.Button(self, label=u"停止运行", pos=(180, 280))
        self.Bind(wx.EVT_BUTTON, self.stopStra, self.button2)
        self.button2 .SetForegroundColour('white')
        self.button2 .SetBackgroundColour(self.themeColor)

        self.lblhear = wx.StaticText(self, label=u"选择币种：", pos=(20, 20))
        self.lblhear.SetForegroundColour(self.themeColor)
        self.lblhear.SetFont(font)
        
        self.sampleList = [u'BTC', u'ETH',u'WKT']
        self.edithear = wx.ComboBox(self, pos=(150, 20), size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
        
        
        self.lblname1 = wx.StaticText(self, label=u"入场点:", pos=(20, 60))
        self.lblname1.SetForegroundColour(self.themeColor)
        self.lblname1.SetFont(font)
        
        self.editname1 = wx.TextCtrl(self, pos=(150, 60), size=(140, -1))
        self.editname1.SetForegroundColour('gray')
        self.editname1.SetFont(enter_font)
        self.Bind(wx.EVT_TEXT, self.EvtText1, self.editname1)

        self.lblname2 = wx.StaticText(self, label=u"出场点:", pos=(20, 100))
        self.lblname2.SetForegroundColour(self.themeColor)
        self.lblname2.SetFont(font)
        self.editname2 = wx.TextCtrl(self, pos=(150, 100), size=(140, -1))
        self.editname2.SetForegroundColour('gray')
        self.editname2.SetFont(enter_font)
        self.Bind(wx.EVT_TEXT, self.EvtText2, self.editname2)
        
        self.lblname3 = wx.StaticText(self, label=u"单笔交易量:", pos=(20, 140))
        self.lblname3.SetForegroundColour(self.themeColor)
        self.lblname3.SetFont(font)
        self.editname3 = wx.TextCtrl(self, pos=(150, 140), size=(140, -1))
        self.editname3.SetForegroundColour('gray')
        self.editname3.SetFont(enter_font)
        self.Bind(wx.EVT_TEXT, self.EvtText3, self.editname3)
        
        self.lblname4 = wx.StaticText(self, label=u"止损(%):", pos=(20, 180))
        self.lblname4.SetForegroundColour(self.themeColor)
        self.lblname4.SetFont(font)
        self.editname4 = wx.TextCtrl(self, pos=(150, 180), size=(140, -1))
        self.editname4.SetForegroundColour('gray')
        self.editname4.SetFont(enter_font)
        self.Bind(wx.EVT_TEXT, self.EvtText4, self.editname4)
        
        self.lblname5 = wx.StaticText(self, label=u"止赢(%):", pos=(20, 220))
        self.lblname5.SetForegroundColour(self.themeColor)
        self.lblname5.SetFont(font)
        self.editname5 = wx.TextCtrl(self, pos=(150, 220), size=(140, -1))
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
        if float(event.GetString()) <= 50 and float(event.GetString()) >= 1:
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
        self.coin_name = 'ETH'
        if event.GetString() == u'BTC':
            self.coin_name = 'BTC'
        elif event.GetString() == u'ETH':
            self.coin_name = 'ETH'
        elif event.GetString() == u'WKT':
            self.coin_name = 'WKT'

    def raiseStra(self, event):
        print(self.coin_name,self.para,wmex,self.logger,self.sendsignal)
        self.stra = CoinStrategy(self.coin_name,self.para,wmex,self.logger,self.sendsignal)
        self.stra.start()

    def stopStra(self, event):
        try:
            self.stra.stop()
            del self.stra
        except:
            wx.MessageBox(u"输入错误", "Error" ,wx.OK | wx.ICON_ERROR)

class PanelOne(wx.Panel):
    def __init__(self, parent,function):
        self.parent = parent
        self.function = function
        wx.Panel.__init__(self, parent)
        
        enter_font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        self.themeColor = (200,0,0)
        #font = wx.Font(14, wx.DEFAULT, wx.BOLD, wx.NORMAL, True)
        font = wx.Font(14, wx.ROMAN,wx.ITALIC,wx.FONTWEIGHT_BOLD)
        accountLabel = wx.StaticText(self, -1, u'账号', pos=(200, 90))
        accountLabel.SetForegroundColour(self.themeColor)
        accountLabel.SetFont(font)

        self.accountInput = wx.TextCtrl(self, -1, u'', pos=(280, 90), size=(180, -1))
        self.accountInput.SetForegroundColour('gray')
        self.accountInput.SetFont(enter_font)

        passwordLabel = wx.StaticText(self, -1, u'密码', pos=(200, 160))
        passwordLabel.SetFont(font)
        passwordLabel.SetForegroundColour(self.themeColor)

        self.passwordInput = wx.TextCtrl(self, -1, u'', pos=(280, 160), size=(180, -1), style=wx.TE_PASSWORD)
        self.passwordInput.SetForegroundColour('gray')
        self.passwordInput.SetFont(enter_font)

        sureButton = wx.Button(self, -1, u'登录', pos=(400, 250), size=(180, 60))
        sureButton.SetForegroundColour('white')
        sureButton.SetBackgroundColour(self.themeColor)
        # 为【确定Button】绑定事件
        self.Bind(wx.EVT_BUTTON, self.sureEvent, sureButton)


    def sureEvent(self, event):
        global wmex
        account = self.accountInput.GetValue()
        password = self.passwordInput.GetValue()
        wmex = wmapi.winmax_api(account,password)
        info = wmex.account_info()
        if info == None:
            wx.MessageBox(u"密码错误，或帐号不存在", "Error" ,wx.OK | wx.ICON_ERROR)
        else:
            self.function(event)


########################################################################
class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,u'数字货币自动交易工具',size=(800,400))
        
        self.panel_one = PanelOne(self,self.onSwitchPanels)
        self.panel_two = PanelTwo(self,self.signal)
        self.panel_two.Hide()
        
                # the combobox Control
        self.statusbar = self.CreateStatusBar()
#        #将状态栏分割为3个区域,比例为1:2:3
#        self.statusbar.SetFieldsCount(3)
#        self.statusbar.SetStatusWidths([-1, -2, -3])
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

    #----------------------------------------------------------------------
    def onSwitchPanels(self, event):
        """"""
        if self.panel_one.IsShown():
            self.SetTitle(u"数字货币自动交易工具")
            self.panel_one.Hide()
            self.panel_two.Show()
            self.Layout()
            time.sleep(30)
            self.panel_one.Show()
            self.panel_two.Hide()
        self.Layout()
        
    def signal(self):
        t = time.localtime(time.time()) 
        StrYMDt = time.strftime("%Y-%m-%d %H:%M", t) 
        self.SetStatusText(u'程序最新运行时间：'+StrYMDt,0)

# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()