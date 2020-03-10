from PyQt5 import QtWidgets
from Connect import Connector
import sys
"""
To Do
1) Collision
2) Reflection
3) Two player
"""
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = Connector()
    sys.exit(app.exec())