from RacketAndBall import Shape
import random

class Board:
    def __init__(self, size):
        self.size = size
        self.racket = Shape(20, 100, [40, self.size.height() // 2 + 50])
        self.ball = Shape(20, 20, [self.size.width() // 2 - 10, self.size.height() // 2 + 10], speed=6,
                          angle=random.randint(20, 60),
                          active=True)
        self.racketEnemy = Shape(20, 100, [self.size.width() - 60, self.size.height() // 2 + 50])
        self.rackets = [self.racket, self.racketEnemy]
        self.fail = False

    def pushRacket(self, d, id):
        self.rackets[id].forcedMove(d)
        self.rackets[id].action()

    def stopRacket(self, id):
        self.rackets[id].passive()

    def moveRacket(self, id):
        if self.rackets[id].active:
            collisionWall, __angle = self.__collisionWall(self.rackets[id])
            collisionShape, __angleR = self.__collisionShape(self.rackets[id], [self.ball])
            if collisionShape:
                self.ball.push([self.rackets[id].getSpeedX() * 0.4, self.rackets[id].getSpeedY() * 0.4])
            elif not collisionWall:
                self.rackets[id].move()

    def moveBall(self):
        collisionWall, __angle = self.__collisionWall(self.ball)
        collisionShape, __angleR = self.__collisionShape(self.ball, self.rackets)
        if collisionWall:
            if __angle == 90:
                self.fail = True
                self.ball.passive()
            self.ball.reflection(__angle)
        elif collisionShape:
            self.ball.reflection(__angleR)
        self.ball.move()

    def __collisionWall(self, shape):
        deltaX = shape.getSpeedX()
        deltaY = shape.getSpeedY()
        if shape.X() + deltaX + shape.W() > self.size.width() or shape.X() + deltaX < 0:
            return True, 90
        elif shape.Y() + deltaY > self.size.height() or shape.Y() + deltaY - shape.H() < 0:
            return True, 0
        return False, None

    def __collisionShape(self, move, state):
        left, lx = self.rackets[0].X() + self.rackets[0].W(), self.ball.X() + self.ball.getSpeedX()
        right, rx = self.rackets[1].X(), lx + self.ball.W()
        if left < lx and rx < right:
            return False, None
        return self.collisionArea(move, state)

    def collisionArea(self, move, state):
        for st in state:
            for i in range(move.getNumberNode()):
                '''
                x1, y1 = move.getNode(i)[0], move.getNode(i)[1]
                x2, y2 = move.getNode(i)[0] + move.getSpeedX(), move.getNode(i)[
                    1] + move.getSpeedY()
                ptMove = [[x1, y1], [x2, y2]]
                '''
                x1, y1 = move.getNode(i)[0] + move.getSpeedX(), move.getNode(i)[
                    1] + move.getSpeedY()
                x2, y2 = move.getNode(i+1)[0] + move.getSpeedX(), move.getNode(i+1)[
                    1] + move.getSpeedY()
                ptMove = [[x1, y1], [x2, y2]]
                for j in range(st.getNumberNode()):
                    ptState = [st.getNode(j), st.getNode(j + 1)]
                    if self.inline(ptMove[0][0], ptMove[1][0], ptState[0][0], ptState[1][0]) and \
                            self.inline(ptMove[0][1], ptMove[1][1], ptState[0][1], ptState[1][1]):

                        if (self.area(ptMove[0], ptMove[1], ptState[0]) * self.area(ptMove[0], ptMove[1],
                                                                                    ptState[1]) <= 0) and \
                                (self.area(ptState[0], ptState[1], ptMove[0]) * self.area(ptState[0], ptState[1],
                                                                                          ptMove[1]) <= 0):
                            if j == 0 or j == 2:
                                return True, 0
                            return True, 90
        return False, None

    @staticmethod
    def area(a, b, c):
        """Ориентированная площадь"""
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    @staticmethod
    def inline(a, b, c, d):
        """Проверка на пересечение проекций на одной из оси"""
        if a > b:
            a, b = b, a
        if c > d:
            c, d = d, c
        return max(a, c) <= min(b, d)

    def getNumberRacket(self):
        return len(self.rackets)
