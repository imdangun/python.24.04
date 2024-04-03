from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication
import sys

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

for stockCode in kiwoom.getStockCodes('10'):
    print(kiwoom.getStockName(stockCode), end=' ')

app.exec()