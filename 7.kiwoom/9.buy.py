from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication
import sys, time
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self.regKey()
        self.regHandlers()
        self.login()
        try:
            f = open('best.dat', 'rb')
            self.best = pickle.load(f)
            f.close()
        except:
            self.best = {}
    
    def regKey(self):
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')
    
    def regHandlers(self):
        self.OnEventConnect.connect(self.onLogin)
        self.OnReceiveTrData.connect(self.onResponse)
        self.OnReceiveMsg.connect(self.onMsg)
    
    def onMsg(self, screenno, rqname, trcode, msg):
        print(f'<{rqname}>: {msg}')
    
    def onResponse(self, screenno, rqname, trcode, rname, next):
        if next == '2': self.isnext = True
        else: self.isnext = False

        if rqname == '일봉':
            candles = []
            for i in range(self.GetRepeatCnt(trcode, rqname)):
                date = self.GetCommData(trcode, rqname, i, '일자').strip()
                close = self.GetCommData(trcode, rqname, i, '현재가').strip()
                open = self.GetCommData(trcode, rqname, i, '시가').strip()
                high = self.GetCommData(trcode, rqname, i, '고가').strip()
                low = self.GetCommData(trcode, rqname, i, '저가').strip()
                vol = self.GetCommData(trcode, rqname, i, '거래량').strip()
                candles.append([date, close, open, high, low, vol])
            self.response = candles
        elif rqname == '예수금':
            deposit = self.GetCommData(trcode, rqname, 0, '주문가능금액')
            if isinstance(deposit, list): deposit = 0
            self.response = int(deposit)
        elif rqname == '잔고': 
            box = []
            for i in range(self.GetRepeatCnt(trcode, rqname)):
                stockCode = self.GetCommData(trcode, rqname, i, '종목번호')
                stockName = self.GetCommData(trcode, rqname, i, '종목명')
                q = self.GetCommData(trcode, rqname, i, '보유수량')
                buyP = self.GetCommData(trcode, rqname, i, '매입가')
                rate = self.GetCommData(trcode, rqname, i, '수익률(%)')
                close = self.GetCommData(trcode, rqname, i, '현재가')
                totP = self.GetCommData(trcode, rqname, i, '매입금액')
                aQ = self.GetCommData(trcode, rqname, i, '매매가능수량')

                stockCode = stockCode.strip()[1:]
                stockName = stockName.strip()
                q = int(q)
                buyP = int(buyP)
                rate = float(rate)
                close = int(close)
                totP = int(totP)
                aQ = int(aQ)

                box.append([stockCode, stockName, q, buyP, rate, close, totP, aQ])
            self.response = box
        
        self.el.exit()
        time.sleep(1)        
    
    def getCandles(self, stockCode):
        self.SetInputValue('종목코드', stockCode)
        self.SetInputValue('수정주가구분', '1')
        self.CommRqData('일봉', 'opt10081', 0, '0001')
        self.el.exec()
        candles = self.response
        time.sleep(1)

        while self.isnext:
            self.SetInputValue('종목코드', stockCode)
            self.SetInputValue('수정주가구분', '1')
            self.CommRqData('일봉', 'opt10081', 2, '0001')
            self.el.exec()
            candles += self.response
            time.sleep(0.3)
        
        df = pd.DataFrame()
        try:
            df = pd.DataFrame(candles, columns=['date', 'close', 'open', 'high', 'low', 'vol']).set_index('date')
            df = df.drop_duplicates()
            df = df.sort_index()
        except: pass
        return df
    
    def onLogin(self, status):
        result = '키움증권 연결 '
        if status == 0: result += '성공'
        else: result += '실패'
        print(f'{result}했습니다.')
        self.el.exit()
    
    def login(self):
        self.CommConnect()
        self.el = QEventLoop()
        self.el.exec()
    
    def getAccNo(self):
        accNo = self.GetLoginInfo('ACCNO').split(';')[0]
        return accNo
    
    def getStockCodes(self, marketType):
        return self.GetCodeListByMarket(marketType).split(';')[:-1]
    
    def getStockName(self, stockCode):
        return self.GetMasterCodeName(stockCode)
    
    def getDeposit(self):
        self.SetInputValue('계좌번호', self.getAccNo())
        self.SetInputValue('비밀번호입력매체구분', '00')
        self.SetInputValue('조회구분', '2')
        self.CommRqData('예수금', 'opw00001', 0, '0002')
        self.el.exec()
        return self.response
    
    def order(self, rqname, orderType, stockCode, q, p, gubun, orderNo=''):
        return self.SendOrder(rqname, '0003', self.getAccNo(),
                              orderType, stockCode, q, p, gubun, orderNo)
    
    def getBalance(self):
        self.SetInputValue('계좌번호', self.getAccNo())
        self.SetInputValue('비밀번호입력매체구분', '00')
        self.SetInputValue('조회구분', '1')
        self.CommRqData('잔고', 'opw00018', 0, '0005')
        self.el.exec()
        return self.response
    
    def buy(self, stockCode):
        candles = self.getCandles(stockCode)

        if not candles.empty:
            data = []
            target = []

            for i in range(len(candles) - 1):
                a = list(candles.iloc[i])
                b = candles.iloc[i + 1, 0]
                data.append(a)
                target.append(b)
            
            data = np.array(data)
            target = np.array(target)

            rf = RandomForestRegressor(oob_score=True)
            rf.fit(data, target)

            lastCandle = list(candles.iloc[-1])
            nextP = round(int(rf.predict([lastCandle])[0]), -2)
            closeP = int(candles.iloc[-1][0])

            if nextP > closeP:
                if self.getDeposit() > closeP:
                    self.order('매수', 1, stockCode, 1, 0, '03')

                    highP = round(int(closeP * closeP * 0.1), -2)
                    if nextP > highP: nextP = highP
                    self.best[stockCode] = nextP

                    f = open('best.dat', 'wb')
                    pickle.dump(self.best, f)
                    f.close()                

app = QApplication(sys.argv)
kiwoom = Kiwoom()

kospi = kiwoom.getStockCodes('0')
kosdaq = kiwoom.getStockCodes('10')

for stockCode in kospi:
    kiwoom.buy(stockCode)

for stockCode in kosdaq:
    kiwoom.buy(stockCode)

app.exec()