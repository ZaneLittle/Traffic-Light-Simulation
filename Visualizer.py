from pylab import *
from tkinter import *
import time as tm
from config import ENV_CONSTANTS
from Agent import Agent
from Environment import Environment

class Visualizer:

    def __init__(self):
        self.environment = Environment(0)

        canvasSize = self.createCanvas()
        self.gui.update()
        self.gui.title("Traffic Light Simulation")
        self.lightOffset = 350
        self.padding = 200

        self.agent = Agent(self.environment)

    def runSimulation(self):
        routes = self.environment.generateRoutes()    
        for time in range(100):
            self.environment.update(time, routes)
            self.agent.update(time, self.environment)
            self.updateFrame(time)
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
        # if queueIndex == ENV_CONSTANTS["QUEUE_DIR"]["n"] and lightIndex == ENV_CONSTANTS["LIGHT_POSITIONS"]["SE"]:
        numCars = queue.getNumCarsDriving()
        self.createCars(numCars, queueCenterX, queueCenterY, queueIndex, lightIndex)
            # print([car.delay for car in queue.cars])

    def drawLightQueue(self, queue, queueIndex, xCenter, yCenter):
        xOffset, yOffset = self.getQueueOffset(queueIndex)
        x = xCenter + xOffset
        y = yCenter + yOffset
        self.canvas.create_text(x, y, font=("Arial", 24), text=str(queue.getNumCarsWaiting()))
        return x, y

    def createCars(self, numCars, queueCenterX, queueCenterY, queueIndex, lightIndex):
        # if numCars:
        self.drawCars(numCars, queueCenterX, queueCenterY, queueIndex, lightIndex)
    
    def drawCars(self, numCars, endX, endY, queueIndex, lightIndex):
        size = 100
        padding = 20

        line = None
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        arrowDirection = None

        xText = None
        yText = None

        if queueIndex == ENV_CONSTANTS["QUEUE_DIR"]["n"]:
            x1 = endX
            y1 = endY + size
            x2 = endX
            y2 = endY + padding
            xText = (x1 + x2) / 2 + padding
            yText = (y1 + y2) / 2
        elif queueIndex == ENV_CONSTANTS["QUEUE_DIR"]["e"]:
            x1 = endX - size
            y1 = endY
            x2 = endX - padding
            y2 = endY
            xText = (x1 + x2) / 2
            yText = (y1 + y2) / 2 + padding
        elif queueIndex == ENV_CONSTANTS["QUEUE_DIR"]["s"]:
            x1 = endX
            y1 = endY - size
            x2 = endX
            y2 = endY - padding
            xText = (x1 + x2) / 2 + padding
            yText = (y1 + y2) / 2
        else:  # ENV_CONSTANTS["QUEUE_DIR"]["w"]
            x1 = endX + size
            y1 = endY
            x2 = endX + padding
            y2 = endY
            xText = (x1 + x2) / 2
            yText = (y1 + y2) / 2 + padding
            

        line = self.canvas.create_line(x1, y1, x2, y2, arrow=LAST, width=3, fill="blue")

        text = self.canvas.create_text(xText, yText, font=("Arial", 16), text=str(numCars), fill="blue")

    def getCoordinatesFromLightIndex(self, lightIndex):
        NW = ENV_CONSTANTS["LIGHT_POSITIONS"]["NW"]
        NE = ENV_CONSTANTS["LIGHT_POSITIONS"]["NE"]
        SE = ENV_CONSTANTS["LIGHT_POSITIONS"]["SE"]
        if lightIndex == NW:
            return (0, 0)
        elif lightIndex == NE:
            return (0, 1)
        elif lightIndex == SE:
            return (1, 1)
        else: # West
            return (1, 0)
    
    def getQueueOffset(self, queueIndex):
        offset = 50
        n = ENV_CONSTANTS["QUEUE_DIR"]["n"]
        e = ENV_CONSTANTS["QUEUE_DIR"]["e"]
        s = ENV_CONSTANTS["QUEUE_DIR"]["s"]

        if queueIndex == n:
            return 0, offset
        elif queueIndex == e:
            return -offset, 0
        elif queueIndex == s:
            return 0, -offset
        else:  # west
            return offset, 0
    
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