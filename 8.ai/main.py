from PyQt5.QtWidgets import QApplication
import sys
from kiwoom import Kiwoom

app = QApplication(sys.argv)
ai = Kiwoom()

stockCodes = ai.getStockCodes('0')

for stockCode in stockCodes:
    ai.buy(stockCode)

app.exec()