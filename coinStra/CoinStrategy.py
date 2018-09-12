import pandas as pd
import time
import numpy as np
import multi_threading as mt

class CoinStrategy():
    def __init__(self,coin_name,para,wmex,logger,sendsignal):
        self.coin_name = coin_name
        self.exCoin = 'UDC_'+coin_name.upper()
        self.wmex = wmex
        self.logger = logger
        self.wm_currency = 'UDC'
        self.status = 'out'
        self.initStra()
        self.sendsignal = sendsignal
        self.ison =True
        
        self.sendsignal()
        self.trethold_buy = para[0]
        self.trethold_sell = para[1]
        self.vol = para[2]
        self.stoploss = para[3]
        self.stopprofit = para[4]
        self.volreal = 0
        
    def initStra(self):
        self.f90 = self.f88 = 0.0
        self.f0 = self.v4 = self.v8 = self.vC = self.v10 = self.v14 = self.v18 = self.v20 = 0.0
        self.f8 = self.f10 = self.f18 = self.f20 = self.f28 = self.f30 = self.f38 = self.f48 = self.v1C = 0.0
        self.f50 = self.f58 = self.f60 = self.f68 = self.f70 = self.f78 = self.f80 = self.f40 = 0.0
        
        info = self.wmex.account_info()
        last_coin_balence = info[self.coin_name.upper()]['available'] + info[self.coin_name.upper()]['lock']
        last_currency_balence = info[self.wm_currency]['available'] + info[self.wm_currency]['lock']
        self.printout('现有UDC'+str(last_currency_balence)+',有'+self.coin_name+str(last_coin_balence))
        self.fillPriceList()
        self.printout('初始化完毕')
    
    def lookingforout(self):
        while self.status == 'in':
            res = self.wmex.get_depth(self.exCoin)
            bid1 = res['buy'][0][0]
            ask1 = res['sell'][0][0]
            if bid1/self.buyprice < 1 - self.stoploss:
                self.printout('止损出场')
                self.closePosition(bid1)
                self.printout('本次收益为'+str(self.closeprice/self.buyprice - 1))
                self.status = 'out'
            elif ask1/self.buyprice > 1 +self.stopprofit:
                self.printout('止赢出场')
                self.closePosition(ask1)
                self.printout('本次收益为'+str(self.closeprice/self.buyprice - 1))
                self.status = 'out'
            time.sleep(10)
            
    def openPosition(self):
        OrderId = self.wmex.limit_order(self.exCoin,round(self.pricelist.close.iloc[-1]*1.2,4),round(self.vol,4),'BUY')
        i = 5
        while True:
            i = i - 1
            time.sleep(1)
            report = self.wmex.check_order(OrderId)
            if report['tradeCoinStatus'] == 'SUCCESS':
                self.volreal = self.vol
                self.buyprice = report['matchedMoney']/report['tradedNumber']
                self.printout('用均价'+str(self.buyprice)+'做多'+str(self.vol)+'个币')
                break
            elif i == 0:
                self.wmex.order_cancel(OrderId)
                self.volreal = report['tradedNumber']
                self.buyprice = report['matchedMoney']/report['tradedNumber']
                self.printout('用均价'+str(self.buyprice)+'做多'+str(self.volreal)+'个币')
                break
            
    def closePosition(self,price):
        OrderId = self.wmex.limit_order(self.exCoin,round(price*0.8,4),round(self.volreal,4),'sell')
        i = 1
        allprice = 0
        vol = 0
        while True:
            i = i + 1
            time.sleep(10)
            report = self.wmex.check_order(OrderId)
            if report['tradeCoinStatus'] == 'SUCCESS':
                allprice = allprice + report['matchedMoney']
                vol = vol + report['tradedNumber']
                self.buyprice = report['matchedMoney']/report['tradedNumber']
                self.printout('用均价'+str(self.buyprice)+'卖了'+str(self.volreal)+'个币')
                break
            else:
                self.wmex.order_cancel(OrderId)
                allprice = allprice + report['matchedMoney']
                vol = vol + report['tradedNumber']
                self.buyprice = report['matchedMoney']/report['tradedNumber']
                self.printout('用均价'+str(self.buyprice)+'卖了'+str(self.vol)+'个币')
                OrderId = self.wmex.limit_order(self.exCoin,round(price*0.8**i,4),round(self.volreal - report['tradedNumber'],4),'sell')
                self.volreal = self.volreal - report['tradedNumber']
            if i > 3:
                break
        self.closeprice = allprice / vol
            
    def fillPriceList(self):
        K5 = self.wmex.get_kline(self.exCoin,300,'5m')
        K5close = pd.DataFrame(K5['data']['pages']['list'])
        K15 = self.wmex.get_kline(self.exCoin,300,'15m')
        K15close = pd.DataFrame(K15['data']['pages']['list'])
        close = np.nan
        value = []
        for t in range(K15close['time'].iloc[-1],K5close['time'].iloc[0] + 1,5*60):
            res = K5close.loc[K5close['time'] == t]
            if len(res) == 0:
                res = K15close.loc[K15close['time'] == t]
                if len(res) == 0:
                    value.append({'time':t,'close':close})
                else:
                    close = res.close.iloc[0]
                    value.append({'time':t,'close':close})
            else:
                close = res.close.iloc[0]
                value.append({'time':t,'close':close})
        self.pricelist = pd.DataFrame(value)
        self.pricelist['rolling1'] = self.pricelist.close.rolling(240).mean()
        self.pricelist['rolling2'] = self.pricelist.close.rolling(480).mean()
        self.pricelist['KDJ'] = self.pricelist.close.rolling(14).apply(self._calKDJ)
        
    def updatePriceList(self):
        while self.ison:
            K5 = self.wmex.get_kline(self.exCoin,1,'5m')
            timedate = K5['data']['pages']['list'][0]['time']
            if timedate > self.pricelist['time'].iloc[-1]:
                close = K5['data']['pages']['list'][0]['close']
                rolling1 = self.pricelist.close.iloc[-240:-1].sum() / 240 + close / 240
                rolling2 = self.pricelist.close.iloc[-480:-1].sum() / 480 + close / 480
                KDJ = self._calKDJ(np.insert(np.array(self.pricelist.close.iloc[-14:-1]),13,close))
                self.pricelist.loc[len(self.pricelist)] = pd.Series({'time':timedate,'close':close,'rolling1':rolling1,'rolling2':rolling2,'KDJ':KDJ})
                if self.status == 'out' and self.pricelist.rolling1.iloc[-1] > self.pricelist.rolling2.iloc[-1] and KDJ < self.trethold_buy:
                    self.printout('信号入场')
                    self.openPosition()
                    self.status = 'in'
                    m = mt.MyThread(self.lookingforout,args = ())
                    m.start()
                elif self.status == 'in' and KDJ > self.trethold_sell:
                    self.printout('信号出场')
                    self.closePosition(close)
                    self.printout('本次收益为'+str(self.closeprice/self.buyprice - 1))
                    self.status = 'out'
                print('KDJ =',round(KDJ,1),'meanclose1 = ',self.pricelist.rolling1.iloc[-1],'meanclose2 = ',self.pricelist.rolling2.iloc[-1])
            time.sleep(30)
            
            self.sendsignal()
            
    def start(self):
        try:
            mt1 = mt.MyThread(self.updatePriceList,args = ())
            mt1.start()
        except BaseException as e:
            print(e)
            self.printout('error')
            return None
    
    def stop(self):
        self.status = 'out'
        self.ison = False
    
    def printout(self,txt):
        print(txt)
        self.logger.AppendText(txt+'\n')
        
    def _calKDJ(self,x):
        if self.f90 == 0:
            self.f90 = 1.0
            self.f0 = 0.0
            self.f88 = 14-1.0
            self.f8 = 100.0*(x[-1])
            self.f18 = 3.0 / (14 + 2.0)
            self.f20 = 1.0 - self.f18
        else:
            if self.f88 <= self.f90:
                self.f90 = self.f88 + 1
            else:
                self.f90 = self.f90 + 1
            self.f10 = self.f8
            self.f8 = 100 * x[-1]
            self.v8 = self.f8 - self.f10
            
            self.f28 = self.f20 * self.f28 + self.f18 * self.v8
            self.f30 = self.f18 * self.f28 + self.f20 * self.f30
            self.vC = self.f28 * 1.5 - self.f30 * 0.5
            
            self.f38 = self.f20 * self.f38 + self.f18 * self.vC
            self.f40 = self.f18 * self.f38 + self.f20 * self.f40
            self.v10 = self.f38 * 1.5 - self.f40 * 0.5
            
            self.f48 = self.f20 * self.f48 + self.f18 * self.v10
            self.f50 = self.f18 * self.f48 + self.f20 * self.f50
            self.v14 = self.f48 * 1.5 - self.f50 * 0.5
            
            self.f58 = self.f20 * self.f58 + self.f18 * abs(self.v8)
            self.f60 = self.f18 * self.f58 + self.f20 * self.f60
            self.v18 = self.f58 * 1.5 - self.f60 * 0.5
            
            self.f68 = self.f20 * self.f68 + self.f18 * self.v18
            self.f70 = self.f18 * self.f68 + self.f20 * self.f70
            self.v1C = self.f68 * 1.5 - self.f70 * 0.5
            
            self.f78 = self.f20 * self.f78 + self.f18 * self.v1C
            self.f80 = self.f18 * self.f78 + self.f20 * self.f80
            self.v20 = self.f78 * 1.5 - self.f80 * 0.5
            
            if self.f88 >= self.f90 and self.f8 != self.f10:
                self.f0 = 1.0
            if self.f88 == self.f90 and self.f0 == 0.0:
                self.f90 = 0.0
        
        if self.f88 < self.f90 and self.v20 > 0.0000000001:
            self.v4 = (self.v14 / self.v20 + 1.0)*50.0
            if self.v4 > 100.0:
                self.v4 = 100.0
            if self.v4 < 0.0:
                self.v4 =0.0
        else:
            self.v4 = 50.0
            
        return self.v4
