from LightQueue import LightQueue
from Car import Car
from TrafficLight import TrafficLight
from Environment import Environment

'''
Testing the classes
'''
lq1 = LightQueue(cars=[Car(['right', 'right', 'left']), Car(['left', 'right'])])
lq2 = LightQueue(cars=[Car(['right', 'right', 'left']), Car(['left', 'right'])], time=14)


lq2.push(lq1.pop(), 16)

tl = TrafficLight()
tl.qN = lq1

env = Environment()