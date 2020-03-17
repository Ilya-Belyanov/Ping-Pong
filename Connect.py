from PyQt5 import QtCore, QtGui, QtWidgets
from MainWindows import Ui_MainWindow
from Board import Board


class Connector(QtWidgets.QMainWindow):
    def __init__(self):
        """Connect main Window"""
        super(Connector, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.timerMove = QtCore.QBasicTimer()
        self.show()
        self.modeBot = True
        self.createBoard()

    def createBoard(self):
        self.board = Board(self.ui.frame.size(), self.modeBot)
        self.ui.frame.setBoard(self.board)
        self.ui.statusbar.showMessage("Bot:( "+str(self.modeBot)+" )change - 'B', special button 'N'")

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_W:
            self.board.pushRacket((0, 6), 0)

        if key == QtCore.Qt.Key_S:
            self.board.pushRacket((0, -6), 0)

        if key == QtCore.Qt.Key_Up and not self.board.rackets[1].bot:
            self.board.pushRacket((0, 6), 1)

        if key == QtCore.Qt.Key_Down and not self.board.rackets[1].bot:
            self.board.pushRacket((0, -6), 1)

        if key == QtCore.Qt.Key_Space:
            if self.board.fail:
                self.createBoard()
            self.timerMove.start(15, self)
            self.ui.frame.firstPress = False

        if key == QtCore.Qt.Key_N:
            self.createBoard()
            self.timerMove.start(15, self)

        if key == QtCore.Qt.Key_B:
            self.board.rackets[1].setBot()
            self.modeBot = self.board.rackets[1].bot
            self.ui.statusbar.showMessage("Bot:( " + str(self.modeBot) + " )change - 'B', special button 'N'")

        if key == QtCore.Qt.Key_Escape:
            self.close()

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_W:
            self.board.stopRacket(0)

        if key == QtCore.Qt.Key_S:
            self.board.stopRacket(0)

        if key == QtCore.Qt.Key_Up and not self.board.rackets[1].bot:
            self.board.stopRacket(1)

        if key == QtCore.Qt.Key_Down and not self.board.rackets[1].bot:
            self.board.stopRacket(1)

    def timerEvent(self, event):
        if event.timerId() == self.timerMove.timerId():
            if self.board.fail:
                self.timerMove.stop()
            else:
                self.board.moveBall()
                for i in range(self.board.getNumberRacket()):
                    self.board.moveRacket(i)
                self.update()
