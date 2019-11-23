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

    def runSimulation(self):
        for time in range(10):
            self.environment.update(time)
            self.updateFrame(time);
            tm.sleep(0.1)


    def updateFrame(self, time):
        self.canvas.delete("all")
        self.updateTrafficLights()
        self.canvas.config(bg="red" if time % 2 else "blue")
        self.gui.update()

    def updateTrafficLights(self):
        for lightIndex, light in enumerate(environment.lights):
            self.createTrafficLight(light, lightIndex)

    def createTrafficLight(self,light, lightIndex):
        for queueIndex, queue in light.queues:
            self.createLightQueue(queue, lightIndex, queueIndex)

    def createLightQueue(self, queue, lightIndex, queueIndex):
        for car in queue.cars:
            if car.delay:
                self.createDrivingCar(car, lightIndex, queueIndex)

    def createDrivingCar(self, car, lightIndex, queueIndex):
        pass

    # def moveTo(self, canvas, oval, x, y):
    #     currentCoords = canvas.coords(oval)
    #     currentX = (currentCoords[0] + currentCoords[2]) // 2
    #     currentY = (currentCoords[1] + currentCoords[3]) // 2

    #     xDiff = x - currentX
    #     yDiff = y - currentY

    #     canvas.move(oval, xDiff, yDiff)

    def createCanvas(self):
        self.gui = Tk()
        canvasSize = min(int(self.gui.winfo_screenheight() * 0.9), 900)
        self.gui.geometry("{}x{}".format(canvasSize, canvasSize))
        self.canvas = Canvas(self.gui, width=canvasSize,
                        height=canvasSize, background="#fafafa")
        self.canvas.pack()
        return canvasSize

gui = Visualizer()

gui.runSimulation()