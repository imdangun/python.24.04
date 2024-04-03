from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication
import sys, time
import pandas as pd

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self.regKey()
        self.regHandlers()
        self.login()
    
    def regKey(self):
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')
    
    def regHandlers(self):
        self.OnEventConnect.connect(self.onLogin)
        self.OnReceiveTrData.connect(self.onResponse)
    
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

app = QApplication(sys.argv)
kiwoom = Kiwoom()

candles = kiwoom.getCandles('344820')
print(candles)

app.exec()