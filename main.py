from PyQt5 import QtWidgets
from Connect import Connector
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = Connector()
    sys.exit(app.exec())