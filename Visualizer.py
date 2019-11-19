from tkinter import *
import time

class Visualization(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.canvas = Canvas(master)
        self.lights = [TrafficLight(self.canvas, 0, 0, True), TrafficLight(self.canvas, 0, 1, False), TrafficLight(self.canvas, 1, 1, True), TrafficLight(self.canvas, 1, 0, False)]
    
    def updateLightDirections(self, directions):
        for i, direction in enumerate(directions):
            self.lights[i].update(direction)

    def updateQueueLengths(self):
        pass

    def updateCarsInTransit(self):
        pass


class TrafficLight():
    def __init__(self, canvas, x, y, isNorthSouth):
        self.size = 50
        self.canvas = canvas
        self.x = x*100
        self.y = y*100
        self.centerX = self.x + self.size / 2
        self.centerY = self.y + self.size / 2
        self.isNorthSouth = isNorthSouth
        self.createArrow()
    
    def update(self, isNorthSouth):
        self.isNorthSouth = isNorthSouth
        self.deleteArrow()
        self.createArrow()
    
    def deleteArrow(self):
        self.canvas.delete(self.arrow)
    
    def createArrow(self):
        startX = None
        startY = None
        endX = None
        endY = None
        if self.isNorthSouth:
            startX = self.centerX
            endX = self.centerX
            startY = self.y
            endY = self.y + self.size
        else:
            startY = self.centerY
            endY = self.centerY
            startX = self.x
            endX = self.x + self.size

        self.arrow = self.canvas.create_line(startX, startY, endX, endY, arrow=BOTH, width=3)
        
class QueueLabel():
    pass

class Car():
    pass

if __name__ == "__main__":
    root = Tk()
    app = Visualization(root)
    app.canvas.pack()
    root.update()
    time.sleep(1)
    app.updateLightDirections([True,True,True,True])
    root.update()
    time.sleep(1)
    app.updateLightDirections([False,False,False,False])
    root.update()