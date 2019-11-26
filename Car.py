from config import CAR_CONSTS 

class Car:
    '''
    Defines each car in the environment
    :startTime: (int) the time the car got to a light, None if not at a light
    :route: a list of directions representing the route the car will take through the environment 
        route is represented as follows: ['n', 's', 'e', 'w']
    '''

    def __init__(self, route, startTime=None):
        #self.startLocation = route.pop(0)
        self.position = route[0]
        self.MAX_DELAY = CAR_CONSTS["MAX_DELAY"]
        self.route = route
        self.startTime = startTime
        self.delay = CAR_CONSTS["MAX_DELAY"]
        self.enteredEnvironment = startTime
