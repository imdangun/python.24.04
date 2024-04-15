from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication
import sys, time
import pandas as pd
import fidDic
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self.regKey()
        self.regHandlers()
        self.login()
        self.best = {}
    
    def regKey(self):
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')
    
    def regHandlers(self):
        self.OnEventConnect.connect(self.onLogin)
        self.OnReceiveTrData.connect(self.onResponse)
        self.OnReceiveMsg.connect(self.onMsg)
        self.OnReceiveChejanData.connect(self.onAfterOrder)
        self.OnReceiveRealData.connect(self.onReal)
    
    def setReal(self, screenno, stockCodes, fid, optType):
        self.SetRealReg(screenno, stockCodes, fid, optType)
    
    def onReal(self, stockCode, realType):
        if realType == '주식체결':
            signedTime = self.GetCommRealData(stockCode, fidDic.getFid('체결시간'))
            close = self.GetCommRealData(stockCode, fidDic.getFid('현재가'))
            open = self.GetCommRealData(stockCode, fidDic.getFid('시가'))
            high = self.GetCommRealData(stockCode, fidDic.getFid('고가'))
            low = self.GetCommRealData(stockCode, fidDic.getFid('저가'))
            topSell = self.GetCommRealData(stockCode, fidDic.getFid('(최우선)매도호가'))
            topBuy = self.GetCommRealData(stockCode, fidDic.getFid('(최우선)매수호가'))
            volume = self.GetCommRealData(stockCode, fidDic.getFid('누적거래량'))

            close = abs(int(close))
            open = abs(int(open))
            high = abs(int(high))
            low = abs(int(low))
            topSell = abs(int(topSell))
            topBuy = abs(int(topBuy))
            volume = abs(int(volume))

            print([stockCode, signedTime, close, open, high, low, topSell, topBuy, volume])
        else: pass
    
    def onResponse(self, screeno, rqname, trcode, rname, next):
        rowCnt = self.GetRepeatCnt(trcode, rqname)

        if next == '2': self.isnext = True
        else: self.isnext = False

        if rqname == '일봉':
            candles = []
            for i in range(rowCnt):
                date = self.GetCommData(trcode, rqname, i, '일자').strip()
                close = self.GetCommData(trcode, rqname, i, '현재가').strip()
                open = self.GetCommData(trcode, rqname, i, '시가').strip()
                high = self.GetCommData(trcode, rqname, i, '고가').strip()
                low = self.GetCommData(trcode, rqname, i, '저가').strip()
                volume = self.GetCommData(trcode, rqname, i, '거래량').strip()
                candles.append([date, close, open, high, low, volume])
            self.response = candles
        elif rqname == '예수금':
            deposit = self.GetCommData(trcode, rqname, 0, '주문가능금액')
            self.response = int(deposit)  
        elif rqname == '주문':
            box = []
            for i in range(rowCnt):
                stockCode = self.GetCommData(trcode, rqname, i, '종목코드')
                stockName = self.GetCommData(trcode, rqname, i, '종목명')
                orderNo = self.GetCommData(trcode, rqname, i, '주문번호')
                orderStatus = self.GetCommData(trcode, rqname, i, '주문상태')
                orderQ = self.GetCommData(trcode, rqname, i, '주문수량')
                orderP = self.GetCommData(trcode, rqname, i, '주문가격')
                currentP = self.GetCommData(trcode, rqname, i, '현재가')
                orderType = self.GetCommData(trcode, rqname, i, '주문구분')
                leftQ = self.GetCommData(trcode, rqname, i, '미체결수량')
                executedQ = self.GetCommData(trcode, rqname, i, '체결량')
                orderTime = self.GetCommData(trcode, rqname, i, '시간')
                fee = self.GetCommData(trcode, rqname, i, '당일매매수수료')
                tax = self.GetCommData(trcode, rqname, i, '당일매매세금')

                stockCode = stockCode.strip()
                stockName = stockName.strip()
                orderNo = str(int(orderNo.strip()))
                orderStatus = orderStatus.strip()
                orderQ = int(orderQ.strip())
                orderP = int(orderP.strip())
                currentP = int(currentP.strip().lstrip('+').lstrip('-'))
                orderType = orderType.strip().lstrip('+').lstrip('-')
                leftQ = int(leftQ.strip())
                executedQ = int(executedQ.strip())
                orderTime = orderTime.strip()
                fee = int(fee)
                tax = int(tax)

                box.append([stockCode, stockName, orderNo, orderStatus, orderQ, orderP,
                            currentP, orderType, leftQ, executedQ, orderTime, fee, tax])
            self.response = box
        elif rqname == '잔고':
            box = []
            for i in range(rowCnt):
                stockCode = self.GetCommData(trcode, rqname, i, '종목번호')
                stockName = self.GetCommData(trcode, rqname, i, '종목명')
                quantity = self.GetCommData(trcode, rqname, i, '보유수량')
                buyP = self.GetCommData(trcode, rqname, i, '매입가')
                returnRate = self.GetCommData(trcode, rqname, i, '수익률(%)')
                currentP = self.GetCommData(trcode, rqname, i, '현재가')
                totBuyP = self.GetCommData(trcode, rqname, i, '매입금액')
                availableQ = self.GetCommData(trcode, rqname, i, '매매가능수량')

                stockCode = stockCode.strip()[1:]
                stockName = stockName.strip()
                quantity = int(quantity)
                buyP = int(buyP)
                returnRate = float(returnRate)
                currentP = int(currentP)
                totBuyP = int(totBuyP)
                availableQ = int(availableQ)

                box.append([stockCode, stockName, quantity, buyP, returnRate, currentP,
                            totBuyP, availableQ])
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
            candles += self.response
            time.sleep(1)
        
        df = pd.DataFrame(candles, columns=['date', 'close', 'open', 'high', 'low', 'volume']).set_index('date')
        df = df.drop_duplicates()
        df = df.sort_index()
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
        accountNo = self.GetLoginInfo('ACCNO').split(';')[0]
        return accountNo
    
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
    
    def order(self, rqname, orderType, stockCode, quantity, price, gubun, orderNo=''):
        return self.SendOrder(rqname, '0003', self.getAccNo(), 
                              orderType, stockCode, quantity, price, gubun, orderNo)
    
    def onMsg(self, screenno, rqname, trcode, msg):
        print(f'<{rqname}>: {msg}')
    
    def onAfterOrder(self, gubun, rowCnt, fids):
        pass
        # for fid in fids.split(';'):
        #     val = self.GetChejanData(int(fid)).lstrip('+').lstrip('-')
        #     if val.isdigit(): val = int(val)
        #     try:
        #         fidName = fidDic.FID_CODES[fid]
        #         print(f'{fidName}: {val}')
        #     except: pass
    
    def getOrder(self):
        self.SetInputValue('계좌번호', self.getAccNo())
        self.SetInputValue('전체종목구분', '0')
        self.SetInputValue('체결구분', '0')
        self.SetInputValue('매매구분', '0')
        self.CommRqData('주문', 'opt10075', 0, '0004')
        self.el.exec()
        return self.response
    
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

                    highP = round(int(closeP * closeP * 0.25), -2)
                    if nextP > highP: nextP = highP
                    self.best[stockCode] = nextP

                    f = open('best.dat', 'wb')
                    pickle.dump(self.best, f)
                    f.close()

app = QApplication(sys.argv)
kiwoom = Kiwoom()

print(type(kiwoom.getDeposit()))

kospi = kiwoom.getStockCodes('0')
kosdaq = kiwoom.getStockCodes('10')

for stockCode in kospi:
    kiwoom.buy(stockCode)

for stockCode in kosdaq:
    kiwoom.buy(stockCode)

app.exec()