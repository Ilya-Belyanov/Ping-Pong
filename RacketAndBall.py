import math


class Vector:
    def __init__(self, speed, angle):
        self.speed = speed
        self.radian = self.convertToRadian(angle)
        self.tg = math.tan(self.radian)

        self.__deltaX = (self.speed / math.sqrt(1 + self.tg ** 2)) * self.checkSign(math.cos(self.radian))
        self.__deltaY = (abs(self.tg) * self.__deltaX) * self.checkSign(math.sin(self.radian))

    def reflection(self, a):
        radian = self.convertToRadian(a)

        Yfdop1 = self.__deltaX * math.sin(radian) * -1

        Xf = self.__deltaX * math.cos(radian) + self.__deltaY * math.sin(radian)
        Yf = (Yfdop1 + self.__deltaY * math.cos(radian)) * -1

        Xdop1 = Xf * math.cos(radian)
        Xdop2 = Yf * math.sin(radian) * -1

        Ydop1 = Xf * math.sin(radian)
        Ydop2 = Yf * math.cos(radian)

        self.__deltaX = Xdop1 + Xdop2
        self.__deltaY = Ydop1 + Ydop2

    def changeSpeed(self, direct):
        self.__deltaX = direct[0]
        self.__deltaY = direct[1]

    def addSpeed(self, p):
        self.__deltaX += p[0]
        self.__deltaY += p[1]

    def getSpeedX(self):
        return self.__deltaX

    def getSpeedY(self):
        return self.__deltaY

    @staticmethod
    def convertToRadian(a):
        return (a * math.pi) / 180

    @staticmethod
    def checkSign(function):
        if function < 0:
            return -1
        else:
            return 1


class Shape:
    def __init__(self, w, h, coords, speed=0, angle=90, active=False):
        self.width = w
        self.height = h
        self.coords = coords
        self.color = (0, 0, 0, 255)
        self.speed = speed
        self.vector = Vector(self.speed, angle)
        self.node = [[self.X(), self.Y()],\
                     [self.X() + self.W(), self.Y()], \
                     [self.X() + self.W(), self.Y() - self.H()], \
                     [self.X(), self.Y() - self.H()]]

        self.active = active

    def move(self):
        if self.active:
            self.coords[0] += self.vector.getSpeedX()
            self.coords[1] += self.vector.getSpeedY()

    def forcedMove(self, d):
        self.vector.changeSpeed(d)

    def push(self, p):
        self.vector.addSpeed(p)

    def reflection(self, angle):
        self.vector.reflection(angle)

    def getNumberNode(self):
        return len(self.node)

    def getNode(self, id):
        self.node = [[self.X(), self.Y()], \
                     [self.X() + self.W(), self.Y()], \
                     [self.X() + self.W(), self.Y() - self.H()], \
                     [self.X(), self.Y() - self.H()]]
        while id >= self.getNumberNode():
            id -= 4
        return self.node[id]

    def action(self):
        self.active = True

    def passive(self):
        self.active = False

    def getSpeedX(self):
        return self.vector.getSpeedX()

    def getSpeedY(self):
        return self.vector.getSpeedY()

    def X(self):
        return self.coords[0]

    def Y(self):
        return self.coords[1]

    def W(self):
        return self.width

    def H(self):
        return self.height
