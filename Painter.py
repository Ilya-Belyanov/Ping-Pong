from PyQt5 import QtCore, QtGui, QtWidgets


class Paint(QtWidgets.QFrame):
    """Central frame"""
    def __init__(self, parent):
        super().__init__(parent)
        self.firstPress = True

    def setBoard(self, board):
        self.board = board
        self.update()

    def paintEvent(self, event):
        """ Draw all elements"""
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawImage(qp)
        self.drawRacket(qp)
        self.drawRect(qp)
        self.drawBall(qp)
        if self.firstPress:
            self.drawGame(qp, event, 'Press Space', [0, 0, 200, 255])
        if self.board.fail:
            self.drawGame(qp, event, 'Game Over \n press space', [200, 0, 0, 255])
        qp.end()

    def drawImage(self, qp):
        qp.drawPixmap(100, 0, QtGui.QPixmap("static/DeathMagnetic.jpg"))


    def drawRacket(self, qp):
        for racket in self.board.rackets:
            color = racket.color
            w = racket.width
            h = racket.height
            coords = racket.coords
            color = QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3])
            qp.fillRect(coords[0], self.size().height() - coords[1], w, h, color)

    def drawBall(self, qp):
        color = self.board.ball.color
        color = QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3])
        w = self.board.ball.width
        h = self.board.ball.height
        coords = self.board.ball.coords
        qp.setBrush(color)
        qp.drawEllipse(coords[0], self.size().height() - coords[1], w, h)

    def drawRect(self, qp):
        color = QtGui.QColor.fromRgb(0, 0, 0, 255)
        pen = QtGui.QPen(color, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawRect(0, 0, self.size().width(), self.size().height())

    def drawGame(self, qp, event, text, color):
        color = QtGui.QColor.fromRgb(color[0], color[1], color[2], color[3])
        pen = QtGui.QPen(color, 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(QtGui.QFont('Decorative', 80))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, text)
