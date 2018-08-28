import wx
import winmax_api_v02 as wmapi
import time


class MyFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(


class MyFrame2(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(

class MyApp(wx.App):
  def OnInit(self):
    self.myframe = MyFrame()
    self.myframe2 = MyFrame2()
    self.SetTopWindow(self.myframe)
    self.myframe.Show(True)
    self.myframe2.Show(True)
    return True

if __name__=='__main__':
  app = MyApp(0)
  app.MainLoop()