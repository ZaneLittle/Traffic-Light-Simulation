from pylab import *
from tkinter import *
import time as tm

from Environment import Environment

class Visualizer:

    def __init__(self):
        self.environment = Environment(0, 10)

        canvasSize = self.createCanvas()
        self.gui.update()
        self.gui.title("Traffic Light Simulation")
        self.lightOffset = 350
        self.padding = 200

    def runSimulation(self):
        routes = self.environment.generateRoutes()    
        for time in range(40):
            self.environment.update(time, routes)
            self.updateFrame(time);
            tm.sleep(0.3)


    def updateFrame(self, time):
        self.canvas.delete("all")
        self.updateTrafficLights()
        self.gui.update()

    def updateTrafficLights(self):
        for lightIndex, light in enumerate(self.environment.lights):
            self.createTrafficLight(light, lightIndex)

    def createTrafficLight(self,light, lightIndex):
        xCenter, yCenter = self.drawTrafficLight(light, lightIndex)
        for queueIndex, queue in enumerate(light.queues):
            self.createLightQueue(queue, queueIndex, lightIndex, xCenter, yCenter)
    
    def encodeEmoji(self, emoji):
        return ''.join(chr(x) for x in struct.unpack('>2H', emoji.encode('utf-16be')))

    def drawTrafficLight(self, light, lightIndex):
        direction = light.directionIsNorthSouth
        position = self.getCoordinatesFromLightIndex(lightIndex)
        length = 60

        xLeft = position[0] * self.lightOffset + self.padding
        yTop = position[1] * self.lightOffset + self.padding
        xRight = xLeft + length
        yBottom = yTop + length

        xCenter = (xLeft + xRight) / 2
        yCenter = (yTop + yBottom) / 2

        if direction: # N/S
            self.canvas.create_line(xCenter, yTop, xCenter, yBottom, arrow=BOTH, width=4, arrowshape=(8,12,8))
        else: # E/W
            self.canvas.create_line(xLeft, yCenter, xRight, yCenter, arrow=BOTH, width=4, arrowshape=(8,12,8))

        return xCenter, yCenter

    def createLightQueue(self, queue, queueIndex, lightIndex, lightCenterX, lightCenterY):
        queueCenterX, queueCenterY = self.drawLightQueue(queue, queueIndex, lightCenterX, lightCenterY)
        numCars = len([car for car in queue.cars if car.delay])
        self.createCars(numCars, queueCenterX, queueCenterY, queueIndex)

    def drawLightQueue(self, queue, queueIndex, xCenter, yCenter):
        xOffset, yOffset = self.getQueueOffset(queueIndex)
        x = xCenter + xOffset
        y = yCenter + yOffset
        
        self.canvas.create_text(x, y, font=("Arial", 24), text=str(queue.getNumCars()))

        return x, y

    def createCars(self, numCars, queueCenterX, queueCenterY, queueIndex):
        if numCars:
            self.drawCars(numCars, queueCenterX, queueCenterY, queueIndex)
    
    def drawCars(self, numCars, endX, endY, queueIndex):
        size = 100
        padding = 40

        line = None
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        arrowDirection = None

        xText = None
        yText = None

        if queueIndex == 0:
            x1 = endX
            y1 = endY - size
            x2 = endX
            y2 = endY - padding

            xText = (x1 + x2) / 2 + padding
            yText = (y1 + y2) / 2
        elif queueIndex == 1:
            x1 = endX + size
            y1 = endY
            x2 = endX + padding
            y2 = endY

            xText = (x1 + x2) / 2
            yText = (y1 + y2) / 2 + padding
        elif queueIndex == 2:
            x1 = endX
            y1 = endY + size
            x2 = endX
            y2 = endY + padding

            xText = (x1 + x2) / 2 + padding
            yText = (y1 + y2) / 2
        else:
            x1 = endX - size
            y1 = endY
            x2 = endX - padding
            y2 = endY

            xText = (x1 + x2) / 2
            yText = (y1 + y2) / 2 + padding

        line = self.canvas.create_line(x1, y1, x2, y2, arrow=LAST, width=3)

        text = self.canvas.create_text(xText, yText, font=("Arial", 16), text=str(numCars))
        
        self.canvas.after(10, self.canvas.delete, line)
        self.canvas.after(10, self.canvas.update)

    def getCoordinatesFromLightIndex(self, lightIndex):
        if lightIndex == 0:
            return (0, 0)
        elif lightIndex == 1:
            return (0, 1)
        elif lightIndex == 2:
            return (1, 1)
        else:
            return (1, 0)
    
    def getQueueOffset(self, queueIndex):
        offset = 50
        if queueIndex == 0:
            return 0, -offset
        elif queueIndex == 1:
            return offset, 0
        elif queueIndex == 2:
            return 0, offset
        else:
            return -offset, 0
    
    def getCarOffset(self, progress, queueIndex):
        maxOffset = 30
        if queueIndex == 0:
            return 0, progress * maxOffset
        elif queueIndex == 1:
            return progress * maxOffset, 0
        elif queueIndex == 2:
            return 0, progress * maxOffset
        else:
            return progress * maxOffset, 0

    def createCanvas(self):
        self.gui = Tk()
        canvasSize = min(int(self.gui.winfo_screenheight() * 0.9), 800)
        self.gui.geometry("{}x{}".format(canvasSize, canvasSize))
        self.canvas = Canvas(self.gui, width=canvasSize,
                        height=canvasSize, background="#fafafa")
        self.canvas.pack()
        return canvasSize

gui = Visualizer()

gui.runSimulation()